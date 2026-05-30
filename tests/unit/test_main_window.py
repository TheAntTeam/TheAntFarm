from unittest.mock import MagicMock, patch


class TestCloseEvent:
    """Test MainWindow.closeEvent with unsaved settings changes dialog."""

    def setup_main_window(self, has_unsaved=True):
        from TheAntFarm.the_ant_farm import MainWindow

        main_window = MainWindow.__new__(MainWindow)
        main_window.ui_manager = MagicMock()
        main_window.ui = MagicMock()
        main_window.serialWo = MagicMock()
        main_window.serial_thread = MagicMock()
        main_window.control_thread = MagicMock()

        main_window.ui_manager.ui_settings_tab_m.has_unsaved_changes.return_value = has_unsaved

        mock_event = MagicMock()

        return main_window, mock_event

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_clean_no_dialog(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=False)

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        mock_msgbox.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_called_once()
        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        main_window.serialWo.close_port.assert_called_once()
        mock_event.ignore.assert_not_called()

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_save_saves_and_closes(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = save_btn

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_called_once()
        main_window.ui_manager.save_all_settings.assert_not_called()
        main_window.serialWo.close_port.assert_called_once()
        mock_event.ignore.assert_not_called()

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_discard_closes(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = discard_btn

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_called_once()
        main_window.serialWo.close_port.assert_called_once()
        mock_event.ignore.assert_not_called()

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_cancel_ignores(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = cancel_btn

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_not_called()
        mock_event.ignore.assert_called_once()
