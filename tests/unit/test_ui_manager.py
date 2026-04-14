import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock


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