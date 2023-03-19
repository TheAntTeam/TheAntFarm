import os
from .settings_app import AppSettingsHandler
from .settings_job import JobSettingsHandler
from .settings_gcode_files import GCodeFilesSettingsHandler
from .settings_machine import MachineSettingsHandler


class SettingsHandler:
    # Configuration file folder
    CONFIG_FOLDER = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'configurations'))

    def __init__(self, main_win):
        self.config_folder = self.CONFIG_FOLDER
        if os.path.isdir(main_win.local_path):
            self.config_folder = os.path.join(main_win.local_path, "configurations")
        if not os.path.isdir(self.config_folder):
            os.makedirs(self.config_folder)

        self.main_win = main_win
        self.local_path = self.main_win.local_path

        self.app_settings = AppSettingsHandler(self.config_folder, main_win)
        self.jobs_settings = JobSettingsHandler(self.config_folder)
        self.gcf_settings = GCodeFilesSettingsHandler(self.config_folder)
        self.machine_settings = MachineSettingsHandler(self.config_folder, main_win)

    def read_all_settings(self):
        """ Read all settings from ini files """
        self.app_settings.read_all_app_settings()
        self.jobs_settings.read_all_jobs_settings()
        self.gcf_settings.read_all_gcf_settings()
        self.machine_settings.read_all_machine_settings()

    def write_all_settings(self, all_settings_od=None):
        """ Write all settings to ini files """
        # if "app_settings" in all_settings_od:
        #    self.app_settings.write_all_app_settings(all_settings_od["app_settings"])

        self.app_settings.write_all_app_settings()
        if all_settings_od:
            if "jobs_settings" in all_settings_od:
                self.jobs_settings.write_all_jobs_settings(all_settings_od["jobs_settings"])
        self.gcf_settings.write_all_gcf_settings()
        self.machine_settings.write_all_machine_settings()
