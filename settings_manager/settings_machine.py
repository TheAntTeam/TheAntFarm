import configparser
import os


class MachineSettingsHandler:
    # MACHINE CONFIGURATION DEFAULT VALUES
    PROBE_Z_MAX_DEFAULT = 1.0
    PROBE_Z_MIN_DEFAULT = -11.0

    TOOL_PROBE_OFFSET_MPOS_X_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_WPOS_X_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT = 0.0

    TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT = 0.0
    TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT = 0.0
    TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT = 0.0

    TOOL_PROBE_Z_LIMIT = -11.0

    TOOL_CHANGE_REL_FLAG = False

    def __init__(self, config_folder, main_win):
        self.machine_config_path = os.path.normpath(os.path.join(config_folder, 'machine_config.ini'))
        self.machine_settings = configparser.ConfigParser()
        self.main_win = main_win

        self.probe_z_min = self.PROBE_Z_MIN_DEFAULT
        self.probe_z_max = self.PROBE_Z_MAX_DEFAULT

        self.tool_probe_offset_x_mpos = self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT
        self.tool_probe_offset_y_mpos = self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT
        self.tool_probe_offset_z_mpos = self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT
        self.tool_probe_offset_x_wpos = self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT
        self.tool_probe_offset_y_wpos = self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT
        self.tool_probe_offset_z_wpos = self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT

        self.tool_change_offset_x_mpos = self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT
        self.tool_change_offset_y_mpos = self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT
        self.tool_change_offset_z_mpos = self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT

        self.tool_probe_rel_flag = self.TOOL_CHANGE_REL_FLAG

        self.tool_probe_z_limit = self.TOOL_PROBE_Z_LIMIT

    def read_all_machine_settings(self):
        """ Read all machine settings from ini files """
        # If app settings file does NOT exist create it with default values
        if not os.path.isfile(self.machine_config_path):
            self.restore_machine_settings()

        # Read application ini file #
        self.machine_settings.read(self.machine_config_path)

        # GENERAL application settings #
        if "GENERAL" in self.machine_settings:
            machine_general = self.machine_settings["GENERAL"]
            self.probe_z_min = machine_general.getfloat("probe_z_min", self.PROBE_Z_MIN_DEFAULT)
            self.probe_z_max = machine_general.getfloat("probe_z_max", self.PROBE_Z_MAX_DEFAULT)

            self.tool_probe_rel_flag = machine_general.getboolean("tool_probe_relative_flag", self.TOOL_CHANGE_REL_FLAG)
            self.tool_probe_offset_x_mpos = machine_general.getfloat("tool_probe_x_mpos",
                                                                     self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT)
            self.tool_probe_offset_y_mpos = machine_general.getfloat("tool_probe_y_mpos",
                                                                     self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT)
            self.tool_probe_offset_z_mpos = machine_general.getfloat("tool_probe_z_mpos",
                                                                     self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT)

            self.tool_probe_offset_x_wpos = machine_general.getfloat("tool_probe_x_wpos",
                                                                     self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT)
            self.tool_probe_offset_y_wpos = machine_general.getfloat("tool_probe_y_wpos",
                                                                     self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT)
            self.tool_probe_offset_z_wpos = machine_general.getfloat("tool_probe_z_wpos",
                                                                     self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT)

            self.tool_change_offset_x_mpos = machine_general.getfloat("tool_change_x_mpos",
                                                                      self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT)
            self.tool_change_offset_y_mpos = machine_general.getfloat("tool_change_y_mpos",
                                                                      self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT)
            self.tool_change_offset_z_mpos = machine_general.getfloat("tool_change_z_mpos",
                                                                      self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT)

            self.tool_probe_z_limit = machine_general.getfloat("tool_probe_z_limit", self.TOOL_PROBE_Z_LIMIT)

    def write_all_machine_settings(self):
        """ Write all machine settings to ini files """
        self.machine_settings["DEFAULT"] = {"probe_z_min": self.PROBE_Z_MIN_DEFAULT,
                                            "probe_z_max": self.PROBE_Z_MAX_DEFAULT,
                                            "tool_probe_relative_flag": self.TOOL_CHANGE_REL_FLAG,
                                            "tool_probe_x_mpos": self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_probe_y_mpos": self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_probe_z_mpos": self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_x_wpos": self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT,
                                            "tool_probe_y_wpos": self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT,
                                            "tool_probe_z_wpos": self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT,
                                            "tool_change_x_mpos": self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_change_y_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_change_z_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_z_limit": self.TOOL_PROBE_Z_LIMIT}

        # GENERAL machine settings #
        self.machine_settings["GENERAL"] = {}
        machine_general = self.machine_settings["GENERAL"]

        machine_general["probe_z_min"] = str(self.probe_z_min)
        machine_general["probe_z_max"] = str(self.probe_z_max)
        machine_general["tool_probe_relative_flag"] = str(self.tool_probe_rel_flag)  # todo: substitute with check value
        machine_general["tool_probe_x_mpos"] = str(self.tool_probe_offset_x_mpos)
        machine_general["tool_probe_y_mpos"] = str(self.tool_probe_offset_y_mpos)
        machine_general["tool_probe_z_mpos"] = str(self.tool_probe_offset_z_mpos)
        machine_general["tool_probe_x_wpos"] = str(self.tool_probe_offset_x_wpos)
        machine_general["tool_probe_y_wpos"] = str(self.tool_probe_offset_y_mpos)
        machine_general["tool_probe_z_wpos"] = str(self.tool_probe_offset_z_mpos)
        machine_general["tool_change_x_mpos"] = str(self.tool_change_offset_x_mpos)
        machine_general["tool_change_y_mpos"] = str(self.tool_change_offset_y_mpos)
        machine_general["tool_change_z_mpos"] = str(self.tool_change_offset_z_mpos)
        machine_general["tool_probe_z_limit"] = str(self.tool_probe_z_limit)

        # Write machine ini file #
        with open(self.machine_config_path, 'w') as configfile:
            self.machine_settings.write(configfile)

    def restore_machine_settings(self):
        """ Restore all machine settings to default and create ini file if it doesn't exists """
        self.machine_settings["DEFAULT"] = {"probe_z_min": self.PROBE_Z_MIN_DEFAULT,
                                            "probe_z_max": self.PROBE_Z_MAX_DEFAULT,
                                            "tool_probe_relative_flag": self.TOOL_CHANGE_REL_FLAG,
                                            "tool_probe_x_mpos": self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_probe_y_mpos": self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_probe_z_mpos": self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_x_wpos": self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT,
                                            "tool_probe_y_wpos": self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT,
                                            "tool_probe_z_wpos": self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT,
                                            "tool_change_x_mpos": self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_change_y_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_change_z_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_z_limit": self.TOOL_PROBE_Z_LIMIT}

        # GENERAL machine settings #
        self.machine_settings["GENERAL"] = {}
        machine_general = self.machine_settings["GENERAL"]
        machine_general["probe_z_min"] = str(self.PROBE_Z_MIN_DEFAULT)
        machine_general["probe_z_max"] = str(self.PROBE_Z_MAX_DEFAULT)
        machine_general["tool_probe_relative_flag"] = str(self.tool_probe_rel_flag)  # todo: substitute with check value
        machine_general["tool_probe_x_mpos"] = str(self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT)
        machine_general["tool_probe_y_mpos"] = str(self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT)
        machine_general["tool_probe_z_mpos"] = str(self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT)
        machine_general["tool_probe_x_wpos"] = str(self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT)
        machine_general["tool_probe_y_wpos"] = str(self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT)
        machine_general["tool_probe_z_wpos"] = str(self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT)
        machine_general["tool_change_x_mpos"] = str(self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT)
        machine_general["tool_change_y_mpos"] = str(self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT)
        machine_general["tool_change_z_mpos"] = str(self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT)
        machine_general["tool_probe_z_limit"] = str(self.TOOL_PROBE_Z_LIMIT)

        # Write machine ini file #
        with open(self.machine_config_path, 'w') as configfile:
            self.machine_settings.write(configfile)
