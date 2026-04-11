"""
Tests for Geometry Manager - Shape Conversion & Path Processing
Covers requirements: GEO-001 to GEO-003, PTH-001 to PTH-004, MRG-001 to MRG-003
"""

import pytest
from shapely.geometry import Polygon
from shapely import geometry as shg

from TheAntFarm.shape_core.geometry_manager import (
    Geom,
    fill_holes_sh,
    get_bbox_area_sh,
    get_poly_diameter,
    merge_polygons,
    merge_polygons_path,
    offset_polygon,
    offset_polygon_holes,
)


class TestGeomClass:
    """Tests for the Geom class (GEO-001 to GEO-003)."""

    def test_create_simple_polygon(self):
        """GEO-001: Convert simple polygon data to geometry."""
        gdata = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        assert geom is not None
        assert geom.closed is True
        assert geom.polarity == "dark"
        assert geom.geom is not None
        assert geom.geom.is_valid

    def test_create_open_linestring(self):
        """GEO-001: Convert open path data to LineString."""
        gdata = {
            "points": [(0, 0), (1, 0), (1, 1)],
            "polarity": "dark",
            "closed": False,
        }
        geom = Geom(gdata)
        assert geom is not None
        assert geom.closed is False
        assert geom.geom is not None
        assert geom.geom.geom_type == "LineString"

    def test_create_complex_polygon_with_holes(self):
        """GEO-001: Convert polygon with holes."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(3, 3), (7, 3), (7, 7), (3, 7), (3, 3)]
        gdata = {
            "points": [exterior, hole],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata, complex=True)
        assert geom is not None
        assert geom.geom is not None
        assert geom.geom.geom_type == "Polygon"
        assert len(list(geom.geom.interiors)) == 1

    def test_geom_empty_points(self):
        """Test Geom with empty points."""
        gdata = {
            "points": [],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        assert geom.geom is None

    def test_geom_none_points(self):
        """Test Geom with None points."""
        gdata = {
            "points": None,
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        assert geom.geom is None

    def test_polygon_orientation(self):
        """GEO-001: Verify polygon orientation is correct (counter-clockwise)."""
        gdata = {
            "points": [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        assert geom.geom.exterior.is_ccw


class TestMergePolygons:
    """Tests for polygon merging (MRG-001 to MRG-003)."""

    def test_merge_two_overlapping_polygons(self):
        """MRG-001: Merge overlapping geometries."""
        square1_data = {
            "points": [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        square2_data = {
            "points": [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)],
            "polarity": "dark",
            "closed": True,
        }
        geom1 = Geom(square1_data)
        geom2 = Geom(square2_data)

        layer, others = merge_polygons([geom1, geom2])
        assert len(layer) == 1
        assert len(others) == 0
        assert layer[0].geom.area > geom1.geom.area
        assert layer[0].geom.area > geom2.geom.area

    def test_merge_non_overlapping_polygons(self):
        """MRG-001: Merge non-overlapping geometries keeps them separate."""
        square1_data = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        square2_data = {
            "points": [(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)],
            "polarity": "dark",
            "closed": True,
        }
        geom1 = Geom(square1_data)
        geom2 = Geom(square2_data)

        layer, others = merge_polygons([geom1, geom2])
        assert len(layer) == 2
        assert len(others) == 0

    def test_merge_with_clear_polarity(self):
        """MRG-002: Handle boolean difference operation (dark - clear)."""
        dark_data = {
            "points": [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        clear_data = {
            "points": [(3, 3), (7, 3), (7, 7), (3, 7), (3, 3)],
            "polarity": "clear",
            "closed": True,
        }
        dark_geom = Geom(dark_data)
        clear_geom = Geom(clear_data)

        layer, others = merge_polygons([dark_geom, clear_geom])
        assert len(layer) >= 1
        total_area = sum(g.geom.area for g in layer)
        assert total_area < dark_geom.geom.area

    def test_merge_open_paths_go_to_others(self):
        """MRG-001: Open paths should be collected in 'others'."""
        closed_data = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        open_data = {
            "points": [(2, 0), (3, 0), (3, 1)],
            "polarity": "dark",
            "closed": False,
        }
        closed_geom = Geom(closed_data)
        open_geom = Geom(open_data)

        layer, others = merge_polygons([closed_geom, open_geom])
        assert len(layer) == 1
        assert len(others) == 1


class TestMergePolygonsPath:
    """Tests for merge_polygons_path function."""

    def test_merge_shapely_polygons(self):
        """MRG-001: Merge Shapely polygon objects."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])

        result = merge_polygons_path([poly1, poly2])
        assert len(result) == 1
        assert result[0].area > poly1.area


class TestOffsetPolygon:
    """Tests for polygon offset operations."""

    def test_offset_polygon_outward(self):
        """PTH-001: Offset polygon outward for isolation routing."""
        gdata = {
            "points": [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        original_area = geom.geom.area

        offset_geom = offset_polygon(geom, 1.0)
        assert offset_geom is not None
        assert offset_geom.area > original_area

    def test_offset_polygon_inward(self):
        """PTH-001: Offset polygon inward."""
        gdata = {
            "points": [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        original_area = geom.geom.area

        offset_geom = offset_polygon(geom, -1.0)
        assert offset_geom is not None
        assert offset_geom.area < original_area

    def test_offset_polygon_too_much_returns_empty(self):
        """PTH-001: Large inward offset should return empty geometry."""
        gdata = {
            "points": [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)

        offset_geom = offset_polygon(geom, -10.0)
        assert offset_geom.is_empty

    def test_offset_shapely_polygon_directly(self):
        """PTH-001: Offset Shapely polygon directly."""
        poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        original_area = poly.area

        offset_poly = offset_polygon(poly, 1.0, shapely_poly=True)
        assert offset_poly is not None
        assert offset_poly.area > original_area


class TestGeometryUtilities:
    """Tests for geometry utility functions."""

    def test_fill_holes_single_polygon(self):
        """MRG-003: Fill holes in polygon."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(3, 3), (7, 3), (7, 7), (3, 7), (3, 3)]
        poly_with_hole = Polygon(exterior, [hole])

        filled = fill_holes_sh(poly_with_hole)
        assert filled.area > poly_with_hole.area
        assert len(list(filled.interiors)) == 0

    def test_get_bbox_area(self):
        """Test bounding box area calculation."""
        poly = Polygon([(0, 0), (5, 0), (5, 3), (0, 3), (0, 0)])
        area = get_bbox_area_sh(poly)
        assert area == 15.0

    def test_get_poly_diameter(self):
        """Test polygon diameter calculation."""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        diameters = get_poly_diameter(poly)
        assert len(diameters) == 1
        assert diameters[0] > 0


class TestPathProcessing:
    """Tests for path processing (PTH-001 to PTH-004)."""

    def test_polygon_simplification(self):
        """MRG-003: Polygon simplification removes redundant vertices."""
        points = []
        for i in range(100):
            points.append((i * 0.1, 0))
        for i in range(100):
            points.append((10, i * 0.1))
        for i in range(100):
            points.append((10 - i * 0.1, 10))
        for i in range(100):
            points.append((0, 10 - i * 0.1))
        points.append((0, 0))

        gdata = {
            "points": points,
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)

        simplified = geom.geom.simplify(0.1, preserve_topology=True)
        assert len(simplified.exterior.coords) < len(points)

    def test_polygon_validation(self):
        """GEO-001: Created polygons should be valid."""
        gdata = {
            "points": [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        assert geom.geom.is_valid
        assert not geom.geom.is_empty

    def test_fill_holes_sh_multipolygon(self):
        """Test fill_holes_sh with MultiPolygon."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(3, 0), (5, 0), (5, 2), (3, 2), (3, 0)])
        multipoly = shg.MultiPolygon([poly1, poly2])
        result = fill_holes_sh(multipoly)
        assert result.geom_type == "MultiPolygon"

    def test_fill_holes_sh_single_polygon(self):
        """Test fill_holes_sh with single Polygon."""
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        result = fill_holes_sh(poly)
        assert result.geom_type == "Polygon"

    def test_get_poly_diameter_multipolygon(self):
        """Test get_poly_diameter with MultiPolygon."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(5, 0), (7, 0), (7, 2), (5, 2), (5, 0)])
        multipoly = shg.MultiPolygon([poly1, poly2])
        diameter = get_poly_diameter(multipoly)
        assert isinstance(diameter, list) and len(diameter) == 2

    def test_get_bbox_area_sh(self):
        """Test get_bbox_area_sh calculation."""
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        area = get_bbox_area_sh(poly)
        assert area == 4.0

    def test_offset_polygon_holes(self):
        """Test offset_polygon_holes with holes."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(3, 3), (7, 3), (7, 7), (3, 7), (3, 3)]
        gdata = {
            "points": [exterior, hole],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata, complex=True)
        offset_result = offset_polygon_holes(geom, 0.5)
        assert offset_result is not None

    def test_offset_polygon_positive(self):
        """Test offset_polygon with positive offset (outward)."""
        gdata = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        result = offset_polygon(geom, 0.1)
        assert result.area > geom.geom.area

    def test_offset_polygon_negative(self):
        """Test offset_polygon with negative offset (inward)."""
        gdata = {
            "points": [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        result = offset_polygon(geom, -0.1)
        assert result.area < geom.geom.area

    def test_offset_polygon_shapely_poly(self):
        """Test offset_polygon with shapely_poly=True."""
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        result = offset_polygon(poly, 0.1, shapely_poly=True)
        assert result.area > poly.area

    def test_offset_polygon_returns_none_when_offset_too_large(self):
        """Test offset_polygon returns None when offset is too large."""
        gdata = {
            "points": [(0, 0), (0.1, 0), (0.1, 0.1), (0, 0.1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        result = offset_polygon(geom, -100)
        assert result is None or result.is_empty

    def test_merge_polygons_path(self):
        """Test merge_polygons_path function."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        result = merge_polygons_path([poly1, poly2])
        assert len(result) > 0

    def test_merge_polygons_path_empty(self):
        """Test merge_polygons_path with empty list."""
        result = merge_polygons_path([])
        assert len(result) == 0 or (len(result) == 1 and result[0].is_empty)

    def test_geom_with_single_exterior_and_holes(self):
        """Test Geom with single exterior and multiple holes."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole1 = [(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)]
        hole2 = [(6, 2), (8, 2), (8, 4), (6, 4), (6, 4)]
        gdata = {
            "points": [exterior, hole1, hole2],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata, complex=True)
        assert geom is not None
        assert len(list(geom.geom.interiors)) == 2

    def test_merge_polygons_path_multipolygon_result(self):
        """Test merge_polygons_path returns list when result is MultiPolygon."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(3, 0), (5, 0), (5, 2), (3, 2), (3, 0)])
        poly3 = Polygon([(6, 0), (8, 0), (8, 2), (6, 2), (6, 0)])
        result = merge_polygons_path([poly1, poly2, poly3])
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_get_max_distance(self):
        """Test get_max_distance function."""
        from TheAntFarm.shape_core.geometry_manager import get_max_distance
        coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        center = shg.Point(0.5, 0.5)
        max_dist = get_max_distance(center, coords)
        assert max_dist > 0
        assert max_dist <= 0.71

    def test_merge_polygons_with_clear_and_dark(self):
        """Test merge_polygons with mixed clear and dark polarities."""
        dark_data = {
            "points": [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        clear_data = {
            "points": [(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)],
            "polarity": "clear",
            "closed": True,
        }
        another_dark = {
            "points": [(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)],
            "polarity": "dark",
            "closed": True,
        }
        dark_geom = Geom(dark_data)
        clear_geom = Geom(clear_data)
        another_dark_geom = Geom(another_dark)

        layer, others = merge_polygons([dark_geom, clear_geom, another_dark_geom])
        assert len(layer) >= 1

    def test_merge_polygons_open_paths_go_to_others(self):
        """Test merge_polygons with open paths (non-closed)."""
        closed_data = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        open_data = {
            "points": [(5, 0), (6, 0), (6, 1)],
            "polarity": "dark",
            "closed": False,
        }
        closed_geom = Geom(closed_data)
        open_geom = Geom(open_data)

        layer, others = merge_polygons([closed_geom, open_geom])
        assert len(others) == 1

    def test_get_bbox_area_sh_with_multipolygon(self):
        """Test get_bbox_area_sh with MultiPolygon."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(5, 0), (7, 0), (7, 2), (5, 2), (5, 0)])
        multipoly = shg.MultiPolygon([poly1, poly2])
        area = get_bbox_area_sh(multipoly)
        assert area == 14.0  # (0-7) * (0-2) = 14

    def test_offset_polygon_zero_offset(self):
        """Test offset_polygon with zero offset."""
        gdata = {
            "points": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
            "polarity": "dark",
            "closed": True,
        }
        geom = Geom(gdata)
        result = offset_polygon(geom, 0)
        assert result.area == geom.geom.area

    def test_offset_polygon_shapely_poly_with_holes(self):
        """Test offset_polygon with shapely polygon that has holes."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(3, 3), (7, 3), (7, 7), (3, 7), (3, 7)]
        poly = shg.Polygon(exterior, [hole])
        result = offset_polygon(poly, 0.5, shapely_poly=True)
        assert result is not None
