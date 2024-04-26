from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QColorDialog
from collections import OrderedDict as Od
import logging

logger = logging.getLogger(__name__)


class UiSettingsPreferencesTab(QObject):
    """Class dedicated to UI <--> Settings interactions on Settings/Preferences Tab. """

    ask_status_report_s = Signal()
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
        self.app_settings = settings.app_settings
        self.jobs_settings = settings.jobs_settings
        self.machine_settings = settings.machine_settings

        self.get_tool_change_flag = False
        self.get_tool_probe_flag = False
        self.get_tool_camera_offset_flag = False

        self.reset_tool_probe_initial_enables()

        self.ui.tool_probe_wm_pos_chb.clicked.connect(self.tool_probe_wm_pos_checked)
        self.ui.get_tool_probe_pb.clicked.connect(self.ask_tool_probe_position)
        self.ask_status_report_s.connect(self.control_wo.report_status_report)
        self.control_wo.report_status_report_s.connect(self.get_and_manage_status_report)
        self.ui.get_tool_change_pb.clicked.connect(self.ask_tool_change_position)
        self.load_gcoder_cfg_s.connect(self.control_wo.update_gerber_cfg)
        self.ui.save_settings_preferences_pb.clicked.connect(self.save_settings_preferences)
        self.ui.get_tool_camera_offset_pb.clicked.connect(self.ask_tool_camera_offset)

        self.ui_tool_probe_set_enabling(enable=False)
        self.ui_tool_change_set_enabling(enable=False)

        self.reset_probe_initial_settings()
        self.reset_tool_machine_initial_settings()
        self.reset_jobs_common_initial_settings()
        self.ui.tool_probe_x_mpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_probe_y_mpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_probe_z_mpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_probe_x_wpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_probe_y_wpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_probe_z_wpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_change_x_mpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_change_y_mpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_change_z_mpos_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.tool_probe_z_limit_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.hold_on_probe_chb.clicked.connect(self.set_focus_lost)
        self.ui.zeroing_after_probe_chb.clicked.connect(self.set_focus_lost)
        self.ui.feedrate_xy_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.feedrate_z_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.feedrate_probe_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.x_mirror_rb.clicked.connect(self.set_focus_lost)
        self.ui.y_mirror_rb.clicked.connect(self.set_focus_lost)
        self.ui.alignment_drill_diameter_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.x_tool_camera_offset_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.y_tool_camera_offset_dsb.valueChanged.connect(self.set_focus_lost)
        self.ui.restore_settings_preferences_pb.clicked.connect(self.restore_initial_settings)

        self.reset_application_settings()
        self.ui.top_layer_color_pb.clicked.connect(lambda: self.layer_color_choice("top"))
        self.ui.bottom_layer_color_pb.clicked.connect(lambda: self.layer_color_choice("bottom"))
        self.ui.profile_layer_color_pb.clicked.connect(lambda: self.layer_color_choice("profile"))
        self.ui.drill_layer_color_pb.clicked.connect(lambda: self.layer_color_choice("drill"))
        self.ui.nc_top_layer_color_pb.clicked.connect(lambda: self.layer_color_choice("nc_top"))
        self.ui.nc_bottom_layer_color_pb.clicked.connect(lambda: self.layer_color_choice("nc_bottom"))

    def reset_application_settings(self):
        """Resets ui elements values according to application settings."""
        self.ui.top_layer_color_la.setStyleSheet("background-color: {}".format(self.app_settings.layer_color["top"]))
        self.ui.bottom_layer_color_la.setStyleSheet(
            "background-color: {}".format(self.app_settings.layer_color["bottom"]))
        self.ui.profile_layer_color_la.setStyleSheet(
            "background-color: {}".format(self.app_settings.layer_color["profile"]))
        self.ui.drill_layer_color_la.setStyleSheet(
            "background-color: {}".format(self.app_settings.layer_color["drill"]))
        self.ui.nc_top_layer_color_la.setStyleSheet(
            "background-color: {}".format(self.app_settings.layer_color["nc_top"]))
        self.ui.nc_bottom_layer_color_la.setStyleSheet(
            "background-color: {}".format(self.app_settings.layer_color["nc_bottom"]))

    def reset_jobs_common_initial_settings(self):
        """Reset status of common jobs settings. """
        mirror_axis = self.jobs_settings.jobs_settings_od["common"]["mirroring_axis"]
        if mirror_axis.lower() == "x":
            self.ui.x_mirror_rb.setChecked(True)
        elif mirror_axis.lower() == "y":
            self.ui.y_mirror_rb.setChecked(True)

    def reset_tool_probe_initial_enables(self):
        """Reset status of tool probe checkbox checked (or not) and wpos/mpos fields enabled or disabled. """
        self.ui.tool_probe_wm_pos_chb.setChecked(self.machine_settings.tool_probe_rel_flag)
        self.enable_disable_tool_probe_wpos_mpos(self.machine_settings.tool_probe_rel_flag)

    def reset_probe_initial_settings(self):
        """Initialize or re-initialize ui value from initial probe machine settings."""
        self.ui.hold_on_probe_chb.setChecked(self.machine_settings.hold_on_probe_flag)
        self.ui.zeroing_after_probe_chb.setChecked(self.machine_settings.zeroing_after_probe_flag)

    def reset_tool_machine_initial_settings(self):
        """Initialize or re-initialize ui value from initial machine settings."""
        self.ui.tool_probe_x_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_x_mpos)
        self.ui.tool_probe_y_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_y_mpos)
        self.ui.tool_probe_z_mpos_dsb.setValue(self.machine_settings.tool_probe_offset_z_mpos)
        self.ui.tool_probe_x_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_x_wpos)
        self.ui.tool_probe_y_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_y_wpos)
        self.ui.tool_probe_z_wpos_dsb.setValue(self.machine_settings.tool_probe_offset_z_wpos)

        self.ui.tool_change_x_mpos_dsb.setValue(self.machine_settings.tool_change_offset_x_mpos)
        self.ui.tool_change_y_mpos_dsb.setValue(self.machine_settings.tool_change_offset_y_mpos)
        self.ui.tool_change_z_mpos_dsb.setValue(self.machine_settings.tool_change_offset_z_mpos)

        self.ui.tool_probe_z_limit_dsb.setValue(self.machine_settings.tool_probe_z_limit)

        self.ui.feedrate_xy_dsb.setValue(self.machine_settings.feedrate_xy)
        self.ui.feedrate_z_dsb.setValue(self.machine_settings.feedrate_z)
        self.ui.feedrate_probe_dsb.setValue(self.machine_settings.feedrate_probe)

        self.ui.alignment_drill_diameter_dsb.setValue(self.machine_settings.alignment_drill_diameter)
        self.ui.x_tool_camera_offset_dsb.setValue(self.machine_settings.tool_camera_offset_x)
        self.ui.y_tool_camera_offset_dsb.setValue(self.machine_settings.tool_camera_offset_y)

    def restore_initial_settings(self):
        """Restore initial settings in ui fields. """
        self.reset_application_settings()
        self.reset_jobs_common_initial_settings()
        self.reset_probe_initial_settings()
        self.reset_tool_machine_initial_settings()
        self.reset_tool_probe_initial_enables()
        self.reset_focus_lost()
        self.ui.status_bar.showMessage("Settings/Preferences restored.")

    def ui_tool_probe_set_enabling(self, enable=False):
        """Enable or disable tool probe get button. """
        self.ui.get_tool_probe_pb.setEnabled(enable)

    def ui_tool_change_set_enabling(self, enable=False):
        """Enable or disable tool change get button. """
        self.ui.get_tool_change_pb.setEnabled(enable)

    @Slot()
    def tool_probe_wm_pos_checked(self):
        """Update tool probe field passing from relative to absolute position and vice-versa. """
        wpos_flag = self.ui.tool_probe_wm_pos_chb.isChecked()
        self.enable_disable_tool_probe_wpos_mpos(wpos_flag)
        self.set_focus_lost()

    def enable_disable_tool_probe_wpos_mpos(self, wpos_flag):
        """
        Enable/disable tool probe wpos ui fields or mpos ui fields.

        Parameters
        ----------
        wpos_flag

        Returns
        -------

        """
        if wpos_flag:
            self.ui.tool_probe_x_mpos_dsb.setEnabled(False)
            self.ui.tool_probe_y_mpos_dsb.setEnabled(False)
            self.ui.tool_probe_z_mpos_dsb.setEnabled(False)
            self.ui.tool_probe_x_wpos_dsb.setEnabled(True)
            self.ui.tool_probe_y_wpos_dsb.setEnabled(True)
            self.ui.tool_probe_z_wpos_dsb.setEnabled(True)
        else:
            self.ui.tool_probe_x_mpos_dsb.setEnabled(True)
            self.ui.tool_probe_y_mpos_dsb.setEnabled(True)
            self.ui.tool_probe_z_mpos_dsb.setEnabled(True)
            self.ui.tool_probe_x_wpos_dsb.setEnabled(False)
            self.ui.tool_probe_y_wpos_dsb.setEnabled(False)
            self.ui.tool_probe_z_wpos_dsb.setEnabled(False)

    def ask_status_report(self):
        """ Emit a signal asking asynchronously the controller status report. """
        self.ask_status_report_s.emit()

    @Slot(Od)
    def get_and_manage_status_report(self, actual_status_report):
        """ Asynchronously get status report and call function relative to function that asked for it. """
        if self.get_tool_probe_flag:
            self.get_tool_probe_flag = False
            self.get_tool_probe_position(actual_status_report)
        elif self.get_tool_change_flag:
            self.get_tool_change_flag = False
            self.get_tool_change_position(actual_status_report)
        elif self.get_tool_camera_offset_flag:
            self.get_tool_camera_offset_flag = False
            self.get_tool_camera_offset(actual_status_report)

    def ask_tool_probe_position(self):
        """ Set get_tool_probe_flag at true and ask controller status report. """
        self.get_tool_probe_flag = True
        self.ask_status_report()

    def ask_tool_change_position(self):
        """ Set get_tool_probe_flag at true and ask controller status report. """
        self.get_tool_change_flag = True
        self.ask_status_report()

    def ask_tool_camera_offset(self):
        """ Set get_tool_camera_offset_flag at true and ask controller status report. """
        self.get_tool_camera_offset_flag = True
        self.ask_status_report()

    def get_tool_probe_position(self, actual_status_report):
        """ Get tool offset mpos and wpos and update corresponding ui fields. """
        wpos_flag = self.ui.tool_probe_wm_pos_chb.isChecked()
        if wpos_flag:
            tool_probe_wpos = actual_status_report["wpos"]
            self.ui.tool_probe_x_wpos_dsb.setValue(tool_probe_wpos[0])
            self.ui.tool_probe_y_wpos_dsb.setValue(tool_probe_wpos[1])
            self.ui.tool_probe_z_wpos_dsb.setValue(tool_probe_wpos[2])
        else:
            tool_probe_mpos = actual_status_report["mpos"]
            self.ui.tool_probe_x_mpos_dsb.setValue(tool_probe_mpos[0])
            self.ui.tool_probe_y_mpos_dsb.setValue(tool_probe_mpos[1])
            self.ui.tool_probe_z_mpos_dsb.setValue(tool_probe_mpos[2])

    def get_tool_change_position(self, actual_status_report):
        """ Get tool change mpos and wpos and update corresponding ui fields. """
        tool_change_mpos = actual_status_report["mpos"]
        self.ui.tool_change_x_mpos_dsb.setValue(tool_change_mpos[0])
        self.ui.tool_change_y_mpos_dsb.setValue(tool_change_mpos[1])
        self.ui.tool_change_z_mpos_dsb.setValue(tool_change_mpos[2])

        self.load_gcoder_cfg_s.emit()

    def get_tool_camera_offset(self, actual_status_report):
        tool_camera_offset_wpos = actual_status_report["wpos"]
        self.ui.x_tool_camera_offset_dsb.setValue(tool_camera_offset_wpos[0])
        self.ui.y_tool_camera_offset_dsb.setValue(tool_camera_offset_wpos[1])

    def save_settings_preferences(self):
        """Save settings preferences from UI to settings."""
        if self.ui.x_mirror_rb.isChecked():
            self.jobs_settings.jobs_settings_od["common"]["mirroring_axis"] = "x"
        elif self.ui.y_mirror_rb.isChecked():
            self.jobs_settings.jobs_settings_od["common"]["mirroring_axis"] = "y"

        self.machine_settings.tool_probe_rel_flag = self.ui.tool_probe_wm_pos_chb.isChecked()

        self.machine_settings.tool_probe_offset_x_mpos = self.ui.tool_probe_x_mpos_dsb.value()
        self.machine_settings.tool_probe_offset_y_mpos = self.ui.tool_probe_y_mpos_dsb.value()
        self.machine_settings.tool_probe_offset_z_mpos = self.ui.tool_probe_z_mpos_dsb.value()

        self.machine_settings.tool_probe_offset_x_wpos = self.ui.tool_probe_x_wpos_dsb.value()
        self.machine_settings.tool_probe_offset_y_wpos = self.ui.tool_probe_y_wpos_dsb.value()
        self.machine_settings.tool_probe_offset_z_wpos = self.ui.tool_probe_z_wpos_dsb.value()

        self.machine_settings.tool_change_offset_x_mpos = self.ui.tool_change_x_mpos_dsb.value()
        self.machine_settings.tool_change_offset_y_mpos = self.ui.tool_change_y_mpos_dsb.value()
        self.machine_settings.tool_change_offset_z_mpos = self.ui.tool_change_z_mpos_dsb.value()

        self.machine_settings.tool_probe_z_limit = self.ui.tool_probe_z_limit_dsb.value()
        self.machine_settings.hold_on_probe_flag = self.ui.hold_on_probe_chb.isChecked()
        self.machine_settings.zeroing_after_probe_flag = self.ui.zeroing_after_probe_chb.isChecked()

        self.machine_settings.feedrate_xy = self.ui.feedrate_xy_dsb.value()
        self.machine_settings.feedrate_z = self.ui.feedrate_z_dsb.value()
        self.machine_settings.feedrate_probe = self.ui.feedrate_probe_dsb.value()

        self.machine_settings.alignment_drill_diameter = self.ui.alignment_drill_diameter_dsb.value()
        self.machine_settings.tool_camera_offset_x = self.ui.x_tool_camera_offset_dsb.value()
        self.machine_settings.tool_camera_offset_y = self.ui.y_tool_camera_offset_dsb.value()

        self.app_settings.layer_color["top"] = self.ui.top_layer_color_la.palette().background().color().name()
        self.app_settings.layer_color["bottom"] = self.ui.bottom_layer_color_la.palette().background().color().name()
        self.app_settings.layer_color["profile"] = self.ui.profile_layer_color_la.palette().background().color().name()
        self.app_settings.layer_color["drill"] = self.ui.drill_layer_color_la.palette().background().color().name()
        self.app_settings.layer_color["nc_top"] = self.ui.nc_top_layer_color_la.palette().background().color().name()
        self.app_settings.layer_color["nc_bottom"] = self.ui.nc_bottom_layer_color_la.palette().background().color().name()

        self.load_gcoder_cfg_s.emit()
        # Emit a signal to write all settings
        self.save_all_settings_s.emit()
        self.ui.status_bar.showMessage("Settings/Preferences saved.")
        self.reset_focus_lost()

    def set_focus_lost(self):
        """ When a setting is changed but not saved the focus is lost. We signal it coloring pushbutton in red. """
        self.ui.save_settings_preferences_pb.setStyleSheet("background-color:red")
        self.ui.status_bar.showMessage("Settings/Preferences modified but still not saved.")

    def reset_focus_lost(self):
        """Reset lost focus to False, the changed settings have been saved or restored. """
        self.ui.save_settings_preferences_pb.setStyleSheet("")

    def layer_color_choice(self, layer):
        """
        Choose a different color for the given layer.

        Parameters
        ----------
        layer: string
            Name of the layer for which the new color is chosen.

        """
        current_label = None
        if layer == "top":
            current_label = self.ui.top_layer_color_la
        elif layer == "bottom":
            current_label = self.ui.bottom_layer_color_la
        elif layer == "profile":
            current_label = self.ui.profile_layer_color_la
        elif layer == "drill":
            current_label = self.ui.drill_layer_color_la
        elif layer == "nc_top":
            current_label = self.ui.nc_top_layer_color_la
        elif layer == "nc_bottom":
            current_label = self.ui.nc_bottom_layer_color_la
        if current_label:
            current_color = current_label.palette().background().color()
            logger.debug(current_color)
            color = QColorDialog.getColor(initial=current_color)
            if color.isValid():
                logger.debug("color " + str(color.name()))
                current_label.setStyleSheet("background-color: {}".format(color.name()))
                self.set_focus_lost()
