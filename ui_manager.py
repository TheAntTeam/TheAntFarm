import os
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap


class UiManager(QObject):
    """Manage UI objects, signals and slots"""

    load_layer_s = Signal(str, str, str)
    align_active_s = Signal(bool)
    update_threshold_s = Signal(int)

    def __init__(self, main_win, ui, control_worker, serial_worker, *args, **kwargs):
        super(UiManager, self).__init__()
        self.last_open_dir = "."
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker

        # Connect Widgets signals and slots
        # From UI to UI Manager
        self.ui.tabWidget.currentChanged.connect(self.check_align_is_active)
        self.ui.verticalSlider.valueChanged.connect(self.update_threshold)
        # From UI Manager to Controller
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.load_layer_s.connect(self.controlWo.set_new_layer)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)
        self.ui.topLoadButton.clicked.connect(lambda: self.load_gerber_file("top", "Load Top Gerber File", "Gerber (*.gbr *.GBR)", "red"))
        self.ui.bottomLoadButton.clicked.connect(lambda: self.load_gerber_file("bottom", "Load Bottom Gerber File", "Gerber (*.gbr *.GBR)", "blue"))
        self.ui.profileLoadButton.clicked.connect(lambda: self.load_gerber_file("profile", "Load Profile Gerber File", "Gerber (*.gbr *.GBR)", "black"))
        self.ui.drillLoadButton.clicked.connect(lambda: self.load_gerber_file("drill", "Load Drill Excellon File", "Excellon (*.xln *.XLN)", "green"))
        # From Controller Thread to UI Manager
        self.controlWo.signals.update_path_s.connect(self.set_layer_path)
        self.controlWo.signals.update_camera_image_s.connect(self.update_camera_image)
        self.controlWo.signals.update_status_s.connect(self.update_status)
        self.controlWo.signals.update_console_text_s.connect(self.update_console_text)
        # From Serial Thread to UI Manager
        self.serialWo.signals.update_console_text_s.connect(self.update_console_text)

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

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        self.ui.label_2.setPixmap(pixmap)

    @Slot(list)
    def update_status(self, status_l):
        self.ui.statusLabel.setText(status_l[0])
        self.ui.mpos_x_label.setText(status_l[1][0])
        self.ui.mpos_y_label.setText(status_l[1][1])
        self.ui.mpos_z_label.setText(status_l[1][2])

    @Slot(str)
    def update_console_text(self, new_text):
        self.ui.textEdit.append(new_text)

    def check_align_is_active(self):
        # print(self.ui.tabWidget.currentWidget().objectName())
        if self.ui.tabWidget.currentWidget().objectName() == "alignTab":
            self.align_active_s.emit(True)
        else:
            self.align_active_s.emit(False)

    def update_threshold(self):
        self.update_threshold_s.emit(self.ui.verticalSlider.value())


if __name__ == "__main__":
    pass
