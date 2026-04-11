import os
import pytest

from TheAntFarm.shape_core.macros_manager import Macros


class MockParent:
    def format_float(self, value):
        return f"{value:.4f}"


class TestMacros:
    @pytest.fixture
    def parent(self):
        return MockParent()

    @pytest.fixture
    def macros(self, parent):
        return Macros(parent)

    def test_init(self, parent):
        m = Macros(parent)
        assert m.parent is parent
        assert m.cfg is not None
        assert m.macros_default_path is not None
        assert "M6" in m.macros_dict

    def test_load_cfg_default(self, macros):
        assert macros.cfg["tool_probe_pos"] == (-1.0, -1.0, -11.0)
        assert macros.cfg["tool_probe_working"] is True
        assert macros.cfg["safe_pos"] == (-1.0, -1.0, -1.0)

    def test_load_cfg_custom(self, parent):
        custom_cfg = {
            "tool_probe_pos": (0, 0, -5),
            "tool_probe_working": False,
        }
        m = Macros(parent)
        m.load_cfg(custom_cfg)
        assert m.cfg["tool_probe_pos"] == (0, 0, -5)
        assert m.cfg["tool_probe_working"] is False

    def test_is_macro_true(self, macros):
        assert macros.is_macro("M6") is True

    def test_is_macro_false(self, macros):
        assert macros.is_macro("G0") is False

    def test_is_macro_case_insensitive(self, macros):
        assert macros.is_macro("m6") is True
        assert macros.is_macro("M6 ") is True

    def test_get_macro_string_not_macro(self, macros):
        result = macros.get_macro_string("G0")
        assert result == ""

    def test_get_macro_string_invalid_path(self, macros, tmp_path):
        macros.macros_default_path = str(tmp_path / "nonexistent")
        result = macros.get_macro_string("M6", local_path=str(tmp_path / "nonexistent"))
        assert result == ""

    def test_get_tags_family(self, macros):
        tags = macros.get_tags_family()
        assert "PROBE" in tags
        assert "CHANGE" in tags
        assert "SAFE" in tags

    def test_format_float(self, macros):
        result = macros.format_float(1.234)
        assert result is not None

    def test_check_tag_in_string_true(self, macros):
        assert macros.check_tag_in_string("@PROBE") is True
        assert macros.check_tag_in_string("G0 @PROBE") is True

    def test_check_tag_in_string_false(self, macros):
        assert macros.check_tag_in_string("G0 X10") is False

    def test_compute_probe_tag_pos_x(self, macros):
        stag = ["PROBE", "POS", "X"]
        dro = {"WPO": [0, 0, 0], "MPO": [0, 0, 0]}
        probe_data = [[0, 0, -1], [0, 0, 0]]
        result = macros.compute_probe_tag(stag, dro, probe_data)
        assert result == "-1.0000"

    def test_compute_probe_tag_pos_z(self, macros):
        stag = ["PROBE", "POS", "Z"]
        dro = {"WPO": [0, 0, 0], "MPO": [0, 0, 0]}
        probe_data = [[0, 0, -1], [0, 0, 0]]
        result = macros.compute_probe_tag(stag, dro, probe_data)
        assert result == "-11.0000"

    def test_compute_probe_tag_pos_min(self, macros):
        stag = ["PROBE", "POS", "MIN"]
        dro = {"WPO": [0, 0, 0], "MPO": [0, 0, 0]}
        probe_data = [[0, 0, -1], [0, 0, 0]]
        result = macros.compute_probe_tag(stag, dro, probe_data)
        assert result == "-11.0000"

    def test_compute_probe_tag_type_working(self, macros):
        macros.cfg["tool_probe_working"] = True
        stag = ["PROBE", "TYPE", "POS"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "G54"

    def test_compute_probe_tag_type_machine(self, macros):
        macros.cfg["tool_probe_working"] = False
        stag = ["PROBE", "TYPE", "POS"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "G53"

    def test_compute_probe_tag_feed_slow(self, macros):
        stag = ["PROBE", "FEED", "SLOW"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "50.0000"

    def test_compute_probe_tag_feed_fast(self, macros):
        stag = ["PROBE", "FEED", "FAST"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "80.0000"

    def test_compute_probe_tag_feed_xy(self, macros):
        stag = ["PROBE", "FEED", "XY"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "300.0000"

    def test_compute_probe_tag_hold_true(self, macros):
        macros.cfg["tool_probe_hold"] = True
        stag = ["PROBE", "HOLD"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "M0"

    def test_compute_probe_tag_hold_false(self, macros):
        macros.cfg["tool_probe_hold"] = False
        stag = ["PROBE", "HOLD"]
        result = macros.compute_probe_tag(stag, {}, [])
        assert result == "(NO HOLD)"

    def test_compute_change_tag_pos(self, macros):
        stag = ["CHANGE", "POS", "X"]
        result = macros.compute_change_tag(stag)
        assert result == "-41.2000"

    def test_compute_change_tag_pos_z(self, macros):
        stag = ["CHANGE", "POS", "Z"]
        result = macros.compute_change_tag(stag)
        assert result == "-1.0000"

    def test_compute_safe_tag(self, macros):
        stag = ["SAFE", "POS", "Z"]
        result = macros.compute_safe_tag(stag)
        assert result == "-1.0000"

    def test_compute_tlo_tag_n(self, macros):
        stag = ["TLO", "TYPE", "N"]
        wsp = {"TLO": 0}
        probe_data = [[0, 0, -1.5], [0, 0, 0]]
        result = macros.compute_tlo_tag(stag, wsp, probe_data)
        assert result == "-1.5000"

    def test_compute_tlo_tag_a(self, macros):
        stag = ["TLO", "TYPE", "A"]
        wsp = {"TLO": 0.5}
        probe_data = [[0, 0, -1.5], [0, 0, 0]]
        result = macros.compute_tlo_tag(stag, wsp, probe_data)
        assert result == "-1.0000"

    def test_compute_pre_tag(self, macros):
        stag = ["PRE", "POS", "X"]
        dro = {"WPO": [1.0, 2.0, 3.0]}
        result = macros.compute_pre_tag(stag, dro)
        assert result == "1.0000"