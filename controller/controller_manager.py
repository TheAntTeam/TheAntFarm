from PySide2.QtCore import Slot, QObject, Signal, QTimer
from PySide2.QtGui import QPixmap
import re
from collections import OrderedDict as Od
from .controller_view import ViewController
from .controller_control import ControlController
from .controller_align import AlignController
import logging
import traceback

from shape_core.gcode_manager import GCoder

logger = logging.getLogger(__name__)


class ControllerWorker(QObject):
    update_layer_s = Signal(Od, str, str, bool)  # Signal to update layer visualization
    update_path_s = Signal(str, list)            # Signal to update path visualization
    update_camera_image_s = Signal(QPixmap)      # Signal to update Camera Image
    update_status_s = Signal(list)               # Signal to update controller status
    update_console_text_s = Signal(str)          # Signal to send text to the console textEdit
    serial_send_s = Signal(bytes)                # Signal to send text to the serial
    serial_tx_available_s = Signal()             # Signal to send text to the serial

    update_probe_s = Signal(list)                # Signal to update probe value
    send_abl_s = Signal(tuple, tuple)
    update_abl_s = Signal(list)                  # Signal to update Auto-Bed-Levelling value
    update_bbox_s = Signal(tuple)
    update_gcode_s = Signal(str, list, bool, bool)

    update_file_progress_s = Signal(float)

    reset_controller_status_s = Signal()
    stop_send_s = Signal()

    REMOTE_RX_BUFFER_MAX_SIZE = 128

    def __init__(self, serial_rx_queue, serial_tx_queue, settings):
        super(ControllerWorker, self).__init__()

        self.serialRxQueue = serial_rx_queue
        self.serialTxQueue = serial_tx_queue
        self.settings = settings

        self.view_controller = ViewController(self.settings)
        self.control_controller = ControlController(self.settings)
        self.align_controller = AlignController(self.settings)

        self.poll_timer = None
        self.alive_timer = None
        self.camera_timer = None

        self.align_active = False

        self.status_l = []
        self.status_to_ack = 0
        self.buffered_cmds = []
        self.cmds_to_ack = 0
        self.wait_tag_decoding = False
        self.dro_status_updated = False

        self.abl_apply_active = True
        self.prb_activated = False
        self.abl_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.prb_val = []
        self.abl_val = []
        self.abl_cmd_ls = []
        self.prb_num_todo = 0
        self.prb_num_done = 0
        self.prb_reps_todo = 1
        self.prb_reps_done = 0

        self.sending_file = False
        self.file_content = []
        self.file_progress = 0.0
        self.sent_lines = 0
        self.ack_lines = 0
        self.tot_lines = 0
        self.buffered_size = 0
        self.max_buffered_lines = 100
        self.min_buffer_threshold = 80

        self.active_gcode_path = ""

        self.gcr = GCoder("dummy", "commander")

    @Slot(bool)
    def on_controller_connection(self, connected):
        if connected:
            self.buffered_size = 0
            self.poll_timer.start()
        else:
            self.poll_timer.stop()

    def init_timers(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.on_poll_timeout)
        self.poll_timer.setInterval(120)
        # self.poll_timer.setSingleShot(True)
        # self.poll_timer.start()

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.on_camera_timeout)
        self.camera_timer.setInterval(120)
        self.camera_timer.start()

    # ***************** VIEW related functions. ***************** #

    @Slot(str, str)
    def load_new_layer(self, layer, layer_path):
        [loaded_layer, exc_flag] = self.view_controller.load_new_layer(layer, layer_path)
        if loaded_layer is not None:
            self.update_layer_s.emit(loaded_layer, layer, layer_path, exc_flag)

    @Slot(str, Od, str)
    def generate_new_path(self, tag, cfg, machining_type):
        new_paths = self.view_controller.generate_new_path(tag, cfg, machining_type)
        self.view_controller.generate_new_gcode_file(tag, cfg, machining_type, new_paths)
        self.update_path_s.emit(tag, new_paths)

    # ***************** CONTROL related functions. ***************** #
    def reset_dro_status_updated(self):
        self.dro_status_updated = False

    def send_to_tx_queue(self, data):
        parsered_cmd_str = self.decode_tag(data)
        logger.info(data)
        self.serialTxQueue.put(parsered_cmd_str)
        self.serial_tx_available_s.emit()

    def on_poll_timeout(self):
        status_poll = b"?"
        if not self.dro_status_updated:
            self.serial_send_s.emit(status_poll)
            # self.send_to_tx_queue(status_poll)
        else:
            self.serial_send_s.emit(status_poll)
            # self.send_to_tx_queue(status_poll)

    @Slot()
    def parse_rx_queue(self):
        if not self.serialRxQueue.empty():
            try:
                element = self.serialRxQueue.get(block=False)
                if element:
                    logger.debug("Element received: " + str(element))
                    if re.match("^<.*>\s*$\s", element):
                        self.update_status_s.emit(self.control_controller.parse_bracket_angle(element))
                        # This variable should be set to true the first time an ack is received.
                        if not self.dro_status_updated:
                            self.dro_status_updated = True
                    elif re.match("^\[.*\]\s*$\s", element):
                        self.control_controller.parse_bracket_square(element)
                        [ack_prb_flag, ack_abl_flag, send_next, other_cmd_flag] = \
                            self.control_controller.process_probe_and_abl()
                        if ack_prb_flag:
                            self.ack_probe()
                        if ack_abl_flag:
                            self.ack_auto_bed_levelling()
                        if send_next:
                            self.send_next_abl()
                        if other_cmd_flag:
                            if element:
                                self.update_console_text_s.emit(element)
                                logger.debug(element)
                    elif re.match("ok\s*$\s", element):
                        logger.debug("buffered size: " + str(self.buffered_size))
                        if self.sending_file and self.cmds_to_ack > 0:
                            # Update progress #
                            self.cmds_to_ack -= 1
                            self.ack_lines += 1
                            self.buffered_size -= len(self.buffered_cmds[0])
                            self.buffered_cmds.pop(0)
                            self.file_progress = (self.ack_lines / self.tot_lines) * 100
                            logger.debug("Acknowledged lines: " + str(self.ack_lines))
                            self.update_file_progress_s.emit(self.file_progress)

                            # all lines have been sent?
                            end_of_file = self.sent_lines >= self.tot_lines
                            print("End Of File: " + str(end_of_file))
                            if not end_of_file:
                                cmd_to_send = self.file_content[self.sent_lines]
                                # check if next command has tags
                                print("Cmd To Send: " + str(cmd_to_send))
                                if self.gcr.TAG in cmd_to_send:
                                    print("TAG Found")
                                    # if self.cmds_to_ack > 0:
                                    logger.info(str(self.ack_lines) + " <-> " + str(self.sent_lines))
                                    if self.ack_lines != self.sent_lines:
                                        # wait that the machine execute all previous lines
                                        # to be able to decode the tag
                                        print("Wait")
                                        self.wait_tag_decoding = True
                                    else:
                                        # machine execution queue is empty, let's go
                                        print("Run")
                                        self.wait_tag_decoding = False

                                # does data fit the buffer?
                                buff_available = (self.buffered_size + len(cmd_to_send)) < self.REMOTE_RX_BUFFER_MAX_SIZE
                            else:
                                self.wait_tag_decoding = False
                                buff_available = False

                            if not end_of_file and buff_available and not self.wait_tag_decoding:
                                # cmd_to_send = self.file_content[self.sent_lines]
                                self.send_to_tx_queue(cmd_to_send)
                                self.buffered_cmds.append(cmd_to_send)
                                logger.debug("TX:" + cmd_to_send)
                                self.buffered_size += len(cmd_to_send)
                                self.sent_lines += 1
                                self.cmds_to_ack += 1

                            if self.ack_lines == self.tot_lines:
                                self.stop_send_s.emit()
                                self.sending_file = False
                                logger.info("End of File sending.")

                    elif "error" in element.lower():
                        self.update_console_text_s.emit(element)
                        logger.error(element)
                        logger.debug(self.buffered_size)
                        logger.debug(self.sent_lines)
                        logger.debug(self.ack_lines)
                    else:
                        self.update_console_text_s.emit(element)
                        logger.debug(element)
            except BlockingIOError as e:
                logger.error(e, exc_info=True)
            except:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    def decode_tag(self, gcode_str):
        status = self.control_controller.status
        probe_data = self.control_controller.prb_val
        ret_str = self.gcr.compute_tag(gcode_str, status, probe_data)

        if self.gcr.TAG in str(gcode_str):
            logger.info("Tag Found: " + str(ret_str) + " [" + gcode_str + "]" )
        return ret_str

    def execute_gcode_cmd(self, cmd_str):
        """ Send generic G-CODE command coming from elsewhere. """
        print("Execute Gcode")
        parsered_cmd_str = self.decode_tag(cmd_str)
        logger.info("Sent GCODE: " + str(parsered_cmd_str))
        self.serial_send_s.emit(parsered_cmd_str)

    def cmd_probe(self, probe_z_max, probe_feed_rate):
        probe_cmd_s = self.control_controller.cmd_probe(probe_z_max, probe_feed_rate)
        logger.info(probe_cmd_s)
        self.serial_send_s.emit(probe_cmd_s)  # Execute probe

    def ack_probe(self):
        prb_val = self.control_controller.get_probe_value()
        logger.info("Probe: " + str(prb_val))
        self.update_probe_s.emit(prb_val)

    # def cmd_auto_bed_levelling(self, xy_coord_list, travel_z, probe_z_max, probe_feed_rate):
    #     self.control_controller.cmd_auto_bed_levelling(xy_coord_list, travel_z, probe_z_max, probe_feed_rate)
    #     self.send_next_abl()  # Send first probe command.
    def cmd_auto_bed_levelling(self, bbox_t, steps_t):
        self.control_controller.cmd_auto_bed_levelling(bbox_t, steps_t)
        self.send_next_abl()  # Send first probe command.

    def send_next_abl(self):
        next_abl_cmd = self.control_controller.get_next_abl_cmd()
        logger.info(next_abl_cmd)
        self.serial_send_s.emit(next_abl_cmd)  # Execute next Probe of Auto-Bed-Levelling

    def ack_auto_bed_levelling(self):
        self.abl_val = self.control_controller.get_abl_value()
        logger.info("ABL values: " + str(self.abl_val))
        # self.update_abl_s.emit(self.abl_val)
        self.select_active_gcode(self.active_gcode_path)

    def set_abl_active(self, abl_active=True):
        self.abl_apply_active = abl_active
        self.select_active_gcode(self.active_gcode_path)

    def vectorize_new_gcode_file(self, gcode_path):
        self.control_controller.load_gcode_file({}, gcode_path)

    def select_active_gcode(self, gcode_path):
        self.active_gcode_path = gcode_path
        redraw = False
        visible = True
        print("ABL_val " + str(self.abl_val))
        print("ABL_active " + str(self.abl_apply_active))
        if self.abl_val and self.abl_apply_active:
            self.control_controller.apply_abl(gcode_path)
            redraw = True
        else:
            redraw = self.control_controller.remove_abl(gcode_path)
        (tag, v) = self.control_controller.get_gcode_tag_and_v(gcode_path)
        self.update_gcode_s.emit(tag, v, visible, redraw)

    def get_gcode_data(self, gcode_path):
        return self.control_controller.get_gcode_tag_and_v(gcode_path)

    @Slot(str)
    def send_gcode_file(self, gcode_path):
        self.file_content = self.control_controller.get_gcode_lines(gcode_path)
        # with open(gcode_path) as f:            # DEBUG: take directly from file
        #     self.file_content = f.readlines()
        logger.debug(self.file_content)
        logger.info(self.file_content)
        if self.file_content:
            self.file_progress = 0.0
            self.cmds_to_ack = 0
            self.sent_lines = 0
            self.ack_lines = 0
            self.tot_lines = len(self.file_content)
            logger.info("Sending file: " + str(gcode_path))
            logger.info("Total lines: " + str(self.tot_lines))

            while self.sent_lines < self.tot_lines and \
                    (self.buffered_size + len(self.file_content[self.sent_lines])) < self.REMOTE_RX_BUFFER_MAX_SIZE:
                cmd_to_send = self.file_content[self.sent_lines]
                self.send_to_tx_queue(cmd_to_send)
                self.buffered_cmds.append(cmd_to_send)
                logger.debug(cmd_to_send)
                self.buffered_size += len(cmd_to_send)
                self.sent_lines += 1
                self.cmds_to_ack += 1
            logger.debug("Buffered size: " + str(self.buffered_size))
            self.sending_file = True

    def stop_gcode_file(self):
        self.sending_file = False
        self.execute_gcode_cmd(b"!")
        self.execute_gcode_cmd(b'\030')
        self.file_progress = 0.0
        self.cmds_to_ack = 0
        self.sent_lines = 0
        self.ack_lines = 0
        self.tot_lines = 0
        self.buffered_cmds = []
        self.buffered_size = 0
        self.wait_tag_decoding = False

    def pause_resume(self):
        logger.info("Status: " + str(self.control_controller.status))
        if "hold" in self.control_controller.status.lower():
            logger.info("UnHold")
            self.execute_gcode_cmd(b"~")
        else:
            logger.info("Hold")
            self.execute_gcode_cmd(b"!")

    def get_boundary_box(self):
        if not self.active_gcode_path == "":
            bbox_t = self.control_controller.get_boundary_box(self.active_gcode_path)
            self.update_bbox_s.emit(bbox_t)


# ***************** ALIGN related functions. ***************** #

    def on_camera_timeout(self):
        if self.align_active:
            image = self.align_controller.camera_new_frame()
            self.update_camera_image_s.emit(QPixmap.fromImage(image))

    @Slot(bool)
    def set_align_is_active(self, align_is_active):
        self.align_active = align_is_active

    @Slot(int)
    def update_threshold_value(self, new_threshold):
        self.align_controller.update_threshold_value(new_threshold)
