import os
from .settings_app import AppSettingsHandler
from .settings_job import JobSettingsHandler
from .settings_gcode_files import GCodeFilesSettingsHandler
from .settings_machine import MachineSettingsHandler


class SettingsHandler:
    # Configuration file folder
    CONFIG_FOLDER = os.path.normpath(os.path.join(os.path.dirname(__file__), '../configurations'))

    def __init__(self, main_win):
        if not os.path.isdir(self.CONFIG_FOLDER):
            os.makedirs(self.CONFIG_FOLDER)

        self.main_win = main_win

        self.app_settings = AppSettingsHandler(self.CONFIG_FOLDER, main_win)
        self.jobs_settings = JobSettingsHandler(self.CONFIG_FOLDER)
        self.gcf_settings = GCodeFilesSettingsHandler(self.CONFIG_FOLDER)
        self.machine_settings = MachineSettingsHandler(self.CONFIG_FOLDER, main_win)

    def read_all_settings(self):
        """ Read all settings from ini files """
        self.app_settings.read_all_app_settings()
        self.jobs_settings.read_all_jobs_settings()
        self.gcf_settings.read_all_gcf_settings()
        self.machine_settings.read_all_machine_settings()

    def write_all_settings(self, all_settings_od):
        """ Write all settings to ini files """
        # if "app_settings" in all_settings_od:
        #    self.app_settings.write_all_app_settings(all_settings_od["app_settings"])

        self.app_settings.write_all_app_settings()
        if "jobs_settings" in all_settings_od:
            self.jobs_settings.write_all_jobs_settings(all_settings_od["jobs_settings"])
        self.gcf_settings.write_all_gcf_settings()
        self.machine_settings.write_all_machine_settings()
