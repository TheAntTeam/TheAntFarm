from PySide2.QtCore import QRunnable, Slot, QTimer
from PySide2.QtGui import QPixmap
import re
import qimage2ndarray
from double_side_manager import DoubleSideManager
from pcb_manager import PcbObj


class ViewWorker(QRunnable):
    """View Worker thread"""

    def __init__(self, ui, vis_layer, *args, **kwargs):
        super(ViewWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs

        self.ui = ui
        self.vis_layer = vis_layer

        self.new_layer = ""
        self.new_layer_flag = False
        self.new_layer_path = ""
        self.new_layer_color = ""

        # self.signal = signal
        self.finish_signal = False  # Thread termination signal

    def terminate_thread(self):
        """This function is to terminate thread."""
        self.finish_signal = True

    def plot_layer(self, layer_path, color):
        pcb = PcbObj()
        pcb.load_gerber(layer_path, 'top')
        pcb.get_gerber('top')
        top_layer = pcb.get_gerber_layer('top')
        self.vis_layer.add_layer(top_layer[0], color)

    @Slot()
    def run(self):
        # print("Init Controller Worker Thread")
        # self.text_out.append("Init Controller Worker Thread")

        while not self.finish_signal:
            if self.new_layer_flag:
                self.plot_layer(self.new_layer_path,self.new_layer_color)
                self.new_layer_flag = False


if __name__ == "__main__":
    pass
