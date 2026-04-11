import pytest
from shapely.geometry import LineString

from TheAntFarm.shape_core.gerber_path_optimizer import GerberPathOptimizer


class TestGerberPathOptimizer:
    @pytest.fixture
    def sample_lines(self):
        return [
            LineString([(0, 0), (1, 0)]),
            LineString([(1, 1), (0, 1)]),
            LineString([(2, 2), (3, 2)]),
        ]

    @pytest.fixture
    def optimizer(self, sample_lines):
        return GerberPathOptimizer(sample_lines)

    def test_init(self, sample_lines):
        opt = GerberPathOptimizer(sample_lines)
        assert opt.num_lines == 3
        assert len(opt.endpoints) == 3
        assert opt.visited == [False, False, False]

    def test_init_empty_lines(self):
        opt = GerberPathOptimizer([])
        assert opt.num_lines == 0

    def test_endpoints_extraction(self, sample_lines):
        opt = GerberPathOptimizer(sample_lines)
        assert opt.endpoints[0] == ((0, 0), (1, 0))
        assert opt.endpoints[1] == ((1, 1), (0, 1))
        assert opt.endpoints[2] == ((2, 2), (3, 2))

    def test_optimize_start_default(self, optimizer):
        result = optimizer.optimize()
        assert len(result) == 3

    def test_optimize_start_origin(self, optimizer):
        result = optimizer.optimize(start_point=(0, 0))
        assert len(result) == 3
        assert all(isinstance(line, LineString) for line in result)

    def test_optimize_start_custom(self, optimizer):
        result = optimizer.optimize(start_point=(0.5, 0.5))
        assert len(result) == 3

    def test_optimize_returns_line_strings(self, optimizer):
        result = optimizer.optimize()
        for line in result:
            assert isinstance(line, LineString)

    def test_optimize_same_length_as_input(self, sample_lines):
        opt = GerberPathOptimizer(sample_lines)
        result = opt.optimize()
        assert len(result) == len(sample_lines)

    def test_optimize_empty_lines_returns_empty(self):
        opt = GerberPathOptimizer([])
        result = opt.optimize()
        assert result == []

    def test_optimize_single_line(self):
        lines = [LineString([(0, 0), (1, 1)])]
        opt = GerberPathOptimizer(lines)
        result = opt.optimize()
        assert len(result) == 1

    def test_optimize_respects_visisted_mask(self, optimizer):
        initial_visited = optimizer.visited.copy()
        optimizer.optimize()
        assert all(initial_visited[i] == optimizer.visited[i] for i in range(len(initial_visited)))

    def test_optimize_endpoint_orientation_preserved(self):
        lines = [
            LineString([(0, 0), (1, 0)]),
            LineString([(0, 1), (1, 1)]),
        ]
        opt = GerberPathOptimizer(lines)
        result = opt.optimize(start_point=(0.5, 0.5))
        assert len(result) == 2

    def test_optimize_all_reachable(self, optimizer):
        dists = optimizer.optimize()
        assert len(dists) == optimizer.num_lines