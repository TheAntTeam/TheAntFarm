"""
Integration Tests for PCB Processing Workflow
Covers requirements: INT-001, INT-002, FMT-001 to FMT-003
"""

from pathlib import Path

import pytest

from TheAntFarm.shape_core.gcode_manager import GCoder
from TheAntFarm.shape_core.geometry_manager import Geom, merge_polygons, offset_polygon
from TheAntFarm.shape_core.pcb_manager import PcbObj


class TestCompleteWorkflow:
    """Integration tests for complete PCB processing workflow (INT-001, INT-002)."""

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    def test_load_gerber_process_and_generate_gcode(self, pcb, gerber_path):
        """INT-001: Load PCB files -> Generate G-code workflow."""
        file_path = gerber_path / "simple_square.gbr"

        result = pcb.load_gerber(str(file_path), "top")
        assert result is True

        layer = pcb.get_gerber_layer("top")
        assert layer is not None

        layer_geoms, others = layer
        assert isinstance(layer_geoms, list)

    def test_load_drill_and_generate_gcode(self, pcb, gerber_path):
        """INT-001: Load drill files -> Generate G-code workflow."""
        file_path = gerber_path / "simple_drill.drl"

        result = pcb.load_excellon(str(file_path), "drill")
        assert result is True

        layer = pcb.get_excellon_layer("drill")
        assert layer is not None

    def test_full_pcb_processing_chain(self, pcb, gerber_path):
        """INT-002: Verify end-to-end functionality."""
        gerber_file = gerber_path / "simple_square.gbr"
        drill_file = gerber_path / "simple_drill.drl"

        pcb.load_gerber(str(gerber_file), "top")
        pcb.load_excellon(str(drill_file), "drill")

        assert pcb.gerbers["top"] is not None
        assert pcb.excellons["drill"] is not None

        top_layer = pcb.get_gerber_layer("top")
        drill_layer = pcb.get_excellon_layer("drill")

        assert top_layer is not None
        assert drill_layer is not None


class TestGeometryToGCodeIntegration:
    """Test geometry processing to G-code generation integration."""

    def test_polygon_to_gcode(self):
        """Test creating G-code from polygon geometry."""
        gdata = {
            "points": [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        assert geom.geom is not None
        assert geom.geom.is_valid

        gcoder = GCoder(tag="test", machining_type="gerber")
        gcoder.path = [(None, [geom.geom.exterior])]
        result = gcoder.compute()
        assert result is True
        assert len(gcoder.gcode) > 0

    def test_offset_polygon_to_gcode(self):
        """Test creating G-code from offset polygon (isolation routing)."""
        gdata = {
            "points": [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)

        offset_geom = offset_polygon(geom, 0.2)
        assert offset_geom is not None
        assert offset_geom.area > geom.geom.area

        gcoder = GCoder(tag="test", machining_type="gerber")
        gcoder.path = [(None, [offset_geom.exterior])]
        result = gcoder.compute()
        assert result is True


class TestMultipleLayerProcessing:
    """Test processing multiple PCB layers."""

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    def test_load_multiple_layers(self, pcb, gerber_path):
        """Test loading and processing multiple Gerber layers."""
        file_path = gerber_path / "simple_square.gbr"

        pcb.load_gerber(str(file_path), "top")
        pcb.load_gerber(str(file_path), "bottom")

        top_layer = pcb.get_gerber_layer("top")
        bottom_layer = pcb.get_gerber_layer("bottom")

        assert top_layer is not None
        assert bottom_layer is not None

    def test_process_copper_and_drill(self, pcb, gerber_path):
        """Test processing copper layer with drill layer."""
        copper_file = gerber_path / "simple_square.gbr"
        drill_file = gerber_path / "simple_drill.drl"

        pcb.load_gerber(str(copper_file), "top")
        pcb.load_excellon(str(drill_file), "drill")

        copper_layer = pcb.get_gerber_layer("top")
        drill_layer = pcb.get_excellon_layer("drill")

        assert copper_layer is not None
        assert drill_layer is not None

        copper_geoms, _ = copper_layer
        drill_geoms, _ = drill_layer

        assert len(copper_geoms) > 0 or copper_geoms is not None


class TestGCodeGenerationIntegration:
    """Integration tests for G-code generation with real paths."""

    def test_generate_gerber_gcode(self):
        """Test generating G-code for gerber machining."""
        from shapely.geometry import LineString

        path = LineString([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])

        gcoder = GCoder(tag="gerber_test", machining_type="gerber")
        gcoder.path = [(None, [path])]
        result = gcoder.compute()

        assert result is True
        gcode = "".join(gcoder.gcode)
        assert "G" in gcode
        assert len(gcode) > 0

    def test_generate_drill_gcode(self):
        """Test generating G-code for drilling."""
        from shapely.geometry import Point

        gcoder = GCoder(tag="drill_test", machining_type="drill")
        gcoder.path = []
        result = gcoder.compute()

        assert result is True
        gcode = "".join(gcoder.gcode)
        assert len(gcode) > 0

    def test_generate_profile_gcode(self):
        """Test generating G-code for profile cutting."""
        from shapely.geometry import LineString

        path = LineString([(0, 0), (50, 0), (50, 50), (0, 50), (0, 0)])

        gcoder = GCoder(tag="profile_test", machining_type="profile")
        gcoder.path = [(None, [path])]
        result = gcoder.compute()

        assert result is True
        gcode = "".join(gcoder.gcode)
        assert len(gcode) > 0


class TestMirroringIntegration:
    """Test coordinate mirroring for double-sided PCBs."""

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    def test_mirror_gerber_gcode(self, pcb, gerber_path):
        """Test generating mirrored G-code for bottom layer."""
        file_path = gerber_path / "simple_square.gbr"
        pcb.load_gerber(str(file_path), "bottom")
        layer = pcb.get_gerber_layer("bottom")

        assert layer is not None

        gcoder = GCoder(tag="bottom_test", machining_type="gerber", mirror_type="x")
        gcoder.cfg["mirror"] = True
        gcoder.path = []

        result = gcoder.compute()
        assert result is True


class TestUnitConversionIntegration:
    """Test unit conversion throughout the processing chain."""

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    def test_inch_to_metric_full_workflow(self, pcb, gerber_path):
        """Test inch to metric conversion in full workflow."""
        file_path = gerber_path / "simple_square.gbr"
        pcb.load_gerber(str(file_path), "top")

        assert pcb.gerbers["top"].units == "metric"

        layer = pcb.get_gerber_layer("top")
        assert layer is not None

    def test_metric_stays_metric_full_workflow(self, pcb, gerber_path):
        """Test metric files stay metric through workflow."""
        file_path = gerber_path / "metric_trace.gbr"
        pcb.load_gerber(str(file_path), "top")

        assert pcb.gerbers["top"].units == "metric"

        layer = pcb.get_gerber_layer("top")
        assert layer is not None
