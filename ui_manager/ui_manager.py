from PySide6.QtCore import Signal, Slot, QObject
from PySide6.QtGui import QActionGroup
from shape_core.visual_manager import VisualLayer

from .ui_align_tab import UiAlignTab
from .ui_control_tab import UiControlTab
from .ui_create_job_tab_manager import UiCreateJobLayerTab
from .ui_view_load_layer_tab import UiViewLoadLayerTab

import logging

logger = logging.getLogger(__name__)


class UiManager(QObject):
    """Manage UI objects, signals and slots"""
    L_TAGS = ("top", "bottom", "profile", "drill", "no_copper_top", "no_copper_bottom")
    L_NAMES = ("TOP", "BOTTOM", "PROFILE", "DRILL", "NO COPPER TOP", "NO COPPER BOTTOM")
    LOG_COLORS = {
        logging.DEBUG:    'white',
        logging.INFO:     'light blue',
        logging.WARNING:  'orange',
        logging.ERROR:    'red',
        logging.CRITICAL: 'purple',
    }

    def __init__(self, main_win, ui, control_worker, serial_worker, settings):
        super(UiManager, self).__init__()
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.settings = settings

        self.hide_show_console()
        self.hide_show_preferences_tab()

        self.vis_layer = VisualLayer(self.ui.viewCanvasWidget)
        self.ctrl_layer = VisualLayer(self.ui.controlCanvasWidget)

        # UI Sub-Managers
        self.ui_load_layer_m = UiViewLoadLayerTab(main_win, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES,
                                                  self.settings.app_settings)
        self.ui_create_job_m = UiCreateJobLayerTab(ui, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES, self.settings.jobs_settings)
        self.ui_control_tab_m = UiControlTab(ui, control_worker, serial_worker, self.ctrl_layer,
                                             self.settings.app_settings, self.settings.gcf_settings)
        self.ui_align_tab_m = UiAlignTab(ui, control_worker)

        self.ui.prepare_widget.currentChanged.connect(self.from_load_to_create)
        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)
        self.ui.actionSettings_Preferences.triggered.connect(self.hide_show_preferences_tab)
        self.ui.actionSave_Settings.triggered.connect(self.save_all_settings)

        self.make_log_action_mutually_exclusive()

    def save_all_settings(self):
        all_settings_od = {"jobs_settings": self.ui_create_job_m.get_all_settings()}
        self.settings.write_all_settings(all_settings_od)

    def from_load_to_create(self):
        if self.ui.prepare_widget.currentWidget().objectName() == "create_job_tab":
            self.ui_create_job_m.load_active_layers(self.ui_load_layer_m.get_loaded_layers())
        elif self.ui.prepare_widget.currentWidget().objectName() == "load_layers_tab":
            self.ui_load_layer_m.visualize_all_active_layers()

    @Slot(str, logging.LogRecord)
    def update_logging_status(self, status, record):
        color = self.LOG_COLORS.get(record.levelno, 'black')
        if "<" in status:
            status = status.replace("<", "&lt;")
            status = status.replace(">", "&gt;")
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.ui.logging_plain_te.appendHtml(s)
        # self.ui.logging_plain_te.appendPlainText(record)  # Use only for debug.

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()

    def hide_show_preferences_tab(self):
        setting_tab_idx = self.ui.main_tab_widget.indexOf(self.ui.settings_tab)
        if self.ui.actionSettings_Preferences.isChecked():
            self.ui.main_tab_widget.setTabVisible(setting_tab_idx, True)
        else:
            self.ui.main_tab_widget.setTabVisible(setting_tab_idx, False)

    def make_log_action_mutually_exclusive(self):
        log_level_group = QActionGroup(self.main_win)
        log_level_group.addAction(self.ui.action_critical)
        log_level_group.addAction(self.ui.action_error)
        log_level_group.addAction(self.ui.action_warning)
        log_level_group.addAction(self.ui.action_info)
        log_level_group.addAction(self.ui.action_debug)
        log_level_group.setExclusive(True)
