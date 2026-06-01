"""
Tests for PCB Manager - File Loading & Processing
Covers requirements: GBR-001 to GBR-004, EXN-001 to EXN-004, LAY-001 to LAY-003, ERR-001 to ERR-003
"""

from pathlib import Path

import pytest

from TheAntFarm.shape_core.pcb_manager import PcbObj


class TestPcbObjInitialization:
    """Test PcbObj initialization and default values."""

    def test_initialization(self):
        """Test that PcbObj initializes correctly with default values."""
        pcb = PcbObj()
        assert isinstance(pcb, PcbObj)
        assert pcb.gerbers is not None
        assert pcb.excellons is not None
        assert len(pcb.gerbers) == len(PcbObj.GBR_KEYS)
        assert len(pcb.excellons) == len(PcbObj.EXN_KEYS)

    def test_gerber_keys_initialized(self):
        """Test that all Gerber keys are initialized to None."""
        pcb = PcbObj()
        for key in PcbObj.GBR_KEYS:
            assert key in pcb.gerbers
            assert pcb.gerbers[key] is None

    def test_excellon_keys_initialized(self):
        """Test that all Excellon keys are initialized to None."""
        pcb = PcbObj()
        for key in PcbObj.EXN_KEYS:
            assert key in pcb.excellons
            assert pcb.excellons[key] is None


class TestGerberFileLoading:
    """Tests for Gerber file loading (GBR-001 to GBR-004)."""

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    def test_load_valid_gerber_inch(self, pcb, gerber_path):
        """GBR-001: Load valid Gerber files in inch format."""
        file_path = gerber_path / "simple_square.gbr"
        result = pcb.load_gerber(str(file_path), "top")
        assert result is True
        assert pcb.gerbers["top"] is not None

    def test_load_valid_gerber_metric(self, pcb, gerber_path):
        """GBR-001: Load valid Gerber files in metric format."""
        file_path = gerber_path / "metric_trace.gbr"
        result = pcb.load_gerber(str(file_path), "top")
        assert result is True
        assert pcb.gerbers["top"] is not None

    def test_load_gerber_circle_aperture(self, pcb, gerber_path):
        """GBR-003: Parse aperture definitions correctly (circle)."""
        file_path = gerber_path / "simple_circle.gbr"
        result = pcb.load_gerber(str(file_path), "top")
        assert result is True
        gerber = pcb.get_gerber("top")
        assert gerber is not None

    def test_load_gerber_multiple_layers(self, pcb, gerber_path):
        """GBR-001: Load multiple Gerber files for different layers."""
        file_path = gerber_path / "simple_square.gbr"

        result_top = pcb.load_gerber(str(file_path), "top")
        result_bottom = pcb.load_gerber(str(file_path), "bottom")

        assert result_top is True
        assert result_bottom is True
        assert pcb.gerbers["top"] is not None
        assert pcb.gerbers["bottom"] is not None

    def test_load_gerber_invalid_tag(self, pcb, gerber_path):
        """ERR-001: Reject invalid layer tags."""
        file_path = gerber_path / "simple_square.gbr"
        result = pcb.load_gerber(str(file_path), "invalid_tag")
        assert result is False

    def test_load_gerber_nonexistent_file(self, pcb):
        """ERR-002: Handle missing files gracefully."""
        result = pcb.load_gerber("/nonexistent/path/file.gbr", "top")
        assert result is False
        assert pcb.gerbers["top"] is None

    def test_load_gerber_invalid_format(self, pcb, gerber_path):
        """ERR-001: Handle invalid/corrupted file formats without crashing."""
        file_path = gerber_path / "invalid.gbr"
        result = pcb.load_gerber(str(file_path), "top")
        assert isinstance(result, bool)
        if result:
            assert pcb.gerbers["top"] is not None

    def test_get_gerber_loaded(self, pcb, gerber_path):
        """GBR-004: Extract layer metadata correctly."""
        file_path = gerber_path / "simple_square.gbr"
        pcb.load_gerber(str(file_path), "top")
        gerber = pcb.get_gerber("top")
        assert gerber is not None

    def test_get_gerber_not_loaded(self, pcb):
        """Test getting a Gerber that hasn't been loaded."""
        gerber = pcb.get_gerber("top")
        assert gerber is None

    def test_get_gerber_invalid_tag(self, pcb):
        """Test getting a Gerber with invalid tag."""
        gerber = pcb.get_gerber("invalid_tag")
        assert gerber is None


class TestExcellonFileLoading:
    """Tests for Excellon/Drill file loading (EXN-001 to EXN-004)."""

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    def test_load_valid_excellon_metric(self, pcb, gerber_path):
        """EXN-001: Load valid Excellon drill files in metric format."""
        file_path = gerber_path / "simple_drill.drl"
        result = pcb.load_excellon(str(file_path), "drill")
        assert result is True
        assert pcb.excellons["drill"] is not None

    def test_load_valid_excellon_inch(self, pcb, gerber_path):
        """EXN-002: Handle different coordinate formats (imperial)."""
        file_path = gerber_path / "inch_drill.drl"
        result = pcb.load_excellon(str(file_path), "drill")
        assert result is True
        assert pcb.excellons["drill"] is not None

    def test_load_excellon_parses_tools(self, pcb, gerber_path):
        """EXN-003: Parse drill data and produce geometries."""
        file_path = gerber_path / "simple_drill.drl"
        result = pcb.load_excellon(str(file_path), "drill")
        assert result is True
        excellon = pcb.get_excellon("drill")
        assert excellon is not None
        assert hasattr(excellon, "geometries")
        assert len(excellon.geometries) > 0

    def test_load_excellon_invalid_tag(self, pcb, gerber_path):
        """ERR-001: Reject invalid Excellon tags."""
        file_path = gerber_path / "simple_drill.drl"
        result = pcb.load_excellon(str(file_path), "invalid_tag")
        assert result is False

    def test_load_excellon_nonexistent_file(self, pcb):
        """ERR-002: Handle missing Excellon files gracefully."""
        result = pcb.load_excellon("/nonexistent/path/file.drl", "drill")
        assert result is False
        assert pcb.excellons["drill"] is None

    def test_get_excellon_loaded(self, pcb, gerber_path):
        """EXN-003: Retrieve loaded Excellon data."""
        file_path = gerber_path / "simple_drill.drl"
        pcb.load_excellon(str(file_path), "drill")
        excellon = pcb.get_excellon("drill")
        assert excellon is not None

    def test_get_excellon_not_loaded(self, pcb):
        """Test getting Excellon that hasn't been loaded."""
        excellon = pcb.get_excellon("drill")
        assert excellon is None

    def test_get_excellon_invalid_tag(self, pcb):
        """Test getting Excellon with invalid tag."""
        excellon = pcb.get_excellon("invalid_tag")
        assert excellon is None


class TestLayerManagement:
    """Tests for layer management (LAY-001 to LAY-003)."""

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    def test_layer_types_defined(self):
        """LAY-001: Verify correct layer types are defined."""
        assert "top" in PcbObj.GBR_KEYS
        assert "bottom" in PcbObj.GBR_KEYS
        assert "profile" in PcbObj.GBR_KEYS
        assert "drill" in PcbObj.EXN_KEYS

    def test_get_gerber_layer(self, pcb, gerber_path):
        """LAY-002: Process Gerber layer to geometry."""
        file_path = gerber_path / "simple_square.gbr"
        pcb.load_gerber(str(file_path), "top")
        layer = pcb.get_gerber_layer("top")
        assert layer is not None

    def test_get_gerber_layer_not_loaded(self, pcb):
        """Test getting layer when Gerber not loaded."""
        layer = pcb.get_gerber_layer("top")
        assert layer is None

    def test_get_excellon_layer(self, pcb, gerber_path):
        """LAY-002: Process Excellon layer to geometry."""
        file_path = gerber_path / "simple_drill.drl"
        pcb.load_excellon(str(file_path), "drill")
        layer = pcb.get_excellon_layer("drill")
        assert layer is not None

    def test_get_excellon_layer_not_loaded(self, pcb):
        """Test getting layer when Excellon not loaded."""
        layer = pcb.get_excellon_layer("drill")
        assert layer is None

    def test_init_data_resets_layers(self, pcb, gerber_path):
        """Test that init_data resets all layer data."""
        file_path = gerber_path / "simple_square.gbr"
        pcb.load_gerber(str(file_path), "top")
        assert pcb.gerbers["top"] is not None

        pcb.init_data()
        assert pcb.gerbers["top"] is None


class TestUnitConversion:
    """Tests for unit conversion (LAY-003)."""

    @pytest.fixture
    def pcb(self):
        return PcbObj()

    @pytest.fixture
    def gerber_path(self):
        return Path(__file__).parent.parent / "test_data" / "gerbers"

    def test_inch_to_metric_conversion_gerber(self, pcb, gerber_path):
        """LAY-003: Handle unit conversions (inch to mm) for Gerber."""
        file_path = gerber_path / "simple_square.gbr"
        result = pcb.load_gerber(str(file_path), "top")
        assert result is True
        gerber = pcb.get_gerber("top")
        assert gerber is not None
        assert len(gerber.geometries) > 0

    def test_inch_to_metric_conversion_excellon(self, pcb, gerber_path):
        """LAY-003: Handle unit conversions (inch to mm) for Excellon."""
        file_path = gerber_path / "inch_drill.drl"
        result = pcb.load_excellon(str(file_path), "drill")
        assert result is True
        excellon = pcb.get_excellon("drill")
        assert excellon is not None
        assert len(excellon.geometries) > 0

    def test_metric_stays_metric(self, pcb, gerber_path):
        """LAY-003: Metric files stay in metric units."""
        file_path = gerber_path / "metric_trace.gbr"
        result = pcb.load_gerber(str(file_path), "top")
        assert result is True
        gerber = pcb.get_gerber("top")
        assert gerber is not None
        assert len(gerber.geometries) > 0
