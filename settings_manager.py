from PySide2.QtCore import QPoint, QSize
import configparser
import os


class SettingsHandler:
    # Configuration file folder
    CONFIG_FOLDER = os.path.join(os.path.dirname(__file__), 'configurations')

    def __init__(self, main_win):
        if not os.path.isdir(self.CONFIG_FOLDER):
            os.makedirs(self.CONFIG_FOLDER)

        self.main_win = main_win

        self.app_settings = AppSettingsHandler(self.CONFIG_FOLDER, main_win)
        self.jobs_settings = JobSettingsHandler(self.CONFIG_FOLDER)
        self.gcf_settings = GCodeFilesSettingsHandler(self.CONFIG_FOLDER)

    def read_all_settings(self):
        """ Read all settings from ini files """
        self.app_settings.read_all_app_settings()
        self.jobs_settings.read_all_jobs_settings()
        self.gcf_settings.read_all_gcf_settings()

    def write_all_settings(self, all_settings_od):
        """ Write all settings to ini files """
        #if "app_settings" in all_settings_od:
        #    self.app_settings.write_all_app_settings(all_settings_od["app_settings"])

        self.app_settings.write_all_app_settings()
        if "jobs_settings" in all_settings_od:
            self.jobs_settings.write_all_jobs_settings(all_settings_od["jobs_settings"])
        self.gcf_settings.write_all_gcf_settings()


class AppSettingsHandler:
    # APP CONFIGURATION DEFAULT VALUES
    WIN_POS_X_DEFAULT = 200
    WIN_POS_Y_DEFAULT = 200
    WIN_SIZE_W_DEFAULT = 1160
    WIN_SIZE_H_DEFAULT = 720
    LAYER_LAST_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), '.')
    GCODE_LAST_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), '.')

    def __init__(self, config_folder, main_win):
        self.app_config_path = config_folder + os.path.sep + 'app_config.ini'
        self.app_settings = configparser.ConfigParser()

        self.main_win = main_win
        self.pos = QPoint(self.WIN_POS_X_DEFAULT, self.WIN_POS_Y_DEFAULT)
        self.size = QSize(self.WIN_SIZE_W_DEFAULT, self.WIN_SIZE_H_DEFAULT)
        self.layer_last_dir = self.LAYER_LAST_DIR_DEFAULT
        self.gcode_last_dir = self.GCODE_LAST_DIR_DEFAULT

    def read_all_app_settings(self):
        """ Read all application settings from ini files """
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
        self.main_win.resize(self.size)

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

        # Layers related application settings #
        self.app_settings["GCODES"] = {}
        app_layers = self.app_settings["GCODES"]
        app_layers["gcode_last_dir"] = self.gcode_last_dir

        # Write application ini file #
        with open(self.app_config_path, 'w') as configfile:
            self.app_settings.write(configfile)


class JobSettingsHandler:
    # JOBS CONFIGURATION DEFAULT VALUES
    TOOL_DIAMETER_DEFAULT = 1.0
    PASSAGES_DEFAULT = 1
    OVERLAP_DEFAULT = 0.40
    CUT_Z_DEFAULT = -0.07
    TRAVEL_Z_DEFAULT = 1.0
    SPINDLE_SPEED_DEFAULT = 1000.0
    XY_FEEDRATE_DEFAULT = 250.0
    Z_FEEDRATE_DEFAULT = 40.0
    MARGIN_DEFAULT = 0.01
    DEPTH_PER_PASS_DEFAULT = 0.06
    MULTI_PATH_FLAG_DEFAULT = False
    TAPS_LENGTH_DEFAULT = 1.0
    TAPS_TYPE_INDEX_DEFAULT = 3

    def __init__(self, config_folder):
        self.jobs_config_path = config_folder + os.path.sep + 'jobs_sets_config.ini'
        self.jobs_settings = configparser.ConfigParser()
        self.jobs_settings_od = {}

    def read_all_jobs_settings(self):
        """ Read all jobs'settings from ini files """
        # Read jobs'settings ini file #
        self.jobs_settings.read(self.jobs_config_path)

        # Top job related settings #
        if "TOP" in self.jobs_settings:
            top_settings = self.jobs_settings["TOP"]
            top_set_od = ({})
            top_set_od["tool_diameter"] = top_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            top_set_od["passages"] = top_settings.getint("passages", self.PASSAGES_DEFAULT)
            top_set_od["overlap"] = top_settings.getfloat("overlap", self.OVERLAP_DEFAULT)
            top_set_od["cut"] = top_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            top_set_od["travel"] = top_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            top_set_od["spindle"] = top_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            top_set_od["xy_feedrate"] = top_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            top_set_od["z_feedrate"] = top_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            self.jobs_settings_od["top"] = top_set_od

        # Bottom job related settings #
        if "BOTTOM" in self.jobs_settings:
            bottom_settings = self.jobs_settings["BOTTOM"]
            bottom_set_od = ({})
            bottom_set_od["tool_diameter"] = bottom_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            bottom_set_od["passages"] = bottom_settings.getint("passages", self.PASSAGES_DEFAULT)
            bottom_set_od["overlap"] = bottom_settings.getfloat("overlap", self.OVERLAP_DEFAULT)
            bottom_set_od["cut"] = bottom_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            bottom_set_od["travel"] = bottom_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            bottom_set_od["spindle"] = bottom_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            bottom_set_od["xy_feedrate"] = bottom_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            bottom_set_od["z_feedrate"] = bottom_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            self.jobs_settings_od["bottom"] = bottom_set_od

        # Profile job related settings #
        if "PROFILE" in self.jobs_settings:
            profile_settings = self.jobs_settings["PROFILE"]
            profile_set_od = ({})
            profile_set_od["tool_diameter"] = profile_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            profile_set_od["margin"] = profile_settings.getfloat("margin", self.MARGIN_DEFAULT)
            profile_set_od["multi_depth"] = profile_settings.getboolean("multi_depth", self.MULTI_PATH_FLAG_DEFAULT)
            profile_set_od["depth_per_pass"] = profile_settings.getfloat("depth_per_pass", self.DEPTH_PER_PASS_DEFAULT)
            profile_set_od["cut"] = profile_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            profile_set_od["passages"] = profile_settings.getint("passages", self.PASSAGES_DEFAULT)
            profile_set_od["travel"] = profile_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            profile_set_od["spindle"] = profile_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            profile_set_od["xy_feedrate"] = profile_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            profile_set_od["z_feedrate"] = profile_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            profile_set_od["taps_type"] = profile_settings.getint("taps_type", self.TAPS_TYPE_INDEX_DEFAULT)
            profile_set_od["taps_length"] = profile_settings.getfloat("taps_length", self.TAPS_LENGTH_DEFAULT)
            self.jobs_settings_od["profile"] = profile_set_od

        if "DRILL" in self.jobs_settings:
            drill_settings = self.jobs_settings["DRILL"]
            drill_set_od = ({})
            drill_set_od["milling_tool"] = drill_settings.getboolean("milling_tool_flag", False)
            drill_set_od["tool_diameter"] = drill_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            drill_set_od["cut"] = drill_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            drill_set_od["travel"] = drill_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            drill_set_od["spindle"] = drill_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            drill_set_od["xy_feedrate"] = drill_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            drill_set_od["z_feedrate"] = drill_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            drill_set_od["optimize"] = drill_settings.getboolean("optimize", False)

            drill_bits_names_list = []
            drill_bits_diameter_list = []
            # Section dedicated to drill bits #
            if "DRILL_BITS" in self.jobs_settings:
                drill_bits_settings = self.jobs_settings["DRILL_BITS"]
                for elem in drill_bits_settings:
                    if "bit" in elem:  # This is needed to avoid to read default settings too.
                        drill_bits_names_list.append(elem)
                        drill_bits_diameter_list.append(drill_bits_settings.getfloat(elem, 0.1))  # todo: set fallback value

            drill_set_od["bits_names"] = drill_bits_names_list
            drill_set_od["bits_diameter"] = drill_bits_diameter_list
            self.jobs_settings_od["drill"] = drill_set_od

        if "NC_TOP" in self.jobs_settings:
            nc_top_settings = self.jobs_settings["NC_TOP"]
            nc_top_set_od = ({})
            nc_top_set_od["tool_diameter"] = nc_top_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            nc_top_set_od["overlap"] = nc_top_settings.getfloat("overlap", self.OVERLAP_DEFAULT)
            nc_top_set_od["cut"] = nc_top_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            nc_top_set_od["travel"] = nc_top_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            nc_top_set_od["spindle"] = nc_top_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            nc_top_set_od["xy_feedrate"] = nc_top_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            nc_top_set_od["z_feedrate"] = nc_top_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            self.jobs_settings_od["no_copper_top"] = nc_top_set_od

        if "NC_BOTTOM" in self.jobs_settings:
            nc_bottom_settings = self.jobs_settings["NC_BOTTOM"]
            nc_bottom_set_od = ({})
            nc_bottom_set_od["tool_diameter"] = nc_bottom_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            nc_bottom_set_od["overlap"] = nc_bottom_settings.getfloat("overlap", self.OVERLAP_DEFAULT)
            nc_bottom_set_od["cut"] = nc_bottom_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            nc_bottom_set_od["travel"] = nc_bottom_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            nc_bottom_set_od["spindle"] = nc_bottom_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            nc_bottom_set_od["xy_feedrate"] = nc_bottom_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            nc_bottom_set_od["z_feedrate"] = nc_bottom_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            self.jobs_settings_od["no_copper_bottom"] = nc_bottom_set_od

    def write_all_jobs_settings(self, job_settings_od):
        """ Write all jobs settings to ini files """
        self.jobs_settings['DEFAULT'] = {"tool_diameter": self.TOOL_DIAMETER_DEFAULT,
                                         "passages": self.PASSAGES_DEFAULT,
                                         "overlap": self.OVERLAP_DEFAULT,
                                         "cut": self.CUT_Z_DEFAULT,
                                         "travel": self.TRAVEL_Z_DEFAULT,
                                         "spindle": self.SPINDLE_SPEED_DEFAULT,
                                         "xy_feedrate": self.XY_FEEDRATE_DEFAULT,
                                         "z_feedrate": self.Z_FEEDRATE_DEFAULT,
                                         "margin": self.MARGIN_DEFAULT,
                                         "depth_per_pass": self.DEPTH_PER_PASS_DEFAULT,
                                         "multi_depth": self.MULTI_PATH_FLAG_DEFAULT,
                                         "taps_type": self.TAPS_TYPE_INDEX_DEFAULT,
                                         "taps_length": self.TAPS_LENGTH_DEFAULT}

        # Top job related settings #
        self.jobs_settings["TOP"] = {}
        top_settings = self.jobs_settings["TOP"]
        top_set_od = job_settings_od["top"]
        top_settings["tool_diameter"] = str(top_set_od["tool_diameter"])
        top_settings["passages"] = str(top_set_od["passages"])
        top_settings["overlap"] = str(top_set_od["overlap"])
        top_settings["cut"] = str(top_set_od["cut"])
        top_settings["travel"] = str(top_set_od["travel"])
        top_settings["spindle"] = str(top_set_od["spindle"])
        top_settings["xy_feedrate"] = str(top_set_od["xy_feedrate"])
        top_settings["z_feedrate"] = str(top_set_od["z_feedrate"])

        # Bottom job related settings #
        self.jobs_settings["BOTTOM"] = {}
        bottom_settings = self.jobs_settings["BOTTOM"]
        bottom_set_od = job_settings_od["bottom"]
        bottom_settings["tool_diameter"] = str(bottom_set_od["tool_diameter"])
        bottom_settings["passages"] = str(bottom_set_od["passages"])
        bottom_settings["overlap"] = str(bottom_set_od["overlap"])
        bottom_settings["cut"] = str(bottom_set_od["cut"])
        bottom_settings["travel"] = str(bottom_set_od["travel"])
        bottom_settings["spindle"] = str(bottom_set_od["spindle"])
        bottom_settings["xy_feedrate"] = str(bottom_set_od["xy_feedrate"])
        bottom_settings["z_feedrate"] = str(bottom_set_od["z_feedrate"])

        # Profile job related settings #
        self.jobs_settings["PROFILE"] = {}
        profile_settings = self.jobs_settings["PROFILE"]
        profile_set_od = job_settings_od["profile"]
        profile_settings["tool_diameter"] = str(profile_set_od["tool_diameter"])
        profile_settings["margin"] = str(profile_set_od["margin"])
        profile_settings["multi_depth"] = str(profile_set_od["multi_depth"])
        profile_settings["depth_per_pass"] = str(profile_set_od["depth_per_pass"])
        profile_settings["cut"] = str(profile_set_od["cut"])
        profile_settings["passages"] = str(profile_set_od["passages"])
        profile_settings["travel"] = str(profile_set_od["travel"])
        profile_settings["spindle"] = str(profile_set_od["spindle"])
        profile_settings["xy_feedrate"] = str(profile_set_od["xy_feedrate"])
        profile_settings["z_feedrate"] = str(profile_set_od["z_feedrate"])
        profile_settings["taps_type"] = str(profile_set_od["taps_type"])
        profile_settings["taps_length"] = str(profile_set_od["taps_length"])

        # Drill job related settings #
        self.jobs_settings["DRILL"] = {}
        drill_settings = self.jobs_settings["DRILL"]
        drill_set_od = job_settings_od["drill"]
        drill_settings["milling_tool_flag"] = str(drill_set_od["milling_tool"])
        drill_settings["tool_diameter"] = str(drill_set_od["tool_diameter"])
        drill_settings["cut"] = str(drill_set_od["cut"])
        drill_settings["travel"] = str(drill_set_od["travel"])
        drill_settings["spindle"] = str(drill_set_od["spindle"])
        drill_settings["xy_feedrate"] = str(drill_set_od["xy_feedrate"])
        drill_settings["z_feedrate"] = str(drill_set_od["z_feedrate"])
        drill_settings["optimize"] = str(drill_set_od["optimize"])

        # Section dedicated to drill bits #
        self.jobs_settings["DRILL_BITS"] = {}
        drill_bits_settings = self.jobs_settings["DRILL_BITS"]

        for index, elem in enumerate(drill_set_od["bits_names"]):
            drill_bits_settings[elem] = str(drill_set_od["bits_diameter"][index])

        # No-Copper Top job related settings #
        self.jobs_settings["NC_TOP"] = {}
        nc_top_settings = self.jobs_settings["NC_TOP"]
        nc_top_set_od = job_settings_od["no_copper_top"]
        nc_top_settings["tool_diameter"] = str(nc_top_set_od["tool_diameter"])
        nc_top_settings["overlap"] = str(nc_top_set_od["overlap"])
        nc_top_settings["cut"] = str(nc_top_set_od["cut"])
        nc_top_settings["travel"] = str(nc_top_set_od["travel"])
        nc_top_settings["spindle"] = str(nc_top_set_od["spindle"])
        nc_top_settings["xy_feedrate"] = str(nc_top_set_od["xy_feedrate"])
        nc_top_settings["z_feedrate"] = str(nc_top_set_od["z_feedrate"])

        # No-Copper Bottom job related settings #
        self.jobs_settings["NC_BOTTOM"] = {}
        nc_bottom_settings = self.jobs_settings["NC_BOTTOM"]
        nc_bottom_set_od = job_settings_od["no_copper_bottom"]
        nc_bottom_settings["tool_diameter"] = str(nc_bottom_set_od["tool_diameter"])
        nc_bottom_settings["overlap"] = str(nc_bottom_set_od["overlap"])
        nc_bottom_settings["cut"] = str(nc_bottom_set_od["cut"])
        nc_bottom_settings["travel"] = str(nc_bottom_set_od["travel"])
        nc_bottom_settings["spindle"] = str(nc_bottom_set_od["spindle"])
        nc_bottom_settings["xy_feedrate"] = str(nc_bottom_set_od["xy_feedrate"])
        nc_bottom_settings["z_feedrate"] = str(nc_bottom_set_od["z_feedrate"])

        # Write application ini file #
        with open(self.jobs_config_path, 'w') as configfile:
            self.jobs_settings.write(configfile)


class GCodeFilesSettingsHandler:
    # G-Code Files CONFIGURATION DEFAULT VALUES

    def __init__(self, config_folder):
        self.gcf_config_path = os.path.join(config_folder, 'gcode_files_config.ini')
        self.gcf_settings = configparser.ConfigParser()

    def read_all_gcf_settings(self):
        """ Read all g-code files'settings from ini files """
        # Read g-code files'settings ini file #
        self.gcf_settings.read(self.gcf_config_path)

        # if "FILES" in self.gcf_settings:
        #     self.gcf_settings["FILES"]["gcode_folder"]

    def write_all_gcf_settings(self):
        """ Write all g-code files'settings to ini files """
        # self.gcf_settings['DEFAULT'] = {}

        gcf_settings_od = {}
        self.gcf_settings["FILES"] = {}
        files_settings = self.gcf_settings["FILES"]
        files_settings["gcode_folder"] = os.path.dirname(self.gcf_config_path)

        # Write application ini file #
        with open(self.gcf_config_path, 'w') as configfile:
            self.gcf_settings.write(configfile)
