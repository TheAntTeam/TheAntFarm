import os

import pytest

from TheAntFarm.settings_manager.settings_job import JobSettingsHandler


class TestJobSettingsHandler:
    @pytest.fixture
    def config_folder(self, tmp_path):
        """Fixture providing a valid config folder"""
        folder = tmp_path / "configurations"
        folder.mkdir()
        return str(folder)

    @pytest.fixture
    def job_settings(self, config_folder):
        """Fixture providing JobSettingsHandler"""
        return JobSettingsHandler(config_folder)

    def test_init(self, config_folder):
        """Test initialization"""
        handler = JobSettingsHandler(config_folder)
        assert handler.jobs_config_path == os.path.normpath(
            os.path.join(config_folder, "jobs_sets_config.ini")
        )
        assert isinstance(handler.jobs_settings, object)
        assert handler.jobs_settings_od == {}

    def test_read_all_jobs_settings_creates_default(self, job_settings):
        """Test that read creates default config if file doesn't exist"""
        job_settings.read_all_jobs_settings()

        assert os.path.exists(job_settings.jobs_config_path)
        assert "common" in job_settings.jobs_settings_od
        assert job_settings.jobs_settings_od["common"]["mirroring_axis"] == "x"

    def test_read_all_jobs_settings_with_existing_file(self, job_settings, config_folder):
        """Test reading existing config"""
        import configparser

        config = configparser.ConfigParser()
        config["COMMON"] = {"mirroring_axis": "y"}
        config["TOP"] = {
            "tool_diameter": "2.0",
            "passages": "3",
            "cut": "-0.1",
        }
        config["BOTTOM"] = {"mirror": "True"}
        config["PROFILE"] = {"margin": "0.05", "multi_depth": "True"}
        config["DRILL"] = {"milling_tool_flag": "True", "algorithm": "1"}
        config["NC_TOP"] = {"overlap": "0.5"}
        config["NC_BOTTOM"] = {"tool_diameter": "1.5"}

        with open(job_settings.jobs_config_path, "w") as f:
            config.write(f)

        job_settings.read_all_jobs_settings()

        assert job_settings.jobs_settings_od["common"]["mirroring_axis"] == "y"
        assert job_settings.jobs_settings_od["top"]["tool_diameter"] == 2.0
        assert job_settings.jobs_settings_od["top"]["passages"] == 3
        assert job_settings.jobs_settings_od["bottom"]["mirror"] is True
        assert job_settings.jobs_settings_od["profile"]["margin"] == 0.05
        assert job_settings.jobs_settings_od["profile"]["multi_depth"] is True
        assert job_settings.jobs_settings_od["drill"]["milling_tool"] is True
        assert job_settings.jobs_settings_od["drill"]["optimize"] == 1
        assert job_settings.jobs_settings_od["nc_top"]["overlap"] == 0.5
        assert job_settings.jobs_settings_od["nc_bottom"]["tool_diameter"] == 1.5

    def test_write_all_jobs_settings(self, job_settings, config_folder):
        """Test writing jobs settings"""
        test_settings = {
            "common": {"mirroring_axis": "y"},
            "top": {
                "tool_diameter": 2.5,
                "passages": 2,
                "overlap": 0.3,
                "cut": -0.15,
                "travel": 2.0,
                "spindle": 1500.0,
                "xy_feedrate": 300.0,
                "z_feedrate": 50.0,
                "mirror": True,
            },
            "bottom": {
                "tool_diameter": 2.5,
                "passages": 2,
                "overlap": 0.3,
                "cut": -0.15,
                "travel": 2.0,
                "spindle": 1500.0,
                "xy_feedrate": 300.0,
                "z_feedrate": 50.0,
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

        job_settings.write_all_jobs_settings(test_settings)

        new_handler = JobSettingsHandler(config_folder)
        new_handler.read_all_jobs_settings()

        assert new_handler.jobs_settings_od["common"]["mirroring_axis"] == "y"
        assert new_handler.jobs_settings_od["top"]["tool_diameter"] == 2.5
        assert new_handler.jobs_settings_od["top"]["passages"] == 2
        assert new_handler.jobs_settings_od["bottom"]["mirror"] is False
        assert new_handler.jobs_settings_od["profile"]["margin"] == 0.02
        assert new_handler.jobs_settings_od["profile"]["multi_depth"] is True
        assert new_handler.jobs_settings_od["drill"]["milling_tool"] is True
        assert new_handler.jobs_settings_od["drill"]["optimize"] == 1
        assert new_handler.jobs_settings_od["drill"]["bits_names"] == ["bit_1", "bit_2"]
        assert new_handler.jobs_settings_od["drill"]["bits_diameter"] == [0.8, 1.0]
        assert new_handler.jobs_settings_od["nc_top"]["overlap"] == 0.4
        assert new_handler.jobs_settings_od["nc_bottom"]["tool_diameter"] == 1.0

    def test_restore_job_settings(self, job_settings, config_folder):
        """Test restoring default settings"""
        job_settings.jobs_settings_od = {"common": {"mirroring_axis": "y"}}
        job_settings.restore_job_settings()

        import configparser

        config = configparser.ConfigParser()
        config.read(job_settings.jobs_config_path)

        assert config["COMMON"]["mirroring_axis"] == "x"
        assert config["TOP"]["tool_diameter"] == "1.0"
        assert config["TOP"]["passages"] == "1"
        assert config["BOTTOM"]["mirror"] == "True"
        assert config["PROFILE"]["margin"] == "0.01"
        assert config["DRILL"]["milling_tool_flag"] == "False"
        assert config["DRILL"]["optimize"] == "0"
        assert config["NC_TOP"]["overlap"] == "0.4"

    def test_read_missing_sections(self, job_settings, config_folder):
        """Test reading config with missing sections - missing sections use defaults"""
        import configparser

        config = configparser.ConfigParser()
        config["COMMON"] = {"mirroring_axis": "y"}
        config["TOP"] = {"tool_diameter": "2.0"}

        with open(job_settings.jobs_config_path, "w") as f:
            config.write(f)

        job_settings.read_all_jobs_settings()

        assert job_settings.jobs_settings_od["common"]["mirroring_axis"] == "y"
        assert job_settings.jobs_settings_od["top"]["tool_diameter"] == 2.0
        assert job_settings.jobs_settings_od["top"]["passages"] == 1

    def test_read_drill_bits(self, job_settings, config_folder):
        """Test reading drill bits from config"""
        import configparser

        config = configparser.ConfigParser()
        config["DRILL"] = {
            "milling_tool_flag": "True",
            "algorithm": "1",
        }
        config["DRILL_BITS"] = {
            "bit_0.8mm": "0.8",
            "bit_1.0mm": "1.0",
            "bit_1.2mm": "1.2",
        }

        with open(job_settings.jobs_config_path, "w") as f:
            config.write(f)

        job_settings.read_all_jobs_settings()

        assert "drill" in job_settings.jobs_settings_od
        assert job_settings.jobs_settings_od["drill"]["milling_tool"] is True
        assert job_settings.jobs_settings_od["drill"]["optimize"] == 1
        assert "bit_0.8mm" in job_settings.jobs_settings_od["drill"]["bits_names"]
        assert job_settings.jobs_settings_od["drill"]["bits_diameter"] == [0.8, 1.0, 1.2]

    def test_default_values_top(self, job_settings):
        """Test default values for TOP job"""
        job_settings.read_all_jobs_settings()

        top = job_settings.jobs_settings_od["top"]
        assert top["tool_diameter"] == 1.0
        assert top["passages"] == 1
        assert top["overlap"] == 0.4
        assert top["cut"] == -0.07
        assert top["travel"] == 1.0
        assert top["spindle"] == 1000.0
        assert top["xy_feedrate"] == 250.0
        assert top["z_feedrate"] == 40.0
        assert top["mirror"] is False

    def test_default_values_bottom(self, job_settings):
        """Test default values for BOTTOM job"""
        job_settings.read_all_jobs_settings()

        bottom = job_settings.jobs_settings_od["bottom"]
        assert bottom["mirror"] is True

    def test_default_values_profile(self, job_settings):
        """Test default values for PROFILE job"""
        job_settings.read_all_jobs_settings()

        profile = job_settings.jobs_settings_od["profile"]
        assert profile["tool_diameter"] == 1.0
        assert profile["margin"] == 0.01
        assert profile["multi_depth"] is False
        assert profile["depth_per_pass"] == 0.06
        assert profile["taps_type"] == 3
        assert profile["taps_length"] == 1.0

    def test_default_values_drill(self, job_settings):
        """Test default values for DRILL job"""
        job_settings.read_all_jobs_settings()

        drill = job_settings.jobs_settings_od["drill"]
        assert drill["milling_tool"] is False
        assert drill["tool_diameter"] == 1.0
        assert drill["cut"] == -0.07
        assert drill["travel"] == 1.0
        assert drill["spindle"] == 1000.0
        assert drill["xy_feedrate"] == 250.0
        assert drill["z_feedrate"] == 40.0
        assert drill["optimize"] == 0
        assert drill["mirror"] is False