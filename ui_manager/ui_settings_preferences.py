from PySide2.QtCore import QObject, Signal, Slot
import logging

logger = logging.getLogger(__name__)


class UiSettingsPreferencesTab(QObject):
    """Class dedicated to UI <--> Settings interactions on Settings/Preferences Tab. """

    load_gcoder_cfg_s = Signal()
    save_all_settings_s = Signal()

    def __init__(self, ui, control_worker, settings):
        """
        Initialize ui elements of Settings/Preferences tab.

        Parameters
        ----------
        ui: Ui_MainWindow
            User interface object. Contains all user interface's children objects.
        control_worker: ControllerWorker
            Control thread worker object.
        settings: SettingsHandler
            Handler object that allows the access all the settings.
        """
        super(UiSettingsPreferencesTab, self).__init__()
        self.ui = ui
        self.control_wo = control_worker
        self.settings = settings
        self.machine_settings = settings.machine_settings

        self.ui.tool_probe_wm_pos_chb.setChecked(self.machine_settings.tool_probe_rel_flag)
        self.tool_probe_wm_pos_checked()

        self.ui.tool_probe_wm_pos_chb.clicked.connect(self.tool_probe_wm_pos_checked)
        self.ui.get_tool_offset_pb.clicked.connect(self.get_tool_probe_position)
        self.ui.get_tool_change_pb.clicked.connect(self.get_tool_change_position)
        self.load_gcoder_cfg_s.connect(self.control_wo.update_gerber_cfg)
        self.ui.save_settings_preferences_pb.clicked.connect(self.save_settings_preferences)

        self.ui_tool_probe_set_enabling(enable=False)
        self.ui_tool_change_set_enabling(enable=False)

        self.set_tool_machine_initial_settings()

    def set_tool_machine_initial_settings(self):
        """Initialize ui value from initial machine settings."""
        self.ui.tool_offset_x_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_x_mpos)
        self.ui.tool_offset_y_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_y_mpos)
        self.ui.tool_offset_z_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_z_mpos)
        self.ui.tool_offset_x_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_x_wpos)
        self.ui.tool_offset_y_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_y_wpos)
        self.ui.tool_offset_z_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_z_wpos)

        self.ui.tool_change_x_mpos_dsb.setValue(self.machine_settings.tool_change_offset_x_mpos)
        self.ui.tool_change_y_mpos_dsb.setValue(self.machine_settings.tool_change_offset_y_mpos)
        self.ui.tool_change_z_mpos_dsb.setValue(self.machine_settings.tool_change_offset_z_mpos)

        self.ui.tool_probe_z_limit_dsb.setValue(self.machine_settings.tool_probe_z_limit)

        self.ui.feedrate_xy_dsb.setValue(self.machine_settings.feedrate_xy)
        self.ui.feedrate_z_dsb.setValue(self.machine_settings.feedrate_z)
        self.ui.feedrate_probe_dsb.setValue(self.machine_settings.feedrate_probe)

    def ui_tool_probe_set_enabling(self, enable=False):
        """Enable or disable tool probe get button. """
        self.ui.get_tool_offset_pb.setEnabled(enable)

    def ui_tool_change_set_enabling(self, enable=False):
        """Enable or disable tool change get button. """
        self.ui.get_tool_change_pb.setEnabled(enable)

    @Slot()
    def tool_probe_wm_pos_checked(self):
        """Update tool probe field passing from relative to absolute position and vice-versa. """
        wpos_flag = self.ui.tool_probe_wm_pos_chb.isChecked()
        if wpos_flag:
            self.ui.tool_offset_x_mpos_dsb.setEnabled(False)
            self.ui.tool_offset_y_mpos_dsb.setEnabled(False)
            self.ui.tool_offset_z_mpos_dsb.setEnabled(False)
            self.ui.tool_offset_x_wpos_dsb.setEnabled(True)
            self.ui.tool_offset_y_wpos_dsb.setEnabled(True)
            self.ui.tool_offset_z_wpos_dsb.setEnabled(True)
        else:
            self.ui.tool_offset_x_mpos_dsb.setEnabled(True)
            self.ui.tool_offset_y_mpos_dsb.setEnabled(True)
            self.ui.tool_offset_z_mpos_dsb.setEnabled(True)
            self.ui.tool_offset_x_wpos_dsb.setEnabled(False)
            self.ui.tool_offset_y_wpos_dsb.setEnabled(False)
            self.ui.tool_offset_z_wpos_dsb.setEnabled(False)

    def get_tool_probe_position(self):
        """
        Get tool offset mpos and wpos and update corresponding ui fields.
        This should be done with signals/slots because of the access to
        another thread, momentarily made with function calls to control_wo.
        """
        actual_status_report = self.control_wo.get_status_report()
        wpos_flag = self.machine_settings.tool_probe_rel_flag
        if wpos_flag:
            tool_offset_wpos = actual_status_report["wpos"]
            self.ui.tool_offset_x_wpos_dsb.setValue(tool_offset_wpos[0])
            self.ui.tool_offset_y_wpos_dsb.setValue(tool_offset_wpos[1])
            self.ui.tool_offset_z_wpos_dsb.setValue(tool_offset_wpos[2])
        else:
            tool_offset_mpos = actual_status_report["mpos"]
            self.ui.tool_offset_x_mpos_dsb.setValue(tool_offset_mpos[0])
            self.ui.tool_offset_y_mpos_dsb.setValue(tool_offset_mpos[1])
            self.ui.tool_offset_z_mpos_dsb.setValue(tool_offset_mpos[2])

    def get_tool_change_position(self):
        """
        Get tool change mpos and wpos and update corresponding ui fields.
        This should be done with signals/slots because of the access to
        another thread, momentarily made with function calls to control_wo.
        """
        actual_status_report = self.control_wo.get_status_report()
        tool_change_mpos = actual_status_report["mpos"]
        self.machine_settings.tool_probe_offset_x_mpos = tool_change_mpos[0]
        self.machine_settings.tool_probe_offset_y_mpos = tool_change_mpos[1]
        self.machine_settings.tool_probe_offset_z_mpos = tool_change_mpos[2]
        self.ui.tool_change_x_mpos_dsb.setValue(tool_change_mpos[0])
        self.ui.tool_change_y_mpos_dsb.setValue(tool_change_mpos[1])
        self.ui.tool_change_z_mpos_dsb.setValue(tool_change_mpos[2])

        self.load_gcoder_cfg_s.emit()

    def save_settings_preferences(self):
        """Save settings preferences from UI to settings."""
        self.machine_settings.tool_probe_rel_flag = self.ui.tool_probe_wm_pos_chb.isChecked()

        self.machine_settings.tool_probe_offset_x_mpos = self.ui.tool_offset_x_mpos_dsb.value()
        self.machine_settings.tool_probe_offset_y_mpos = self.ui.tool_offset_y_mpos_dsb.value()
        self.machine_settings.tool_probe_offset_z_mpos = self.ui.tool_offset_z_mpos_dsb.value()

        self.machine_settings.tool_probe_offset_x_wpos = self.ui.tool_offset_x_wpos_dsb.value()
        self.machine_settings.tool_probe_offset_y_wpos = self.ui.tool_offset_y_wpos_dsb.value()
        self.machine_settings.tool_probe_offset_z_wpos = self.ui.tool_offset_z_wpos_dsb.value()

        self.machine_settings.tool_change_offset_x_mpos = self.ui.tool_change_x_mpos_dsb.value()
        self.machine_settings.tool_change_offset_y_mpos = self.ui.tool_change_y_mpos_dsb.value()
        self.machine_settings.tool_change_offset_z_mpos = self.ui.tool_change_z_mpos_dsb.value()

        self.machine_settings.tool_probe_z_limit = self.ui.tool_probe_z_limit_dsb.value()

        self.machine_settings.feedrate_xy = self.ui.feedrate_xy_dsb.value()
        self.machine_settings.feedrate_z = self.ui.feedrate_z_dsb.value()
        self.machine_settings.feedrate_probe = self.ui.feedrate_probe_dsb.value()

        self.load_gcoder_cfg_s.emit()

        # self.settings.write_all_settings()
        self.save_all_settings_s.emit()
