import os
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import Signal, Slot, QObject
from controller_thread import ControllerWorker


class UiManager(QObject):
    """Manage UI objects, signals and slots"""

    load_layer_s = Signal(str, str, str)

    def __init__(self, main_win, ui, control_worker, *args, **kwargs):
        super(UiManager, self).__init__()
        self.last_open_dir = "."
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker

        # Connect Widgets signals and slots
        self.load_layer_s.connect(self.controlWo.set_new_layer)
        self.controlWo.signals.updatePath.connect(self.set_layer_path)
        self.ui.topLoadButton.clicked.connect(lambda: self.load_gerber_file("top", "Load Top Gerber File", "Gerber (*.gbr *.GBR)", "red"))
        self.ui.bottomLoadButton.clicked.connect(lambda: self.load_gerber_file("bottom", "Load Bottom Gerber File", "Gerber (*.gbr *.GBR)", "blue"))
        self.ui.profileLoadButton.clicked.connect(lambda: self.load_gerber_file("profile", "Load Profile Gerber File", "Gerber (*.gbr *.GBR)", "black"))
        self.ui.drillLoadButton.clicked.connect(lambda: self.load_gerber_file("drill", "Load Drill Excellon File", "Excellon (*.xln *.XLN)", "green"))

    def load_gerber_file(self, layer="top", load_text="Load File", extensions="", color="red"):
        filters = extensions + ";;All files (*.*)"
        load_file_path = QFileDialog.getOpenFileName(self.main_win, load_text, self.last_open_dir, filters)
        if load_file_path[0]:
            self.last_open_dir = os.path.dirname(load_file_path[0])
            self.ui.consoleTextEdit.append("Loading " + load_file_path[0])

            self.load_layer_s.emit(layer, load_file_path[0], color)

    @Slot(str, str)
    def set_layer_path(self, layer, layer_path):
        if layer == "top": #todo: use a dictionary or something similar???
            self.ui.topFileLineEdit.setText(layer_path)
        elif layer == "bottom":
            self.ui.bottomFileLineEdit.setText(layer_path)
        elif layer == "profile":
            self.ui.profileFileLineEdit.setText(layer_path)
        elif layer == "drill":
            self.ui.drillFileLineEdit.setText(layer_path)

