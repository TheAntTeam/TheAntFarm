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


class TestPublicApi:
    """The package exposes a stable API instead of the single modules."""

    def test_core_classes_are_exported(self):
        import importlib

        shape_core = importlib.import_module("TheAntFarm.shape_core")

        for name in (
            "GCoder",
            "GCodeParser",
            "GCodeMacro",
            "MachinePath",
            "Gapper",
            "ToolPath",
            "PcbObj",
            "Geom",
            "Macros",
            "MacroContext",
            "AlignManager",
            "CommandManager",
            "DrillGcodeConverter",
        ):
            assert hasattr(shape_core, name), name
            assert name in shape_core.__all__

    def test_configuration_helpers_are_exported(self):
        import importlib

        shape_core = importlib.import_module("TheAntFarm.shape_core")

        assert "default_config" in shape_core.__all__
        assert "merge_config" in shape_core.__all__
        assert shape_core.PROBE_DEFAULTS["tool_probe_min"] == -11.0

    def test_visual_layer_is_imported_on_demand(self):
        import importlib
        import sys

        shape_core = importlib.import_module("TheAntFarm.shape_core")
        module_name = "TheAntFarm.shape_core.visual_manager"

        visual_layer = shape_core.VisualLayer

        assert visual_layer.__name__ == "VisualLayer"
        assert module_name in sys.modules

    def test_unknown_name_raises_attribute_error(self):
        import importlib

        import pytest

        shape_core = importlib.import_module("TheAntFarm.shape_core")

        with pytest.raises(AttributeError):
            shape_core.NotAnExport

    def test_dir_lists_the_public_names(self):
        import importlib

        shape_core = importlib.import_module("TheAntFarm.shape_core")

        assert "GCoder" in dir(shape_core)
        assert "VisualLayer" in dir(shape_core)
