import pytest
from shapely import geometry as shg
from shapely.geometry import LineString, Point

from TheAntFarm.shape_core.path_manager import Gapper, MachinePath, remap_invalid_ids


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

class TestMachinePathDrilling:
    """Drilling: hole position per polygon part, bit selection, DRC of the bits."""

    class _GeomStub:
        """Minimal stand-in for Geom/FakeGeom: MachinePath only reads ``.geom``."""

        def __init__(self, geom):
            self.geom = geom

    @staticmethod
    def _circle(x, y, diameter, segments=64):
        return Point(x, y).buffer(diameter / 2.0, quad_segs=segments // 4)

    @pytest.fixture
    def machine_path(self):
        path = MachinePath("test_drill", "drill")
        path.cfg["optimize"] = False
        return path

    @staticmethod
    def _bit_diameters(machine_path):
        return sorted(bit for (bit, _kind), _paths in machine_path.path)

    def test_multipart_hole_is_drilled_at_every_part(self, machine_path):
        """A hole made of two polygons used to raise IndexError (c.coords[j])."""
        hole = shg.MultiPolygon([self._circle(0, 0, 0.8), self._circle(5, 0, 0.8)])
        machine_path.load_geom([self._GeomStub(hole)])

        drilled = machine_path.execute_drill()

        assert drilled == [True]
        (bit, kind), paths = machine_path.path[0]
        coords = list(paths[0].coords)
        assert kind == "drill"
        assert len(coords) == 2
        assert sorted(round(c[0], 3) for c in coords) == [0.0, 5.0]

    def test_single_hole_bit_gets_a_valid_path(self, machine_path):
        """One hole per bit must not produce an invalid one-point LineString."""
        machine_path.load_geom([self._GeomStub(self._circle(1.0, 2.0, 0.8))])

        drilled = machine_path.execute_drill()

        assert drilled == [True]
        line = machine_path.path[0][1][0]
        assert len(line.coords) == 2
        assert line.length == pytest.approx(0.0, abs=1e-9)

    def test_hole_smaller_than_every_bit_is_not_drilled(self, machine_path):
        machine_path.cfg["bits_diameter"] = [0.8]
        machine_path.load_geom([self._GeomStub(self._circle(0, 0, 0.5))])

        drilled = machine_path.execute_drill()

        assert drilled == [False]
        assert machine_path.path == []

    def test_bit_with_same_diameter_as_hole_is_selected(self, machine_path):
        """Regression: the inscribed diameter is slightly smaller than the nominal one."""
        machine_path.cfg["bits_diameter"] = [0.8]
        machine_path.load_geom([self._GeomStub(self._circle(0, 0, 0.8))])

        assert machine_path.execute_drill() == [True]
        assert machine_path.path

    def test_largest_fitting_bit_is_selected(self, machine_path):
        machine_path.cfg["bits_diameter"] = [1.0, 0.8, 0.5]
        machine_path.load_geom(
            [
                self._GeomStub(self._circle(0, 0, 1.0)),
                self._GeomStub(self._circle(5, 0, 0.6)),
            ]
        )

        assert machine_path.execute_drill() == [True, True]
        assert self._bit_diameters(machine_path) == [0.5, 1.0]

    def test_partially_drillable_hole_is_reported(self, machine_path):
        """A hole is reported as drilled only when every part has been drilled."""
        machine_path.cfg["bits_diameter"] = [0.8]
        machine_path.load_geom(
            [
                self._GeomStub(self._circle(0, 0, 0.8)),
                self._GeomStub(shg.MultiPolygon([self._circle(5, 0, 0.8), self._circle(6, 0, 0.4)])),
            ]
        )

        assert machine_path.execute_drill() == [True, False]

    def test_not_to_drill_is_respected(self, machine_path):
        machine_path.load_geom(
            [
                self._GeomStub(self._circle(0, 0, 0.8)),
                self._GeomStub(self._circle(5, 0, 0.8)),
            ]
        )

        drilled = machine_path.execute_drill(not_to_drill=[True, False])

        assert drilled == [False, True]
        assert self._bit_diameters(machine_path) == [0.8]

    def test_no_bits_defined(self, machine_path):
        machine_path.cfg["bits_diameter"] = []
        machine_path.load_geom([self._GeomStub(self._circle(0, 0, 0.8))])

        assert machine_path.execute_drill() == [False]


class _GeomStub:
    """Minimal stand-in for Geom/FakeGeom: MachinePath only reads ``.geom``."""

    def __init__(self, geom):
        self.geom = geom


class TestCheckMinArea:
    """check_min_area must report the old index of every surviving polygon."""

    @pytest.fixture
    def machine_path(self):
        return MachinePath("test_gerber", "gerber")

    def test_small_polygon_is_dropped_and_old_indices_are_kept(self, machine_path):
        small = shg.box(0, 0, 0.05, 0.05)  # area 0.0025 < MIN_AREA
        big = shg.box(0, 0, 2, 2)
        big2 = shg.box(5, 0, 7, 2)

        polygons, kept_indices = machine_path.check_min_area([small, big, big2])

        assert len(polygons) == 2
        assert kept_indices == [1, 2]

    def test_nothing_is_dropped(self, machine_path):
        polygons, kept_indices = machine_path.check_min_area([shg.box(0, 0, 2, 2)])
        assert len(polygons) == 1
        assert kept_indices == [0]

    def test_empty_list(self, machine_path):
        assert machine_path.check_min_area([]) == ([], [])


class TestRemapInvalidIds:
    """DRC indices computed before filtering must be remapped after it."""

    def test_without_filtering(self):
        assert remap_invalid_ids([0, 1, 2], [1]) == [1]

    def test_after_dropping_an_element(self):
        # the polygon that was at position 2 is now at position 1
        assert remap_invalid_ids([0, 2, 3], [2]) == [1]

    def test_invalid_element_dropped(self):
        assert remap_invalid_ids([0, 2], [1]) == []

    def test_no_invalid_ids(self):
        assert remap_invalid_ids([0, 1], []) == []

    def test_empty_kept_indices(self):
        assert remap_invalid_ids([], [0, 1]) == []


class TestExecuteGerberInvalidIds:
    """The invalid path indices of the generated path must index the path list."""

    def test_invalid_path_ids_are_valid_path_indices(self):
        machine_path = MachinePath("test_gerber", "gerber")
        machine_path.load_geom([_GeomStub(shg.box(0, 0, 10, 10))])

        machine_path.execute_gerber()

        _tool, paths, invalid_path_ids = machine_path.path[0]
        assert paths
        assert all(0 <= path_id < len(paths) for path_id in invalid_path_ids)
