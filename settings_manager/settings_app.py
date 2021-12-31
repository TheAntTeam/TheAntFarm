from PySide2.QtCore import QPoint, QSize
import configparser
import os


class AppSettingsHandler:
    # APP CONFIGURATION DEFAULT VALUES
    LOGS_DIR_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../app_logs'))
    LOGS_FILE_DEFAULT = os.path.normpath(os.path.join(LOGS_DIR_DEFAULT, 'app_logs.log'))
    LOGS_MAX_BYTES = 1000000
    LOGS_BACKUP_COUNT = 10
    WIN_POS_X_DEFAULT = 200
    WIN_POS_Y_DEFAULT = 200
    WIN_SIZE_W_DEFAULT = 1160
    WIN_SIZE_H_DEFAULT = 720
    MAIN_TAB_INDEX_DEFAULT = 0
    CTRL_TAB_INDEX_DEFAULT = 0
    SHOW_CONSOLE_DEFAULT = False
    LAYER_LAST_DIR_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    GCODE_LAST_DIR_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

    def __init__(self, config_folder, main_win):
        self.app_config_path = os.path.normpath(os.path.join(config_folder, 'app_config.ini'))
        self.app_settings = configparser.ConfigParser()

        if not os.path.isdir(self.LOGS_DIR_DEFAULT):
            os.makedirs(self.LOGS_DIR_DEFAULT)
        self.logs_folder = self.LOGS_DIR_DEFAULT
        self.logs_file = self.LOGS_FILE_DEFAULT
        self.logs_max_bytes = self.LOGS_MAX_BYTES
        self.logs_backup_count = self.LOGS_BACKUP_COUNT

        self.main_win = main_win
        self.pos = QPoint(self.WIN_POS_X_DEFAULT, self.WIN_POS_Y_DEFAULT)
        self.size = QSize(self.WIN_SIZE_W_DEFAULT, self.WIN_SIZE_H_DEFAULT)
        self.main_tab_index = self.MAIN_TAB_INDEX_DEFAULT
        self.ctrl_tab_index = self.CTRL_TAB_INDEX_DEFAULT
        self.console_visibility = self.SHOW_CONSOLE_DEFAULT
        self.layer_last_dir = self.LAYER_LAST_DIR_DEFAULT
        self.gcode_last_dir = self.GCODE_LAST_DIR_DEFAULT

    def read_all_app_settings(self):
        """ Read all application settings from ini files """
        # If app settings file does NOT exist create it with default values
        if not os.path.isfile(self.app_config_path):
            self.restore_app_settings()

        # Read application ini file #
        self.app_settings.read(self.app_config_path)

        # GENERAL application settings #
        if "GENERAL" in self.app_settings:
            app_general = self.app_settings["GENERAL"]
            self.pos = QPoint(app_general.getint("win_position_x", self.WIN_POS_X_DEFAULT),
                              app_general.getint("win_position_y", self.WIN_POS_Y_DEFAULT))
            self.main_win.move(self.pos)  # Restore position
            self.size = QSize(app_general.getint("win_width", self.WIN_SIZE_W_DEFAULT),
                              app_general.getint("win_height", self.WIN_SIZE_H_DEFAULT))
            self.main_tab_index = app_general.getint("main_tab_index", self.MAIN_TAB_INDEX_DEFAULT)
            self.ctrl_tab_index = app_general.getint("ctrl_tab_index", self.CTRL_TAB_INDEX_DEFAULT)
            self.console_visibility = app_general.getboolean("console_visibility", self.SHOW_CONSOLE_DEFAULT)
            self.logs_file = app_general.get('logs_file', self.LOGS_FILE_DEFAULT)
            self.logs_max_bytes = app_general.getint('logs_max_bytes', self.LOGS_MAX_BYTES)
            self.logs_backup_count = app_general.getint('logs_backup_count', self.LOGS_BACKUP_COUNT)
        # Apply general settings.
        self.main_win.resize(self.size)
        self.main_win.ui.main_tab_widget.setCurrentIndex(self.main_tab_index)
        self.main_win.ui.ctrl_tab_widget.setCurrentIndex(self.ctrl_tab_index)
        self.main_win.ui.actionHide_Show_Console.setChecked(self.console_visibility)

        # Layers related application settings #
        if "LAYERS" in self.app_settings:
            app_layers_settings = self.app_settings["LAYERS"]
            self.layer_last_dir = app_layers_settings.get("layer_last_dir", self.LAYER_LAST_DIR_DEFAULT)

        if "GCODES" in self.app_settings:
            app_gcode_settings = self.app_settings["GCODES"]
            self.gcode_last_dir = app_gcode_settings.get("gcode_last_dir", self.GCODE_LAST_DIR_DEFAULT)

    def write_all_app_settings(self):
        """ Write all application settings to ini files """
        self.app_settings["DEFAULT"] = {"win_position_x": self.WIN_POS_X_DEFAULT,
                                        "win_position_y": self.WIN_POS_Y_DEFAULT,
                                        "win_width": self.WIN_SIZE_W_DEFAULT,
                                        "win_height": self.WIN_SIZE_H_DEFAULT,
                                        "main_tab_index": self.MAIN_TAB_INDEX_DEFAULT,
                                        "ctrl_tab_index": self.CTRL_TAB_INDEX_DEFAULT,
                                        "console_visibility": self.console_visibility,
                                        "layer_last_dir": self.LAYER_LAST_DIR_DEFAULT,
                                        "gcode_last_dir": self.GCODE_LAST_DIR_DEFAULT,
                                        "logs_file": self.LOGS_FILE_DEFAULT,
                                        "logs_max_bytes": self.LOGS_MAX_BYTES,
                                        "logs_backup_count": self.LOGS_BACKUP_COUNT}

        # GENERAL application settings #
        self.app_settings["GENERAL"] = {}
        app_general = self.app_settings["GENERAL"]
        app_general["win_position_x"] = str(self.main_win.pos().x())
        app_general["win_position_y"] = str(self.main_win.pos().y())
        app_general["win_width"] = str(self.main_win.width())
        app_general["win_height"] = str(self.main_win.height())
        app_general["main_tab_index"] = str(self.main_win.ui.main_tab_widget.currentIndex())
        app_general["ctrl_tab_index"] = str(self.main_win.ui.ctrl_tab_widget.currentIndex())
        app_general["console_visibility"] = str(self.main_win.ui.actionHide_Show_Console.isChecked())
        app_general["logs_file"] = str(self.LOGS_FILE_DEFAULT)
        app_general["logs_max_bytes"] = str(self.LOGS_MAX_BYTES)
        app_general["logs_backup_count"] = str(self.LOGS_BACKUP_COUNT)

        # Layers related application settings #
        self.app_settings["LAYERS"] = {}
        app_layers = self.app_settings["LAYERS"]
        app_layers["layer_last_dir"] = self.layer_last_dir

        # Layers related application settings #
        self.app_settings["GCODES"] = {}
        app_layers = self.app_settings["GCODES"]
        app_layers["gcode_last_dir"] = self.gcode_last_dir

        # Write application ini file #
        with open(self.app_config_path, 'w') as configfile:
            self.app_settings.write(configfile)

    def restore_app_settings(self):
        """ Restore all application settings to default and create ini file if it doesn't exists """
        self.app_settings["DEFAULT"] = {"win_position_x": self.WIN_POS_X_DEFAULT,
                                        "win_position_y": self.WIN_POS_Y_DEFAULT,
                                        "win_width": self.WIN_SIZE_W_DEFAULT,
                                        "win_height": self.WIN_SIZE_H_DEFAULT,
                                        "main_tab_index": self.MAIN_TAB_INDEX_DEFAULT,
                                        "ctrl_tab_index": self.CTRL_TAB_INDEX_DEFAULT,
                                        "console_visibility": self.console_visibility,
                                        "layer_last_dir": self.LAYER_LAST_DIR_DEFAULT,
                                        "gcode_last_dir": self.GCODE_LAST_DIR_DEFAULT,
                                        "logs_file": self.LOGS_FILE_DEFAULT,
                                        "logs_max_bytes": self.LOGS_MAX_BYTES,
                                        "logs_backup_count": self.LOGS_BACKUP_COUNT}

        # GENERAL application settings #
        self.app_settings["GENERAL"] = {}
        app_general = self.app_settings["GENERAL"]
        app_general["win_position_x"] = str(self.WIN_POS_X_DEFAULT)
        app_general["win_position_y"] = str(self.WIN_POS_Y_DEFAULT)
        app_general["win_width"] = str(self.WIN_SIZE_W_DEFAULT)
        app_general["win_height"] = str(self.WIN_SIZE_H_DEFAULT)
        app_general["main_tab_index"] = str(self.MAIN_TAB_INDEX_DEFAULT)
        app_general["ctrl_tab_index"] = str(self.CTRL_TAB_INDEX_DEFAULT)
        app_general["console_visibility"] = str(self.SHOW_CONSOLE_DEFAULT)
        app_general["logs_file"] = str(self.LOGS_FILE_DEFAULT)
        app_general["logs_max_bytes"] = str(self.LOGS_MAX_BYTES)
        app_general["logs_backup_count"] = str(self.LOGS_BACKUP_COUNT)

        # Layers related application settings #
        self.app_settings["LAYERS"] = {}
        app_layers = self.app_settings["LAYERS"]
        app_layers["layer_last_dir"] = str(self.LAYER_LAST_DIR_DEFAULT)

        # Layers related application settings #
        self.app_settings["GCODES"] = {}
        app_layers = self.app_settings["GCODES"]
        app_layers["gcode_last_dir"] = str(self.GCODE_LAST_DIR_DEFAULT)

        # Write application ini file #
        with open(self.app_config_path, 'w') as configfile:
            self.app_settings.write(configfile)

