import os

import pytest


class TestSettingsHandler:
    @pytest.fixture
    def mock_main_window(self, mocker):
        """Fixture for mocked main window"""
        mock_main_win = mocker.Mock()
        mock_main_win.local_path = ""
        mock_main_win.pos.return_value.x.return_value = 100
        mock_main_win.pos.return_value.y.return_value = 100
        mock_main_win.normalGeometry.return_value.width.return_value = 800
        mock_main_win.normalGeometry.return_value.height.return_value = 600
        mock_main_win.isMaximized.return_value = False
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
        mock_main_win.ui = mock_ui
        return mock_main_win

    def test_init_default_config_folder(self, mock_main_window):
        """Test initialization with default config folder when local_path is empty"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        import TheAntFarm.settings_manager.settings_manager as sm_module
        mock_main_window.local_path = ""
        
        handler = SettingsHandler(mock_main_window)
        
        expected = os.path.normpath(os.path.join(os.path.dirname(sm_module.__file__), "..", "configurations"))
        assert handler.config_folder == expected

    def test_init_custom_config_folder(self, mock_main_window, tmp_path):
        """Test initialization with custom config folder from local_path"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        
        handler = SettingsHandler(mock_main_window)
        
        expected = os.path.join(str(tmp_path), "configurations")
        assert handler.config_folder == expected

    def test_init_creates_config_folder(self, mock_main_window, tmp_path):
        """Test that config folder is created if it doesn't exist"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path / "new_project")
        
        handler = SettingsHandler(mock_main_window)
        
        assert os.path.isdir(handler.config_folder)

    def test_init_sets_local_path(self, mock_main_window, tmp_path):
        """Test that local_path is set correctly"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        
        handler = SettingsHandler(mock_main_window)
        
        assert handler.local_path == str(tmp_path)

    def test_init_creates_all_settings_handlers(self, mock_main_window, tmp_path):
        """Test that all settings handlers are created"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        from TheAntFarm.settings_manager.settings_app import AppSettingsHandler
        from TheAntFarm.settings_manager.settings_job import JobSettingsHandler
        from TheAntFarm.settings_manager.settings_gcode_files import GCodeFilesSettingsHandler
        from TheAntFarm.settings_manager.settings_machine import MachineSettingsHandler
        
        mock_main_window.local_path = str(tmp_path)
        handler = SettingsHandler(mock_main_window)
        
        assert isinstance(handler.app_settings, AppSettingsHandler)
        assert isinstance(handler.jobs_settings, JobSettingsHandler)
        assert isinstance(handler.gcf_settings, GCodeFilesSettingsHandler)
        assert isinstance(handler.machine_settings, MachineSettingsHandler)

    def test_read_all_settings(self, mock_main_window, tmp_path):
        """Test that read_all_settings calls all read methods"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        handler = SettingsHandler(mock_main_window)
        
        handler.read_all_settings()
        
        assert handler.app_settings.app_config_path is not None
        assert handler.jobs_settings.jobs_config_path is not None
        assert handler.gcf_settings.gcf_config_path is not None
        assert handler.machine_settings.machine_config_path is not None

    def test_write_all_settings_default(self, mock_main_window, tmp_path):
        """Test that write_all_settings writes app, gcf and machine settings with defaults"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        handler = SettingsHandler(mock_main_window)
        
        handler.write_all_settings()
        
        assert os.path.exists(handler.app_settings.app_config_path)
        assert os.path.exists(handler.gcf_settings.gcf_config_path)
        gcf_path = os.path.join(str(tmp_path), "configurations", "gcode_files_config.ini")
        machine_path = os.path.join(str(tmp_path), "configurations", "machine_config.ini")
        assert os.path.exists(gcf_path)
        assert os.path.exists(machine_path)

    def test_write_all_settings_with_jobs(self, mock_main_window, tmp_path):
        """Test that write_all_settings writes jobs settings when provided"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        handler = SettingsHandler(mock_main_window)
        
        test_jobs_settings = {
            "common": {"mirroring_axis": "y"},
            "top": {
                "tool_diameter": 2.0,
                "passages": 2,
                "overlap": 0.5,
                "cut": -0.1,
                "travel": 2.0,
                "spindle": 1200.0,
                "xy_feedrate": 280.0,
                "z_feedrate": 45.0,
                "mirror": True,
            },
            "bottom": {
                "tool_diameter": 2.0,
                "passages": 2,
                "overlap": 0.5,
                "cut": -0.1,
                "travel": 2.0,
                "spindle": 1200.0,
                "xy_feedrate": 280.0,
                "z_feedrate": 45.0,
                "mirror": False,
            },
            "profile": {
                "tool_diameter": 1.0,
                "margin": 0.02,
                "multi_depth": True,
                "depth_per_pass": 0.05,
                "cut": -0.1,
                "passages": 1,
                "travel": 1.0,
                "spindle": 1000.0,
                "xy_feedrate": 250.0,
                "z_feedrate": 40.0,
                "taps_type": 2,
                "taps_length": 1.5,
                "mirror": False,
            },
            "drill": {
                "milling_tool": True,
                "tool_diameter": 0.8,
                "cut": -0.05,
                "travel": 1.0,
                "spindle": 800.0,
                "xy_feedrate": 200.0,
                "z_feedrate": 30.0,
                "optimize": 1,
                "mirror": False,
                "bits_names": ["bit_1", "bit_2"],
                "bits_diameter": [0.8, 1.0],
            },
            "nc_top": {
                "tool_diameter": 1.0,
                "overlap": 0.4,
                "cut": -0.07,
                "travel": 1.0,
                "spindle": 1000.0,
                "xy_feedrate": 250.0,
                "z_feedrate": 40.0,
            },
            "nc_bottom": {
                "tool_diameter": 1.0,
                "overlap": 0.4,
                "cut": -0.07,
                "travel": 1.0,
                "spindle": 1000.0,
                "xy_feedrate": 250.0,
                "z_feedrate": 40.0,
            },
        }
        
        handler.write_all_settings({"jobs_settings": test_jobs_settings})
        
        new_handler = SettingsHandler(handler.main_win)
        new_handler.read_all_settings()
        
        assert new_handler.jobs_settings.jobs_settings_od["common"]["mirroring_axis"] == "y"
        assert new_handler.jobs_settings.jobs_settings_od["top"]["tool_diameter"] == 2.0
        assert new_handler.jobs_settings.jobs_settings_od["drill"]["milling_tool"] is True

    def test_write_all_settings_empty_dict(self, mock_main_window, tmp_path):
        """Test that write_all_settings works with empty dict"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        handler = SettingsHandler(mock_main_window)
        
        handler.write_all_settings({})
        
        assert os.path.exists(handler.app_settings.app_config_path)

    def test_config_folder_uses_local_path_when_directory(self, mock_main_window, tmp_path):
        """Test that config_folder uses local_path when it's a valid directory"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        mock_main_window.local_path = str(tmp_path)
        
        handler = SettingsHandler(mock_main_window)
        
        expected = os.path.join(str(tmp_path), "configurations")
        assert handler.config_folder == expected

    def test_config_folder_fallback_to_default(self, mock_main_window):
        """Test that config_folder falls back to default when local_path is not a directory"""
        from TheAntFarm.settings_manager.settings_manager import SettingsHandler
        import TheAntFarm.settings_manager.settings_manager as sm_module
        mock_main_window.local_path = "/nonexistent/path"
        
        handler = SettingsHandler(mock_main_window)
        
        expected = os.path.normpath(os.path.join(os.path.dirname(sm_module.__file__), "..", "configurations"))
        assert handler.config_folder == expected