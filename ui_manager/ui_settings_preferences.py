from PySide2.QtCore import QObject
import logging

logger = logging.getLogger(__name__)


class UiSettingsPreferencesTab(QObject):
    """Class dedicated to UI <--> Settings interactions on Settings/Preferences Tab. """
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

        self.ui.get_tool_offset_pb.clicked.connect(self.get_tool_offset)
        self.ui.get_tool_change_pb.clicked.connect(self.get_tool_change)

    def get_tool_offset(self):
        """
        Get tool offset mpos and wpos and update corresponding ui fields.
        This should be done with signals/slots because of the access to
        another thread, momentarily made with function calls to control_wo.
        """
        actual_status_report = self.control_wo.get_status_report()
        tool_offset_mpos = actual_status_report["mpos"]
        tool_offset_wpos = actual_status_report["wpos"]
        self.ui.tool_offset_x_mpos_dsb.setValue(tool_offset_mpos[0])
        self.ui.tool_offset_y_mpos_dsb.setValue(tool_offset_mpos[1])
        self.ui.tool_offset_z_mpos_dsb.setValue(tool_offset_mpos[2])
        self.ui.tool_offset_x_wpos_dsb.setValue(tool_offset_wpos[0])
        self.ui.tool_offset_y_wpos_dsb.setValue(tool_offset_wpos[1])
        self.ui.tool_offset_z_wpos_dsb.setValue(tool_offset_wpos[2])

    def get_tool_change(self):
        """
        Get tool change mpos and wpos and update corresponding ui fields.
        This should be done with signals/slots because of the access to
        another thread, momentarily made with function calls to control_wo.
        """
        actual_status_report = self.control_wo.get_status_report()
        tool_change_mpos = actual_status_report["mpos"]
        tool_change_wpos = actual_status_report["wpos"]
        self.ui.tool_change_x_mpos_dsb.setValue(tool_change_mpos[0])
        self.ui.tool_change_y_mpos_dsb.setValue(tool_change_mpos[1])
        self.ui.tool_change_z_mpos_dsb.setValue(tool_change_mpos[2])
        self.ui.tool_change_x_wpos_dsb.setValue(tool_change_wpos[0])
        self.ui.tool_change_y_wpos_dsb.setValue(tool_change_wpos[1])
        self.ui.tool_change_z_wpos_dsb.setValue(tool_change_wpos[2])
