from pathlib import Path

import pytest

from app.events import GCodeResult, LayerResult, PathResult
from app.services.pcb_service import PcbService


@pytest.fixture
def pcb_service():
    return PcbService()


@pytest.fixture
def gerber_path():
    return Path(__file__).parent.parent / "test_data" / "gerbers"


class TestLoadLayer:
    def test_load_gerber_layer_success(self, pcb_service, gerber_path):
        result = pcb_service.load_layer("top", str(gerber_path / "simple_square.gbr"))
        assert isinstance(result, LayerResult)
        assert result.ok is True
        assert result.layer_data is not None
        assert result.layer_type == "top"
        assert result.has_drill_exceptions is False

    def test_load_excellon_layer_success(self, pcb_service, gerber_path):
        result = pcb_service.load_layer("drill", str(gerber_path / "simple_drill.drl"))
        assert isinstance(result, LayerResult)
        assert result.ok is True
        assert result.layer_data is not None
        assert result.layer_type == "drill"
        assert result.has_drill_exceptions is True

    def test_load_invalid_file_returns_not_ok(self, pcb_service, gerber_path):
        result = pcb_service.load_layer("top", str(gerber_path / "invalid.gbr"))
        assert isinstance(result, LayerResult)
        assert result.ok is False
        assert result.layer_data is None

    def test_load_unknown_layer_type_returns_not_ok(self, pcb_service, gerber_path):
        result = pcb_service.load_layer("unknown", str(gerber_path / "simple_square.gbr"))
        assert isinstance(result, LayerResult)
        assert result.ok is False
        assert result.layer_data is None

    def test_load_nonexistent_file_returns_not_ok(self, pcb_service):
        result = pcb_service.load_layer("top", "/nonexistent/path.gbr")
        assert isinstance(result, LayerResult)
        assert result.ok is False
        assert result.layer_data is None


class TestGeneratePath:
    def test_generate_path_gerber(self, pcb_service, gerber_path):
        pcb_service.load_layer("top", str(gerber_path / "simple_square.gbr"))
        cfg = {"cut": -0.07, "travel": 0.7, "xy_feedrate": 250.0, "z_feedrate": 40.0, "spindle": 1000.0, "tool_diameter": 0.1}
        result = pcb_service.generate_path("top", cfg, "gerber")
        assert isinstance(result, PathResult)
        assert result.tag == "top"

    def test_generate_path_unknown_machining_type_returns_empty(self, pcb_service, gerber_path):
        pcb_service.load_layer("top", str(gerber_path / "simple_square.gbr"))
        result = pcb_service.generate_path("top", {}, "invalid_type")
        assert isinstance(result, PathResult)
        assert result.paths == []


class TestGenerateGcode:
    def test_generate_gcode_full_chain(self, pcb_service, gerber_path, tmp_path):
        pcb_service.load_layer("top", str(gerber_path / "simple_square.gbr"))
        cfg = {"cut": -0.07, "travel": 0.7, "xy_feedrate": 250.0, "z_feedrate": 40.0, "spindle": 1000.0, "tool_diameter": 0.1}
        path_result = pcb_service.generate_path("top", cfg, "gerber")
        result = pcb_service.generate_gcode("top", cfg, "gerber", path_result.paths, str(tmp_path))
        assert isinstance(result, GCodeResult)
        assert result.tag == "top"
        assert result.gcode_path != ""
        assert Path(result.gcode_path).exists()

    def test_generate_gcode_with_mirror(self, pcb_service, gerber_path, tmp_path):
        pcb_service.load_layer("top", str(gerber_path / "simple_square.gbr"))
        cfg = {"cut": -0.07, "travel": 0.7, "xy_feedrate": 250.0, "z_feedrate": 40.0, "spindle": 1000.0, "tool_diameter": 0.1, "mirror": True}
        path_result = pcb_service.generate_path("top", cfg, "gerber")
        result = pcb_service.generate_gcode("top", cfg, "gerber", path_result.paths, str(tmp_path), mirror_type="x")
        assert result.gcode_path != ""

    def test_generate_gcode_empty_paths_returns_empty(self, pcb_service, tmp_path):
        cfg = {"cut": -0.07}
        result = pcb_service.generate_gcode("top", cfg, "gerber", [], str(tmp_path))
        assert isinstance(result, GCodeResult)
        assert result.gcode_path == ""
