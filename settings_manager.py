from PySide2.QtCore import QPoint, QSize
import configparser
import os


class SettingsHandler:
    APP_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'configurations' + os.path.sep + 'app_config.ini')
    JOBS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'configurations' + os.path.sep + 'jobs_sets_config.ini')
    WIN_POS_X_DEFAULT = 200
    WIN_POS_Y_DEFAULT = 200
    WIN_SIZ_W_DEFAULT = 960
    WIN_SIZ_H_DEFAULT = 720
    LAYER_LAST_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), '.')

    def __init__(self, main_win):
        self.app_settings = configparser.ConfigParser()
        self.jobs_settings = configparser.ConfigParser()
        self.main_win = main_win
        self.pos = QPoint(self.WIN_POS_X_DEFAULT, self.WIN_POS_Y_DEFAULT)
        self.size = QSize(self.WIN_SIZ_W_DEFAULT, self.WIN_SIZ_H_DEFAULT)
        self.layer_last_dir = self.LAYER_LAST_DIR_DEFAULT

    def read_all_settings(self):
        """ Read all settings from ini files """
        self.read_all_app_settings()
        self.read_all_jobs_settings()

    def read_all_app_settings(self):
        """ Read all application settings from ini files """
        # Read application ini file #
        self.app_settings.read(self.APP_CONFIG_PATH)

        # GENERAL application settings #
        if "GENERAL" in self.app_settings:
            app_general = self.app_settings["GENERAL"]
            self.pos = QPoint(app_general.getint("win_position_x"), app_general.getint("win_position_y"))
            self.main_win.move(self.pos)  # Restore position
            self.size = QSize(app_general.getint("win_width"), app_general.getint("win_height"))
        self.main_win.resize(self.size)

        # Layers related application settings #
        if "LAYERS" in self.app_settings:
            app_layers_settings = self.app_settings["LAYERS"]
            self.layer_last_dir = app_layers_settings["layer_last_dir"]

    def read_all_jobs_settings(self):
        """ Read all jobs'settings from ini files """
        # Read jobs'settings ini file #
        self.jobs_settings.read(self.JOBS_CONFIG_PATH)

        # Top job related settings #
        if "TOP" in self.jobs_settings:
            top_settings = self.jobs_settings["TOP"]

    def write_all_settings(self):
        """ Write all settings to ini files """
        self.write_all_app_settings()
        self.write_all_jobs_settings()

    def write_all_app_settings(self):
        """ Write all application settings to ini files """
        self.app_settings["DEFAULT"] = {"win_position_x": self.WIN_POS_X_DEFAULT,
                                        "win_position_y": self.WIN_POS_Y_DEFAULT,
                                        "win_width": self.WIN_SIZ_W_DEFAULT,
                                        "win_height": self.WIN_SIZ_H_DEFAULT,
                                        "layer_last_dir": self.layer_last_dir}

        # GENERAL application settings #
        self.app_settings["GENERAL"] = {}
        app_general = self.app_settings["GENERAL"]
        app_general["win_position_x"] = str(self.main_win.pos().x())
        app_general["win_position_y"] = str(self.main_win.pos().y())
        app_general["win_width"] = str(self.main_win.width())
        app_general["win_height"] = str(self.main_win.height())

        # Layers related application settings #
        self.app_settings["LAYERS"] = {}
        app_layers = self.app_settings["LAYERS"]
        app_layers["last_load_dir"] = self.layer_last_dir

        # Write application ini file #
        with open(self.APP_CONFIG_PATH, 'w') as configfile:
            self.app_settings.write(configfile)

    def write_all_jobs_settings(self):
        """ Write all jobs settings to ini files """
        self.jobs_settings['DEFAULT'] = {"tool_diameter": 1.0}

        # Top job related settings #
        self.jobs_settings["TOP"] = {}
        top_settings = self.jobs_settings["TOP"]
        top_settings["tool_diameter"] = str(1.0)

        # Bottom job related settings #
        self.jobs_settings["BOTTOM"] = {}
        bottom_settings = self.jobs_settings["BOTTOM"]
        bottom_settings["tool_diameter"] = str(1.0)

        # Profile job related settings #
        self.jobs_settings["PROFILE"] = {}
        profile_settings = self.jobs_settings["PROFILE"]
        profile_settings["tool_diameter"] = str(1.0)

        # Drill job related settings #
        self.jobs_settings["DRILL"] = {}
        drill_settings = self.jobs_settings["DRILL"]
        drill_settings["tool_diameter"] = str(1.0)

        # No-Copper Top job related settings #
        self.jobs_settings["NC_TOP"] = {}
        nc_top_settings = self.jobs_settings["NC_TOP"]
        nc_top_settings["tool_diameter"] = str(1.0)

        # No-Copper Bottom job related settings #
        self.jobs_settings["NC_BOTTOM"] = {}
        nc_bottom_settings = self.jobs_settings["NC_BOTTOM"]
        nc_bottom_settings["tool_diameter"] = str(1.0)

        # Write application ini file #
        with open(self.JOBS_CONFIG_PATH, 'w') as configfile:
            self.jobs_settings.write(configfile)
