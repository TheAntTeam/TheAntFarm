from unittest.mock import MagicMock, patch


class TestUiManagerConstants:
    def test_l_tags(self):
        from TheAntFarm.ui_manager.ui_manager import UiManager

        assert UiManager.L_TAGS == ("top", "bottom", "profile", "drill", "nc_top", "nc_bottom")

    def test_l_names(self):
        from TheAntFarm.ui_manager.ui_manager import UiManager

        assert UiManager.L_NAMES == ("TOP", "BOTTOM", "PROFILE", "DRILL", "NO COPPER TOP", "NO COPPER BOTTOM")

    def test_log_colors(self):
        from TheAntFarm.ui_manager.ui_manager import UiManager

        assert UiManager.LOG_COLORS[10] == "white"
        assert UiManager.LOG_COLORS[20] == "light blue"
        assert UiManager.LOG_COLORS[30] == "orange"
        assert UiManager.LOG_COLORS[40] == "red"
        assert UiManager.LOG_COLORS[50] == "purple"


class TestHideShowConsole:
    def test_hide_show_console_checked(self):
        mock_ui = MagicMock()
        mock_ui.actionHide_Show_Console.isChecked.return_value = True
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.hide_show_console()
        mock_ui.logging_plain_te.show.assert_called_once()

    def test_hide_show_console_not_checked(self):
        mock_ui = MagicMock()
        mock_ui.actionHide_Show_Console.isChecked.return_value = False
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.hide_show_console()
        mock_ui.logging_plain_te.hide.assert_called_once()


class TestHideShowAlignTab:
    def test_hide_show_align_tab_visible(self):
        mock_ui = MagicMock()
        mock_ui.actionHide_Show_Align_Tab.isChecked.return_value = True
        mock_ui.main_tab_widget.indexOf.return_value = 2
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.hide_show_align_tab()
        mock_ui.main_tab_widget.setTabVisible.assert_called_with(2, True)

    def test_hide_show_align_tab_hidden(self):
        mock_ui = MagicMock()
        mock_ui.actionHide_Show_Align_Tab.isChecked.return_value = False
        mock_ui.main_tab_widget.indexOf.return_value = 2
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.hide_show_align_tab()
        mock_ui.main_tab_widget.setTabVisible.assert_called_with(2, False)


class TestHideShowPreferencesTab:
    def test_hide_show_preferences_visible(self):
        mock_ui = MagicMock()
        mock_ui.actionSettings_Preferences.isChecked.return_value = True
        mock_ui.main_tab_widget.indexOf.return_value = 3
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.hide_show_preferences_tab()
        mock_ui.main_tab_widget.setTabVisible.assert_called_with(3, True)

    def test_hide_show_preferences_hidden(self):
        mock_ui = MagicMock()
        mock_ui.actionSettings_Preferences.isChecked.return_value = False
        mock_ui.main_tab_widget.indexOf.return_value = 3
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.hide_show_preferences_tab()
        mock_ui.main_tab_widget.setTabVisible.assert_called_with(3, False)


class TestOnMainTabChanged:
    """Test UiManager._on_main_tab_changed with unsaved settings."""

    def setup_ui_manager(self, settings_tab_index=2, previous_index=0, dirty=True):
        mock_ui = MagicMock()
        mock_ui.main_tab_widget.indexOf.return_value = settings_tab_index
        mock_ui.settings_tab = MagicMock()

        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = mock_ui
        ui_manager.main_win = MagicMock()
        ui_manager.main_win.ui = mock_ui
        ui_manager._previous_main_tab_index = previous_index
        ui_manager._settings_switch_in_progress = False
        ui_manager.ui_settings_tab_m = MagicMock()
        ui_manager.ui_settings_tab_m.has_unsaved_changes.return_value = dirty

        return ui_manager, mock_ui

    @patch("TheAntFarm.ui_manager.ui_manager.QMessageBox")
    def test_no_dialog_when_not_leaving_settings(self, mock_msgbox):
        ui_manager, mock_ui = self.setup_ui_manager(settings_tab_index=2, previous_index=0, dirty=True)
        ui_manager._on_main_tab_changed(1)

        mock_msgbox.assert_not_called()
        assert ui_manager._previous_main_tab_index == 1

    @patch("TheAntFarm.ui_manager.ui_manager.QMessageBox")
    def test_no_dialog_when_clean(self, mock_msgbox):
        ui_manager, mock_ui = self.setup_ui_manager(settings_tab_index=2, previous_index=2, dirty=False)
        ui_manager._on_main_tab_changed(1)

        mock_msgbox.assert_not_called()
        assert ui_manager._previous_main_tab_index == 1

    @patch("TheAntFarm.ui_manager.ui_manager.QMessageBox")
    def test_save_saves_and_switches(self, mock_msgbox):
        ui_manager, mock_ui = self.setup_ui_manager(settings_tab_index=2, previous_index=2, dirty=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = save_btn

        ui_manager._on_main_tab_changed(1)

        ui_manager.ui_settings_tab_m.save_settings_preferences.assert_called_once()
        ui_manager.ui_settings_tab_m.restore_initial_settings.assert_not_called()
        assert ui_manager._previous_main_tab_index == 1

    @patch("TheAntFarm.ui_manager.ui_manager.QMessageBox")
    def test_discard_restores_and_switches(self, mock_msgbox):
        ui_manager, mock_ui = self.setup_ui_manager(settings_tab_index=2, previous_index=2, dirty=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = discard_btn

        ui_manager._on_main_tab_changed(1)

        ui_manager.ui_settings_tab_m.restore_initial_settings.assert_called_once()
        ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        assert ui_manager._previous_main_tab_index == 1

    @patch("TheAntFarm.ui_manager.ui_manager.QMessageBox")
    def test_cancel_stays(self, mock_msgbox):
        ui_manager, mock_ui = self.setup_ui_manager(settings_tab_index=2, previous_index=2, dirty=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = cancel_btn

        ui_manager._on_main_tab_changed(1)

        mock_ui.main_tab_widget.setCurrentIndex.assert_called_once_with(2)
        assert ui_manager._previous_main_tab_index == 2


class TestStyleActions:
    """Dark and Light are exclusive and also set the background of the three canvases."""

    @staticmethod
    def _ui_manager(style_manager):
        from TheAntFarm.ui_manager.ui_manager import UiManager

        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = MagicMock()
        ui_manager.main_win = MagicMock()
        ui_manager.style_manager = style_manager
        ui_manager.vis_layer = MagicMock()
        ui_manager.ctrl_layer = MagicMock()
        ui_manager.vis_align_layer = MagicMock()
        return ui_manager

    @staticmethod
    def _trigger(action):
        for call in action.triggered.connect.call_args_list:
            call.args[0]()

    def _canvases(self, ui_manager):
        return [layer.canvas for layer in (ui_manager.vis_layer, ui_manager.ctrl_layer, ui_manager.vis_align_layer)]

    @patch("TheAntFarm.ui_manager.ui_manager.QActionGroup")
    def test_dark_sets_the_dark_background_on_every_canvas(self, mock_group):
        ui_manager = self._ui_manager(MagicMock())

        ui_manager.make_style_action_mutually_exclusive()
        self._trigger(ui_manager.ui.actionDark)

        for canvas in self._canvases(ui_manager):
            canvas.set_canvas_bgcolor.assert_called_once_with(hex_color="#444444")

    @patch("TheAntFarm.ui_manager.ui_manager.QActionGroup")
    def test_light_sets_the_light_background_on_every_canvas(self, mock_group):
        ui_manager = self._ui_manager(MagicMock())

        ui_manager.make_style_action_mutually_exclusive()
        self._trigger(ui_manager.ui.actionLight)

        for canvas in self._canvases(ui_manager):
            canvas.set_canvas_bgcolor.assert_called_once_with(hex_color="#FFFFFF")

    @patch("TheAntFarm.ui_manager.ui_manager.QActionGroup")
    def test_actions_are_exclusive_and_given_to_the_style_manager(self, mock_group):
        style_manager = MagicMock()
        ui_manager = self._ui_manager(style_manager)

        ui_manager.make_style_action_mutually_exclusive()

        mock_group.return_value.setExclusive.assert_called_once_with(True)
        style_manager.connect_palette_actions.assert_called_once_with(
            ui_manager.ui.actionDark, ui_manager.ui.actionLight
        )

    @patch("TheAntFarm.ui_manager.ui_manager.QActionGroup")
    def test_without_style_manager_nothing_is_connected(self, mock_group):
        ui_manager = self._ui_manager(None)

        ui_manager.make_style_action_mutually_exclusive()

        ui_manager.ui.actionDark.triggered.connect.assert_not_called()
        ui_manager.ui.actionLight.triggered.connect.assert_not_called()
