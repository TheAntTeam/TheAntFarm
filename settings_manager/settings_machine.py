import configparser
import os


class MachineSettingsHandler:
    # MACHINE CONFIGURATION DEFAULT VALUES
    PROBE_Z_MAX_DEFAULT = 1.0
    PROBE_Z_MIN_DEFAULT = -11.0
    X_BBOX_STEP_DEFAULT = 1
    Y_BBOX_STEP_DEFAULT = 1
    XY_STEP_IDX_DEFAULT = 3
    XY_STEP_VALUE_DEFAULT = 1.0
    Z_STEP_IDX_DEFAULT = 3
    Z_STEP_VALUE_DEFAULT = 0.1
    FEEDRATE_XY_DEFAULT = 300.0
    FEEDRATE_Z_DEFAULT = 40.0
    FEEDRATE_PROBE_DEFAULT = 40.0

    TOOL_PROBE_OFFSET_MPOS_X_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_WPOS_X_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT = 0.0
    TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT = 0.0

    TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT = 0.0
    TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT = 0.0
    TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT = 0.0

    TOOL_PROBE_Z_LIMIT_DEFAULT = -11.0
    TOOL_PROBE_REL_FLAG_DEFAULT = False
    HOLD_ON_PROBE_FLAG_DEFAULT = False

    def __init__(self, config_folder, main_win):
        self.machine_config_path = os.path.normpath(os.path.join(config_folder, 'machine_config.ini'))
        self.machine_settings = configparser.ConfigParser()
        self.main_win = main_win

        self.probe_z_min = self.PROBE_Z_MIN_DEFAULT
        self.probe_z_max = self.PROBE_Z_MAX_DEFAULT
        self.x_bbox_step = self.X_BBOX_STEP_DEFAULT
        self.y_bbox_step = self.Y_BBOX_STEP_DEFAULT
        self.xy_step_idx = self.XY_STEP_IDX_DEFAULT
        self.xy_step_value = self.XY_STEP_VALUE_DEFAULT
        self.z_step_idx = self.Z_STEP_IDX_DEFAULT
        self.z_step_value = self.Z_STEP_VALUE_DEFAULT
        self.feedrate_xy = self.FEEDRATE_XY_DEFAULT
        self.feedrate_z = self.FEEDRATE_Z_DEFAULT
        self.feedrate_probe = self.FEEDRATE_PROBE_DEFAULT

        self.tool_probe_offset_x_mpos = self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT
        self.tool_probe_offset_y_mpos = self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT
        self.tool_probe_offset_z_mpos = self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT
        self.tool_probe_offset_x_wpos = self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT
        self.tool_probe_offset_y_wpos = self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT
        self.tool_probe_offset_z_wpos = self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT

        self.tool_change_offset_x_mpos = self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT
        self.tool_change_offset_y_mpos = self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT
        self.tool_change_offset_z_mpos = self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT

        self.tool_probe_z_limit = self.TOOL_PROBE_Z_LIMIT_DEFAULT
        self.tool_probe_rel_flag = self.TOOL_PROBE_REL_FLAG_DEFAULT
        self.hold_on_probe_flag = self.HOLD_ON_PROBE_FLAG_DEFAULT

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
            self.x_bbox_step = machine_general.getint("x_bbox_step", self.X_BBOX_STEP_DEFAULT)
            self.y_bbox_step = machine_general.getint("y_bbox_step", self.Y_BBOX_STEP_DEFAULT)
            self.xy_step_idx = machine_general.getint("xy_step_idx", self.XY_STEP_IDX_DEFAULT)
            self.xy_step_value = machine_general.getfloat("xy_step_value", self.XY_STEP_VALUE_DEFAULT)
            self.z_step_idx = machine_general.getint("z_step_idx", self.Z_STEP_IDX_DEFAULT)
            self.z_step_value = machine_general.getfloat("z_step_value", self.Z_STEP_VALUE_DEFAULT)
            self.feedrate_xy = machine_general.getfloat("feedrate_xy", self.FEEDRATE_XY_DEFAULT)
            self.feedrate_z = machine_general.getfloat("feedrate_z", self.FEEDRATE_Z_DEFAULT)
            self.feedrate_probe = machine_general.getfloat("feedrate_probe", self.FEEDRATE_PROBE_DEFAULT)

            self.tool_probe_rel_flag = machine_general.getboolean("tool_probe_relative_flag",
                                                                  self.TOOL_PROBE_REL_FLAG_DEFAULT)
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

            self.tool_probe_z_limit = machine_general.getfloat("tool_probe_z_limit", self.TOOL_PROBE_Z_LIMIT_DEFAULT)
            self.hold_on_probe_flag = machine_general.getboolean("hold_on_probe_flag", self.HOLD_ON_PROBE_FLAG_DEFAULT)

    def write_all_machine_settings(self):
        """ Write all machine settings to ini files """
        self.machine_settings["DEFAULT"] = {"probe_z_min": self.PROBE_Z_MIN_DEFAULT,
                                            "probe_z_max": self.PROBE_Z_MAX_DEFAULT,
                                            "x_bbox_step": self.X_BBOX_STEP_DEFAULT,
                                            "y_bbox_step": self.Y_BBOX_STEP_DEFAULT,
                                            "xy_step_idx": self.XY_STEP_IDX_DEFAULT,
                                            "xy_step_value": self.XY_STEP_VALUE_DEFAULT,
                                            "z_step_idx": self.Z_STEP_IDX_DEFAULT,
                                            "z_step_value": self.Z_STEP_VALUE_DEFAULT,
                                            "feedrate_xy": self.FEEDRATE_XY_DEFAULT,
                                            "feedrate_z": self.FEEDRATE_Z_DEFAULT,
                                            "feedrate_probe": self.FEEDRATE_PROBE_DEFAULT,
                                            "tool_probe_relative_flag": self.TOOL_PROBE_REL_FLAG_DEFAULT,
                                            "hold_on_probe_flag": self.HOLD_ON_PROBE_FLAG_DEFAULT,
                                            "tool_probe_x_mpos": self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_probe_y_mpos": self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_probe_z_mpos": self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_x_wpos": self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT,
                                            "tool_probe_y_wpos": self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT,
                                            "tool_probe_z_wpos": self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT,
                                            "tool_change_x_mpos": self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_change_y_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_change_z_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_z_limit": self.TOOL_PROBE_Z_LIMIT_DEFAULT}

        # GENERAL machine settings #
        self.machine_settings["GENERAL"] = {}
        machine_general = self.machine_settings["GENERAL"]

        machine_general["probe_z_min"] = str(self.probe_z_min)
        machine_general["probe_z_max"] = str(self.probe_z_max)
        machine_general["x_bbox_step"] = str(self.x_bbox_step)
        machine_general["y_bbox_step"] = str(self.y_bbox_step)
        machine_general["xy_step_idx"] = str(self.xy_step_idx)
        machine_general["xy_step_value"] = str(self.xy_step_value)
        machine_general["z_step_idx"] = str(self.z_step_idx)
        machine_general["z_step_value"] = str(self.z_step_value)
        machine_general["feedrate_xy"] = str(self.feedrate_xy)
        machine_general["feedrate_z"] = str(self.feedrate_z)
        machine_general["feedrate_probe"] = str(self.feedrate_probe)
        machine_general["tool_probe_relative_flag"] = str(self.tool_probe_rel_flag)
        machine_general["hold_on_probe_flag"] = str(self.hold_on_probe_flag)
        machine_general["tool_probe_x_mpos"] = str(self.tool_probe_offset_x_mpos)
        machine_general["tool_probe_y_mpos"] = str(self.tool_probe_offset_y_mpos)
        machine_general["tool_probe_z_mpos"] = str(self.tool_probe_offset_z_mpos)
        machine_general["tool_probe_x_wpos"] = str(self.tool_probe_offset_x_wpos)
        machine_general["tool_probe_y_wpos"] = str(self.tool_probe_offset_y_wpos)
        machine_general["tool_probe_z_wpos"] = str(self.tool_probe_offset_z_wpos)
        machine_general["tool_change_x_mpos"] = str(self.tool_change_offset_x_mpos)
        machine_general["tool_change_y_mpos"] = str(self.tool_change_offset_y_mpos)
        machine_general["tool_change_z_mpos"] = str(self.tool_change_offset_z_mpos)
        machine_general["tool_probe_z_limit"] = str(self.tool_probe_z_limit)

        # Write machine ini file #
        with open(self.machine_config_path, 'w') as configfile:
            self.machine_settings.write(configfile)

    def restore_machine_settings(self):
        """ Restore all machine settings to default and create ini file if it doesn't exist """
        self.machine_settings["DEFAULT"] = {"probe_z_min": self.PROBE_Z_MIN_DEFAULT,
                                            "probe_z_max": self.PROBE_Z_MAX_DEFAULT,
                                            "x_bbox_step": self.X_BBOX_STEP_DEFAULT,
                                            "y_bbox_step": self.Y_BBOX_STEP_DEFAULT,
                                            "xy_step_idx": self.XY_STEP_IDX_DEFAULT,
                                            "xy_step_value": self.XY_STEP_VALUE_DEFAULT,
                                            "z_step_idx": self.Z_STEP_IDX_DEFAULT,
                                            "z_step_value": self.Z_STEP_VALUE_DEFAULT,
                                            "feedrate_xy": self.FEEDRATE_XY_DEFAULT,
                                            "feedrate_z": self.FEEDRATE_Z_DEFAULT,
                                            "feedrate_probe": self.FEEDRATE_PROBE_DEFAULT,
                                            "tool_probe_relative_flag": self.TOOL_PROBE_REL_FLAG_DEFAULT,
                                            "hold_on_probe_flag": self.HOLD_ON_PROBE_FLAG_DEFAULT,
                                            "tool_probe_x_mpos": self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_probe_y_mpos": self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_probe_z_mpos": self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_x_wpos": self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT,
                                            "tool_probe_y_wpos": self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT,
                                            "tool_probe_z_wpos": self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT,
                                            "tool_change_x_mpos": self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT,
                                            "tool_change_y_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT,
                                            "tool_change_z_mpos": self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT,
                                            "tool_probe_z_limit": self.TOOL_PROBE_Z_LIMIT_DEFAULT}

        # GENERAL machine settings #
        self.machine_settings["GENERAL"] = {}
        machine_general = self.machine_settings["GENERAL"]
        machine_general["probe_z_min"] = str(self.PROBE_Z_MIN_DEFAULT)
        machine_general["probe_z_max"] = str(self.PROBE_Z_MAX_DEFAULT)
        machine_general["x_bbox_step"] = str(self.X_BBOX_STEP_DEFAULT)
        machine_general["y_bbox_step"] = str(self.Y_BBOX_STEP_DEFAULT)
        machine_general["xy_step_idx"] = str(self.XY_STEP_IDX_DEFAULT)
        machine_general["xy_step_value"] = str(self.XY_STEP_VALUE_DEFAULT)
        machine_general["z_step_idx"] = str(self.Z_STEP_IDX_DEFAULT)
        machine_general["z_step_value"] = str(self.Z_STEP_VALUE_DEFAULT)
        machine_general["feedrate_xy"] = str(self.FEEDRATE_XY_DEFAULT)
        machine_general["feedrate_z"] = str(self.FEEDRATE_Z_DEFAULT)
        machine_general["feedrate_probe"] = str(self.FEEDRATE_PROBE_DEFAULT)
        machine_general["tool_probe_relative_flag"] = str(self.TOOL_PROBE_REL_FLAG_DEFAULT)
        machine_general["hold_on_probe_flag"] = str(self.HOLD_ON_PROBE_FLAG_DEFAULT)
        machine_general["tool_probe_x_mpos"] = str(self.TOOL_PROBE_OFFSET_MPOS_X_DEFAULT)
        machine_general["tool_probe_y_mpos"] = str(self.TOOL_PROBE_OFFSET_MPOS_Y_DEFAULT)
        machine_general["tool_probe_z_mpos"] = str(self.TOOL_PROBE_OFFSET_MPOS_Z_DEFAULT)
        machine_general["tool_probe_x_wpos"] = str(self.TOOL_PROBE_OFFSET_WPOS_X_DEFAULT)
        machine_general["tool_probe_y_wpos"] = str(self.TOOL_PROBE_OFFSET_WPOS_Y_DEFAULT)
        machine_general["tool_probe_z_wpos"] = str(self.TOOL_PROBE_OFFSET_WPOS_Z_DEFAULT)
        machine_general["tool_change_x_mpos"] = str(self.TOOL_CHANGE_OFFSET_MPOS_X_DEFAULT)
        machine_general["tool_change_y_mpos"] = str(self.TOOL_CHANGE_OFFSET_MPOS_Y_DEFAULT)
        machine_general["tool_change_z_mpos"] = str(self.TOOL_CHANGE_OFFSET_MPOS_Z_DEFAULT)
        machine_general["tool_probe_z_limit"] = str(self.TOOL_PROBE_Z_LIMIT_DEFAULT)

        # Write machine ini file #
        with open(self.machine_config_path, 'w') as configfile:
            self.machine_settings.write(configfile)
