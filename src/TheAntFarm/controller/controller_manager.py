import logging
import os
import time
import traceback
from collections import OrderedDict as Od

from PySide6.QtCore import QTimer, Slot
from PySide6.QtGui import QPixmap
from app.services.align_point_service import AlignPointService
from app.services.file_send_service import FileSendService
from app.services.manager_adapter_service import ManagerAdapterService
from app.services.macro_service import MacroService
from app.services.rx_coordinator_service import RxCoordinatorService
from app.services.rx_line_service import RxLineService
from app.services.streaming_service import StreamingService
from shape_core.gcode_manager import GCoder

from .controller_align import AlignController
from .controller_control import ControlController
from .controller_signals import ControllerSignals
from .controller_view import ViewController

logger = logging.getLogger(__name__)


class ControllerWorker(ControllerSignals):
    REMOTE_RX_BUFFER_MAX_SIZE = 128

    def __init__(
        self,
        serial_rx_queue,
        serial_tx_queue,
        settings,
        *,
        manager_adapter=None,
        macro_service=None,
        rx_coordinator_service=None,
        rx_line_service=None,
        streaming_service=None,
        file_send_service=None,
        align_point_service=None,
        view_controller=None,
        control_controller=None,
        align_controller=None,
        gcr=None,
    ):
        super(ControllerWorker, self).__init__()

        self.serialRxQueue = serial_rx_queue
        self.serialTxQueue = serial_tx_queue
        self.settings = settings

        self.connected = False  # Flag to know if the controller is connected
        self._manager_adapter = manager_adapter if manager_adapter is not None else ManagerAdapterService()
        self._macro = macro_service if macro_service is not None else MacroService()
        self._rx_coordinator = rx_coordinator_service if rx_coordinator_service is not None else RxCoordinatorService()
        self._rx_line = rx_line_service if rx_line_service is not None else RxLineService()
        self._streaming = (
            streaming_service if streaming_service is not None else StreamingService(self.REMOTE_RX_BUFFER_MAX_SIZE)
        )
        self._file_send = file_send_service if file_send_service is not None else FileSendService()
        self._align_point = align_point_service if align_point_service is not None else AlignPointService()

        self.view_controller = view_controller if view_controller is not None else ViewController(self.settings)
        self.control_controller = control_controller if control_controller is not None else ControlController(self.settings)
        self.align_controller = align_controller if align_controller is not None else AlignController(self.settings)

        self.send_tool_change_s.connect(self.start_tool_change)

        self.poll_timer = None
        self.camera_timer = None
        self.progress_timer = None

        self.align_active = False

        self.buffered_cmds = []
        self.cmds_to_ack = 0
        self.wait_tag_decoding = False
        self.dro_status_updated = False

        self.abl_apply_active = True
        self.align_apply_active = True

        self.sending_file = False
        self.file_content = []
        self.content_line = 0
        self.file_progress = 0.0
        self.sent_lines = 0
        self.ack_lines = 0
        self.tot_lines = 0
        self.buffered_size = 0
        self.eof_wait_for_idle = False
        self.start_time = None

        self.active_gcode_path = ""

        self.gcr = gcr if gcr is not None else GCoder("dummy", "commander")
        self.update_gerber_cfg()

        self.send_soft_reset = True

        self.camera_zoom = 1

    @property
    def buffered_cmds(self):
        return self._streaming.buffered_cmds

    @buffered_cmds.setter
    def buffered_cmds(self, value):
        self._streaming.buffered_cmds = value

    @property
    def cmds_to_ack(self):
        return self._streaming.cmds_to_ack

    @cmds_to_ack.setter
    def cmds_to_ack(self, value):
        self._streaming.cmds_to_ack = value

    @property
    def wait_tag_decoding(self):
        return self._streaming.wait_tag_decoding

    @wait_tag_decoding.setter
    def wait_tag_decoding(self, value):
        self._streaming.wait_tag_decoding = value

    @property
    def sending_file(self):
        return self._streaming.sending_file

    @sending_file.setter
    def sending_file(self, value):
        self._streaming.sending_file = value

    @property
    def file_content(self):
        return self._streaming.file_content

    @file_content.setter
    def file_content(self, value):
        self._streaming.file_content = value

    @property
    def content_line(self):
        return self._streaming.content_line

    @content_line.setter
    def content_line(self, value):
        self._streaming.content_line = value

    @property
    def file_progress(self):
        return self._streaming.file_progress

    @file_progress.setter
    def file_progress(self, value):
        self._streaming.file_progress = value

    @property
    def sent_lines(self):
        return self._streaming.sent_lines

    @sent_lines.setter
    def sent_lines(self, value):
        self._streaming.sent_lines = value

    @property
    def ack_lines(self):
        return self._streaming.ack_lines

    @ack_lines.setter
    def ack_lines(self, value):
        self._streaming.ack_lines = value

    @property
    def tot_lines(self):
        return self._streaming.tot_lines

    @tot_lines.setter
    def tot_lines(self, value):
        self._streaming.tot_lines = value

    @property
    def buffered_size(self):
        return self._streaming.buffered_size

    @buffered_size.setter
    def buffered_size(self, value):
        self._streaming.buffered_size = value

    @property
    def eof_wait_for_idle(self):
        return self._streaming.eof_wait_for_idle

    @eof_wait_for_idle.setter
    def eof_wait_for_idle(self, value):
        self._streaming.eof_wait_for_idle = value

    @Slot(bool)
    def on_controller_connection(self, connected):
        self.connected = connected
        if connected:
            self.buffered_size = 0
            self.poll_timer.start()
        else:
            self.poll_timer.stop()

    def init_timers(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.on_poll_timeout)
        self.poll_timer.setInterval(self._manager_adapter.POLL_INTERVAL_MS)
        # self.poll_timer.setSingleShot(True)
        # self.poll_timer.start()

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.on_camera_timeout)
        self.camera_timer.setInterval(self._manager_adapter.POLL_INTERVAL_MS)
        self.camera_timer.start()

    def on_progress_timeout(self):
        elapsed_time = self._manager_adapter.format_elapsed_time(self.start_time)
        self.update_file_progress_s.emit(-1.0, elapsed_time)

    # ***************** VIEW related functions. ***************** #

    @Slot(str, str)
    def load_new_layer(self, layer, layer_path):
        [loaded_layer, exc_flag] = self.view_controller.load_new_layer(layer, layer_path)
        if loaded_layer is not None:
            self.update_layer_s.emit(loaded_layer, layer, layer_path, exc_flag)
        else:
            logger.warning("Invalid file data. No geometries found in file: " + str(layer_path))
            self.update_layer_s.emit(None, layer, "", False)

    @Slot(str, Od, str)
    def generate_new_path(self, tag, cfg, machining_type):
        new_paths = self.view_controller.generate_new_path(tag, cfg, machining_type)
        self.view_controller.generate_new_gcode_file(tag, cfg, machining_type, new_paths)
        self.update_path_s.emit(tag, new_paths)

    # ***************** CONTROL related functions. ***************** #
    def check_eof_and_idle(self):
        if self.eof_wait_for_idle and self.cmds_to_ack == 0:
            sta = self.control_controller.status_report_od["state"].lower()
            if "idle" in sta:
                self.stop_send_s.emit()
                self.eof_wait_for_idle = False

    def reset_dro_status_updated(self):
        self.dro_status_updated = False

    def send_to_tx_queue(self, data):
        parsed_cmd_str = self._manager_adapter.prepare_tx_payload(data, self.decode_tag)
        # logger.info(data)
        self.serialTxQueue.put(parsed_cmd_str)
        self.serial_tx_available_s.emit()

    def on_poll_timeout(self):
        status_poll = self._manager_adapter.get_poll_payload()
        self.serial_send_s.emit(status_poll)
        # self.send_to_tx_queue(status_poll)

    @Slot()
    def parse_rx_queue(self):
        if not self.serialRxQueue.empty():
            try:
                element = self.serialRxQueue.get(block=False)
                if element:
                    line_kind = self._rx_line.classify(element)
                    # logger.debug("Element received: " + str(element))
                    if line_kind == "status":
                        result = self._rx_coordinator.process_line(
                            line_kind,
                            element,
                            dro_status_updated=self.dro_status_updated,
                            status_payload=self.control_controller.parse_bracket_angle(element),
                        )
                        self.update_status_s.emit(result["status_payload"])
                        if result["mark_dro_updated"]:
                            self.dro_status_updated = True
                        if result["check_eof_and_idle"]:
                            self.check_eof_and_idle()
                    elif line_kind == "square":
                        self.control_controller.parse_bracket_square(element)
                        square_flags = (
                            self.control_controller.process_probe_and_abl()
                        )
                        result = self._rx_coordinator.process_line(
                            line_kind,
                            element,
                            square_flags=square_flags,
                        )
                        if result["touched_probe"]:
                            self.touched_probe_s.emit()
                        if result["ack_probe"]:
                            self.ack_probe()
                        if result["ack_auto_bed_levelling"]:
                            self.ack_auto_bed_levelling()
                        if result["send_next_abl"]:
                            self.send_next_abl()
                        if result["console_text"] is not None:
                            self.update_console_text_s.emit(result["console_text"])
                            logger.debug(result["console_text"])
                    elif line_kind == "ok":
                        logger.debug("buffered size: " + str(self.buffered_size))
                        self.update_console_text_s.emit(element)
                        result = self._rx_coordinator.process_line(
                            line_kind,
                            element,
                            streaming=self._streaming,
                            macro=self._macro,
                            prepare_file_command=self.macro_check,
                            workspace_parameters=self.get_workspace_parameters(),
                            probe_data=self.control_controller.prb_val,
                        )
                        if result["acknowledged"]:
                            logger.debug("Acknowledged lines: " + str(self.ack_lines))
                            self.update_file_progress_s.emit(self.file_progress, "")
                            logger.debug("wait: " + str(self.wait_tag_decoding))
                            if result["send_command"] is not None:
                                self.send_to_tx_queue(result["send_command"])
                                logger.debug("TX:" + result["send_command"])
                                self.update_console_text_s.emit(result["send_command"])
                            if result["finished_file"]:
                                self.update_file_progress_s.emit(self.file_progress, "")
                                logger.info("End of File sending.")

                    elif line_kind == "error":
                        result = self._rx_coordinator.process_line(line_kind, element)
                        self.update_console_text_s.emit(result["console_text"])
                        logger.error(result["console_text"])
                        logger.debug(self.buffered_size)
                        logger.debug(self.sent_lines)
                        logger.debug(self.ack_lines)
                    else:
                        result = self._rx_coordinator.process_line(line_kind, element)
                        self.update_console_text_s.emit(result["console_text"])
                        logger.debug(result["console_text"])
            except BlockingIOError as e:
                logger.error(e, exc_info=True)
            except Exception:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    def macro_check(self, cmd_to_send):
        macro_result = self._macro.prepare_command(
            cmd_to_send,
            self.ack_lines,
            self.sent_lines,
            self.control_controller.wpos_a,
            self.control_controller.mpos_a,
            self.settings.local_path,
            self.gcr,
        )
        self.wait_tag_decoding = macro_result["wait_tag_decoding"]
        self.tot_lines += macro_result["total_lines_delta"]
        return macro_result["command"]

    def decode_tag(self, gcode_str):
        # status = self.control_controller.status
        # probe_data = self.control_controller.prb_val
        # wsp = self.get_workspace_parameters()
        # ret_str = self.gcr.compute_tag(gcode_str, wsp, probe_data)
        #
        # if self.gcr.TAG in str(gcode_str):
        #     logger.info("Tag Found: " + str(ret_str) + " [" + gcode_str + "]" )
        return gcode_str

    @Slot(str, tuple)
    def execute_user_interface_cmd(self, cmd_key, cmd_data_values):

        str_l = self.gcr.user_cmd.get_command_str(cmd_key, cmd_data_values)

        if len(str_l) == 1:
            logger.info("Sending Short User Command")
            self.update_console_text_s.emit(str(str_l[0]))  # To string because it can be a byte.
            self.serial_send_s.emit(str_l[0])
        elif len(str_l) > 1:
            logger.info("Sending Long User Command")
            self.send_soft_reset = False
            self.send_gcode_lines(str_l)

    def execute_gcode_cmd(self, cmd_str):
        """Send generic G-CODE command coming from elsewhere."""
        logger.debug("Execute Gcode")
        parsed_cmd_str = self.decode_tag(cmd_str)
        logger.info("Sent GCODE: " + str(parsed_cmd_str))
        self.serial_send_s.emit(parsed_cmd_str)

    def cmd_probe(self, probe_z_min):
        self.control_controller.cmd_probe()
        self.execute_user_interface_cmd("probe", (None, None, probe_z_min))

    def ack_probe(self):
        prb_val = self.control_controller.get_probe_value()
        logger.info("Probe: " + str(prb_val))
        self.update_probe_s.emit(prb_val)

    def cmd_auto_bed_levelling(self, bbox_t, steps_t):
        probe_feed_rate = self.settings.machine_settings.feedrate_probe
        self.control_controller.cmd_auto_bed_levelling(bbox_t, steps_t, probe_feed_rate)
        self.send_next_abl()  # Send first probe command.

    def send_next_abl(self):
        next_abl_cmd = self.control_controller.get_next_abl_cmd()
        logger.info(next_abl_cmd)
        self.serial_send_s.emit(next_abl_cmd)  # Execute next Probe of Auto-Bed-Levelling

    def ack_auto_bed_levelling(self):
        abl_val = self.control_controller.get_abl_value()
        logger.debug("ABL values: " + str(abl_val))
        # self.update_abl_s.emit(abl_val)
        self.select_active_gcode(self.active_gcode_path)

    def set_abl_active(self, abl_active=True):
        self.abl_apply_active = abl_active
        self.select_active_gcode(self.active_gcode_path)

    def set_align_active(self, align_active=True, align_data=()):
        self.control_controller.set_align_data(align_data)
        self.align_apply_active = align_active
        self.select_active_gcode(self.active_gcode_path)

    def vectorize_new_gcode_file(self, gcode_path):
        self.control_controller.load_gcode_file({}, gcode_path)
        self.gcode_vectorized_s.emit(gcode_path)

    def select_active_gcode(self, gcode_path):
        if os.path.isfile(gcode_path):
            self.active_gcode_path = gcode_path
            redraw = False
            visible = True

            abl_val = self.control_controller.get_abl_value()
            logger.debug("ABL_val " + str(abl_val))
            logger.debug("ABL_active " + str(self.abl_apply_active))

            align_data = self.control_controller.get_align_data()
            logger.debug("Align_val " + str(align_data))
            logger.debug("Align_active " + str(self.align_apply_active))

            if align_data and self.align_apply_active:
                logger.debug("Apply Alignment")
                self.control_controller.apply_alignment(gcode_path)
                redraw_align = True
            else:
                logger.debug("Remove Alignment")
                redraw_align = self.control_controller.remove_alignment(gcode_path)

            if abl_val and self.abl_apply_active:
                logger.debug("Apply ABL")
                self.control_controller.apply_abl(gcode_path)
                redraw_abl = True
            else:
                logger.debug("Remove ABL")
                redraw_abl = self.control_controller.remove_abl(gcode_path)
            redraw = redraw_abl or redraw_align
            logger.debug("ABL Done")
            tag, v = self.control_controller.get_gcode_tag_and_v(gcode_path)
            logger.debug("Update Gcode View: " + str(redraw))
            self.update_gcode_s.emit(tag, v, visible, redraw)
        else:
            logger.warning("No GCode Data Available. Please select a valid gcode file.")

    def get_gcode_data(self, gcode_path):
        return self.control_controller.get_gcode_tag_and_v(gcode_path)

    @Slot(str)
    def remove_gcode(self, gcode_path):
        self.control_controller.remove_gcode_file(gcode_path)

    @Slot(str)
    def send_gcode_file(self, gcode_path):
        lines = self.control_controller.get_gcode_lines(gcode_path)
        logger.info("Sending file: " + str(gcode_path))
        self.send_gcode_lines(lines)

    def send_gcode_lines(self, lines):
        send_state = self._file_send.begin_send(self._streaming, lines, buffered_size=self.buffered_size)
        logger.debug(self.file_content)
        if send_state["has_content"]:
            self.start_time = time.time()
            self.progress_timer = QTimer()
            self.progress_timer.timeout.connect(self.on_progress_timeout)
            self.progress_timer.setInterval(self._manager_adapter.PROGRESS_INTERVAL_MS)
            self.progress_timer.start()
            self._macro.reset()
            logger.info("Total lines: " + str(send_state["total_lines"]))

            initial_cmd = self._file_send.prepare_initial_command(self._streaming, self.macro_check)
            cmd_to_send = initial_cmd["command"]
            if cmd_to_send is not None:
                self.send_to_tx_queue(cmd_to_send)
                self.update_console_text_s.emit(cmd_to_send)
                logger.debug(cmd_to_send)

            logger.debug("Buffered size: " + str(self.buffered_size))

    def stop_gcode_file(self):
        self.sending_file = False
        self.progress_timer.stop()
        stop_state = self._file_send.stop_send(self._streaming, self.send_soft_reset)
        for cmd in stop_state["reset_commands"]:
            self.execute_gcode_cmd(cmd)
        self.send_soft_reset = stop_state["next_send_soft_reset"]

    def pause_resume(self):
        logger.info("Status: " + str(self.control_controller.status))
        if "hold" in self.control_controller.status.lower():
            logger.info("UnHold")
            self.execute_gcode_cmd(b"~")
        else:
            logger.info("Hold")
            self.execute_gcode_cmd(b"!")

    def get_boundary_box(self):
        if self.active_gcode_path != "":
            bbox_t = self.control_controller.get_boundary_box(self.active_gcode_path)
            if bbox_t is not None:
                self.update_bbox_s.emit(bbox_t)

    def get_status_report(self):
        return self.control_controller.status_report_od

    @Slot()
    def report_status_report(self):
        self.report_status_report_s.emit(self.control_controller.status_report_od)

    def get_workspace_parameters(self):
        return self.control_controller.workspace_params_od

    @Slot()
    def start_tool_change(self):
        logger.info("Tool change is starting!")
        lines = self.control_controller.get_change_tool_lines()
        self.send_soft_reset = False
        self.send_gcode_lines(lines)

    # ***************** ALIGN related functions. ***************** #

    @Slot(str, str)
    def load_new_align_layer(self, layer, layer_path):
        [loaded_layer, exc_flag] = self.align_controller.load_new_align_layer(layer, layer_path)
        if loaded_layer is not None:
            self.update_align_layer_s.emit(loaded_layer, layer, layer_path, exc_flag)
        else:
            logger.warning("Invalid file data. No geometries found in file: " + str(layer_path))
            self.update_align_layer_s.emit(None, layer, "", False)

    @Slot(bool)
    def flip_align_layer_horizontally(self, flipped):
        self.align_controller.flip_align_layer_horizontally(flipped)
        # todo: emit signal here to update align layer
        self.update_align_layer_view_s.emit(self.align_controller.flipping_view)

    @Slot(bool)
    def flip_align_layer_vertically(self, flipped):
        self.align_controller.flip_align_layer_vertically(flipped)
        # todo: emit signal here to update align layer
        self.update_align_layer_view_s.emit(self.align_controller.flipping_view)

    @Slot(list, tuple)
    def add_new_align_point(self, geometry_point, offset_flag):
        result = self._align_point.prepare_align_point(
            connected=self.connected,
            status=self.get_status_report(),
            geometry_point=geometry_point,
            offset_flag=offset_flag,
            camera_offset_xy=(
                self.settings.machine_settings.tool_camera_offset_x,
                self.settings.machine_settings.tool_camera_offset_y,
            ),
            flipping_view=self.align_controller.flipping_view,
        )

        if not result["ok"]:
            if result["reason"] == "invalid_wpos":
                logger.warning("Invalid Working Position Information")
            elif result["reason"] == "invalid_status":
                logger.warning("Invalid Machine Status Information")
            else:
                logger.warning("Machine Disconnected")
            return

        align_data = self.align_controller.add_new_align_point(
            result["geometry_point"], result["working_position_point"]
        )
        self.update_align_points_s.emit(align_data)

    @Slot(list)
    def remove_align_points(self, selected_rows):
        align_data = self.align_controller.remove_align_points(selected_rows)
        self.update_align_points_s.emit(align_data)

    def on_camera_timeout(self):
        if self.align_active:
            image = self.align_controller.camera_new_frame(self.camera_zoom)
            if image:
                self.update_camera_image_s.emit(QPixmap.fromImage(image))
            else:
                self.update_camera_image_s.emit(QPixmap())  # empty image

    def refresh_camera_list(self):
        cam_list = self.align_controller.get_camera_list()
        self.update_camera_list_s.emit(cam_list)

    def update_camera_selected(self, index):
        # Take in account that index 0 indicates NO CAMERA
        self.align_controller.update_camera_selected(index - 1)

    @Slot(int)
    def update_camera_zoom_value(self, zoom_value):
        self.camera_zoom = zoom_value

    @Slot(float)
    def set_camera_rotation(self, angle):
        """Set camera rotation angle."""
        self.align_controller.set_camera_rotation(angle)

    @Slot(bool)
    def set_camera_flip_h(self, flip_h):
        """Set camera horizontal flip."""
        self.align_controller.set_camera_flip_h(flip_h)

    @Slot(bool)
    def set_camera_flip_v(self, flip_v):
        """Set camera vertical flip."""
        self.align_controller.set_camera_flip_v(flip_v)

    @Slot(bool)
    def set_align_is_active(self, align_is_active):
        self.align_active = align_is_active

    @Slot(int)
    def update_threshold_value(self, new_threshold):
        self.align_controller.update_threshold_value(new_threshold)

    # ******* SETTINGS/PREFERENCES related functions. ******** #

    @Slot()
    def update_gerber_cfg(self):
        machine_sets = self.settings.machine_settings
        probe_working = machine_sets.tool_probe_rel_flag
        if probe_working:
            probe_pos = (
                machine_sets.tool_probe_offset_x_wpos,
                machine_sets.tool_probe_offset_y_wpos,
                machine_sets.tool_probe_offset_z_wpos,
            )
        else:
            probe_pos = (
                machine_sets.tool_probe_offset_x_mpos,
                machine_sets.tool_probe_offset_y_mpos,
                machine_sets.tool_probe_offset_z_mpos,
            )
        change_pos = (
            machine_sets.tool_change_offset_x_mpos,
            machine_sets.tool_change_offset_y_mpos,
            machine_sets.tool_change_offset_z_mpos,
        )
        cfg = Od(
            {
                "tool_probe_pos": probe_pos,
                "tool_probe_working": probe_working,  # False: machine pos or True: working pos
                "tool_probe_min": machine_sets.tool_probe_z_limit,
                "tool_change_pos": change_pos,
                "tool_probe_feedrate": (machine_sets.feedrate_xy, machine_sets.feedrate_z, machine_sets.feedrate_probe),
                "tool_probe_hold": machine_sets.hold_on_probe_flag,
                "tool_probe_zero": machine_sets.zeroing_after_probe_flag,
            }
        )
        self.gcr.load_cfg(cfg)
