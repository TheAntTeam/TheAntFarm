import pytest
from shapely.geometry import Polygon

from TheAntFarm.shape_core.visual_manager import GLUTess


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