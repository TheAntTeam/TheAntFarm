from PySide2.QtCore import Slot, QObject, Signal, QTimer
from PySide2.QtGui import QPixmap
import re
from collections import OrderedDict as Od
from .controller_view import ViewController
from .controller_control import ControlController
from .controller_align import AlignController
import logging
import traceback

logger = logging.getLogger(__name__)


class ControllerWorker(QObject):
    update_layer_s = Signal(Od, str, str, bool)  # Signal to update layer visualization
    update_path_s = Signal(str, list)            # Signal to update path visualization
    update_camera_image_s = Signal(QPixmap)      # Signal to update Camera Image
    update_status_s = Signal(list)               # Signal to update controller status
    update_console_text_s = Signal(str)          # Signal to send text to the console textEdit
    serial_send_s = Signal(str)                  # Signal to send text to the serial

    update_probe_s = Signal(list)                # Signal to update probe value
    update_abl_s = Signal(list)                  # Signal to update Auto-Bed-Levelling value

    def __init__(self, serial_rx_queue):
        super(ControllerWorker, self).__init__()

        self.view_controller = ViewController()
        self.control_controller = ControlController()
        self.align_controller = AlignController()

        self.serialRxQueue = serial_rx_queue

        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.on_poll_timeout)
        self.poll_timer.setInterval(120)
        self.poll_timer.start()

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.on_camera_timeout)
        self.camera_timer.setInterval(120)
        self.camera_timer.start()

        self.status_l = []

        self.align_active = False

        self.dro_status_updated = False
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

    def on_poll_timeout(self):
        self.serial_send_s.emit(str("?\n"))  # "?\n")

    @Slot()
    def parse_rx_queue(self):
        if not self.serialRxQueue.empty():
            try:
                element = self.serialRxQueue.get(block=False)
                if element:
                    logging.debug("Element received: " + element)
                    if re.match("^<.*>\s*$\s", element):
                        self.update_status_s.emit(self.control_controller.parse_bracket_angle(element))
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
                            self.update_console_text_s.emit(element)
                    elif re.match("ok\s*$\s", element):
                        pass
                    else:
                        self.update_console_text_s.emit(element)
            except BlockingIOError as e:
                logging.error(e, exc_info=True)
            except:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    def execute_gcode_cmd(self, cmd_str):
        """ Send generic G-CODE command coming from elsewhere. """
        logging.debug(cmd_str)
        self.serial_send_s.emit(cmd_str)

    def cmd_probe(self, probe_z_max, probe_feed_rate):
        probe_cmd_s = self.control_controller.cmd_probe(probe_z_max, probe_feed_rate)
        logging.info(probe_cmd_s)
        self.serial_send_s.emit(probe_cmd_s)  # Execute probe

    def ack_probe(self):
        prb_val = self.control_controller.get_probe_value()
        logging.info("Probe: " + str(prb_val))
        self.update_probe_s.emit(prb_val)

    def cmd_auto_bed_levelling(self, xy_coord_list, travel_z, probe_z_max, probe_feed_rate):
        self.control_controller.cmd_auto_bed_levelling(xy_coord_list, travel_z, probe_z_max, probe_feed_rate)
        self.send_next_abl()  # Send first probe command.

    def send_next_abl(self):
        next_abl_cmd = self.control_controller.get_next_abl_cmd()
        logging.info(next_abl_cmd)
        self.serial_send_s.emit(next_abl_cmd)  # Execute next Probe of Auto-Bed-Levelling

    def ack_auto_bed_levelling(self):
        abl_values = self.control_controller.get_abl_value()
        logging.info("ABL values: " + str(abl_values))
        self.update_abl_s.emit(abl_values)

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
