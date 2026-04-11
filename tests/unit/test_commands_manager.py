import pytest

from TheAntFarm.shape_core.commands_manager import CommandManager


class MockParent:
    def format_float(self, value):
        if value is None:
            return ""
        return f"{value:.4f}"


class TestCommandManager:
    @pytest.fixture
    def parent(self):
        return MockParent()

    @pytest.fixture
    def cmd_manager(self, parent):
        return CommandManager(parent)

    def test_init(self, parent):
        """Test CommandManager initialization."""
        cm = CommandManager(parent)
        assert cm.parent is parent
        assert cm.cfg is not None

    def test_default_cfg_values(self, cmd_manager):
        """Test default configuration values."""
        assert cmd_manager.cfg["tool_probe_pos"] == (-1.0, -1.0, -11.0)
        assert cmd_manager.cfg["tool_probe_working"] is True
        assert cmd_manager.cfg["tool_probe_min"] == -11.0
        assert cmd_manager.cfg["tool_change_pos"] == (-41.2, -120.88, -1.0)
        assert cmd_manager.cfg["tool_probe_feedrate"] == (300.0, 80.0, 50.0)
        assert cmd_manager.cfg["tool_probe_hold"] is False
        assert cmd_manager.cfg["tool_probe_zero"] is False
        assert cmd_manager.cfg["safe_pos"] == (-1.0, -1.0, -1.0)

    def test_load_cfg_custom(self, cmd_manager):
        """Test load_cfg with custom config."""
        custom_cfg = {
            "tool_probe_pos": (0.0, 0.0, -5.0),
            "tool_probe_working": False,
            "tool_probe_min": -5.0,
            "tool_change_pos": (0.0, 0.0, 0.0),
            "tool_probe_feedrate": (100.0, 50.0, 25.0),
            "tool_probe_hold": True,
            "tool_probe_zero": True,
        }
        cmd_manager.load_cfg(custom_cfg)
        assert cmd_manager.cfg["tool_probe_pos"] == (0.0, 0.0, -5.0)
        assert cmd_manager.cfg["tool_probe_working"] is False
        assert cmd_manager.cfg["tool_probe_hold"] is True
        assert cmd_manager.cfg["tool_probe_zero"] is True
        assert cmd_manager.cfg["safe_pos"] == (-1.0, -1.0, -1.0)

    def test_get_command_str_soft_reset(self, cmd_manager):
        """Test get_command_str for soft_reset."""
        result = cmd_manager.get_command_str("soft_reset", [None, None, None])
        assert result == [b"\x18"]

    def test_get_command_str_unlock(self, cmd_manager):
        """Test get_command_str for unlock."""
        result = cmd_manager.get_command_str("unlock", [None, None, None])
        assert result == ["$X\n"]

    def test_get_command_str_homing(self, cmd_manager):
        """Test get_command_str for homing."""
        result = cmd_manager.get_command_str("homing", [None, None, None])
        assert result == ["$H\n"]

    def test_get_command_str_jog_xy(self, cmd_manager):
        """Test get_command_str for jog with X and Y."""
        result = cmd_manager.get_command_str("jog", [10.0, 20.0, None])
        assert len(result) == 1
        assert "X10.0000" in result[0]
        assert "Y20.0000" in result[0]
        assert "F300.0000" in result[0]

    def test_get_command_str_jog_z(self, cmd_manager):
        """Test get_command_str for jog with Z only."""
        result = cmd_manager.get_command_str("jog", [None, None, -5.0])
        assert len(result) == 1
        assert "Z-5.0000" in result[0]
        assert "F80.0000" in result[0]

    def test_get_command_str_jog_xyz(self, cmd_manager):
        """Test get_command_str for jog with X, Y, Z."""
        result = cmd_manager.get_command_str("jog", [10.0, 20.0, -5.0])
        assert len(result) == 2

    def test_get_command_str_goto_xy(self, cmd_manager):
        """Test get_command_str for goto with X and Y."""
        result = cmd_manager.get_command_str("goto", [10.0, 20.0, None])
        assert len(result) == 1
        assert "G90 G00 X10.0000 Y20.0000 F300.0000\n" in result[0]

    def test_get_command_str_goto_z(self, cmd_manager):
        """Test get_command_str for goto with Z only."""
        result = cmd_manager.get_command_str("goto", [None, None, -5.0])
        assert len(result) == 1
        assert "G90 G00 Z-5.0000\n" in result[0]

    def test_get_command_str_goto_xyz(self, cmd_manager):
        """Test get_command_str for goto with X, Y, Z."""
        result = cmd_manager.get_command_str("goto", [10.0, 20.0, -5.0])
        assert len(result) == 2

    def test_get_command_str_set_wps_xyz(self, cmd_manager):
        """Test get_command_str for set_wps with X, Y, Z."""
        result = cmd_manager.get_command_str("set_wps", [10.0, 20.0, -5.0])
        assert len(result) == 1
        assert "G10 P1 L20 X10.0000 Y20.0000 Z-5.0000\n" in result[0]

    def test_get_command_str_set_wps_partial(self, cmd_manager):
        """Test get_command_str for set_wps with only X."""
        result = cmd_manager.get_command_str("set_wps", [10.0, None, None])
        assert len(result) == 1
        assert "G10 P1 L20 X10.0000\n" in result[0]

    def test_get_command_str_probe_xy_z(self, cmd_manager):
        """Test get_command_str for probe with X, Y, Z."""
        result = cmd_manager.get_command_str("probe", [10.0, 20.0, -5.0])
        assert len(result) == 1
        assert "G38.2 F50.0000 X10.0000 Y20.0000 Z-5.0000\n" in result[0]

    def test_get_command_str_probe_z_only(self, cmd_manager):
        """Test get_command_str for probe with Z only."""
        result = cmd_manager.get_command_str("probe", [None, None, -5.0])
        assert len(result) == 1
        assert "G38.2 F50.0000 Z-5.0000\n" in result[0]

    def test_get_command_str_probe_with_hold(self, cmd_manager):
        """Test get_command_str for probe with tool_probe_hold enabled."""
        cmd_manager.cfg["tool_probe_hold"] = True
        result = cmd_manager.get_command_str("probe", [None, None, -5.0])
        assert len(result) == 2
        assert "M0\n" in result[0]
        assert "G38.2" in result[1]

    def test_format_float_integration(self, parent):
        """Test that format_float is called correctly for values."""
        class TestParent:
            def format_float(self, value):
                return f"{value:.2f}"

        cm = CommandManager(TestParent())
        result = cm.get_command_str("goto", [1.5, 2.5, None])
        assert "X1.50" in result[0]