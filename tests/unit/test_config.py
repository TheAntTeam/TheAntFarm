"""Tests of the default configuration shared by the CAM pipeline."""

import pytest

from TheAntFarm.shape_core.config import (
    COMMON_GCODE,
    GCODE_DEFAULTS,
    PATH_DEFAULTS,
    PROBE_DEFAULTS,
    default_config,
    merge_config,
)

ALL_GCODE_TYPES = ("gerber", "profile", "pocketing", "drill", "commander")
ALL_PATH_TYPES = ("gerber", "profile", "pocketing", "drill")


class TestDefaultConfig:
    @pytest.mark.parametrize("machining_type", ALL_PATH_TYPES)
    def test_every_path_type_has_defaults(self, machining_type):
        assert default_config("path", machining_type)

    @pytest.mark.parametrize("machining_type", ALL_GCODE_TYPES)
    def test_every_gcode_type_has_defaults(self, machining_type):
        assert default_config("gcode", machining_type)

    def test_unknown_type_has_no_defaults(self):
        assert default_config("path", "unknown") == {}
        assert default_config("gcode", "unknown") == {}

    def test_defaults_are_a_copy(self):
        cfg = default_config("gcode", "gerber")
        cfg["cut"] = -99.0
        assert default_config("gcode", "gerber")["cut"] == COMMON_GCODE["cut"]

    @pytest.mark.parametrize("machining_type", ALL_PATH_TYPES)
    def test_gcode_defaults_include_the_common_values(self, machining_type):
        cfg = default_config("gcode", machining_type)
        for key, value in COMMON_GCODE.items():
            assert key in cfg
            if key != "cut":
                # only the cut depth depends on the job, see the next test
                assert cfg[key] == value

    def test_cut_depth_depends_on_the_job(self):
        assert default_config("gcode", "gerber")["cut"] == COMMON_GCODE["cut"]
        assert default_config("gcode", "profile")["cut"] == -1.8
        assert default_config("gcode", "drill")["cut"] == -2.1

    def test_commander_uses_the_probe_defaults(self):
        cfg = default_config("gcode", "commander")
        assert cfg["tool_probe_pos"] == PROBE_DEFAULTS["tool_probe_pos"]
        assert cfg["tool_probe_feedrate"] == PROBE_DEFAULTS["tool_probe_feedrate"]

    def test_path_and_gcode_defaults_are_different_sets(self):
        assert "passages" in PATH_DEFAULTS["gerber"]
        assert "passages" not in GCODE_DEFAULTS["gerber"]


class TestMergeConfig:
    def test_partial_configuration_keeps_the_defaults(self):
        cfg = merge_config("gcode", "gerber", {"cut": -0.2})

        assert cfg["cut"] == -0.2
        assert cfg["travel"] == COMMON_GCODE["travel"]

    def test_none_values_do_not_override_the_defaults(self):
        cfg = merge_config("gcode", "gerber", {"travel": None})

        assert cfg["travel"] == COMMON_GCODE["travel"]

    def test_none_configuration(self):
        cfg = merge_config("path", "drill", None)

        assert cfg["bits_diameter"] == PATH_DEFAULTS["drill"]["bits_diameter"]

    def test_unknown_type_keeps_the_given_keys(self):
        assert merge_config("gcode", "unknown", {"custom": 1}) == {"custom": 1}

    def test_extra_keys_are_kept(self):
        cfg = merge_config("path", "gerber", {"custom": 1})
        assert cfg["custom"] == 1
        assert cfg["passages"] == PATH_DEFAULTS["gerber"]["passages"]
