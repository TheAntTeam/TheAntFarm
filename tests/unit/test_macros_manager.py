"""Tests for the macro system: tag catalog, template validation and expansion."""

import numpy as np
import pytest

from TheAntFarm.shape_core.gcode_manager import GCodeMacro, GCoder
from TheAntFarm.shape_core.macros_manager import (
    DEFAULT_CFG,
    MACROS,
    TAGS,
    MacroDataError,
    Macros,
    MacroSyntaxError,
    UnknownMacroTag,
    find_tags,
    validate_template,
)


class MockParent:
    """Stand-in for GCoder: the macros only use its float formatting."""

    DIGITS = 4

    def format_float(self, value):
        return f"{value:.4f}"


@pytest.fixture
def cfg():
    return {
        "tool_probe_pos": (-1.0, -1.0, -11.0),
        "tool_probe_working": True,
        "tool_probe_min": -11.0,
        "tool_change_pos": (-41.2, -120.88, -1.0),
        "tool_probe_feedrate": (300.0, 80.0, 50.0),
        "tool_probe_hold": False,
        "safe_pos": (-1.0, -1.0, -1.0),
    }


@pytest.fixture
def macrodir(tmp_path):
    """Local macro folder, to test the user templates without touching the app ones."""
    macros_folder = tmp_path / "macros"
    macros_folder.mkdir()
    return tmp_path


@pytest.fixture
def macros(cfg):
    manager = Macros(MockParent())
    manager.load_cfg(cfg)
    return manager


@pytest.fixture
def dro():
    return {"WPO": np.array([1.234, 2.345, 3.456]), "MPO": np.array([11.234, 12.345, 13.456])}


@pytest.fixture
def probe_data():
    # newest probe first, machine coordinates, same values used by the golden tests
    return [[7.0, 8.0, 9.0], [1.0, 1.0, 1.0]]


@pytest.fixture
def wsp():
    return {"TLO": 0.25}


@pytest.fixture
def context(macros, wsp, probe_data, dro):
    return macros.make_context(wsp, probe_data, dro)


class TestMacroContext:
    def test_format(self, context):
        assert context.fmt(1.23456) == "1.2346"

    def test_wco(self, context):
        assert context.wco == pytest.approx([10.0, 10.0, 10.0])

    def test_probe_values_are_converted_to_work_coordinates(self, context):
        assert context.probe("ACT", "Z") == pytest.approx(-1.0)
        assert context.probe("PRE", "Z") == pytest.approx(-9.0)

    def test_tlo(self, context):
        assert context.tlo() == pytest.approx(0.25)

    def test_tlo_delta(self, context):
        assert context.tlo_delta() == pytest.approx(8.0)

    def test_missing_probe_data(self, macros, wsp, dro):
        context = macros.make_context(wsp, [], dro)
        with pytest.raises(MacroDataError):
            context.probe("PRE", "Z")

    def test_missing_tlo(self, macros, probe_data, dro):
        context = macros.make_context({}, probe_data, dro)
        with pytest.raises(MacroDataError):
            context.tlo()

    def test_missing_machine_position(self, macros, wsp, probe_data):
        context = macros.make_context(wsp, probe_data, {})
        with pytest.raises(MacroDataError):
            context.wco

    def test_missing_config_key(self, context):
        with pytest.raises(MacroDataError):
            context.cfg_value("not_a_key")

    def test_config_key_default(self, context):
        assert context.cfg_value("not_a_key", 42) == 42


class TestTagCatalog:
    """Every declared placeholder expands to the documented value."""

    @pytest.mark.parametrize(
        "tag, expected",
        [
            ("PROBE_POS_X", "-1.0000"),
            ("PROBE_POS_Y", "-1.0000"),
            ("PROBE_POS_MIN", "-11.0000"),
            ("PROBE_TYPE_POS", "G54"),
            ("PROBE_FEED_XY", "300.0000"),
            ("PROBE_FEED_FAST", "80.0000"),
            ("PROBE_FEED_SLOW", "50.0000"),
            ("PROBE_HOLD_BEFORE", "(NO HOLD)"),
            ("PROBE_BACKOFF", "1.5000"),
            ("PROBE_VALUE_PREX", "-9.0000"),
            ("PROBE_VALUE_PREY", "-9.0000"),
            ("PROBE_VALUE_PREZ", "-9.0000"),
            ("PROBE_VALUE_ACTX", "-3.0000"),
            ("PROBE_VALUE_ACTY", "-2.0000"),
            ("PROBE_VALUE_ACTZ", "-1.0000"),
            ("CHANGE_POS_X", "-41.2000"),
            ("CHANGE_POS_Y", "-120.8800"),
            ("CHANGE_POS_Z", "-1.0000"),
            ("SETTER_POS_X", "-1.0000"),
            ("SETTER_POS_Y", "-1.0000"),
            ("SETTER_TYPE_POS", "G53"),
            ("CHANGE_TYPE_POS", "G54"),
            ("CHANGE_FEED_SLOW", "50.0000"),
            ("CHANGE_FEED_FAST", "80.0000"),
            ("SAFE_POS_Z", "-1.0000"),
            ("PRE_POS_X", "1.2340"),
            ("PRE_POS_Y", "2.3450"),
            ("PRE_POS_Z", "3.4560"),
            ("SPINDLE_STOP", "M5"),
            ("SPINDLE_DWELL", "1.0000"),
            ("SPINDLE_START", "M3"),
            ("TLO_TYPE_A", "8.2500"),
            ("TLO_TYPE_N", "8.0000"),
        ],
    )
    def test_tag_value(self, macros, context, tag, expected):
        assert tag in TAGS
        assert macros.expand(f"@{tag}@", context) == expected

    def test_no_tag_expands_to_more_than_one_line(self, macros, context):
        """The job is streamed one line at a time: a tag must stay on one line."""
        for name in TAGS:
            value = macros.expand(f"@{name}@", context)
            assert "\n" not in value, f"tag {name} expands to multiple lines"

    def test_catalog_entries_are_documented(self):
        assert TAGS
        for name, tag in TAGS.items():
            assert tag.name == name
            assert tag.description, f"tag {name} has no description"

    def test_probe_hold_enabled(self, macros, context):
        macros.cfg["tool_probe_hold"] = True
        context = macros.make_context({}, [[7.0, 8.0, 9.0], [1.0, 1.0, 1.0]], {"WPO": [0, 0, 0], "MPO": [0, 0, 0]})
        assert macros.expand("@PROBE_HOLD_BEFORE@", context) == "M0"

    def test_machine_coordinates_when_probe_is_in_machine_position(self, macros, context):
        macros.cfg["tool_probe_working"] = False
        context = macros.make_context({}, [[7.0, 8.0, 9.0], [1.0, 1.0, 1.0]], {"WPO": [0, 0, 0], "MPO": [0, 0, 0]})
        assert macros.expand("@PROBE_TYPE_POS@", context) == "G53"
        assert macros.expand("@CHANGE_TYPE_POS@", context) == "G53"

    def test_change_position_can_use_its_own_coordinate_system(self, macros, context):
        macros.cfg["tool_probe_working"] = False
        macros.cfg["tool_change_working"] = True
        context = macros.make_context({}, [[7.0, 8.0, 9.0], [1.0, 1.0, 1.0]], {"WPO": [0, 0, 0], "MPO": [0, 0, 0]})
        assert macros.expand("@CHANGE_TYPE_POS@", context) == "G54"

    def test_change_feed_rate_can_be_configured(self, macros, context):
        macros.cfg["tool_change_feedrate"] = (10.0, 20.0, 30.0)
        context = macros.make_context({}, [[7.0, 8.0, 9.0], [1.0, 1.0, 1.0]], {"WPO": [0, 0, 0], "MPO": [0, 0, 0]})
        assert macros.expand("@CHANGE_FEED_FAST@", context) == "20.0000"
        assert macros.expand("@CHANGE_FEED_SLOW@", context) == "30.0000"

    def test_spindle_start_with_configured_speed(self, macros, context):
        macros.cfg["spindle"] = 1000.0
        context = macros.make_context({}, [[0, 0, 0], [0, 0, 0]], {"WPO": [0, 0, 0], "MPO": [0, 0, 0]})
        assert macros.expand("@SPINDLE_START@", context) == "M3 S1000.0000"


class TestExpand:
    def test_text_without_tags_is_unchanged(self, macros, context):
        assert macros.expand("G0 X10", context) == "G0 X10"

    def test_multiple_tags_in_one_line(self, macros, context):
        assert macros.expand("G00 X@PROBE_POS_X@ Y@PROBE_POS_Y@", context) == "G00 X-1.0000 Y-1.0000"

    def test_tags_are_case_insensitive(self, macros, context):
        assert macros.expand("@probe_pos_x@", context) == "-1.0000"

    def test_comment_without_tags_is_preserved(self, macros, context):
        assert macros.expand("(probe position)", context) == "(probe position)"

    def test_unknown_tag_raises(self, macros, context):
        with pytest.raises(UnknownMacroTag):
            macros.expand("G01 Z@NOT_A_TAG@", context)

    def test_incomplete_tag_raises(self, macros, context):
        with pytest.raises(MacroSyntaxError):
            macros.expand("G01 Z@PROBE_POS_X", context)

    def test_expand_lines(self, macros, context):
        lines = ["G21", "G00 X@PROBE_POS_X@", "(end)"]
        assert list(macros.expand_lines(lines, context)) == ["G21", "G00 X-1.0000", "(end)"]


class TestTemplateValidation:
    @pytest.mark.parametrize("mode", ["wcs", "tlo", "setter"])
    def test_shipped_templates_are_valid(self, macros, mode):
        macros.cfg["tool_change_mode"] = mode
        text = macros.get_macro_string("M6")
        assert validate_template(text) == []

    def test_unknown_tag_is_reported_with_line_number(self):
        problems = validate_template("G21\nG01 Z@NOPE@\n")
        assert problems == [(2, "unknown tag @NOPE@")]

    def test_unbalanced_tag_is_reported(self):
        problems = validate_template("G21\nG01 Z@PROBE_POS_X\n")
        assert problems == [(2, "unbalanced '@'")]

    def test_find_tags(self):
        assert find_tags("X@PROBE_POS_X@ Y@SAFE_POS_Z@") == ["PROBE_POS_X", "SAFE_POS_Z"]


class TestMacrosFacade:
    def test_is_macro(self, macros):
        assert macros.is_macro("M6") is True
        assert macros.is_macro("m6 ") is True
        assert macros.is_macro("G0") is False

    def test_default_variant_is_wcs(self, macros):
        assert macros.get_mode("M6") == "wcs"
        assert macros.get_macro_path("M6").endswith("tool_change_wcs.gcode")

    def test_tlo_variant_can_be_selected(self, macros):
        macros.cfg["tool_change_mode"] = "tlo"
        assert macros.get_mode("M6") == "tlo"
        assert macros.get_macro_path("M6").endswith("tool_change_tlo.gcode")

    def test_setter_variant_can_be_selected(self, macros):
        macros.cfg["tool_change_mode"] = "setter"
        assert macros.get_mode("M6") == "setter"
        assert macros.get_macro_path("M6").endswith("tool_change_setter.gcode")

    def test_setter_position_falls_back_to_the_probe_position(self):
        manager = Macros(MockParent())
        manager.load_cfg({"tool_probe_pos": (12.0, 34.0, -5.0)})
        assert manager.cfg["tool_setter_pos"] == (12.0, 34.0)

    def test_configured_setter_position_is_kept(self):
        manager = Macros(MockParent())
        manager.load_cfg({"tool_setter_pos": (-200.0, -150.0)})
        assert manager.cfg["tool_setter_pos"] == (-200.0, -150.0)

    def test_setter_type_can_use_working_coordinates(self, macros, context):
        macros.cfg["tool_setter_working"] = True
        context = macros.make_context({}, [[7.0, 8.0, 9.0], [1.0, 1.0, 1.0]], {"WPO": [0, 0, 0], "MPO": [0, 0, 0]})
        assert macros.expand("@SETTER_TYPE_POS@", context) == "G54"

    def test_unknown_variant_raises(self, macros):
        macros.cfg["tool_change_mode"] = "nope"
        with pytest.raises(Exception, match="available modes"):
            macros.get_mode("M6")

    def test_unknown_macro_raises(self, macros):
        with pytest.raises(Exception):
            macros.get_macro_string("G0")

    def test_missing_file_raises(self, macros, tmp_path):
        macros.macros_default_path = str(tmp_path / "missing")
        with pytest.raises(Exception, match="not found"):
            macros.get_macro_string("M6")

    def test_local_macro_overrides_the_built_in_one(self, macrodir, cfg):
        (macrodir / "macros" / "tool_change_wcs.gcode").write_text(
            "(user macro)\nG00 X@SAFE_POS_Z@\n", encoding="utf-8"
        )
        manager = Macros(MockParent())
        manager.load_cfg(cfg)
        text = manager.get_macro_string("M6", local_path=str(macrodir))
        assert text.startswith("(user macro)")

    def test_local_folder_without_the_macro_falls_back_to_the_built_in_one(self, macrodir, cfg):
        manager = Macros(MockParent())
        manager.load_cfg(cfg)
        text = manager.get_macro_string("M6", local_path=str(macrodir))
        assert "The Ant Tool Change" in text

    def test_user_config_does_not_modify_the_caller_dictionary(self):
        user_cfg = {"tool_probe_min": -5.0}
        Macros(MockParent()).load_cfg(user_cfg)
        assert user_cfg == {"tool_probe_min": -5.0}

    def test_missing_keys_fall_back_to_the_defaults(self):
        manager = Macros(MockParent())
        manager.load_cfg({"tool_probe_min": -5.0})
        assert manager.cfg["tool_probe_min"] == -5.0
        assert manager.cfg["safe_pos"] == DEFAULT_CFG["safe_pos"]
        assert manager.cfg["tool_probe_feedrate"] == DEFAULT_CFG["tool_probe_feedrate"]

    def test_configurable_safe_position_is_not_overwritten(self):
        manager = Macros(MockParent())
        manager.load_cfg({"safe_pos": (5.0, 6.0, 7.0)})
        assert manager.cfg["safe_pos"] == (5.0, 6.0, 7.0)

    def test_format_float_without_parent(self):
        assert Macros().format_float(1.23456) == "1.2346"

    def test_check_tag_in_string(self, macros):
        assert macros.check_tag_in_string("G0 X@PROBE_POS_X@") is True
        assert macros.check_tag_in_string("G0 X10") is False


GOLDEN_WCS = [
    "(The Ant Tool Change)",
    "(Homing is required: the G53 moves use absolute machine positions)",
    "G21",
    "G49",
    "M5",
    "G4 P1.0000",
    "F80.0000",
    "G53 G00 Z-1.0000",
    "G54",
    "G00 X-1.0000 Y-1.0000 F300.0000",
    "G54",
    "(NO HOLD)",
    "G38.2 Z-11.0000 F80.0000",
    "G91 G00 Z1.5000",
    "G90",
    "G38.2 Z-11.0000 F50.0000",
    "G53 G00 Z-1.0000",
    "G53 G00 X-41.2000",
    "G53 G00 Y-120.8800",
    "M0 (Change the tool, then press Cycle Start)",
    "G53 G01 Z-1.0000 F80.0000",
    "G54",
    "G01 F300.0000",
    "G00 X-1.0000 Y-1.0000",
    "G54",
    "(NO HOLD)",
    "G38.2 Z-11.0000 F80.0000",
    "G91 G00 Z1.5000",
    "G90",
    "G38.2 Z-11.0000 F50.0000",
    "G10 P1 L20 Z-9.0000",
    "G53 G01 Z-1.0000 F80.0000",
    "G54",
    "G01 F300.0000",
    "G00 X1.2340 Y2.3450",
    "G00 Z3.4560",
    "M3",
]

GOLDEN_TLO = list(GOLDEN_WCS)
GOLDEN_TLO[30] = "G43.1 Z8.2500"

GOLDEN_SETTER = [
    "(The Ant Tool Change - fixed tool setter)",
    "(Tool length is measured on the setter, the work zero is not modified)",
    "(Homing is required: the G53 moves use absolute machine positions)",
    "G21",
    "G49",
    "M5",
    "G4 P1.0000",
    "G53 G00 Z-1.0000",
    "G53",
    "G00 X-200.0000 Y-150.0000 F300.0000",
    "G38.2 Z-11.0000 F80.0000",
    "G91 G00 Z1.5000",
    "G90",
    "G38.2 Z-11.0000 F50.0000",
    "G53 G00 Z-1.0000",
    "G53 G00 X-41.2000",
    "G53 G00 Y-120.8800",
    "M0 (Change the tool, then press Cycle Start)",
    "G53",
    "G00 X-200.0000 Y-150.0000 F300.0000",
    "G38.2 Z-11.0000 F80.0000",
    "G91 G00 Z1.5000",
    "G90",
    "G38.2 Z-11.0000 F50.0000",
    "G43.1 Z8.2500",
    "G53 G01 Z-1.0000 F80.0000",
    "G54",
    "G01 F300.0000",
    "G00 X1.2340 Y2.3450",
    "G00 Z3.4560",
    "M3",
]


class TestGoldenTemplates:
    """Freeze the expanded output of the shipped tool change templates."""

    @pytest.mark.parametrize(
        "mode, expected",
        [("wcs", GOLDEN_WCS), ("tlo", GOLDEN_TLO), ("setter", GOLDEN_SETTER)],
    )
    def test_tool_change_template(self, macros, context, mode, expected):
        macros.cfg["tool_change_mode"] = mode
        if mode == "setter":
            macros.cfg["tool_setter_pos"] = (-200.0, -150.0)
        text = macros.get_macro_string("M6")
        expanded = list(macros.expand_lines(text.splitlines(), context))
        assert expanded == expected


class TestGCodeMacro:
    @pytest.fixture
    def gcr(self, cfg):
        gcoder = GCoder("dummy", machining_type="commander")
        gcoder.load_cfg(cfg)
        return gcoder

    @pytest.fixture
    def frozen_dro(self):
        return {"WPO": np.array([1.234, 2.345, 3.456]), "MPO": np.array([11.234, 12.345, 13.456])}

    def test_lines_are_expanded_one_by_one(self, gcr, frozen_dro, wsp, probe_data):
        macro = GCodeMacro(frozen_dro, "M6", gcr)
        lines = []
        while True:
            line = macro.get_next_line(wsp, probe_data)
            if line is None:
                break
            lines.append(line.rstrip("\n"))
        assert lines == GOLDEN_WCS

    def test_no_trailing_blank_line(self, gcr, frozen_dro, wsp, probe_data):
        macro = GCodeMacro(frozen_dro, "M6", gcr)
        assert len(macro.macro_lines) == 37

    def test_broken_template_does_not_break_the_job(self, macrodir, cfg, frozen_dro, wsp, probe_data):
        (macrodir / "macros" / "tool_change_wcs.gcode").write_text("G01 Z@NOT_A_TAG@\n", encoding="utf-8")
        gcoder = GCoder("dummy", machining_type="commander")
        gcoder.load_cfg(cfg)

        macro = GCodeMacro(frozen_dro, "M6", gcoder, local_path=str(macrodir))

        assert macro.macro_lines == []
        assert macro.get_next_line(wsp, probe_data) is None

    def test_macro_ids_are_registered(self):
        assert "M6" in MACROS
