from PySide2.QtCore import QRunnable, Slot, QFile, QTextStream, QObject, Signal, QTimer
from PySide2.QtGui import QPixmap
import re
import qimage2ndarray
from double_side_manager import DoubleSideManager
from pcb_manager import PcbObj


class ControllerSignals(QObject):
    updatePath = Signal(str, str)  # Signal to update layer path in ui


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
        self.save_file = False
        self.save_filename = ""
        self.status_label = ui.statusLabel
        self.mpos_x_label = ui.mpos_x_label
        self.mpos_y_label = ui.mpos_y_label
        self.mpos_z_label = ui.mpos_z_label
        self.text_out = ui.textEdit  # Gui text field where events are logged

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.setInterval(120)
        self.timer.start()
        self.status_flag_poll = False
        self.status_l = []

        self.pcb = PcbObj()
        self.new_layer = ""
        self.new_layer_flag = False
        self.new_layer_path = ""
        self.new_layer_color = ""

        # self.signal = signal
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

    @Slot()
    def run(self):
        # print("Init Controller Worker Thread")
        # self.text_out.append("Init Controller Worker Thread")

        while not self.finish_signal:
            if not self.serialRxQueue.empty():
                try:
                    element = self.serialRxQueue.get(block=False)
                    if element:
                        # self.text_out.append(self.parse_bracket_angle(element))
                        if re.match("^<.*>\s*$\s", element):
                            self.status_l = self.parse_bracket_angle(element)
                            self.status_label.setText(self.status_l[0])
                            self.mpos_x_label.setText(self.status_l[1][0])
                            self.mpos_y_label.setText(self.status_l[1][1])
                            self.mpos_z_label.setText(self.status_l[1][2])
                        elif re.match("ok\s*$\s", element):
                            pass
                        else:
                            self.text_out.append(element)
                except BlockingIOError:
                    pass
            if self.status_flag_poll:
                # refresh webcam frame
                if self.ui.tabWidget.currentIndex() == 1:  # todo: check active tab by name
                    frame = self.double_side_manager.get_webcam_frame()
                    thr1 = self.ui.verticalSlider.value()
                    print(thr1)
                    frame = self.double_side_manager.detect_holes(frame, thr1)
                    image = qimage2ndarray.array2qimage(frame)
                    self.ui.label_2.setPixmap(QPixmap.fromImage(image))
                # Status poll
                self.serialTxQueue.put("?\n")  # todo: to be moved somewhere else
                self.status_flag_poll = False

            if self.new_layer_flag:
                self.plot_layer(self.new_layer, self.new_layer_path, self.new_layer_color)
                self.new_layer_flag = False
                self.signals.updatePath.emit(self.new_layer, self.new_layer_path)


if __name__ == "__main__":
    pass
