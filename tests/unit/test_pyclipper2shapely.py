import pytest

from TheAntFarm.shape_core.pyclipper2shapely import (
    _contour_to_linear_ring,
    polytree_to_shapely,
)


class TestPyClipper2Shapely:
    def test_contour_to_linear_ring_valid(self):
        contour = [(0, 0), (10, 0), (10, 10), (0, 10)]
        ring = _contour_to_linear_ring(contour, scale=1.0)
        assert ring.is_valid
        assert ring.is_closed

    def test_contour_to_linear_ring_empty(self):
        contour = []
        ring = _contour_to_linear_ring(contour, scale=1.0)
        assert ring.is_empty

    def test_contour_to_linear_ring_single_point(self):
        contour = [(0, 0)]
        ring = _contour_to_linear_ring(contour, scale=1.0)
        assert ring.is_empty

    def test_contour_to_linear_ring_two_points(self):
        contour = [(0, 0), (1, 1)]
        ring = _contour_to_linear_ring(contour, scale=1.0)
        assert ring.is_empty

    def test_contour_to_linear_ring_with_scale(self):
        contour = [(0, 0), (1000, 0), (1000, 1000), (0, 1000)]
        ring = _contour_to_linear_ring(contour, scale=1000.0)
        assert ring.is_valid

    def test_polytree_to_shapely_function_exists(self):
        assert callable(polytree_to_shapely)

    def test_contour_to_linear_ring_returns_linear_ring(self):
        contour = [(0, 0), (5, 0), (5, 5), (0, 5)]
        ring = _contour_to_linear_ring(contour, scale=1.0)
        from shapely.geometry import LinearRing
        assert isinstance(ring, LinearRing)

    def test_contour_to_linear_ring_large_contour(self):
        contour = [(i*10, i*10) for i in range(100)]
        ring = _contour_to_linear_ring(contour, scale=1.0)
        assert ring is not None