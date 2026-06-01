import logging

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QActionGroup, QColor, QIcon
from PySide6.QtWidgets import QMessageBox
from shape_core.visual_manager import VisualLayer

from .ui_about import UiAbout
from .ui_align_tab import UiAlignTab
from .ui_control_tab import UiControlTab
from .ui_create_job_tab_manager import UiCreateJobLayerTab
from .ui_settings_preferences import UiSettingsPreferencesTab
from .ui_view_load_layer_tab import UiViewLoadLayerTab

logger = logging.getLogger(__name__)


class UiManager(QObject):
    """Manage UI objects, signals and slots"""

    L_TAGS = ("top", "bottom", "profile", "drill", "nc_top", "nc_bottom")
    L_NAMES = ("TOP", "BOTTOM", "PROFILE", "DRILL", "NO COPPER TOP", "NO COPPER BOTTOM")
    LOG_COLORS = {
        logging.DEBUG: "white",
        logging.INFO: "light blue",
        logging.WARNING: "orange",
        logging.ERROR: "red",
        logging.CRITICAL: "purple",
    }

    def __init__(self, main_win, ui, control_worker, serial_worker, settings, style_manager=None):
        super(UiManager, self).__init__()
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.settings = settings
        self.style_manager = style_manager

        self.hide_show_console()
        self.hide_show_preferences_tab()
        self._previous_main_tab_index = 0
        self._settings_switch_in_progress = False

        self.vis_layer = VisualLayer(self.ui.viewCanvasWidget)
        self.ctrl_layer = VisualLayer(self.ui.controlCanvasWidget)
        self.vis_align_layer = VisualLayer(self.ui.alignCanvasWidget, selectable=True)

        # UI Sub-Managers
        self.ui_load_layer_m = UiViewLoadLayerTab(
            main_win, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES, self.settings.app_settings
        )
        self.ui_create_job_m = UiCreateJobLayerTab(
            ui, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES, self.settings.jobs_settings
        )
        self.ui_control_tab_m = UiControlTab(ui, control_worker, serial_worker, self.ctrl_layer, self.settings)
        self.ui_align_tab_m = UiAlignTab(main_win, control_worker, self.vis_align_layer, self.settings.app_settings)
        self.ui_settings_tab_m = UiSettingsPreferencesTab(ui, control_worker, self.settings)
        self.ui_about_m = UiAbout(main_win, app_settings=self.settings.app_settings)

        self.ui.actionAbout.triggered.connect(self.ui_about_m.show_about_info)
        self.ui_settings_tab_m.save_all_settings_s.connect(self.save_all_settings)

        self._icon_widgets: dict[str, list] = {}
        if self.style_manager:
            self._setup_icon_widgets()
            self.style_manager.theme_changed.connect(self._on_theme_changed)

        self.apply_initial_window_settings(self.settings.app_settings)

    def apply_initial_window_settings(self, app_settings):
        """Apply initial window settings."""
        self.ui.prepare_widget.currentChanged.connect(self.from_load_to_create)
        self.ui.actionSave_Settings.triggered.connect(self.save_all_settings)
        self.make_log_action_mutually_exclusive()
        self.make_style_action_mutually_exclusive()
        if app_settings.win_maximized:
            self.main_win.showMaximized()
        self.main_win.move(app_settings.pos)  # Restore position
        self.main_win.resize(app_settings.size)

        # Initialize tabs visibility according to the saved app settings.
        self.init_tabs_visibility_status()
        # Connect hide/show actions after the initial state has been set (to avoid re-triggering of events).
        self.ui.actionHide_Show_Align_Tab.triggered.connect(self.hide_show_align_tab)
        self.ui.actionSettings_Preferences.triggered.connect(self.hide_show_preferences_tab)

        self.main_win.ui.actionHide_Show_Console.setChecked(app_settings.console_visibility)
        self.hide_show_console()
        # Connect the hide show console action after the initial state has been set.
        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)
        self.main_win.ui.main_tab_widget.setCurrentIndex(app_settings.main_tab_index)
        self._previous_main_tab_index = app_settings.main_tab_index
        self.main_win.ui.ctrl_tab_widget.setCurrentIndex(app_settings.ctrl_tab_index)
        self.main_win.ui.settings_sub_tab.setCurrentIndex(app_settings.settings_tab_index)
        self.main_win.ui.jog_probe_tab_widget.setCurrentIndex(app_settings.jog_probe_tab_index)
        self.main_win.ui.main_tab_widget.currentChanged.connect(self._on_main_tab_changed)

    def save_all_settings(self):
        """Saves all settings in the configuration files."""
        all_settings_od = {"jobs_settings": self.ui_create_job_m.get_all_jobs_settings()}
        self.settings.write_all_settings(all_settings_od)

    def _on_main_tab_changed(self, new_index):
        """Prompt user to save unsaved settings when leaving the Settings/Preferences tab."""
        if self._settings_switch_in_progress:
            return

        settings_tab_idx = self.ui.main_tab_widget.indexOf(self.ui.settings_tab)
        settings_tab = self.ui_settings_tab_m

        if self._previous_main_tab_index == settings_tab_idx and settings_tab.has_unsaved_changes():
            msg = QMessageBox(self.main_win)
            msg.setWindowTitle("Unsaved Settings")
            msg.setText("You have unsaved changes in the Settings/Preferences tab.")
            msg.setInformativeText("Do you want to save your changes before leaving?")
            save_btn = msg.addButton("Save", QMessageBox.ActionRole)
            discard_btn = msg.addButton("Discard", QMessageBox.DestructiveRole)
            cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
            msg.setDefaultButton(cancel_btn)
            msg.exec()

            clicked = msg.clickedButton()
            if clicked == cancel_btn:
                self._settings_switch_in_progress = True
                self.ui.main_tab_widget.setCurrentIndex(self._previous_main_tab_index)
                self._settings_switch_in_progress = False
                return
            elif clicked == save_btn:
                settings_tab.save_settings_preferences()
            elif clicked == discard_btn:
                settings_tab.restore_initial_settings()

        self._previous_main_tab_index = new_index

    def from_load_to_create(self):
        """Do all actions needed to pass from layer loading sub-tab
        to job creation sub-tab and vice-versa."""
        if self.ui.prepare_widget.currentWidget().objectName() == "create_job_tab":
            self.ui_create_job_m.load_active_layers(self.ui_load_layer_m.get_loaded_layers())
        elif self.ui.prepare_widget.currentWidget().objectName() == "load_layers_tab":
            self.ui_load_layer_m.visualize_all_active_layers()

    @Slot(str, logging.LogRecord)
    def update_logging_status(self, status, record):
        """Format and append logging records to the user interface text edit widget."""
        color = self.LOG_COLORS.get(record.levelno, "black")
        if "<" in status:
            status = status.replace("<", "&lt;")
            status = status.replace(">", "&gt;")
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.ui.logging_plain_te.appendHtml(s)
        # self.ui.logging_plain_te.appendPlainText(record)  # Use only for debug.

    def hide_show_console(self):
        """Hide/Show logging console."""
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()

    def init_tabs_visibility_status(self):
        """Hide/Show Align and Settings/Preferences tabs according to the
        application settings and check the relative menu actions."""
        align_tab_visible = self.settings.app_settings.align_tab_visibility
        self.main_win.ui.actionHide_Show_Align_Tab.setChecked(align_tab_visible)
        self.hide_show_align_tab()

        settings_tab_visible = self.settings.app_settings.settings_tab_visibility
        self.main_win.ui.actionSettings_Preferences.setChecked(settings_tab_visible)
        self.hide_show_preferences_tab()

    def hide_show_align_tab(self):
        """Hide/Shows Align tab."""
        align_tab_idx = self.ui.main_tab_widget.indexOf(self.ui.align_tab)
        if self.ui.actionHide_Show_Align_Tab.isChecked():
            self.ui.main_tab_widget.setTabVisible(align_tab_idx, True)
            self.ui.main_tab_widget.setCurrentIndex(align_tab_idx)
        else:
            self.ui.main_tab_widget.setTabVisible(align_tab_idx, False)
            self.ui.main_tab_widget.setCurrentIndex(0)

    def hide_show_preferences_tab(self):
        """Hide/Shows Settings/Preferences tab."""
        setting_tab_idx = self.ui.main_tab_widget.indexOf(self.ui.settings_tab)
        if self.ui.actionSettings_Preferences.isChecked():
            self.ui.main_tab_widget.setTabVisible(setting_tab_idx, True)
            self.ui.main_tab_widget.setCurrentIndex(setting_tab_idx)
        else:
            self.ui.main_tab_widget.setTabVisible(setting_tab_idx, False)
            self.ui.main_tab_widget.setCurrentIndex(0)

    def _setup_icon_widgets(self) -> None:
        icon_map: dict[str, str] = {
            "homing_tb": "home",
            "unlock_tb": "unlock-padlock",
            "play_tb": "play-button-arrowhead",
            "pause_resume_tb": "pause-multimedia-big-gross-symbol-lines",
            "stop_tb": "stop-button-black-rounded-square",
            "tool_change_tb": "milling-machine",
            "soft_reset_tb": "refresh",
            "upload_temp_tb": "upload-file",
            "open_gcode_tb": "open-folder",
            "remove_gcode_tb": "delete",
            "z_plus_pb": "white_north_arrow",
            "z_minus_pb": "white_south_arrow",
            "x_plus_y_plus_pb": "white_north_east_arrow",
            "x_plus_y_minus_pb": "white_south_east_arrow",
            "x_minus_y_plus_pb": "white_north_west_arrow",
            "x_minus_y_minus_pb": "white_south_west_arrow",
            "x_plus_pb": "white_east_arrow",
            "x_minus_pb": "white_west_arrow",
            "y_plus_pb": "white_north_arrow",
            "y_minus_pb": "white_south_arrow",
            "center_tb": "white_circle",
            "z_plus_pb_2": "white_north_arrow",
            "z_minus_pb_2": "white_south_arrow",
            "x_plus_y_plus_pb_2": "white_north_east_arrow",
            "x_plus_y_minus_pb_2": "white_south_east_arrow",
            "x_minus_y_plus_pb_2": "white_north_west_arrow",
            "x_minus_y_minus_pb_2": "white_south_west_arrow",
            "x_plus_pb_2": "white_east_arrow",
            "x_minus_pb_2": "white_west_arrow",
            "y_plus_pb_2": "white_north_arrow",
            "y_minus_pb_2": "white_south_arrow",
            "center_tb_2": "white_circle",
            "apply_alignment_tb_2": "black_apply_align",
        }
        for attr, name in icon_map.items():
            widget = getattr(self.ui, attr, None)
            if widget is not None:
                self._icon_widgets.setdefault(name, []).append(widget)

    def _build_icon(self, icon_name: str, color: QColor) -> QIcon:
        path = f":/resources/resources/icons/{icon_name}.svg"
        return self.style_manager.icon_man.make_icon(path, color)

    def _make_toggle_icon(self, off_name: str, on_name: str, color: QColor) -> QIcon:
        icon = QIcon()
        off_pix = self.style_manager.icon_man.make_icon(f":/resources/resources/icons/{off_name}.svg", color)
        on_pix = self.style_manager.icon_man.make_icon(f":/resources/resources/icons/{on_name}.svg", color)
        icon.addPixmap(off_pix.pixmap(off_pix.availableSizes()[0]), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addPixmap(on_pix.pixmap(on_pix.availableSizes()[0]), QIcon.Mode.Normal, QIcon.State.On)
        return icon

    @Slot(QColor, QColor)
    def _on_theme_changed(self, icon_color: QColor, disabled_color: QColor) -> None:
        sm = self.style_manager
        # Toolbar toggle icon (two states)
        alignment_widgets = self._icon_widgets.get("black_apply_align", [])
        if alignment_widgets:
            toggle_icon = self._make_toggle_icon("black_apply_align", "black_alignment_applied", icon_color)
            for w in alignment_widgets:
                w.setIcon(toggle_icon)
        # Single-state icons
        single_names = [k for k in self._icon_widgets if k != "black_apply_align"]
        for name in single_names:
            icon = self._build_icon(name, icon_color)
            disabled_icon = self._build_icon(name, disabled_color)
            for w in self._icon_widgets[name]:
                q = QIcon()
                pix_size = icon.availableSizes()
                fallback = pix_size[0] if pix_size else w.iconSize()
                q.addPixmap(icon.pixmap(fallback), QIcon.Mode.Normal, QIcon.State.Off)
                q.addPixmap(icon.pixmap(fallback), QIcon.Mode.Normal, QIcon.State.On)
                q.addPixmap(disabled_icon.pixmap(fallback), QIcon.Mode.Disabled, QIcon.State.Off)
                q.addPixmap(disabled_icon.pixmap(fallback), QIcon.Mode.Disabled, QIcon.State.On)
                w.setIcon(q)

    def make_log_action_mutually_exclusive(self):
        """Creates an action group for the log level menu items and makes them mutually exclusive,
        to avoid to check two log levels at the same time."""
        log_level_group = QActionGroup(self.main_win)
        log_level_group.addAction(self.ui.action_critical)
        log_level_group.addAction(self.ui.action_error)
        log_level_group.addAction(self.ui.action_warning)
        log_level_group.addAction(self.ui.action_info)
        log_level_group.addAction(self.ui.action_debug)
        log_level_group.setExclusive(True)

    def make_style_action_mutually_exclusive(self):
        """Creates an action group for the style action menu items and makes them mutually exclusive. """
        style_group = QActionGroup(self.main_win)
        style_group.addAction(self.ui.actionDark)
        style_group.addAction(self.ui.actionLight)
        style_group.setExclusive(True)

        # Connect palette actions to style manager if style_manager is available
        if self.style_manager:
            self.style_manager.connect_palette_actions(self.ui.actionDark, self.ui.actionLight)
            self.ui.actionDark.triggered.connect(lambda : self.vis_layer.canvas.set_canvas_bgcolor(hex_color="#444444"))
            self.ui.actionDark.triggered.connect(lambda : self.ctrl_layer.canvas.set_canvas_bgcolor(hex_color="#444444"))
            self.ui.actionDark.triggered.connect(lambda : self.vis_align_layer.canvas.set_canvas_bgcolor(hex_color="#444444"))
            self.ui.actionLight.triggered.connect(lambda : self.vis_layer.canvas.set_canvas_bgcolor(hex_color="#FFFFFF"))
            self.ui.actionLight.triggered.connect(lambda: self.ctrl_layer.canvas.set_canvas_bgcolor(hex_color="#FFFFFF"))
            self.ui.actionLight.triggered.connect(lambda: self.vis_align_layer.canvas.set_canvas_bgcolor(hex_color="#FFFFFF"))
