#

from vispy.scene import visuals
from vispy.color import Color
from OpenGL import GLU
import numpy as np


class GLUTess:
    # GLUTess from flatcam
    def __init__(self):
        """
        OpenGL GLU triangulation class
        """
        self.tris = []
        self.pts = []
        self.vertex_index = 0

    def _on_begin_primitive(self, type):
        pass

    def _on_new_vertex(self, vertex):
        self.tris.append(vertex)

    # Force GLU to return separate triangles (GLU_TRIANGLES)
    def _on_edge_flag(self, flag):
        pass

    def _on_combine(self, coords, data, weight):
        return (coords[0], coords[1], coords[2])

    def _on_error(self, errno):
        print("GLUTess error:", errno)

    def _on_end_primitive(self):
        pass

    def triangulate(self, polygon, z=0.0):
        """
        Triangulates polygon
        :param polygon: shapely.geometry.polygon
            Polygon to tessellate
        :return: list, list
            Array of triangle vertex indices [t0i0, t0i1, t0i2, t1i0, t1i1, ... ]
            Array of polygon points [(x0, y0), (x1, y1), ... ]
        """
        # Create tessellation object
        tess = GLU.gluNewTess()

        # Setup callbacks
        GLU.gluTessCallback(tess, GLU.GLU_TESS_BEGIN, self._on_begin_primitive)
        GLU.gluTessCallback(tess, GLU.GLU_TESS_VERTEX, self._on_new_vertex)
        GLU.gluTessCallback(tess, GLU.GLU_TESS_EDGE_FLAG, self._on_edge_flag)
        GLU.gluTessCallback(tess, GLU.GLU_TESS_COMBINE, self._on_combine)
        GLU.gluTessCallback(tess, GLU.GLU_TESS_ERROR, self._on_error)
        GLU.gluTessCallback(tess, GLU.GLU_TESS_END, self._on_end_primitive)

        # Reset data
        del self.tris[:]
        del self.pts[:]
        self.vertex_index = 0

        # Define polygon
        GLU.gluTessBeginPolygon(tess, None)

        def define_contour(contour):
            vertices = list(contour.coords)             # Get vertices coordinates
            if vertices[0] == vertices[-1]:             # Open ring
                vertices = vertices[:-1]

            vertices3d = [(v[0], v[1], z) for v in vertices]
            self.pts += vertices3d

            GLU.gluTessBeginContour(tess)               # Start contour

            # Set vertices
            for vertex in vertices:
                point = (vertex[0], vertex[1], z)
                GLU.gluTessVertex(tess, point, self.vertex_index)
                self.vertex_index += 1

            GLU.gluTessEndContour(tess)                 # End contour

        # Polygon exterior
        define_contour(polygon.exterior)

        # Interiors
        for interior in polygon.interiors:
            define_contour(interior)

        # Start tessellation
        GLU.gluTessEndPolygon(tess)

        # Free resources
        GLU.gluDeleteTess(tess)
        return self.tris, self.pts


class VisualLayer:

    def __init__(self, canvas):
        self.canvas = canvas
        self.z = 0.0

    def add_layer(self, geom_list, color=None):
        ldata = [[], []]
        triangulizer = GLUTess()
        for g in geom_list:
            tri, pts = triangulizer.triangulate(g.geom, self.z)
            tri_off = list(np.array(tri[:]) + len(ldata[1]))
            ldata[0] += tri_off
            ldata[1] += pts[:]
        self.create_mesh(ldata, color)
        print("END")
        self.z -= 0.1

    def add_triploy(self, tri, pts):
        self.canvas.unfreeze()
        mesh = visuals.Mesh()
        mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)))
        mesh._bounds_changed()
        self.canvas.view.add(mesh)
        self.canvas.freeze()
        visuals.XYZAxis(parent=self.canvas.view.scene)

    def create_mesh(self, ldata, color=None):

        self.canvas.unfreeze()
        mesh = visuals.Mesh()
        tri = ldata[0]
        pts = ldata[1]
        if color:
            mesh_colors = [Color(color).rgba] * int(len(tri) / 3)
            print(pts[0])
            mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)),
                          face_colors=np.asarray(mesh_colors))
        else:
            mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)))
        mesh._bounds_changed()
        self.canvas.view.add(mesh)
        self.canvas.view.camera.set_range()
        self.canvas.freeze()
        #visuals.XYZAxis(parent=self.canvas.view.scene)
