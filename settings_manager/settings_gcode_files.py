import configparser
import os


class GCodeFilesSettingsHandler:
    # G-Code Files CONFIGURATION DEFAULT VALUES
    GCODE_FOLDER_DEFAULT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../gcode_temp_dir'))

    def __init__(self, config_folder):
        if not os.path.isdir(self.GCODE_FOLDER_DEFAULT):
            os.makedirs(self.GCODE_FOLDER_DEFAULT)
        self.gcf_config_path = os.path.normpath(os.path.join(config_folder, 'gcode_files_config.ini'))
        self.gcode_folder = self.GCODE_FOLDER_DEFAULT
        self.gcf_settings = configparser.ConfigParser()

    def read_all_gcf_settings(self):
        """ Read all g-code files'settings from ini files """
        # If gcode settings file does NOT exist create it with default values
        if not os.path.isfile(self.gcf_config_path):
            self.restore_all_gcf_settings()

        # Read g-code files'settings ini file #
        self.gcf_settings.read(self.gcf_config_path)

        if "FILES" in self.gcf_settings:
            self.gcode_folder = self.gcf_settings["FILES"]["gcode_folder"]

    def write_all_gcf_settings(self):
        """ Write all g-code files'settings to ini files """
        self.gcf_settings["DEFAULT"] = {"gcode_folder": self.GCODE_FOLDER_DEFAULT}

        gcf_settings_od = {}
        self.gcf_settings["FILES"] = {}
        files_settings = self.gcf_settings["FILES"]
        files_settings["gcode_folder"] = self.gcode_folder

        # Write application ini file #
        with open(self.gcf_config_path, 'w') as configfile:
            self.gcf_settings.write(configfile)

    def restore_all_gcf_settings(self):
        """ Restore all g-code files'settings to ini files """
        self.gcf_settings["DEFAULT"] = {"gcode_folder": self.GCODE_FOLDER_DEFAULT}

        gcf_settings_od = {}
        self.gcf_settings["FILES"] = {}
        files_settings = self.gcf_settings["FILES"]
        files_settings["gcode_folder"] = self.GCODE_FOLDER_DEFAULT

        # Write application ini file #
        with open(self.gcf_config_path, 'w') as configfile:
            self.gcf_settings.write(configfile)
