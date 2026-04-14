import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock


class TestUiAboutConstants:
    def test_init(self):
        mock_main_win = MagicMock()
        mock_app_settings = MagicMock()
        mock_app_settings.app_version = "1.0.0"
        from TheAntFarm.ui_manager.ui_about import UiAbout
        ui_about = UiAbout(mock_main_win, mock_app_settings)
        assert ui_about.main_win == mock_main_win
        assert ui_about.app_settings == mock_app_settings