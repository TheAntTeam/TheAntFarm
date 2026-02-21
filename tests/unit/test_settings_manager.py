import pytest
import os
from TheAntFarm.settings_manager.settings_app import AppSettingsHandler


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
        assert new_settings.align_tab_visibility is True
        assert new_settings.settings_tab_visibility is True
        assert new_settings.flip_horizontal_selected is True

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
        assert app_settings_handler.serial_error_warning_threshold == \
            app_settings_handler.SERIAL_ERROR_WARNING_THRESHOLD_DEFAULT
        assert app_settings_handler.serial_error_critical_threshold == \
            app_settings_handler.SERIAL_ERROR_CRITICAL_THRESHOLD_DEFAULT
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

    def test_serial_error_threshold_validation_zero_values(self, app_settings_handler, tmp_path):
        """Test that zero thresholds are accepted - valid edge case for closing on first error"""
        # Set up test config directory
        config_dir = tmp_path / "test_zero_thresholds" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Manually write config with zero values (now valid)
        import configparser
        config = configparser.ConfigParser()
        config["GENERAL"] = {
            "serial_error_warning_threshold": "0",
            "serial_error_critical_threshold": "0"
        }
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(str(config_dir / "app_config.ini"), "w") as f:
            config.write(f)

        # Load settings - should accept (0, 0) as valid
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify thresholds are (0, 0)
        assert new_settings.serial_error_warning_threshold == 0
        assert new_settings.serial_error_critical_threshold == 0

    def test_serial_error_threshold_validation_negative_values(self, app_settings_handler, tmp_path):
        """Test that negative thresholds are rejected and reset to defaults"""
        # Set up test config directory
        config_dir = tmp_path / "test_negative_thresholds" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Manually write invalid config with negative values
        import configparser
        config = configparser.ConfigParser()
        config["GENERAL"] = {
            "serial_error_warning_threshold": "-5",
            "serial_error_critical_threshold": "-10"
        }
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(str(config_dir / "app_config.ini"), "w") as f:
            config.write(f)

        # Load settings - should validate and reset to defaults
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify thresholds were reset to defaults
        assert new_settings.serial_error_warning_threshold == new_settings.SERIAL_ERROR_WARNING_THRESHOLD_DEFAULT
        assert new_settings.serial_error_critical_threshold == new_settings.SERIAL_ERROR_CRITICAL_THRESHOLD_DEFAULT

    def test_serial_error_threshold_validation_invalid_order(self, app_settings_handler, tmp_path):
        """Test that invalid threshold order (warning > critical) is rejected and reset to defaults"""
        # Set up test config directory
        config_dir = tmp_path / "test_invalid_order_thresholds" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Manually write invalid config with warning > critical
        import configparser
        config = configparser.ConfigParser()
        config["GENERAL"] = {
            "serial_error_warning_threshold": "10",
            "serial_error_critical_threshold": "5"
        }
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(str(config_dir / "app_config.ini"), "w") as f:
            config.write(f)

        # Load settings - should validate and reset to defaults
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify thresholds were reset to defaults
        assert new_settings.serial_error_warning_threshold == new_settings.SERIAL_ERROR_WARNING_THRESHOLD_DEFAULT
        assert new_settings.serial_error_critical_threshold == new_settings.SERIAL_ERROR_CRITICAL_THRESHOLD_DEFAULT

    def test_serial_error_threshold_equal_non_zero_values(self, app_settings_handler, tmp_path):
        """Test that equal non-zero thresholds (5, 5) are allowed - skip warning phase"""
        # Set up test config directory
        config_dir = tmp_path / "test_equal_non_zero_thresholds" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Manually write config with equal non-zero values
        import configparser
        config = configparser.ConfigParser()
        config["GENERAL"] = {
            "serial_error_warning_threshold": "5",
            "serial_error_critical_threshold": "5"
        }
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(str(config_dir / "app_config.ini"), "w") as f:
            config.write(f)

        # Load settings - should accept (5, 5) as valid
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify thresholds are (5, 5)
        assert new_settings.serial_error_warning_threshold == 5
        assert new_settings.serial_error_critical_threshold == 5

    def test_serial_error_threshold_valid_with_zero_warning(self, app_settings_handler, tmp_path):
        """Test that (0, 10) is valid - log warning on first error, close on 10th"""
        # Set up test config directory
        config_dir = tmp_path / "test_zero_warning_threshold" / "configurations"
        config_dir.mkdir(parents=True)
        app_settings_handler.app_config_path = str(config_dir / "app_config.ini")

        # Manually write config with (0, 10)
        import configparser
        config = configparser.ConfigParser()
        config["GENERAL"] = {
            "serial_error_warning_threshold": "0",
            "serial_error_critical_threshold": "10"
        }
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(str(config_dir / "app_config.ini"), "w") as f:
            config.write(f)

        # Load settings - should accept (0, 10) as valid
        new_settings = AppSettingsHandler(str(config_dir), app_settings_handler.main_win)
        new_settings.read_all_app_settings()

        # Verify thresholds are (0, 10)
        assert new_settings.serial_error_warning_threshold == 0
        assert new_settings.serial_error_critical_threshold == 10
