import pytest
import os
from pathlib import Path
from TheAntFarm.shape_core.pcb_manager import PcbObj


class TestPcbManager:
    @pytest.fixture
    def pcb_obj(self):
        """Fixture providing a PcbObj instance"""
        return PcbObj()

    def test_initialization(self, pcb_obj):
        """Test PcbObj initialization"""
        assert pcb_obj is not None
        assert pcb_obj.gerbers is not None
        assert pcb_obj.excellons is not None
        assert len(pcb_obj.gerbers) == 5  # init_data populates keys with None values
        assert len(pcb_obj.excellons) == 1  # init_data populates keys with None values

    def test_gerber_keys(self, pcb_obj):
        """Test that GBR_KEYS contains expected layer names"""
        expected_keys = ["top", "bottom", "profile", "noncopper_top", "noncopper_bottom"]
        assert pcb_obj.GBR_KEYS == expected_keys

    def test_excellon_keys(self, pcb_obj):
        """Test that EXN_KEYS contains expected drill names"""
        expected_keys = ["drill"]
        assert pcb_obj.EXN_KEYS == expected_keys

    def test_load_gerber_invalid_tag(self, pcb_obj, tmp_path):
        """Test loading gerber with invalid tag"""
        gerber_file = tmp_path / "test.gbr"
        gerber_file.write_text("G04 Test*\nM02*")
        
        result = pcb_obj.load_gerber(str(gerber_file), "invalid_tag")
        assert result is False

    def test_load_gerber_file_not_found(self, pcb_obj):
        """Test loading gerber when file doesn't exist"""
        result = pcb_obj.load_gerber("/nonexistent/path/file.gbr", "top")
        assert result is False

    def test_load_gerber_valid_file(self, pcb_obj, tmp_path):
        """Test loading a valid gerber file"""
        # Create a minimal valid Gerber file
        gerber_file = tmp_path / "test.gbr"
        gerber_content = """G04 Test Gerber File*
%FSLAX25Y25*%
%MOIN*%
%ADD10C,0.010*%
D10*
X100Y100D02*
X200Y200D01*
M02*
"""
        gerber_file.write_text(gerber_content)
        
        result = pcb_obj.load_gerber(str(gerber_file), "top")
        # load_gerber returns None on success, only returns False on error
        assert pcb_obj.gerbers["top"] is not None
        assert "top" in pcb_obj.gerbers

    def test_layers_initialization(self, pcb_obj):
        """Test that layers dict is initialized"""
        assert pcb_obj.layers is not None
        assert len(pcb_obj.layers) == 0

    def test_arc_parameters(self, pcb_obj):
        """Test arc-related parameters"""
        assert pcb_obj.DEFAULT_ARC_SUBDIVISIONS == 64
        assert pcb_obj.arc_angle > 0
        assert pcb_obj.arc_max_len == 0.5
        assert pcb_obj.arc_min_len == 0.1

    def test_init_data(self, pcb_obj):
        """Test that init_data method can be called"""
        # Call init_data to ensure it doesn't raise an exception
        pcb_obj.init_data()
        assert pcb_obj.layers is not None
