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
        assert colours == {"white", "orange"}

    def test_empty_list_only_warns(self):
        layer = self._layer()

        layer.add_gcode("gcode", [])

        assert layer.calls == []
        assert "gcode" not in layer.paths_geom
