import configparser
import os


class GCodeFilesSettingsHandler:

    def __init__(self, config_folder):
        if os.path.isdir(config_folder):
            local_path = os.path.dirname(config_folder)
            self.gcode_folder_default = os.path.join(local_path, "gcode_temp_dir")

        self.gcf_config_path = os.path.normpath(os.path.join(config_folder, 'gcode_files_config.ini'))
        self.gcode_folder = self.gcode_folder_default
        self.gcf_settings = configparser.ConfigParser()

    def read_all_gcf_settings(self):
        """ Read all g-code files' settings from ini files """
        # If gcode settings file does NOT exist create it with default values
        if not os.path.isfile(self.gcf_config_path):
            self.restore_all_gcf_settings()

        # Read g-code files' settings ini file #
        self.gcf_settings.read(self.gcf_config_path)

        if "FILES" in self.gcf_settings:
            self.gcode_folder = self.gcf_settings["FILES"]["gcode_folder"]

        if not os.path.isdir(self.gcode_folder):
            os.makedirs(self.gcode_folder)

    def write_all_gcf_settings(self):
        """ Write all g-code files' settings to ini files """
        self.gcf_settings["DEFAULT"] = {"gcode_folder": self.gcode_folder_default}

        self.gcf_settings["FILES"] = {}
        files_settings = self.gcf_settings["FILES"]
        files_settings["gcode_folder"] = self.gcode_folder

        # Write application ini file #
        with open(self.gcf_config_path, 'w') as configfile:
            self.gcf_settings.write(configfile)

    def restore_all_gcf_settings(self):
        """ Restore all g-code files' settings to ini files """
        self.gcf_settings["DEFAULT"] = {"gcode_folder": self.gcode_folder_default}

        self.gcf_settings["FILES"] = {}
        files_settings = self.gcf_settings["FILES"]
        files_settings["gcode_folder"] = self.gcode_folder_default

        # Write application ini file #
        with open(self.gcf_config_path, 'w') as configfile:
            self.gcf_settings.write(configfile)
