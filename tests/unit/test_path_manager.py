import pytest
from shapely.geometry import LineString

from TheAntFarm.shape_core.path_manager import Gapper


class TestGapper:
    @pytest.fixture
    def cfg(self):
        return {
            "taps_length": 0.5,
            "tool_diameter": 0.2,
        }

    @pytest.fixture
    def path(self):
        return LineString([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])

    @pytest.fixture
    def gapper(self, path, cfg):
        return Gapper(path, cfg)

    def test_init(self, path, cfg):
        gapper = Gapper(path, cfg)
        assert gapper.cfg == cfg
        assert gapper.in_path == path
        assert gapper.gap_dim == 0.7

    def test_rotate(self):
        result = Gapper.rotate([1, 2, 3, 4], 2)
        assert result == [3, 4, 1, 2]

    def test_rotate_zero(self):
        result = Gapper.rotate([1, 2, 3], 0)
        assert result == [1, 2, 3]

    def test_get_available_strategies(self, gapper):
        strategies = gapper.get_available_strategies()
        assert "none" in strategies
        assert "2h" in strategies
        assert "2v" in strategies
        assert "4p" in strategies
        assert "4h" in strategies
        assert "4v" in strategies
        assert "8p" in strategies
        assert "4x" in strategies

    def test_add_taps_on_external_path_strategy_none(self, gapper):
        result = gapper.add_taps_on_external_path(strategy="none")
        assert len(result) > 0

    def test_add_taps_on_external_path_strategy_2h(self, gapper):
        result = gapper.add_taps_on_external_path(strategy="2h")
        assert len(result) == 2

    def test_add_taps_on_external_path_strategy_4p(self, gapper):
        result = gapper.add_taps_on_external_path(strategy="4p")
        assert len(result) == 4

    def test_add_taps_on_external_path_strategy_invalid(self, gapper):
        result = gapper.add_taps_on_external_path(strategy="invalid")
        assert len(result) > 0