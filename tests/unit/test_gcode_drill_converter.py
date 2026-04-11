import math
import pytest
import numpy as np

from TheAntFarm.shape_core.gcode_drill_converter import DrillGcodeConverter


class TestDrillGcodeConverter:
    @pytest.fixture
    def cfg(self):
        return {"default_gcode_drill_size": 0.1}

    @pytest.fixture
    def converter(self, cfg):
        return DrillGcodeConverter(cfg)

    def test_init(self, cfg):
        converter = DrillGcodeConverter(cfg)
        assert converter.cfg == cfg
        assert converter.gcode_path == ""
        assert converter.parser is not None

    def test_load_gcode(self, converter):
        converter.load_gcode("/test/path.nc")
        assert converter.gcode_path == "/test/path.nc"

    def test_load_gcode_empty(self, converter):
        converter.load_gcode("")
        assert converter.gcode_path == ""

    def test_convert_no_gcode_path(self, converter):
        result = converter.convert()
        assert result is None

    def test_convert_invalid_path(self, converter):
        converter.gcode_path = "/nonexistent/path.nc"
        result = converter.convert()
        assert result is None

    def test_convert_valid_path_no_file(self, converter, tmp_path, mocker):
        fake_path = tmp_path / "test.nc"
        fake_path.write_text("fake content")
        converter.gcode_path = str(fake_path)
        mock_parser = mocker.Mock()
        mock_parser.load_gcode_file = mocker.Mock()
        mock_parser.interp = mocker.Mock()
        mock_parser.vectorize = mocker.Mock()
        converter.parser = mock_parser
        result = converter.convert()
        mock_parser.load_gcode_file.assert_called_once()
        mock_parser.interp.assert_called_once()
        mock_parser.vectorize.assert_called_once()

    def test_get_circle_coord(self):
        result = DrillGcodeConverter.get_circle_coord(0, 0, 0, 0, 1)
        assert result == (1, 0, 0)

    def test_get_circle_coord_pi(self):
        result = DrillGcodeConverter.get_circle_coord(math.pi, 0, 0, 0, 1)
        assert abs(result[0] - -1) < 0.001
        assert abs(result[1] - 0) < 0.001

    def test_get_circle_coord_offset(self):
        result = DrillGcodeConverter.get_circle_coord(0, 5, 10, 2, 2)
        assert result == (7, 10, 2)

    def test_get_all_circle_coords_default(self, converter):
        coords = converter.get_all_circle_coords((0, 0, 0), radius=1, n_points=4)
        assert len(coords) == 4

    def test_get_all_circle_coords_full_circle(self, converter):
        coords = converter.get_all_circle_coords((0, 0, 0), radius=1, n_points=360)
        assert len(coords) == 360
        assert coords[0] == (1, 0, 0)

    def test_get_all_circle_coords_offset(self, converter):
        center = (5, 10, -1)
        radius = 2
        n_points = 8
        coords = converter.get_all_circle_coords(center, radius, n_points)
        assert len(coords) == 8
        assert all(len(c) == 3 for c in coords)