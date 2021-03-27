from PySide2.QtCore import QSettings, QPoint, QSize


class SettingsHandler:
    def __init__(self, organization_name, app_name, set_name, main_win):
        self.app_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, organization_name, app_name)
        self.job_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, organization_name, set_name)
        self.main_win = main_win
        self.pos = QPoint(200, 200)
        self.size = QSize(960, 720)
        self.layer_last_dir = "."

    def read_all_settings(self):
        self.pos = QPoint(self.app_settings.value("pos", QPoint(200, 200)))
        self.size = QSize(self.app_settings.value("size", QSize(960, 720)))
        self.layer_last_dir = self.app_settings.value("layer_last_dir")
        self.main_win.resize(self.size)
        self.main_win.move(self.pos)

    def write_all_settings(self):
        self.app_settings.setValue("pos", self.main_win.pos())
        self.app_settings.setValue("size", self.main_win.size())
        self.app_settings.setValue("layer_last_dir", self.layer_last_dir)
        self.job_settings.setValue("Test", 15)
