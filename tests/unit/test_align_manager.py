import numpy as np
import pytest

from TheAntFarm.shape_core.align_manager import AlignManager, TpsCoefficients


class TestTpsCoefficients:
    @pytest.fixture
    def sample_sampled_points(self):
        """Sample points for TPS calculation."""
        return [
            ((0.0, 0.0), (0.0, 0.0)),
            ((1.0, 0.0), (1.1, 0.1)),
            ((0.0, 1.0), (-0.1, 1.1)),
            ((1.0, 1.0), (1.0, 1.0)),
        ]

    def test_init_with_valid_sampled_points(self, sample_sampled_points):
        """Test TpsCoefficients initialization with valid sampled points."""
        tps = TpsCoefficients(sample_sampled_points)
        assert tps.cx is not None
        assert tps.cy is not None

    def test_init_with_empty_sampled_points(self):
        """Test TpsCoefficients initialization with empty list - raises IndexError."""
        with pytest.raises(IndexError):
            TpsCoefficients([])

    def test_load_empty_sampled_points(self):
        """Test load_sampled_points with empty list - raises IndexError."""
        align_mgr = AlignManager()
        with pytest.raises(IndexError):
            align_mgr.load_sampled_points([])

    def test_is_sampled_point_loaded_true(self):
        """Test is_sampled_point_loaded returns True when points loaded."""
        align_mgr = AlignManager()
        align_mgr.sampled_points = [((0.0, 0.0), (0.0, 0.0))]
        assert align_mgr.is_sampled_point_loaded() is True

    def test_is_sampled_point_loaded_false(self):
        """Test is_sampled_point_loaded returns False when no points."""
        align_mgr = AlignManager()
        assert align_mgr.is_sampled_point_loaded() is False

    def test_update_tps_coefficients(self):
        """Test update_tps_coefficients creates new TPS coefficients."""
        align_mgr = AlignManager()
        sampled_points = [
            ((0.0, 0.0), (0.0, 0.0)),
            ((1.0, 0.0), (1.1, 0.1)),
            ((0.0, 1.0), (-0.1, 1.1)),
        ]
        align_mgr.sampled_points = sampled_points
        align_mgr.update_tps_coefficients()
        assert align_mgr.tps_coeff is not None

    def test_compute_points_transform_with_z(self):
        """Test compute_points_transform with 3D points (x, y, z)."""
        align_mgr = AlignManager()
        sampled_points = [
            ((0.0, 0.0), (0.0, 0.0)),
            ((1.0, 0.0), (1.1, 0.1)),
            ((0.0, 1.0), (-0.1, 1.1)),
        ]
        align_mgr.load_sampled_points(sampled_points)

        points = [(0.5, 0.5, 1.0), (0.0, 1.0, 2.0)]
        result = align_mgr.compute_points_transform(points)
        assert result is not None
        assert len(result) == 2
        assert len(result[0]) == 3

    def test_compute_points_transform_without_z(self):
        """Test compute_points_transform with 2D points (x, y)."""
        align_mgr = AlignManager()
        sampled_points = [
            ((0.0, 0.0), (0.0, 0.0)),
            ((1.0, 0.0), (1.1, 0.1)),
            ((0.0, 1.0), (-0.1, 1.1)),
        ]
        align_mgr.load_sampled_points(sampled_points)

        points = [(0.5, 0.5), (0.0, 1.0)]
        result = align_mgr.compute_points_transform(points)
        assert result is not None
        assert len(result) == 2
        assert len(result[0]) == 2

    def test_compute_points_transform_no_tps_coeff(self):
        """Test compute_points_transform returns None when no TPS coefficients."""
        align_mgr = AlignManager()
        points = [(0.5, 0.5), (0.0, 1.0)]
        result = align_mgr.compute_points_transform(points)
        assert result is None

    def test_compute_points_transform_empty_points(self):
        """Test compute_points_transform returns None with empty points."""
        align_mgr = AlignManager()
        sampled_points = [
            ((0.0, 0.0), (0.0, 0.0)),
            ((1.0, 0.0), (1.1, 0.1)),
            ((0.0, 1.0), (-0.1, 1.1)),
        ]
        align_mgr.load_sampled_points(sampled_points)
        result = align_mgr.compute_points_transform([])
        assert result is None

    def test_compute_points_transform_single_point(self):
        """Test compute_points_transform with single point."""
        align_mgr = AlignManager()
        sampled_points = [
            ((0.0, 0.0), (0.0, 0.0)),
            ((1.0, 0.0), (1.1, 0.1)),
            ((0.0, 1.0), (-0.1, 1.1)),
        ]
        align_mgr.load_sampled_points(sampled_points)

        points = [(0.5, 0.5)]
        result = align_mgr.compute_points_transform(points)
        assert result is not None
        assert len(result) == 1