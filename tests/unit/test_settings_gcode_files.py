import os

import pytest

from TheAntFarm.settings_manager.settings_gcode_files import GCodeFilesSettingsHandler


class TestGCodeFilesSettingsHandler:
    @pytest.fixture
    def config_folder(self, tmp_path):
        """Fixture providing a valid config folder"""
        folder = tmp_path / "configurations"
        folder.mkdir()
        return str(folder)

    @pytest.fixture
    def invalid_config_folder(self, tmp_path):
        """Fixture providing an invalid config folder path"""
        return str(tmp_path / "nonexistent" / "configurations")

    def test_init_valid_config_folder(self, config_folder):
        """Test initialization with valid config folder"""
        handler = GCodeFilesSettingsHandler(config_folder)
        assert handler.gcf_config_path == os.path.normpath(
            os.path.join(config_folder, "gcode_files_config.ini")
        )
        expected_folder = os.path.join(os.path.dirname(config_folder), "gcode_temp_dir")
        assert handler.gcode_folder_default == expected_folder

    def test_init_invalid_config_folder(self, invalid_config_folder):
        """Test initialization with invalid config folder falls back to script directory"""
        from TheAntFarm.settings_manager.settings_gcode_files import GCodeFilesSettingsHandler
        handler = GCodeFilesSettingsHandler(invalid_config_folder)

        import TheAntFarm.settings_manager.settings_gcode_files as gcf_module
        module_file = gcf_module.__file__
        script_dir = os.path.dirname(os.path.dirname(module_file))
        fallback_folder = os.path.join(script_dir, "..", "configurations")
        expected_folder = os.path.join(fallback_folder, "gcode_temp_dir")
        assert handler.gcode_folder_default == expected_folder

    def test_read_all_gcf_settings_creates_default(self, config_folder):
        """Test that read creates default config if file doesn't exist"""
        handler = GCodeFilesSettingsHandler(config_folder)
        handler.read_all_gcf_settings()

        assert os.path.exists(handler.gcf_config_path)
        expected_folder = os.path.join(os.path.dirname(config_folder), "gcode_temp_dir")
        assert handler.gcode_folder == expected_folder
        assert os.path.isdir(handler.gcode_folder)

    def test_read_all_gcf_settings_loads_existing(self, config_folder, tmp_path):
        """Test reading existing config"""
        handler = GCodeFilesSettingsHandler(config_folder)

        custom_folder = tmp_path / "custom_gcode"
        custom_folder.mkdir()
        handler.gcode_folder = str(custom_folder)
        handler.write_all_gcf_settings()

        new_handler = GCodeFilesSettingsHandler(config_folder)
        new_handler.read_all_gcf_settings()

        assert new_handler.gcode_folder == str(custom_folder)

    def test_write_all_gcf_settings(self, config_folder):
        """Test writing gcode settings to file"""
        handler = GCodeFilesSettingsHandler(config_folder)
        handler.gcode_folder = "/test/gcode/output"
        handler.write_all_gcf_settings()

        assert os.path.exists(handler.gcf_config_path)

        import configparser
        config = configparser.ConfigParser()
        config.read(handler.gcf_config_path)

        assert config["FILES"]["gcode_folder"] == "/test/gcode/output"

    def test_restore_all_gcf_settings(self, config_folder):
        """Test restoring default settings"""
        handler = GCodeFilesSettingsHandler(config_folder)

        handler.gcode_folder = "/modified/folder"
        handler.restore_all_gcf_settings()

        expected_folder = os.path.join(os.path.dirname(config_folder), "gcode_temp_dir")

        import configparser
        config = configparser.ConfigParser()
        config.read(handler.gcf_config_path)

        assert config["FILES"]["gcode_folder"] == expected_folder

    def test_gcode_folder_created_if_not_exists(self, config_folder):
        """Test that gcode folder is created if it doesn't exist"""
        handler = GCodeFilesSettingsHandler(config_folder)
        handler.gcode_folder = os.path.join(config_folder, "new_gcode_folder")

        handler.read_all_gcf_settings()

        assert os.path.isdir(handler.gcode_folder)

    def test_gcode_folder_from_config(self, config_folder, tmp_path):
        """Test that gcode_folder is read from config file"""
        handler = GCodeFilesSettingsHandler(config_folder)

        import configparser
        config = configparser.ConfigParser()
        user_folder = tmp_path / "user_specified_folder"
        user_folder.mkdir()
        config["FILES"] = {"gcode_folder": str(user_folder)}
        with open(handler.gcf_config_path, "w") as f:
            config.write(f)

        handler.read_all_gcf_settings()

        assert handler.gcode_folder == str(user_folder)