from PySide2.QtCore import QRunnable, Slot, QFile, QTextStream, QObject, Signal, QTimer
from PySide2.QtGui import QPixmap
import re
import qimage2ndarray
from double_side_manager import DoubleSideManager
from shape_core.pcb_manager import PcbObj
from collections import OrderedDict as Od
import logging

logger = logging.getLogger(__name__)


class ControllerWorker(QObject):
    update_layer_s = Signal(Od, str, str, bool)  # Signal to update layer visualization
    update_camera_image_s = Signal(QPixmap)      # Signal to update Camera Image
    update_status_s = Signal(list)               # Signal to update controller status
    update_console_text_s = Signal(str)          # Signal to send text to the console textEdit
    serial_send_s = Signal(str)                  # Signal to send text to the serial

    SPLITPAT = re.compile(r"[:,]")

    def __init__(self, serial_rx_queue):
        super(ControllerWorker, self).__init__()

        self.double_side_manager = DoubleSideManager()

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
        self.threshold_value = 0

        self.pcb = PcbObj()

        self.align_active = False

    def on_poll_timeout(self):
        self.serial_send_s.emit("?\n")

    def on_camera_timeout(self):
        if self.align_active:
            frame = self.double_side_manager.get_webcam_frame()
            logger.debug(str(self.threshold_value))
            frame = self.double_side_manager.detect_holes(frame, self.threshold_value)
            image = qimage2ndarray.array2qimage(frame)
            self.update_camera_image_s.emit(QPixmap.fromImage(image))

    def parse_bracket_angle(self, line):
        fields = line[1:-1].split("|")
        status = fields[0]
        mpos_l = []

        for field in fields[1:]:
            word = self.SPLITPAT.split(field)
            if word[0] == "MPos":
                try:
                    mpos_l = [word[1], word[2], word[3]]
                except (ValueError, IndexError):
                    logging.error("Error evaluating MPos")

        return [status, mpos_l]

    @Slot(str, str, str)
    def load_new_layer(self, layer, layer_path):
        try:
            grb_tags = self.pcb.GBR_KEYS
            exc_tags = self.pcb.EXN_KEYS
            if layer in grb_tags:
                self.pcb.load_gerber(layer_path, layer)
                self.pcb.get_gerber(layer)
                loaded_layer = self.pcb.get_gerber_layer(layer)
                self.update_layer_s.emit(loaded_layer, layer, layer_path, False)
            if layer in exc_tags:
                self.pcb.load_excellon(layer_path, layer)
                self.pcb.get_excellon(layer)
                loaded_layer = self.pcb.get_excellon_layer(layer)
                self.update_layer_s.emit(loaded_layer, layer, layer_path, True)
        except (AttributeError, ValueError, ZeroDivisionError, IndexError):
            logging.error("Error plotting new layer " + layer_path)

    @Slot(bool)
    def set_align_is_active(self, align_is_active):
        self.align_active = align_is_active

    @Slot(int)
    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    @Slot()
    def parse_rx_queue(self):
        if not self.serialRxQueue.empty():
            try:
                element = self.serialRxQueue.get(block=False)
                if element:
                    # self.update_console_text_s.emit(self.parse_bracket_angle(element))
                    if re.match("^<.*>\s*$\s", element):
                        self.update_status_s.emit(self.parse_bracket_angle(element))
                    elif re.match("ok\s*$\s", element):
                        pass
                    else:
                        self.update_console_text_s.emit(element)
            except BlockingIOError:
                pass
