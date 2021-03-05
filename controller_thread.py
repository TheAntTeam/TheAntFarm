from PySide2.QtCore import QRunnable, Slot, QFile, QTextStream, QObject, Signal, QTimer
from PySide2.QtGui import QPixmap
import re
import qimage2ndarray
from double_side_manager import DoubleSideManager
from pcb_manager import PcbObj


class ControllerSignals(QObject):
    update_path_s = Signal(str, str)         # Signal to update layer path in ui
    update_camera_image_s = Signal(QPixmap)  # Signal to update Camera Image in ui
    update_status_s = Signal(list)
    update_console_text_s = Signal(str)


class ControllerWorker(QRunnable):
    """Controller Worker thread"""

    SPLITPAT = re.compile(r"[:,]")

    def __init__(self, serial_rx_queue, serial_tx_queue, ui, vis_layer, *args, **kwargs):
        super(ControllerWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = ControllerSignals()

        self.ui = ui
        self.vis_layer = vis_layer

        self.double_side_manager = DoubleSideManager()

        self.serialRxQueue = serial_rx_queue
        self.serialTxQueue = serial_tx_queue

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.setInterval(120)
        self.timer.start()
        self.status_flag_poll = False
        self.status_l = []
        self.threshold_value = 0

        self.pcb = PcbObj()
        self.new_layer = ""
        self.new_layer_flag = False
        self.new_layer_path = ""
        self.new_layer_color = ""

        self.align_active = False
        self.finish_signal = False  # Thread termination signal

    def on_timeout(self):
        self.status_flag_poll = True

    def terminate_thread(self):
        """This function is to terminate thread."""
        self.finish_signal = True

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
                    break # todo: signal error

        return [status, mpos_l]

    def plot_layer(self, layer, layer_path, color):
        try:
            self.pcb.load_gerber(layer_path, layer)
            self.pcb.get_gerber(layer)
            top_layer = self.pcb.get_gerber_layer(layer)
            self.vis_layer.add_layer(top_layer[0], color)
        except (AttributeError, ValueError, ZeroDivisionError, IndexError):
            print("Error plotting new layer " + layer)

    @Slot(str, str, str)
    def set_new_layer(self, layer, layer_path, color):
        self.new_layer = layer
        self.new_layer_path = layer_path
        self.new_layer_color = color
        self.new_layer_flag = True

    @Slot(bool)
    def set_align_is_active(self, align_is_active):
        self.align_active = align_is_active

    @Slot(int)
    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    @Slot()
    def run(self):
        # self.signals.update_console_text_s.emit("Init Controller Worker Thread")

        while not self.finish_signal:
            if not self.serialRxQueue.empty():
                try:
                    element = self.serialRxQueue.get(block=False)
                    if element:
                        # self.signals.update_console_text_s.emit(self.parse_bracket_angle(element))
                        if re.match("^<.*>\s*$\s", element):
                            self.signals.update_status_s.emit(self.parse_bracket_angle(element))
                        elif re.match("ok\s*$\s", element):
                            pass
                        else:
                            self.signals.update_console_text_s.emit(element)
                except BlockingIOError:
                    pass
            if self.status_flag_poll:
                # refresh webcam frame
                if self.align_active:
                    frame = self.double_side_manager.get_webcam_frame()
                    # print(self.threshold_value)
                    frame = self.double_side_manager.detect_holes(frame, self.threshold_value)
                    image = qimage2ndarray.array2qimage(frame)
                    self.signals.update_camera_image_s.emit(QPixmap.fromImage(image))
                # Status poll
                self.serialTxQueue.put("?\n")  # todo: to be moved somewhere else
                self.status_flag_poll = False

            if self.new_layer_flag:
                self.plot_layer(self.new_layer, self.new_layer_path, self.new_layer_color)
                self.new_layer_flag = False
                self.signals.update_path_s.emit(self.new_layer, self.new_layer_path)


if __name__ == "__main__":
    pass
