"""The theme is saved in the application settings and applied again at startup."""

import configparser
from unittest.mock import MagicMock, patch

import pytest

from TheAntFarm.settings_manager.settings_app import AppSettingsHandler
from TheAntFarm.ui_manager.ui_manager import UiManager


@pytest.fixture
def app_settings(tmp_path):
    config_folder = tmp_path / "configurations"
    config_folder.mkdir()
    main_window = MagicMock()
    main_window.local_path = str(tmp_path)
    for action in ("actionHide_Show_Align_Tab", "actionSettings_Preferences", "actionHide_Show_Console"):
        getattr(main_window.ui, action).isChecked.return_value = False
    main_window.ui.actionDark.isChecked.return_value = True
    return AppSettingsHandler(str(config_folder), main_window)


def saved_general(app_settings):
    config = configparser.ConfigParser()
    config.read(app_settings.app_config_path)
    return config["GENERAL"]


class TestThemeSetting:
    def test_a_new_configuration_starts_dark(self, app_settings):
        app_settings.read_all_app_settings()

        assert app_settings.dark_theme is True
        assert saved_general(app_settings)["dark_theme"] == "True"

    def test_the_saved_theme_is_read(self, app_settings):
        config = configparser.ConfigParser()
        config["GENERAL"] = {"dark_theme": "False"}
        with open(app_settings.app_config_path, "w") as config_file:
            config.write(config_file)

        app_settings.read_all_app_settings()

        assert app_settings.dark_theme is False

    @pytest.mark.parametrize("dark", [True, False])
    def test_the_checked_theme_is_written(self, app_settings, dark):
        app_settings.main_win.ui.actionDark.isChecked.return_value = dark

        app_settings.write_all_app_settings()

        assert saved_general(app_settings)["dark_theme"] == str(dark)


class TestApplyTheme:
    @staticmethod
    def _ui_manager(style_manager):
        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = MagicMock()
        ui_manager.style_manager = style_manager
        ui_manager.set_dark_canvases = MagicMock()
        return ui_manager

    def test_dark(self):
        ui_manager = self._ui_manager(MagicMock())

        ui_manager.apply_theme(True)

        ui_manager.ui.actionDark.setChecked.assert_called_once_with(True)
        ui_manager.style_manager.set_dark_palette.assert_called_once()
        ui_manager.style_manager.set_light_palette.assert_not_called()
        ui_manager.set_dark_canvases.assert_called_once_with(True)

    def test_light(self):
        ui_manager = self._ui_manager(MagicMock())

        ui_manager.apply_theme(False)

        ui_manager.ui.actionLight.setChecked.assert_called_once_with(True)
        ui_manager.style_manager.set_light_palette.assert_called_once()
        ui_manager.style_manager.set_dark_palette.assert_not_called()
        ui_manager.set_dark_canvases.assert_called_once_with(False)

    def test_without_style_manager_only_the_canvases_change(self):
        ui_manager = self._ui_manager(None)

        ui_manager.apply_theme(False)

        ui_manager.ui.actionLight.setChecked.assert_called_once_with(True)
        ui_manager.set_dark_canvases.assert_called_once_with(False)

    @patch("TheAntFarm.ui_manager.ui_manager.QActionGroup")
    def test_the_saved_theme_is_applied_with_the_window_settings(self, mock_group):
        ui_manager = UiManager.__new__(UiManager)
        ui_manager.ui = MagicMock()
        ui_manager.main_win = MagicMock()
        ui_manager.style_manager = None
        for name in ("make_style_action_mutually_exclusive", "init_tabs_visibility_status", "hide_show_console"):
            setattr(ui_manager, name, MagicMock())
        ui_manager.apply_theme = MagicMock()
        settings = MagicMock(dark_theme=False, win_maximized=False, main_tab_index=0)

        ui_manager.apply_initial_window_settings(settings)

        ui_manager.apply_theme.assert_called_once_with(False)
