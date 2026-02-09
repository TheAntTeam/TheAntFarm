import pytest
import os
from TheAntFarm.settings_manager.settings_app import AppSettingsHandler
from pathlib import Path

class TestAppSettingsHandler:
    @pytest.fixture
    def mock_main_window(self, mocker):
        """Fixture for mocked main window with all required attributes"""
        mock_main_win = mocker.Mock()

        # Mock window position and geometry
        mock_pos = mocker.Mock()
        mock_pos.x.return_value = 200
        mock_pos.y.return_value = 200
        mock_main_win.pos.return_value = mock_pos

        mock_geo = mocker.Mock()
        mock_geo.width.return_value = 1160
        mock_geo.height.return_value = 720
        mock_main_win.normalGeometry.return_value = mock_geo
        mock_main_win.isMaximized.return_value = False

        # Mock UI elements
        mock_ui = mocker.Mock()
        mock_ui.main_tab_widget.currentIndex.return_value = 0
        mock_ui.ctrl_tab_widget.currentIndex.return_value = 0
        mock_ui.settings_sub_tab.currentIndex.return_value = 0
        mock_ui.jog_probe_tab_widget.currentIndex.return_value = 0
        mock_ui.actionHide_Show_Align_Tab.isChecked.return_value = False
        mock_ui.actionSettings_Preferences.isChecked.return_value = False
        mock_ui.actionHide_Show_Console.isChecked.return_value = False
        mock_ui.serial_ports_cb.currentText.return_value = ""
        mock_ui.serial_baud_cb.currentText.return_value = "115200"
        mock_ui.flip_horizontally_tb.isChecked.return_value = False
        mock_ui.flip_vertically_tb.isChecked.return_value = False
        mock_main_win.ui = mock_ui

        return mock_main_win

    @pytest.fixture
    def app_settings_handler(self, mock_main_window, tmp_path):
        """Fixture providing AppSettingsHandler with isolated test config"""
        # Create a temporary config directory for this test
        config_folder = tmp_path / "configurations"
        config_folder.mkdir()

        # Set local path to the temporary directory
        mock_main_window.local_path = str(tmp_path)

        return AppSettingsHandler(str(config_folder), mock_main_window)

    def test_load_config(self, app_settings_handler):
        """Test loading configuration file"""
        # Ensure default values are set when no config exists
        app_settings_handler.read_all_app_settings()
        assert app_settings_handler.win_maximized == app_settings_handler.WIN_MAXIMIZED_DEFAULT
        assert app_settings_handler.main_tab_index == app_settings_handler.MAIN_TAB_INDEX_DEFAULT

    def test_save_config(self, app_settings_handler, tmp_path):
        """Test saving configuration file"""
        # Create a test config file
        config_dir = tmp_path / "test_save" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # First save default settings
        app_settings_handler.restore_app_settings()

        # Modify default settings through main window mock
        app_settings_handler.main_win.ui.actionHide_Show_Align_Tab.isChecked.return_value = True
        app_settings_handler.main_win.ui.actionSettings_Preferences.isChecked.return_value = True
        app_settings_handler.main_win.ui.flip_horizontally_tb.isChecked.return_value = True

        # Write settings
        app_settings_handler.write_all_app_settings()

        # Create a new instance with the same config path
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify settings were saved and read back correctly
        assert new_settings.align_tab_visibility == True
        assert new_settings.settings_tab_visibility == True
        assert new_settings.flip_horizontal_selected == True

    def test_invalid_config(self, mock_main_window, tmp_path):
        """Test loading invalid configuration"""
        # Set up test directories
        test_root = tmp_path / "test_invalid"
        test_root.mkdir()
        mock_main_window.local_path = str(test_root)  # Set local path to our test directory

        # Create new instance with non-existent config path
        test_config_dir = test_root / "configurations"
        new_settings = AppSettingsHandler(str(test_config_dir), mock_main_window)

        # Before reading settings, directory should not exist
        assert not os.path.exists(test_config_dir)

        # Reading settings should create directory and default config
        new_settings.read_all_app_settings()

        # Verify directory and config file were created
        assert os.path.exists(test_config_dir)
        assert os.path.exists(os.path.join(test_config_dir, "app_config.ini"))

    def test_update_settings(self, app_settings_handler):
        """Test updating settings values"""
        # Test updating individual settings
        test_values = {
            'win_maximized': True,
            'main_tab_index': 2,
            'ctrl_tab_index': 1,
            'settings_tab_index': 3,
            'align_tab_visibility': True,
            'console_visibility': True
        }

        # Update settings
        for attr, value in test_values.items():
            setattr(app_settings_handler, attr, value)

        # Verify updates
        for attr, value in test_values.items():
            assert getattr(app_settings_handler, attr) == value

    def test_serial_error_threshold_defaults(self, app_settings_handler):
        """Test that serial error thresholds are initialized with default values"""
        assert app_settings_handler.serial_error_warning_threshold == app_settings_handler.SERIAL_ERROR_WARNING_THRESHOLD_DEFAULT
        assert app_settings_handler.serial_error_critical_threshold == app_settings_handler.SERIAL_ERROR_CRITICAL_THRESHOLD_DEFAULT
        assert app_settings_handler.serial_error_warning_threshold == 3
        assert app_settings_handler.serial_error_critical_threshold == 10

    def test_serial_error_threshold_save_and_load(self, app_settings_handler, tmp_path):
        """Test saving and loading serial error thresholds"""
        # Set up test config directory
        config_dir = tmp_path / "test_thresholds" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Modify thresholds
        app_settings_handler.serial_error_warning_threshold = 5
        app_settings_handler.serial_error_critical_threshold = 15

        # Save settings
        app_settings_handler.write_all_app_settings()

        # Create new instance and load settings
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify modified thresholds were saved and loaded
        assert new_settings.serial_error_warning_threshold == 5
        assert new_settings.serial_error_critical_threshold == 15

    def test_serial_error_threshold_restore_defaults(self, app_settings_handler, tmp_path):
        """Test restoring default serial error thresholds"""
        # Set up test config directory
        config_dir = tmp_path / "test_restore_thresholds" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Modify thresholds
        app_settings_handler.serial_error_warning_threshold = 7
        app_settings_handler.serial_error_critical_threshold = 20

        # Save modified settings
        app_settings_handler.write_all_app_settings()

        # Restore defaults
        app_settings_handler.restore_app_settings()

        # Create new instance and load restored settings
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify thresholds are restored to defaults
        assert new_settings.serial_error_warning_threshold == app_settings_handler.SERIAL_ERROR_WARNING_THRESHOLD_DEFAULT
        assert new_settings.serial_error_critical_threshold == app_settings_handler.SERIAL_ERROR_CRITICAL_THRESHOLD_DEFAULT
