import os

import pytest

from TheAntFarm.settings_manager.settings_machine import MachineSettingsHandler


class TestMachineSettingsHandler:
    @pytest.fixture
    def mock_main_window(self, mocker):
        """Fixture for mocked main window"""
        mock_main_win = mocker.Mock()
        return mock_main_win

    @pytest.fixture
    def config_folder(self, tmp_path):
        """Fixture providing a valid config folder"""
        folder = tmp_path / "configurations"
        folder.mkdir()
        return str(folder)

    @pytest.fixture
    def machine_settings(self, config_folder, mock_main_window):
        """Fixture providing MachineSettingsHandler"""
        return MachineSettingsHandler(config_folder, mock_main_window)

    def test_init(self, config_folder, mock_main_window):
        """Test initialization with default values"""
        handler = MachineSettingsHandler(config_folder, mock_main_window)

        assert handler.machine_config_path == os.path.normpath(
            os.path.join(config_folder, "machine_config.ini")
        )
        assert handler.main_win == mock_main_window
        assert handler.probe_z_min == -11.0
        assert handler.probe_z_max == 1.0
        assert handler.xy_step_idx == 3
        assert handler.xy_step_value == 1.0
        assert handler.z_step_idx == 3
        assert handler.z_step_value == 0.1
        assert handler.feedrate_xy == 300.0
        assert handler.feedrate_z == 40.0
        assert handler.feedrate_probe == 40.0

    def test_read_all_machine_settings_creates_default(self, machine_settings):
        """Test that read creates default config if file doesn't exist"""
        machine_settings.read_all_machine_settings()

        assert os.path.exists(machine_settings.machine_config_path)
        assert machine_settings.probe_z_min == -11.0
        assert machine_settings.probe_z_max == 1.0
        assert machine_settings.xy_step_idx == 3

    def test_read_all_machine_settings_with_existing_file(self, machine_settings, config_folder):
        """Test reading existing config"""
        import configparser

        config = configparser.ConfigParser()
        config["GENERAL"] = {
            "probe_z_min": "-15.0",
            "probe_z_max": "2.0",
            "x_bbox_step": "5",
            "y_bbox_step": "2",
            "xy_step_idx": "5",
            "xy_step_value": "2.5",
            "z_step_idx": "2",
            "z_step_value": "0.05",
            "feedrate_xy": "500.0",
            "feedrate_z": "60.0",
            "feedrate_probe": "50.0",
            "tool_probe_relative_flag": "True",
            "hold_on_probe_flag": "True",
            "zeroing_after_probe_flag": "True",
            "tool_probe_x_mpos": "10.0",
            "tool_probe_y_mpos": "20.0",
            "tool_probe_z_mpos": "5.0",
            "tool_probe_x_wpos": "1.0",
            "tool_probe_y_wpos": "2.0",
            "tool_probe_z_wpos": "0.5",
            "tool_change_x_mpos": "50.0",
            "tool_change_y_mpos": "50.0",
            "tool_change_z_mpos": "10.0",
            "tool_probe_z_limit": "-15.0",
            "alignment_drill_diameter": "3.0",
            "tool_camera_offset_x": "5.0",
            "tool_camera_offset_y": "10.0",
        }

        with open(machine_settings.machine_config_path, "w") as f:
            config.write(f)

        machine_settings.read_all_machine_settings()

        assert machine_settings.probe_z_min == -15.0
        assert machine_settings.probe_z_max == 2.0
        assert machine_settings.x_bbox_step == 5
        assert machine_settings.y_bbox_step == 2
        assert machine_settings.xy_step_idx == 5
        assert machine_settings.xy_step_value == 2.5
        assert machine_settings.z_step_idx == 2
        assert machine_settings.z_step_value == 0.05
        assert machine_settings.feedrate_xy == 500.0
        assert machine_settings.feedrate_z == 60.0
        assert machine_settings.feedrate_probe == 50.0
        assert machine_settings.tool_probe_rel_flag is True
        assert machine_settings.hold_on_probe_flag is True
        assert machine_settings.zeroing_after_probe_flag is True
        assert machine_settings.tool_probe_offset_x_mpos == 10.0
        assert machine_settings.tool_probe_offset_y_mpos == 20.0
        assert machine_settings.tool_probe_offset_z_mpos == 5.0
        assert machine_settings.tool_probe_offset_x_wpos == 1.0
        assert machine_settings.tool_change_offset_x_mpos == 50.0
        assert machine_settings.tool_change_offset_z_mpos == 10.0
        assert machine_settings.tool_probe_z_limit == -15.0
        assert machine_settings.alignment_drill_diameter == 3.0
        assert machine_settings.tool_camera_offset_x == 5.0
        assert machine_settings.tool_camera_offset_y == 10.0

    def test_write_all_machine_settings(self, machine_settings, config_folder):
        """Test writing machine settings"""
        machine_settings.probe_z_min = -20.0
        machine_settings.probe_z_max = 5.0
        machine_settings.x_bbox_step = 10
        machine_settings.xy_step_idx = 4
        machine_settings.feedrate_xy = 600.0
        machine_settings.tool_probe_rel_flag = True
        machine_settings.hold_on_probe_flag = True
        machine_settings.tool_probe_offset_x_mpos = 15.0
        machine_settings.tool_change_offset_x_mpos = 100.0
        machine_settings.tool_probe_z_limit = -20.0
        machine_settings.alignment_drill_diameter = 2.5
        machine_settings.tool_camera_offset_x = 3.5

        machine_settings.write_all_machine_settings()

        new_handler = MachineSettingsHandler(config_folder, machine_settings.main_win)
        new_handler.read_all_machine_settings()

        assert new_handler.probe_z_min == -20.0
        assert new_handler.probe_z_max == 5.0
        assert new_handler.x_bbox_step == 10
        assert new_handler.xy_step_idx == 4
        assert new_handler.feedrate_xy == 600.0
        assert new_handler.tool_probe_rel_flag is True
        assert new_handler.hold_on_probe_flag is True
        assert new_handler.tool_probe_offset_x_mpos == 15.0
        assert new_handler.tool_change_offset_x_mpos == 100.0
        assert new_handler.tool_probe_z_limit == -20.0
        assert new_handler.alignment_drill_diameter == 2.5
        assert new_handler.tool_camera_offset_x == 3.5

    def test_restore_machine_settings(self, machine_settings, config_folder):
        """Test restoring default settings"""
        machine_settings.probe_z_min = -99.0
        machine_settings.probe_z_max = 99.0
        machine_settings.tool_probe_rel_flag = True

        machine_settings.restore_machine_settings()

        new_handler = MachineSettingsHandler(config_folder, machine_settings.main_win)
        new_handler.read_all_machine_settings()

        assert new_handler.probe_z_min == -11.0
        assert new_handler.probe_z_max == 1.0
        assert new_handler.tool_probe_rel_flag is False

    def test_read_missing_general_section(self, machine_settings, config_folder):
        """Test reading config with missing GENERAL section"""
        import configparser

        config = configparser.ConfigParser()
        config["OTHER"] = {"some_key": "some_value"}

        with open(machine_settings.machine_config_path, "w") as f:
            config.write(f)

        machine_settings.read_all_machine_settings()

        assert machine_settings.probe_z_min == -11.0
        assert machine_settings.feedrate_xy == 300.0
        assert machine_settings.tool_probe_rel_flag is False

    def test_default_values_probe(self, machine_settings):
        """Test default values for probe settings"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.probe_z_min == -11.0
        assert machine_settings.probe_z_max == 1.0
        assert machine_settings.x_bbox_step == 1
        assert machine_settings.y_bbox_step == 1
        assert machine_settings.xy_step_idx == 3
        assert machine_settings.xy_step_value == 1.0
        assert machine_settings.z_step_idx == 3
        assert machine_settings.z_step_value == 0.1

    def test_default_values_feedrates(self, machine_settings):
        """Test default values for feedrate settings"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.feedrate_xy == 300.0
        assert machine_settings.feedrate_z == 40.0
        assert machine_settings.feedrate_probe == 40.0

    def test_default_values_tool_probe_mpos(self, machine_settings):
        """Test default values for tool probe mpos settings"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.tool_probe_offset_x_mpos == 0.0
        assert machine_settings.tool_probe_offset_y_mpos == 0.0
        assert machine_settings.tool_probe_offset_z_mpos == 0.0

    def test_default_values_tool_probe_wpos(self, machine_settings):
        """Test default values for tool probe wpos settings"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.tool_probe_offset_x_wpos == 0.0
        assert machine_settings.tool_probe_offset_y_wpos == 0.0
        assert machine_settings.tool_probe_offset_z_wpos == 0.0

    def test_default_values_tool_change(self, machine_settings):
        """Test default values for tool change settings"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.tool_change_offset_x_mpos == 0.0
        assert machine_settings.tool_change_offset_y_mpos == 0.0
        assert machine_settings.tool_change_offset_z_mpos == 0.0

    def test_default_values_probe_flags(self, machine_settings):
        """Test default values for probe flags"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.tool_probe_rel_flag is False
        assert machine_settings.hold_on_probe_flag is False
        assert machine_settings.zeroing_after_probe_flag is False
        assert machine_settings.tool_probe_z_limit == -11.0

    def test_default_values_alignment_drill(self, machine_settings):
        """Test default values for alignment/drill settings"""
        machine_settings.read_all_machine_settings()

        assert machine_settings.alignment_drill_diameter == 0.0
        assert machine_settings.tool_camera_offset_x == 0.0
        assert machine_settings.tool_camera_offset_y == 0.0