from PySide2.QtCore import Signal, Slot, QObject
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
    # L_COLORS = ["red", "blue", "black", "green", "purple", "brown"]
    L_COLORS = ["#FFC300", "#A3E4D7", "black", "green", "purple", "brown"]
    LOG_COLORS = {
        logging.DEBUG:    'white',
        logging.INFO:     'light blue',
        logging.WARNING:  'orange',
        logging.ERROR:    'red',
        logging.CRITICAL: 'purple',
    }

    def __init__(self, main_win, ui, control_worker, serial_worker):
        super(UiManager, self).__init__()
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.hide_show_console()
        self.hide_show_preferences_tab()

        self.vis_layer = VisualLayer(self.ui.viewCanvasWidget)

        # UI Sub-Managers
        self.ui_load_layer_m = UiViewLoadLayerTab(main_win, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES,
                                                  self.L_COLORS)
        self.ui_create_job_m = UiCreateJobLayerTab(ui, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES)
        self.ui_control_tab_m = UiControlTab(ui, control_worker, serial_worker)
        self.ui_align_tab_m = UiAlignTab(ui, control_worker)

        self.ui.prepare_widget.currentChanged.connect(self.from_load_to_create)
        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)
        self.ui.actionSettings_Preferences.triggered.connect(self.hide_show_preferences_tab)

    def from_load_to_create(self):
        if self.ui.prepare_widget.currentWidget().objectName() == "create_job_tab":
            self.ui_create_job_m.load_active_layers(self.ui_load_layer_m.get_loaded_layers())
        elif self.ui.prepare_widget.currentWidget().objectName() == "load_layers_tab":
            self.ui_load_layer_m.visualize_all_active_layers()

    @Slot(str, logging.LogRecord)
    def update_logging_status(self, status, record):
        color = self.LOG_COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.ui.logging_plain_te.appendHtml(s)

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
