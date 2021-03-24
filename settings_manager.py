from PySide2.QtCore import QSettings, QPoint, QSize


class SettingsHandler:
    def __init__(self, organization_name, app_name, main_win):
        self.settings = QSettings(organization_name, app_name)
        self.main_win = main_win
        self.pos = QPoint(200, 200)
        self.size = QSize(960, 720)
        self.layer_last_dir = "."

    def read_all_settings(self):
        self.pos = QPoint(self.settings.value("pos", QPoint(200, 200)))
        self.size = QSize(self.settings.value("size", QSize(960, 720)))
        self.layer_last_dir = self.settings.value("layer_last_dir")
        self.main_win.resize(self.size)
        self.main_win.move(self.pos)

    def write_all_settings(self):
        self.settings.setValue("pos", self.main_win.pos())
        self.settings.setValue("size", self.main_win.size())
        self.settings.setValue("layer_last_dir", self.layer_last_dir)
