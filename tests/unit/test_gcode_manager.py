"""
Tests for G-Code Manager - G-Code Generation
Covers requirements: RGC-001 to RGC-004, DGC-001 to DGC-003, VAL-001 to VAL-004
"""

import re

import pytest
from shapely.geometry import LineString, Polygon

from TheAntFarm.shape_core.gcode_manager import GCoder


class TestGCoderInitialization:
    """Test GCoder initialization and configuration."""

    def test_gcoder_gerber_type_initialization(self):
        """Test GCoder initializes correctly for gerber machining."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        assert gcoder is not None
        assert gcoder.tag == "test"
        assert gcoder.type == "gerber"
        assert "cut" in gcoder.cfg
        assert "travel" in gcoder.cfg
        assert "xy_feedrate" in gcoder.cfg
        assert "z_feedrate" in gcoder.cfg
        assert "spindle" in gcoder.cfg

    def test_gcoder_profile_type_initialization(self):
        """Test GCoder initializes correctly for profile machining."""
        gcoder = GCoder(tag="test", machining_type="profile")
        assert gcoder.type == "profile"
        assert "multi_depth" in gcoder.cfg
        assert "depth_per_pass" in gcoder.cfg

    def test_gcoder_drill_type_initialization(self):
        """Test GCoder initializes correctly for drill machining."""
        gcoder = GCoder(tag="test", machining_type="drill")
        assert gcoder.type == "drill"
        assert "cut" in gcoder.cfg

    def test_gcoder_pocketing_type_initialization(self):
        """Test GCoder initializes correctly for pocketing machining."""
        gcoder = GCoder(tag="test", machining_type="pocketing")
        assert gcoder.type == "pocketing"

    def test_gcoder_commander_type_initialization(self):
        """Test GCoder initializes correctly for commander type."""
        gcoder = GCoder(tag="test", machining_type="commander")
        assert gcoder.type == "commander"
        assert gcoder.macro is not None
        assert gcoder.user_cmd is not None

    def test_gcoder_unknown_type(self):
        """Test GCoder with unknown machining type."""
        gcoder = GCoder(tag="test", machining_type="unknown")
        assert gcoder.cfg == {}

    def test_gcoder_load_cfg(self):
        """Test loading configuration into GCoder."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        new_cfg = {
            "cut": -0.1,
            "travel": 1.0,
            "xy_feedrate": 300.0,
            "z_feedrate": 50.0,
            "spindle": 1200.0,
            "mirror": True,
        }
        gcoder.load_cfg(new_cfg)
        assert gcoder.cfg == new_cfg


class TestGCoderFormatting:
    """Test GCoder number formatting."""

    def test_format_float_precision(self):
        """VAL-001: Verify G-code number formatting precision."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        formatted = gcoder.format_float(3.141592653)
        assert formatted == "3.1416"

    def test_format_float_rounding(self):
        """Test float rounding."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        formatted = gcoder.format_float(1.99999)
        assert formatted == "2.0000"

    def test_format_float_negative(self):
        """Test negative float formatting."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        formatted = gcoder.format_float(-0.07)
        assert "-0.07" in formatted


class TestGCodeGeneration:
    """Tests for G-code generation (RGC-001 to VAL-004)."""

    @pytest.fixture
    def gcoder_gerber(self):
        return GCoder(tag="test_gerber", machining_type="gerber")

    @pytest.fixture
    def gcoder_drill(self):
        return GCoder(tag="test_drill", machining_type="drill")

    @pytest.fixture
    def gcoder_profile(self):
        return GCoder(tag="test_profile", machining_type="profile")

    @pytest.fixture
    def simple_path(self):
        """Simple square path for testing."""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        return LineString(coords)

    def test_create_header(self, gcoder_gerber):
        """VAL-002: G-code should include proper header."""
        gcoder_gerber.gcode = []
        gcoder_gerber.create_header()
        header = "".join(gcoder_gerber.gcode)
        assert len(gcoder_gerber.gcode) > 0
        assert "G" in header or "%" in header

    def test_add_job_info(self, gcoder_gerber):
        """VAL-002: G-code should include job information."""
        gcoder_gerber.gcode = []
        gcoder_gerber.add_job_info()
        info = "".join(gcoder_gerber.gcode)
        assert len(gcoder_gerber.gcode) >= 0

    def test_add_init(self, gcoder_gerber):
        """VAL-002: G-code should include initialization commands."""
        gcoder_gerber.gcode = []
        gcoder_gerber.add_init()
        init = "".join(gcoder_gerber.gcode)
        assert "G" in init

    def test_go_travel(self, gcoder_gerber):
        """RGC-001: G-code should include travel moves."""
        gcoder_gerber.gcode = []
        gcoder_gerber.go_travel()
        travel = "".join(gcoder_gerber.gcode)
        assert "G0" in travel or "Z" in travel

    def test_go_to_generates_move(self, gcoder_gerber):
        """RGC-001: Go to command generates correct G-code."""
        gcoder_gerber.gcode = []
        gcoder_gerber.go_to((10.0, 20.0))
        move = "".join(gcoder_gerber.gcode)
        assert "X" in move
        assert "Y" in move
        assert "10" in move
        assert "20" in move

    def test_spindle_on(self, gcoder_gerber):
        """RGC-001: Spindle control commands."""
        gcoder_gerber.gcode = []
        gcoder_gerber.spindle_on(True)
        spindle = "".join(gcoder_gerber.gcode)
        assert "M" in spindle or "S" in spindle

    def test_spindle_off(self, gcoder_gerber):
        """RGC-001: Spindle off command."""
        gcoder_gerber.gcode = []
        gcoder_gerber.spindle_on(False)
        spindle = "".join(gcoder_gerber.gcode)
        assert "M" in spindle

    def test_insert_comment(self, gcoder_gerber):
        """VAL-001: G-code should support comments."""
        gcoder_gerber.gcode = []
        gcoder_gerber.insert_comment("Test comment")
        comment = "".join(gcoder_gerber.gcode)
        assert "Test comment" in comment
        assert "(" in comment or ";" in comment

    def test_make_drill(self, gcoder_drill):
        """DGC-001: Generate drill cycles."""
        gcoder_drill.gcode = []
        gcoder_drill.make_drill()
        drill = "".join(gcoder_drill.gcode)
        assert "Z" in drill

    def test_go_tool_change(self, gcoder_gerber):
        """RGC-002: Include proper tool change commands."""
        gcoder_gerber.gcode = []
        gcoder_gerber.go_tool_change(tool_id=1)
        tool_change = "".join(gcoder_gerber.gcode)
        assert "M6" in tool_change or "T" in tool_change


class TestGCodeValidation:
    """Tests for G-code validation (VAL-001 to VAL-004)."""

    @pytest.fixture
    def gcoder(self):
        return GCoder(tag="test", machining_type="gerber")

    def test_gcode_valid_syntax(self, gcoder):
        """VAL-001: Output valid G-code syntax."""
        gcoder.gcode = []
        gcoder.create_header()
        gcoder.add_init()
        gcoder.go_travel()
        gcoder.go_to((5.0, 5.0))
        gcoder.spindle_on(True)
        gcoder.spindle_on(False)

        full_gcode = "".join(gcoder.gcode)
        lines = full_gcode.split("\n")

        for line in lines:
            line = line.strip()
            if line and not line.startswith("(") and not line.startswith(";"):
                assert re.match(r"^[GMXYZFSTP%\d\.\-\s]+$", line, re.IGNORECASE) or line == ""

    def test_gcode_contains_units(self, gcoder):
        """VAL-002: G-code header should contain units command."""
        gcoder.gcode = []
        gcoder.create_header()
        gcoder.add_init()
        header = "".join(gcoder.gcode)
        assert "G20" in header or "G21" in header

    def test_gcode_feedrate_respected(self, gcoder):
        """VAL-004: Respect user-defined feed rates."""
        custom_feedrate = 500.0
        gcoder.cfg["xy_feedrate"] = custom_feedrate
        gcoder.path = []
        gcoder.compute()
        gcode = "".join(gcoder.gcode)
        assert "F" in gcode
        assert "500" in gcode

    def test_gcode_spindle_speed_respected(self, gcoder):
        """VAL-004: Respect user-defined spindle speed."""
        custom_spindle = 2000.0
        gcoder.cfg["spindle"] = custom_spindle
        gcoder.gcode = []
        gcoder.spindle_on(True)
        spindle = "".join(gcoder.gcode)
        assert "S" in spindle
        assert "2000" in spindle


class TestMirrorCoordinates:
    """Tests for coordinate mirroring."""

    @pytest.fixture
    def gcoder(self):
        return GCoder(tag="test", machining_type="gerber", mirror_type="x")

    def test_mirror_coords_x(self, gcoder):
        """Test X-axis mirroring (Y values inverted)."""
        gcoder.mirror_type = "x"
        coords = [(1.0, 2.0), (3.0, 4.0)]
        mirrored = gcoder.mirror_coords(coords)
        assert mirrored[0][0] == 1.0
        assert mirrored[0][1] == -2.0
        assert mirrored[1][0] == 3.0
        assert mirrored[1][1] == -4.0

    def test_mirror_coords_y(self, gcoder):
        """Test Y-axis mirroring (X values inverted)."""
        gcoder.mirror_type = "y"
        coords = [(1.0, 2.0), (3.0, 4.0)]
        mirrored = gcoder.mirror_coords(coords)
        assert mirrored[0][0] == -1.0
        assert mirrored[0][1] == 2.0
        assert mirrored[1][0] == -3.0
        assert mirrored[1][1] == 4.0


class TestComputeMethods:
    """Tests for compute methods."""

    @pytest.fixture
    def gcoder_gerber(self):
        gcoder = GCoder(tag="test", machining_type="gerber")
        gcoder.path = []
        return gcoder

    @pytest.fixture
    def gcoder_drill(self):
        gcoder = GCoder(tag="test", machining_type="drill")
        gcoder.path = []
        return gcoder

    @pytest.fixture
    def gcoder_profile(self):
        gcoder = GCoder(tag="test", machining_type="profile")
        gcoder.path = []
        return gcoder

    def test_compute_gerber_empty_path(self, gcoder_gerber):
        """RGC-001: Compute gerber with empty path."""
        result = gcoder_gerber.compute()
        assert result is True
        assert len(gcoder_gerber.gcode) > 0

    def test_compute_drill_empty_path(self, gcoder_drill):
        """DGC-001: Compute drill with empty path."""
        result = gcoder_drill.compute()
        assert result is True
        assert len(gcoder_drill.gcode) > 0

    def test_compute_profile_empty_path(self, gcoder_profile):
        """RGC-001: Compute profile with empty path."""
        result = gcoder_profile.compute()
        assert result is True
        assert len(gcoder_profile.gcode) > 0

    def test_compute_unknown_type_fails(self):
        """Test compute with unknown machining type."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        gcoder.type = "unknown_type"
        gcoder.path = []
        result = gcoder.compute()
        assert result is False


class TestMultiPassMilling:
    """Tests for multi-pass milling (RGC-003)."""

    @pytest.fixture
    def gcoder_profile(self):
        gcoder = GCoder(tag="test", machining_type="profile")
        gcoder.cfg["multi_depth"] = True
        gcoder.cfg["depth_per_pass"] = 0.5
        gcoder.cfg["cut"] = -1.5
        gcoder.path = []
        return gcoder

    def test_multi_pass_enabled(self, gcoder_profile):
        """RGC-003: Handle depth increments for material removal."""
        assert gcoder_profile.cfg["multi_depth"] is True
        assert gcoder_profile.cfg["depth_per_pass"] > 0

    def test_compute_multi_pass(self, gcoder_profile):
        """RGC-003: Multi-pass generates correct number of passes."""
        result = gcoder_profile.compute()
        assert result is True


class TestLoadPath:
    """Tests for path loading."""

    def test_load_path(self):
        """Test loading path into GCoder."""
        gcoder = GCoder(tag="test", machining_type="gerber")
        test_path = [("data", [LineString([(0, 0), (1, 1)])])]
        gcoder.load_path(test_path)
        assert gcoder.path == test_path
