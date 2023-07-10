import configparser
import os


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
    GAPS_LENGTH_DEFAULT = 1.0
    GAPS_TYPE_INDEX_DEFAULT = 3
    MILLING_TOOL_FLAG = False
    OPTIMIZE_FLAG_DEFAULT = True
    MIRROR_ALL_DEFAULT = False
    MIRROR_BOTTOM_DEFAULT = True
    MIRROR_AXIS_DEFAULT = "x"

    def __init__(self, config_folder):
        self.jobs_config_path = os.path.normpath(os.path.join(config_folder, 'jobs_sets_config.ini'))
        self.jobs_settings = configparser.ConfigParser()
        self.jobs_settings_od = {}

    def read_all_jobs_settings(self):
        """ Read all jobs' settings from ini files """
        # If app settings file does NOT exist create it with default values
        if not os.path.isfile(self.jobs_config_path):
            self.restore_job_settings()

        # Read jobs' settings ini file #
        self.jobs_settings.read(self.jobs_config_path)

        # Settings common to all jobs #
        if "COMMON" in self.jobs_settings:
            common_settings = self.jobs_settings["COMMON"]
            common_set_od = ({})
            common_set_od["mirroring_axis"] = common_settings.get("mirroring_axis", self.MIRROR_AXIS_DEFAULT)
            self.jobs_settings_od["common"] = common_set_od
        else:
            self.jobs_settings["COMMON"] = {}
            common_set_od = ({})
            common_set_od["mirroring_axis"] = self.MIRROR_AXIS_DEFAULT
            self.jobs_settings_od["common"] = common_set_od

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
            top_set_od["mirror"] = top_settings.getboolean("mirror", self.MIRROR_ALL_DEFAULT)
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
            bottom_set_od["mirror"] = bottom_settings.getboolean("mirror", self.MIRROR_BOTTOM_DEFAULT)
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
            profile_set_od["taps_type"] = profile_settings.getint("taps_type", self.GAPS_TYPE_INDEX_DEFAULT)
            profile_set_od["taps_length"] = profile_settings.getfloat("taps_length", self.GAPS_LENGTH_DEFAULT)
            profile_set_od["mirror"] = profile_settings.getboolean("mirror", self.MIRROR_ALL_DEFAULT)
            self.jobs_settings_od["profile"] = profile_set_od

        if "DRILL" in self.jobs_settings:
            drill_settings = self.jobs_settings["DRILL"]
            drill_set_od = ({})
            drill_set_od["milling_tool"] = drill_settings.getboolean("milling_tool_flag", self.MILLING_TOOL_FLAG)
            drill_set_od["tool_diameter"] = drill_settings.getfloat("tool_diameter", self.TOOL_DIAMETER_DEFAULT)
            drill_set_od["cut"] = drill_settings.getfloat("cut", self.CUT_Z_DEFAULT)
            drill_set_od["travel"] = drill_settings.getfloat("travel", self.TRAVEL_Z_DEFAULT)
            drill_set_od["spindle"] = drill_settings.getfloat("spindle", self.SPINDLE_SPEED_DEFAULT)
            drill_set_od["xy_feedrate"] = drill_settings.getfloat("xy_feedrate", self.XY_FEEDRATE_DEFAULT)
            drill_set_od["z_feedrate"] = drill_settings.getfloat("z_feedrate", self.Z_FEEDRATE_DEFAULT)
            drill_set_od["optimize"] = drill_settings.getboolean("optimize", self.OPTIMIZE_FLAG_DEFAULT)
            drill_set_od["mirror"] = drill_settings.getboolean("mirror", self.MIRROR_ALL_DEFAULT)

            drill_bits_names_list = []
            drill_bits_diameter_list = []
            # Section dedicated to drill bits #
            if "DRILL_BITS" in self.jobs_settings:
                drill_bits_settings = self.jobs_settings["DRILL_BITS"]
                for elem in drill_bits_settings:
                    if "bit" in elem:  # This is needed to avoid to read default settings too.
                        drill_bits_names_list.append(elem)
                        drill_bits_diameter_list.append(drill_bits_settings.getfloat(elem, 0.1))  # todo: set fallback

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
            self.jobs_settings_od["nc_top"] = nc_top_set_od

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
            self.jobs_settings_od["nc_bottom"] = nc_bottom_set_od

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
                                         "taps_type": self.GAPS_TYPE_INDEX_DEFAULT,
                                         "taps_length": self.GAPS_LENGTH_DEFAULT,
                                         "mirror": self.MIRROR_ALL_DEFAULT,
                                         "mirroring_axis": self.MIRROR_AXIS_DEFAULT}

        # Common jobs' settings.
        self.jobs_settings["COMMON"] = {}
        common_settings = self.jobs_settings["COMMON"]
        common_set_od = job_settings_od["common"]
        common_settings["mirroring_axis"] = str(common_set_od["mirroring_axis"])

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
        top_settings["mirror"] = str(top_set_od["mirror"])

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
        bottom_settings["mirror"] = str(bottom_set_od["mirror"])

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
        profile_settings["mirror"] = str(profile_set_od["mirror"])

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
        drill_settings["mirror"] = str(drill_set_od["mirror"])

        # Section dedicated to drill bits #
        self.jobs_settings["DRILL_BITS"] = {}
        drill_bits_settings = self.jobs_settings["DRILL_BITS"]

        for index, elem in enumerate(drill_set_od["bits_names"]):
            drill_bits_settings[elem] = str(drill_set_od["bits_diameter"][index])

        # No-Copper Top job related settings #
        self.jobs_settings["NC_TOP"] = {}
        nc_top_settings = self.jobs_settings["NC_TOP"]
        nc_top_set_od = job_settings_od["nc_top"]
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
        nc_bottom_set_od = job_settings_od["nc_bottom"]
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

    def restore_job_settings(self):
        """ Restore all jobs settings to default and create ini file if it doesn't exist. """
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
                                         "taps_type": self.GAPS_TYPE_INDEX_DEFAULT,
                                         "taps_length": self.GAPS_LENGTH_DEFAULT,
                                         "mirror": self.MIRROR_ALL_DEFAULT,
                                         "mirroring_axis": self.MIRROR_AXIS_DEFAULT}

        # Common jobs' settings.
        self.jobs_settings["COMMON"] = {}
        common_settings = self.jobs_settings["COMMON"]
        common_settings["mirroring_axis"] = str(self.MIRROR_AXIS_DEFAULT)

        # Top job related settings #
        self.jobs_settings["TOP"] = {}
        top_settings = self.jobs_settings["TOP"]

        top_settings["tool_diameter"] = str(self.TOOL_DIAMETER_DEFAULT)
        top_settings["passages"] = str(self.PASSAGES_DEFAULT)
        top_settings["overlap"] = str(self.OVERLAP_DEFAULT)
        top_settings["cut"] = str(self.CUT_Z_DEFAULT)
        top_settings["travel"] = str(self.TRAVEL_Z_DEFAULT)
        top_settings["spindle"] = str(self.SPINDLE_SPEED_DEFAULT)
        top_settings["xy_feedrate"] = str(self.XY_FEEDRATE_DEFAULT)
        top_settings["z_feedrate"] = str(self.Z_FEEDRATE_DEFAULT)
        top_settings["mirror"] = str(self.MIRROR_ALL_DEFAULT)

        # Bottom job related settings #
        self.jobs_settings["BOTTOM"] = {}
        bottom_settings = self.jobs_settings["BOTTOM"]

        bottom_settings["tool_diameter"] = str(self.TOOL_DIAMETER_DEFAULT)
        bottom_settings["passages"] = str(self.PASSAGES_DEFAULT)
        bottom_settings["overlap"] = str(self.OVERLAP_DEFAULT)
        bottom_settings["cut"] = str(self.CUT_Z_DEFAULT)
        bottom_settings["travel"] = str(self.TRAVEL_Z_DEFAULT)
        bottom_settings["spindle"] = str(self.SPINDLE_SPEED_DEFAULT)
        bottom_settings["xy_feedrate"] = str(self.XY_FEEDRATE_DEFAULT)
        bottom_settings["z_feedrate"] = str(self.Z_FEEDRATE_DEFAULT)
        bottom_settings["mirror"] = str(self.MIRROR_BOTTOM_DEFAULT)

        # Profile job related settings #
        self.jobs_settings["PROFILE"] = {}
        profile_settings = self.jobs_settings["PROFILE"]

        profile_settings["tool_diameter"] = str(self.TOOL_DIAMETER_DEFAULT)
        profile_settings["margin"] = str(self.MARGIN_DEFAULT)
        profile_settings["multi_depth"] = str(self.MULTI_PATH_FLAG_DEFAULT)
        profile_settings["depth_per_pass"] = str(self.DEPTH_PER_PASS_DEFAULT)
        profile_settings["cut"] = str(self.CUT_Z_DEFAULT)
        profile_settings["passages"] = str(self.PASSAGES_DEFAULT)
        profile_settings["travel"] = str(self.TRAVEL_Z_DEFAULT)
        profile_settings["spindle"] = str(self.SPINDLE_SPEED_DEFAULT)
        profile_settings["xy_feedrate"] = str(self.XY_FEEDRATE_DEFAULT)
        profile_settings["z_feedrate"] = str(self.Z_FEEDRATE_DEFAULT)
        profile_settings["taps_type"] = str(self.GAPS_TYPE_INDEX_DEFAULT)
        profile_settings["taps_length"] = str(self.GAPS_LENGTH_DEFAULT)
        profile_settings["mirror"] = str(self.MIRROR_ALL_DEFAULT)

        # Drill job related settings #
        self.jobs_settings["DRILL"] = {}
        drill_settings = self.jobs_settings["DRILL"]

        drill_settings["milling_tool_flag"] = str(self.MILLING_TOOL_FLAG)
        drill_settings["tool_diameter"] = str(self.TOOL_DIAMETER_DEFAULT)
        drill_settings["cut"] = str(self.CUT_Z_DEFAULT)
        drill_settings["travel"] = str(self.TRAVEL_Z_DEFAULT)
        drill_settings["spindle"] = str(self.SPINDLE_SPEED_DEFAULT)
        drill_settings["xy_feedrate"] = str(self.XY_FEEDRATE_DEFAULT)
        drill_settings["z_feedrate"] = str(self.Z_FEEDRATE_DEFAULT)
        drill_settings["optimize"] = str(self.OPTIMIZE_FLAG_DEFAULT)
        drill_settings["mirror"] = str(self.MIRROR_ALL_DEFAULT)

        # Section dedicated to drill bits #
        self.jobs_settings["DRILL_BITS"] = {}
        drill_bits_settings = self.jobs_settings["DRILL_BITS"]

        # No-Copper Top job related settings #
        self.jobs_settings["NC_TOP"] = {}
        nc_top_settings = self.jobs_settings["NC_TOP"]

        nc_top_settings["tool_diameter"] = str(self.TOOL_DIAMETER_DEFAULT)
        nc_top_settings["overlap"] = str(self.OVERLAP_DEFAULT)
        nc_top_settings["cut"] = str(self.CUT_Z_DEFAULT)
        nc_top_settings["travel"] = str(self.TRAVEL_Z_DEFAULT)
        nc_top_settings["spindle"] = str(self.SPINDLE_SPEED_DEFAULT)
        nc_top_settings["xy_feedrate"] = str(self.XY_FEEDRATE_DEFAULT)
        nc_top_settings["z_feedrate"] = str(self.Z_FEEDRATE_DEFAULT)

        # No-Copper Bottom job related settings #
        self.jobs_settings["NC_BOTTOM"] = {}
        nc_bottom_settings = self.jobs_settings["NC_BOTTOM"]

        nc_bottom_settings["tool_diameter"] = str(self.TOOL_DIAMETER_DEFAULT)
        nc_bottom_settings["overlap"] = str(self.OVERLAP_DEFAULT)
        nc_bottom_settings["cut"] = str(self.CUT_Z_DEFAULT)
        nc_bottom_settings["travel"] = str(self.TRAVEL_Z_DEFAULT)
        nc_bottom_settings["spindle"] = str(self.SPINDLE_SPEED_DEFAULT)
        nc_bottom_settings["xy_feedrate"] = str(self.XY_FEEDRATE_DEFAULT)
        nc_bottom_settings["z_feedrate"] = str(self.Z_FEEDRATE_DEFAULT)

        # Write application ini file #
        with open(self.jobs_config_path, 'w') as configfile:
            self.jobs_settings.write(configfile)
