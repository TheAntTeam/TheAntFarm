from unittest.mock import MagicMock, patch

import numpy as np

from TheAntFarm.shape_core.gcode_manager import GcodePoint
from TheAntFarm.shape_core.visual_manager import GLUTess, VisualLayer


class TestGLUTess:
    def test_init(self):
        tess = GLUTess()
        assert tess.tris == []
        assert tess.pts == []
        assert tess.vertex_index == 0

    def test_on_begin_primitive(self):
        tess = GLUTess()
        tess._on_begin_primitive(0)

    def test_on_new_vertex(self):
        tess = GLUTess()
        tess._on_new_vertex((0, 0, 0))
        assert tess.tris == [(0, 0, 0)]

    def test_on_edge_flag(self):
        tess = GLUTess()
        tess._on_edge_flag(0)

    def test_on_combine(self):
        tess = GLUTess()
        result = tess._on_combine((1, 2, 3), None, None)
        assert result == (1, 2, 3)

    def test_on_end_primitive(self):
        tess = GLUTess()
        tess._on_end_primitive()


class TestAddGCode:
    """add_gcode must not touch the vector list of the parser (it is the model)."""

    @staticmethod
    def _layer():
        # The rendering backend is not needed to check how the vectors are grouped
        layer = object.__new__(VisualLayer)
        layer.paths_geom = {}
        layer.calls = []
        layer.create_line = lambda tag, ldata, colors=None, order=0, width=0.1: layer.calls.append(
            {"tag": tag, "data": ldata, "colors": colors}
        )
        return layer

    @staticmethod
    def _point(x, y, travel):
        point = GcodePoint()
        point.coords = np.array([float(x), float(y), 0.0])
        point.type = point.TRAVEL if travel else point.WORKING
        return point

    @staticmethod
    def _square_vectors():
        # travel to the corner, then three working moves (one group)
        return [
            TestAddGCode._point(0, 0, True),
            TestAddGCode._point(10, 0, False),
            TestAddGCode._point(10, 10, False),
            TestAddGCode._point(0, 10, False),
        ]

    def test_input_list_is_not_modified(self):
        layer = self._layer()
        vectors = self._square_vectors()

        layer.add_gcode("gcode", vectors)

        assert len(vectors) == 4
        assert vectors[0].coords[0] == 0.0

    def test_stored_geometry_matches_the_input(self):
        layer = self._layer()
        vectors = self._square_vectors()

        layer.add_gcode("gcode", vectors)

        assert layer.paths_geom["gcode"] == vectors

    def test_single_vector_does_not_raise(self):
        layer = self._layer()
        vectors = [self._point(1, 2, False)]

        layer.add_gcode("gcode", vectors)

        assert len(vectors) == 1
        assert layer.calls
        # a single point is drawn as a zero length segment
        group = layer.calls[0]["data"][0]
        assert len(group) == 2
        assert np.array_equal(group[0], group[1])

    def test_travel_and_working_moves_are_grouped_by_colour(self):
        layer = self._layer()

        layer.add_gcode("gcode", self._square_vectors())

        colours = {call["colors"] for call in layer.calls}
        assert colours == {VisualLayer.FOREGROUND, "orange"}

    def test_empty_list_only_warns(self):
        layer = self._layer()

        layer.add_gcode("gcode", [])

        assert layer.calls == []
        assert "gcode" not in layer.paths_geom


class TestCreateLine:
    """create_line draws all the segments of a tag as one VisPy line."""

    @staticmethod
    def _layer():
        layer = object.__new__(VisualLayer)
        layer.canvas = MagicMock()
        layer.paths = {}
        layer.line_colors = {}
        layer.dark_background = True
        return layer

    @staticmethod
    def _segments():
        return [
            [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)],
            [(5.0, 5.0), (6.0, 5.0)],
        ]

    def test_segments_are_flattened_and_connected_inside_each_segment(self):
        layer = self._layer()

        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            layer.create_line("top", self._segments(), colors="red")

        kwargs = mock_visuals.Line.call_args.kwargs
        assert kwargs["pos"].tolist() == [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [5.0, 5.0], [6.0, 5.0]]
        assert kwargs["connect"].tolist() == [[0, 1], [1, 2], [3, 4]]
        assert kwargs["color"] == ["red"] * 5

    def test_one_colour_per_segment(self):
        layer = self._layer()

        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            layer.create_line("top", self._segments(), colors=["red", "blue"])

        assert mock_visuals.Line.call_args.kwargs["color"] == ["red"] * 3 + ["blue"] * 2

    def test_lines_of_the_same_tag_are_kept_together(self):
        layer = self._layer()

        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            first, second = MagicMock(), MagicMock()
            mock_visuals.Line.side_effect = [first, second]
            layer.create_line("top", self._segments(), colors="red", order=3)
            layer.create_line("top", self._segments(), colors="red")

        assert layer.paths["top"] == [first, second]
        assert first.order == 3
        layer.canvas.view.add.assert_any_call(first)
        layer.canvas.freeze.assert_called()

    def test_missing_colours_are_logged(self, caplog):
        layer = self._layer()

        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            layer.create_line("top", self._segments())

        assert "Path Colors List not Set" in caplog.text
        assert mock_visuals.Line.call_args.kwargs["color"] == []


class TestThemeColours:
    """FOREGROUND lines are white on the dark background and black on the light one, also when already drawn."""

    _layer = staticmethod(TestCreateLine._layer)
    _segments = staticmethod(TestCreateLine._segments)

    def test_foreground_is_white_on_the_dark_background(self):
        layer = self._layer()

        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            layer.create_line("gcode", self._segments(), colors=[VisualLayer.FOREGROUND, "orange"])

        assert mock_visuals.Line.call_args.kwargs["color"] == ["white"] * 3 + ["orange"] * 2

    def test_foreground_is_black_on_the_light_background(self):
        layer = self._layer()
        layer.dark_background = False

        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            layer.create_line("gcode", self._segments(), colors=VisualLayer.FOREGROUND)

        assert mock_visuals.Line.call_args.kwargs["color"] == ["black"] * 5

    def test_switching_theme_recolours_the_foreground_lines(self):
        layer = self._layer()
        with patch("TheAntFarm.shape_core.visual_manager.visuals") as mock_visuals:
            foreground, fixed = MagicMock(), MagicMock()
            mock_visuals.Line.side_effect = [foreground, fixed]
            layer.create_line("gcode", self._segments(), colors=[VisualLayer.FOREGROUND, "orange"])
            layer.create_line("top", self._segments(), colors="red")

        layer.set_dark_background(False)

        layer.canvas.set_canvas_bgcolor.assert_called_with(hex_color="#FFFFFF")
        foreground.set_data.assert_called_once_with(color=["black"] * 3 + ["orange"] * 2)
        fixed.set_data.assert_not_called()

        layer.set_dark_background(True)

        layer.canvas.set_canvas_bgcolor.assert_called_with(hex_color="#444444")
        foreground.set_data.assert_called_with(color=["white"] * 3 + ["orange"] * 2)

    def test_removed_lines_are_forgotten(self):
        layer = self._layer()
        with patch("TheAntFarm.shape_core.visual_manager.visuals"):
            layer.create_line("gcode", self._segments(), colors=VisualLayer.FOREGROUND)
        layer.paths.clear()

        layer.set_dark_background(False)

        assert layer.line_colors == {}


class TestThemeColoursOfANewLayer:
    def test_a_new_layer_starts_on_the_dark_background_with_no_lines(self):
        layer = VisualLayer(MagicMock())

        assert layer.dark_background
        assert layer.line_colors == {}

    def test_lines_without_recorded_colours_are_left_alone(self):
        layer = TestCreateLine._layer()
        line = MagicMock()
        layer.paths = {"other": [line]}

        layer.set_dark_background(False)

        line.set_data.assert_not_called()
        assert layer.line_colors == {}
