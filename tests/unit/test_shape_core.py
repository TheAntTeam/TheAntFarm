import pytest

from TheAntFarm.shape_core.gcode_manager import GCoder
from TheAntFarm.shape_core.geometry_manager import Geom, merge_polygons


class TestGeometryManager:
    @pytest.fixture
    def geometry(self):
        # Create a simple square geometry
        gdata = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],  # Square with coordinates
            "polarity": "dark",  # dark for filled shapes
            "closed": True,  # closed polygon
        }
        return Geom(gdata)

    def test_initialization(self, geometry):
        """Test that Geometry Manager initializes correctly"""
        assert isinstance(geometry, Geom)
        assert geometry.geom is not None  # Should have a valid geometry
        assert geometry.closed is True  # Should be a closed polygon

    def test_merge_polygons(self):
        """Test merging polygons"""
        # Create two overlapping squares
        square1_data = {"points": [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)], "polarity": "dark", "closed": True}
        square2_data = {"points": [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)], "polarity": "dark", "closed": True}
        geom1 = Geom(square1_data)
        geom2 = Geom(square2_data)

        layer, others = merge_polygons([geom1, geom2])  # Pass the Geom objects directly
        assert len(layer) > 0  # Should have at least one merged polygon
        assert len(others) == 0  # Should have no "other" geometries

    def test_invalid_geometry(self):
        """Test handling invalid geometry"""
        with pytest.raises(Exception):  # Replace with specific exception
            merge_polygons(None, None)


class TestGCoder:
    @pytest.fixture
    def gcoder(self):
        return GCoder(tag="test_gcoder")  # Provide a tag to identify this GCoder instance

    def test_initialization(self, gcoder):
        """Test that GCoder initializes correctly"""
        assert isinstance(gcoder, GCoder)
        assert gcoder.tag == "test_gcoder"  # Verify the tag was set correctly

    def test_generate_gcode(self, gcoder):
        """Test G-code generation from geometry"""
        # TODO: Implement with sample geometry
        pass
