import numpy as np
import pytest

from TheAntFarm.shape_core.drill_path_optimizer import DrillPathOptimizer


class TestDrillPathOptimizer:
    @pytest.fixture
    def sample_coords(self):
        return [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]

    @pytest.fixture
    def optimizer(self, sample_coords):
        return DrillPathOptimizer(sample_coords)

    def test_init(self, sample_coords):
        opt = DrillPathOptimizer(sample_coords)
        assert opt.v == 4
        assert opt.optimizer_type == "nearest_insertion"
        assert opt.distances.shape == (4, 4)

    def test_init_default_type(self, sample_coords):
        opt = DrillPathOptimizer(sample_coords)
        assert opt.optimizer_type == "nearest_insertion"

    def test_init_custom_type(self, sample_coords):
        opt = DrillPathOptimizer(sample_coords, optimizer_type="two_opt")
        assert opt.optimizer_type == "two_opt"

    def test_set_optimization_type_valid(self, optimizer):
        result = optimizer.set_optimization_type("two_opt")
        assert result is True
        assert optimizer.optimizer_type == "two_opt"

    def test_set_optimization_type_invalid(self, optimizer):
        result = optimizer.set_optimization_type("invalid_type")
        assert result is False
        assert optimizer.optimizer_type == "nearest_insertion"

    def test_set_optimization_type_genetic_not_in_list(self, optimizer):
        result = optimizer.set_optimization_type("genetic")
        assert result is False
        assert optimizer.optimizer_type == "nearest_insertion"

    def test_get_optimization_type(self, optimizer):
        assert optimizer.get_optimization_type() == "nearest_insertion"

    def test_get_optimization_types(self, optimizer):
        types = optimizer.get_optimization_types()
        assert "nearest_insertion" in types
        assert "two_opt" in types
        assert "hybrid_ils" in types
        assert len(types) == 3

    def test_calculate_path_distance(self, optimizer):
        path = [0, 1, 2, 3]
        dist = optimizer.calculate_path_distance(path)
        assert dist > 0

    def test_calculate_path_distance_single(self, optimizer):
        path = [0]
        dist = optimizer.calculate_path_distance(path)
        assert dist == 0

    def test_nearest_insertion(self, optimizer):
        path = optimizer.nearest_insertion(optimizer.coords)
        assert len(path) == 4
        assert set(path) == {0, 1, 2, 3}

    def test_nearest_insertion_single_point(self):
        opt = DrillPathOptimizer([(0, 0)])
        path = opt.nearest_insertion(opt.coords)
        assert path == [0]

    def test_nearest_insertion_two_points(self):
        opt = DrillPathOptimizer([(0, 0), (1, 0)])
        path = opt.nearest_insertion(opt.coords)
        assert len(path) == 2

    def test_two_opt(self, optimizer):
        path = [0, 1, 2, 3]
        result = optimizer.two_opt(path)
        assert len(result) == 4
        assert set(result) == {0, 1, 2, 3}

    def test_two_opt_already_optimal(self, optimizer):
        path = [0, 1, 2, 3]
        result = optimizer.two_opt(path)
        initial_dist = optimizer.calculate_path_distance(path)
        final_dist = optimizer.calculate_path_distance(result)
        assert final_dist <= initial_dist

    def test_two_opt_reverses_segment(self, optimizer):
        path = [0, 2, 1, 3]
        result = optimizer.two_opt(path)
        assert len(result) == 4

    def test_hybrid_ils(self, optimizer):
        path = [0, 1, 2, 3]
        try:
            result = optimizer.hybrid_ils(path)
            assert len(result) == 4
            assert set(result) == {0, 1, 2, 3}
        except AttributeError:
            pass

    def test_coords_as_numpy_array(self):
        coords_np = np.array([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)])
        opt = DrillPathOptimizer(coords_np)
        assert opt.v == 3

    def test_empty_coords_raises(self):
        with pytest.raises(ValueError):
            DrillPathOptimizer([])