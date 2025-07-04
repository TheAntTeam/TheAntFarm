from PySide6.QtCore import QPoint, QSize
from collections import OrderedDict as Od
from __init__ import __version__
import configparser
import os


class AppSettingsHandler:
    # APP CONFIGURATION DEFAULT VALUES
    APP_VERSION_DEFAULT = "0.3.0"
    LOGS_DIR_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'app_logs'))
    LOGS_FILE_DEFAULT = os.path.normpath(os.path.join(LOGS_DIR_DEFAULT, 'app_logs.log'))
    LOGS_MAX_BYTES = 1000000
    LOGS_BACKUP_COUNT = 2
    WIN_POS_X_DEFAULT = 200
    WIN_POS_Y_DEFAULT = 200
    WIN_SIZE_W_DEFAULT = 1160
    WIN_SIZE_H_DEFAULT = 720
    WIN_MAXIMIZED_DEFAULT = False
    MAIN_TAB_INDEX_DEFAULT = 0
    CTRL_TAB_INDEX_DEFAULT = 0
    SETTINGS_TAB_INDEX_DEFAULT = 0
    SHOW_ALIGN_TAB_DEFAULT = False
    SHOW_SETTINGS_TAB_DEFAULT = False
    SHOW_CONSOLE_DEFAULT = False
    LAST_SERIAL_PORT_DEFAULT = ""
    LAST_SERIAL_BAUD_DEFAULT = 115200
    LAYER_LAST_DIR_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../..'))
    GCODE_LAST_DIR_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../..'))
    TOP_LAYER_COLOR_DEFAULT = "#FFC300"
    BOTTOM_LAYER_COLOR_DEFAULT = "#A3E4D7"
    PROFILE_LAYER_COLOR_DEFAULT = "#000000"
    DRILL_LAYER_COLOR_DEFAULT = "#999999"
    NC_TOP_LAYER_COLOR_DEFAULT = "#800080"
    NC_BOTTOM_LAYER_COLOR_DEFAULT = "#A52A2A"

    CAMERA_SELECTED_OR_TOOL_DEFAULT = False  # Default selection should be tool, camera could be absent
    FLIP_HORIZONTAL_SELECTED_DEFAULT = False
    FLIP_VERTICAL_SELECTED_DEFAULT = False

    def __init__(self, config_folder, main_win):

        if os.path.isdir(main_win.local_path):
            logs_dir_default = os.path.join(main_win.local_path, "app_logs")
            self.logs_file_default = os.path.normpath(os.path.join(logs_dir_default, 'app_logs.log'))
            self.logs_folder = os.path.join(main_win.local_path, "app_logs")
            self.logs_file = self.logs_file_default

            self.layer_last_dir_default = main_win.local_path
            self.gcode_last_dir_default = main_win.local_path

        else:
            self.logs_file_default = self.LOGS_FILE_DEFAULT
            self.logs_folder = self.LOGS_DIR_DEFAULT
            self.logs_file = self.logs_file_default

            self.layer_last_dir_default = self.LAYER_LAST_DIR_DEFAULT
            self.gcode_last_dir_default = self.GCODE_LAST_DIR_DEFAULT

        if not os.path.isdir(self.logs_folder):
            os.makedirs(self.logs_folder)

        self.app_config_path = os.path.normpath(os.path.join(config_folder, 'app_config.ini'))
        self.app_settings = configparser.ConfigParser()

        self.app_version = self.APP_VERSION_DEFAULT

        self.logs_max_bytes = self.LOGS_MAX_BYTES
        self.logs_backup_count = self.LOGS_BACKUP_COUNT

        self.main_win = main_win
        self.pos = QPoint(self.WIN_POS_X_DEFAULT, self.WIN_POS_Y_DEFAULT)
        self.size = QSize(self.WIN_SIZE_W_DEFAULT, self.WIN_SIZE_H_DEFAULT)
        self.win_maximized = self.WIN_MAXIMIZED_DEFAULT
        self.main_tab_index = self.MAIN_TAB_INDEX_DEFAULT
        self.ctrl_tab_index = self.CTRL_TAB_INDEX_DEFAULT
        self.settings_tab_index = self.SETTINGS_TAB_INDEX_DEFAULT
        self.align_tab_visibility = self.SHOW_ALIGN_TAB_DEFAULT
        self.settings_tab_visibility = self.SHOW_SETTINGS_TAB_DEFAULT
        self.console_visibility = self.SHOW_CONSOLE_DEFAULT
        self.last_serial_port = self.LAST_SERIAL_PORT_DEFAULT
        self.last_serial_baud = self.LAST_SERIAL_BAUD_DEFAULT
        self.layer_last_dir = self.layer_last_dir_default
        self.gcode_last_dir = self.gcode_last_dir_default
        self.layer_color = Od({})
        self.layer_color["top"] = self.TOP_LAYER_COLOR_DEFAULT
        self.layer_color["bottom"] = self.BOTTOM_LAYER_COLOR_DEFAULT
        self.layer_color["profile"] = self.PROFILE_LAYER_COLOR_DEFAULT
        self.layer_color["drill"] = self.DRILL_LAYER_COLOR_DEFAULT
        self.layer_color["nc_top"] = self.NC_TOP_LAYER_COLOR_DEFAULT
        self.layer_color["nc_bottom"] = self.NC_BOTTOM_LAYER_COLOR_DEFAULT

        self.camera_selected_or_tool = self.CAMERA_SELECTED_OR_TOOL_DEFAULT
        self.flip_horizontal_selected = self.FLIP_HORIZONTAL_SELECTED_DEFAULT
        self.flip_vertical_selected = self.FLIP_VERTICAL_SELECTED_DEFAULT

    @staticmethod
    def choose_version(version_s, version_default_s):
        """
        Choose between the actual version and the default version.
        The version shall be 3 integer numbers (major, minor, build).
        If both the version and default version strings are in a wrong format,
        "0.0.0" is returned.
        If one of the versions string is in a wrong format, the other one is returned.
        If both the versions are ok, the greater is returned.

        Parameters
        ----------
        version_s
        version_default_s

        Returns
        -------
        The actual cleaned-up version string.
        """
        version_wrong_format_flag = True
        version_wrong_default_format_flag = True
        try:
            version_t = tuple(map(int, (version_s.split("."))))
            if len(version_t) == 3:
                version_wrong_format_flag = False
        except ValueError as e:
            print("version number wrong format")  # logger is not active at this point

        try:
            version_default_t = tuple(map(int, (version_default_s.split("."))))
            if len(version_default_t) == 3:
                version_wrong_default_format_flag = False
        except Exception as e:
            print("default version number wrong format")

        if version_wrong_format_flag and version_wrong_default_format_flag:
            print("both version number wrong format")
            return "0.0.0"
        elif version_wrong_format_flag:
            return version_default_s
        elif version_wrong_default_format_flag:
            return version_s

        if version_t[0] < version_default_t[0]:
            return version_default_s
        elif version_t[0] == version_default_t[0]:
            if version_t[1] < version_default_t[1]:
                return version_default_s
            elif version_t[1] == version_default_t[1]:
                if version_t[2] < version_default_t[2]:
                    return version_default_s
        return version_s

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
            # The following function should choose and clean up the version.
            self.app_version = self.choose_version(__version__, self.APP_VERSION_DEFAULT)

            self.pos = QPoint(app_general.getint("win_position_x", self.WIN_POS_X_DEFAULT),
                              app_general.getint("win_position_y", self.WIN_POS_Y_DEFAULT))
            self.size = QSize(app_general.getint("win_width", self.WIN_SIZE_W_DEFAULT),
                              app_general.getint("win_height", self.WIN_SIZE_H_DEFAULT))
            self.win_maximized = app_general.getboolean("win_maximized", self.WIN_MAXIMIZED_DEFAULT)
            self.main_tab_index = app_general.getint("main_tab_index", self.MAIN_TAB_INDEX_DEFAULT)
            self.ctrl_tab_index = app_general.getint("ctrl_tab_index", self.CTRL_TAB_INDEX_DEFAULT)
            self.settings_tab_index = app_general.getint("settings_tab_index", self.SETTINGS_TAB_INDEX_DEFAULT)
            self.align_tab_visibility = app_general.getboolean("align_tab_visibility", self.SHOW_ALIGN_TAB_DEFAULT)
            self.settings_tab_visibility = app_general.getboolean("settings_tab_visibility",
                                                                  self.SHOW_SETTINGS_TAB_DEFAULT)
            self.console_visibility = app_general.getboolean("console_visibility", self.SHOW_CONSOLE_DEFAULT)
            self.logs_file = app_general.get('logs_file', self.logs_file_default)
            if not os.path.isdir(os.path.dirname(os.path.abspath(self.logs_file))):
                self.logs_file = self.logs_file_default  # restore logs file with the default path
            self.logs_max_bytes = app_general.getint('logs_max_bytes', self.LOGS_MAX_BYTES)
            self.logs_backup_count = app_general.getint('logs_backup_count', self.LOGS_BACKUP_COUNT)
            self.last_serial_port = app_general.get("last_serial_port", self.LAST_SERIAL_PORT_DEFAULT)
            try:
                self.last_serial_baud = app_general.getint("last_serial_baud", self.LAST_SERIAL_BAUD_DEFAULT)
            except Exception:
                self.last_serial_baud = self.LAST_SERIAL_BAUD_DEFAULT

            self.camera_selected_or_tool = app_general.getboolean("camera_selected_or_tool",
                                                                  self.CAMERA_SELECTED_OR_TOOL_DEFAULT)
            self.flip_horizontal_selected = app_general.getboolean("flip_horizontal_selected",
                                                                   self.FLIP_HORIZONTAL_SELECTED_DEFAULT)
            self.flip_vertical_selected = app_general.getboolean("flip_vertical_selected",
                                                                 self.FLIP_VERTICAL_SELECTED_DEFAULT)

        # Layers related application settings #
        if "LAYERS" in self.app_settings:
            app_layers_settings = self.app_settings["LAYERS"]
            self.layer_last_dir = app_layers_settings.get("layer_last_dir", self.layer_last_dir_default)
            self.layer_color["top"] = app_layers_settings.get("top_layer_color", self.TOP_LAYER_COLOR_DEFAULT)
            self.layer_color["bottom"] = app_layers_settings.get("bottom_layer_color", self.BOTTOM_LAYER_COLOR_DEFAULT)
            self.layer_color["profile"] = app_layers_settings.get("profile_layer_color",
                                                                  self.PROFILE_LAYER_COLOR_DEFAULT)
            self.layer_color["drill"] = app_layers_settings.get("drill_layer_color", self.DRILL_LAYER_COLOR_DEFAULT)
            self.layer_color["nc_top"] = app_layers_settings.get("nc_top_layer_color", self.NC_TOP_LAYER_COLOR_DEFAULT)
            self.layer_color["nc_bottom"] = app_layers_settings.get("nc_bottom_layer_color",
                                                                    self.NC_BOTTOM_LAYER_COLOR_DEFAULT)

        if "GCODES" in self.app_settings:
            app_gcode_settings = self.app_settings["GCODES"]
            self.gcode_last_dir = app_gcode_settings.get("gcode_last_dir", self.gcode_last_dir_default)

    def write_all_app_settings(self):
        """ Write all application settings to ini files """
        self.app_settings["DEFAULT"] = {"win_position_x": self.WIN_POS_X_DEFAULT,
                                        "win_position_y": self.WIN_POS_Y_DEFAULT,
                                        "win_width": self.WIN_SIZE_W_DEFAULT,
                                        "win_height": self.WIN_SIZE_H_DEFAULT,
                                        "win_maximized": self.WIN_MAXIMIZED_DEFAULT,
                                        "main_tab_index": self.MAIN_TAB_INDEX_DEFAULT,
                                        "ctrl_tab_index": self.CTRL_TAB_INDEX_DEFAULT,
                                        "settings_tab_index": self.SETTINGS_TAB_INDEX_DEFAULT,
                                        "align_tab_visibility": self.SHOW_ALIGN_TAB_DEFAULT,
                                        "settings_tab_visibility": self.SHOW_SETTINGS_TAB_DEFAULT,
                                        "console_visibility": self.console_visibility,
                                        "layer_last_dir": self.layer_last_dir_default,
                                        "top_layer_color": self.TOP_LAYER_COLOR_DEFAULT,
                                        "bottom_layer_color": self.BOTTOM_LAYER_COLOR_DEFAULT,
                                        "profile_layer_color": self.PROFILE_LAYER_COLOR_DEFAULT,
                                        "drill_layer_color": self.DRILL_LAYER_COLOR_DEFAULT,
                                        "nc_top_layer_color": self.NC_TOP_LAYER_COLOR_DEFAULT,
                                        "nc_bottom_layer_color": self.NC_BOTTOM_LAYER_COLOR_DEFAULT,
                                        "gcode_last_dir": self.gcode_last_dir_default,
                                        "logs_file": self.logs_file_default,
                                        "logs_max_bytes": self.LOGS_MAX_BYTES,
                                        "logs_backup_count": self.LOGS_BACKUP_COUNT,
                                        "last_serial_port": self.LAST_SERIAL_PORT_DEFAULT,
                                        "last_serial_baud": self.LAST_SERIAL_BAUD_DEFAULT,
                                        "camera_selected_or_tool": self.CAMERA_SELECTED_OR_TOOL_DEFAULT,
                                        "flip_horizontal_selected": self.FLIP_HORIZONTAL_SELECTED_DEFAULT,
                                        "flip_vertical_selected": self.FLIP_VERTICAL_SELECTED_DEFAULT}

        # GENERAL application settings #
        self.app_settings["GENERAL"] = {}
        app_general = self.app_settings["GENERAL"]
        window_pos = self.main_win.pos()
        window_geo = self.main_win.normalGeometry()
        app_general["win_position_x"] = str(window_pos.x())
        app_general["win_position_y"] = str(window_pos.y())
        app_general["win_width"] = str(window_geo.width())
        app_general["win_height"] = str(window_geo.height())
        app_general["win_maximized"] = str(self.main_win.isMaximized())
        app_general["main_tab_index"] = str(self.main_win.ui.main_tab_widget.currentIndex())
        app_general["ctrl_tab_index"] = str(self.main_win.ui.ctrl_tab_widget.currentIndex())
        app_general["settings_tab_index"] = str(self.main_win.ui.settings_sub_tab.currentIndex())
        app_general["align_tab_visibility"] = str(self.main_win.ui.actionHide_Show_Align_Tab.isChecked())
        app_general["settings_tab_visibility"] = str(self.main_win.ui.actionSettings_Preferences.isChecked())
        app_general["console_visibility"] = str(self.main_win.ui.actionHide_Show_Console.isChecked())
        app_general["logs_file"] = str(self.logs_file_default)
        app_general["logs_max_bytes"] = str(self.LOGS_MAX_BYTES)
        app_general["logs_backup_count"] = str(self.LOGS_BACKUP_COUNT)
        app_general["last_serial_port"] = str(self.main_win.ui.serial_ports_cb.currentText())
        app_general["last_serial_baud"] = str(self.main_win.ui.serial_baud_cb.currentText())
        app_general["camera_selected_or_tool"] = str(self.camera_selected_or_tool)
        app_general["flip_horizontal_selected"] = str(self.main_win.ui.flip_horizontally_tb.isChecked())
        app_general["flip_vertical_selected"] = str(self.main_win.ui.flip_vertically_tb.isChecked())

        # Layers related application settings #
        self.app_settings["LAYERS"] = {}
        app_layers = self.app_settings["LAYERS"]
        app_layers["layer_last_dir"] = self.layer_last_dir
        app_layers["top_layer_color"] = self.layer_color["top"]
        app_layers["bottom_layer_color"] = self.layer_color["bottom"]
        app_layers["profile_layer_color"] = self.layer_color["profile"]
        app_layers["drill_layer_color"] = self.layer_color["drill"]
        app_layers["nc_top_layer_color"] = self.layer_color["nc_top"]
        app_layers["nc_bottom_layer_color"] = self.layer_color["nc_bottom"]

        # Layers related application settings #
        self.app_settings["GCODES"] = {}
        app_gcodes = self.app_settings["GCODES"]
        app_gcodes["gcode_last_dir"] = self.gcode_last_dir

        # Write application ini file #
        with open(self.app_config_path, 'w') as configfile:
            self.app_settings.write(configfile)

    def restore_app_settings(self):
        """ Restore all application settings to default and create ini file if it doesn't exists """
        self.app_settings["DEFAULT"] = {"win_position_x": self.WIN_POS_X_DEFAULT,
                                        "win_position_y": self.WIN_POS_Y_DEFAULT,
                                        "win_width": self.WIN_SIZE_W_DEFAULT,
                                        "win_height": self.WIN_SIZE_H_DEFAULT,
                                        "win_maximized": self.WIN_MAXIMIZED_DEFAULT,
                                        "main_tab_index": self.MAIN_TAB_INDEX_DEFAULT,
                                        "ctrl_tab_index": self.CTRL_TAB_INDEX_DEFAULT,
                                        "settings_tab_index": self.SETTINGS_TAB_INDEX_DEFAULT,
                                        "align_tab_visibility": self.SHOW_ALIGN_TAB_DEFAULT,
                                        "settings_tab_visibility": self.SHOW_SETTINGS_TAB_DEFAULT,
                                        "console_visibility": self.console_visibility,
                                        "layer_last_dir": self.layer_last_dir_default,
                                        "top_layer_color": self.TOP_LAYER_COLOR_DEFAULT,
                                        "bottom_layer_color": self.BOTTOM_LAYER_COLOR_DEFAULT,
                                        "profile_layer_color": self.PROFILE_LAYER_COLOR_DEFAULT,
                                        "drill_layer_color": self.DRILL_LAYER_COLOR_DEFAULT,
                                        "nc_top_layer_color": self.NC_TOP_LAYER_COLOR_DEFAULT,
                                        "nc_bottom_layer_color": self.NC_BOTTOM_LAYER_COLOR_DEFAULT,
                                        "gcode_last_dir": self.gcode_last_dir_default,
                                        "logs_file": self.logs_file_default,
                                        "logs_max_bytes": self.LOGS_MAX_BYTES,
                                        "logs_backup_count": self.LOGS_BACKUP_COUNT,
                                        "last_serial_port": self.LAST_SERIAL_PORT_DEFAULT,
                                        "last_serial_baud": self.LAST_SERIAL_BAUD_DEFAULT,
                                        "flip_horizontal_selected": self.FLIP_HORIZONTAL_SELECTED_DEFAULT,
                                        "flip_vertical_selected": self.FLIP_VERTICAL_SELECTED_DEFAULT}

        # GENERAL application settings #
        self.app_settings["GENERAL"] = {}
        app_general = self.app_settings["GENERAL"]
        app_general["win_position_x"] = str(self.WIN_POS_X_DEFAULT)
        app_general["win_position_y"] = str(self.WIN_POS_Y_DEFAULT)
        app_general["win_width"] = str(self.WIN_SIZE_W_DEFAULT)
        app_general["win_height"] = str(self.WIN_SIZE_H_DEFAULT)
        app_general["win_maximized"] = str(self.WIN_MAXIMIZED_DEFAULT)
        app_general["main_tab_index"] = str(self.MAIN_TAB_INDEX_DEFAULT)
        app_general["ctrl_tab_index"] = str(self.CTRL_TAB_INDEX_DEFAULT)
        app_general["settings_tab_index"] = str(self.SETTINGS_TAB_INDEX_DEFAULT)
        app_general["align_tab_visibility"] = str(self.main_win.ui.actionHide_Show_Align_Tab.isChecked())
        app_general["settings_tab_visibility"] = str(self.main_win.ui.actionSettings_Preferences.isChecked())
        app_general["console_visibility"] = str(self.SHOW_CONSOLE_DEFAULT)
        app_general["logs_file"] = str(self.logs_file_default)
        app_general["logs_max_bytes"] = str(self.LOGS_MAX_BYTES)
        app_general["logs_backup_count"] = str(self.LOGS_BACKUP_COUNT)
        app_general["last_serial_port"] = str(self.LAST_SERIAL_PORT_DEFAULT)
        app_general["last_serial_baud"] = str(self.LAST_SERIAL_BAUD_DEFAULT)
        app_general["camera_selected_or_tool"] = str(self.CAMERA_SELECTED_OR_TOOL_DEFAULT)
        app_general["flip_horizontal_selected"] = str(self.main_win.ui.flip_horizontally_tb.isChecked())
        app_general["flip_vertical_selected"] = str(self.main_win.ui.flip_vertically_tb.isChecked())

        # Layers related application settings #
        self.app_settings["LAYERS"] = {}
        app_layers = self.app_settings["LAYERS"]
        app_layers["layer_last_dir"] = str(self.layer_last_dir_default)

        # Layers related application settings #
        self.app_settings["GCODES"] = {}
        app_layers = self.app_settings["GCODES"]
        app_layers["gcode_last_dir"] = str(self.gcode_last_dir_default)

        # Write application ini file #
        with open(self.app_config_path, 'w') as configfile:
            self.app_settings.write(configfile)
