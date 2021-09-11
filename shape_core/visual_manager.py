#
# https://programtalk.com/vs2/python/7189/phy/phy/plot/tests/test_panzoom.py/
# https://stackoverflow.com/questions/33942728/how-to-get-world-coordinates-from-screen-coordinates-in-vispy

from vispy import gloo
from vispy.scene import visuals, PanZoomCamera, TurntableCamera
from vispy.color import Color
from vispy.visuals.filters import Alpha
from OpenGL import GLU
import numpy as np
from collections import OrderedDict


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

        id = len(self.pts)
        new_tris = self.tris[:]
        for i, t in enumerate(self.tris):
            if not isinstance(t, int):
                # print("locos " + str(t))
                self.pts.append((t[0], t[1], z))
                new_tris[i] = id
                id += 1

        self.tris = new_tris

        return self.tris, self.pts


class VisualLayer:

    DELTA = 1
    TOP_ORDER = {'drill': 0, 'profile': 1, 'top': 3, 'bottom': 4, 'nc_top': 2, 'nc_bottom': 5}
    BTM_ORDER = {'drill': 0, 'profile': 1, 'top': 4, 'bottom': 3, 'nc_top': 5, 'nc_bottom': 2}

    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.view.camera = PanZoomCamera(aspect=1)
        self.translucent_filter = Alpha()
        self.meshes = OrderedDict({})
        self.paths = OrderedDict({})
        self.view = 0

    def top_view(self):
        self.canvas.view.camera.up = "+z"
        self.canvas.view.camera.flip = (False, False, False)

        for m in self.meshes.keys():
            self.meshes[m].order = self.TOP_ORDER[m]

        self.canvas._draw_order.clear()
        self.canvas.update()

    def bottom_view(self):
        self.canvas.view.camera.up = "-z"
        self.canvas.view.camera.flip = (True, False, True)

        for m in self.meshes.keys():
            self.meshes[m].order = self.BTM_ORDER[m]

        self.canvas._draw_order.clear()
        self.canvas.update()

    def on_mouse_double_click(self, event):
        # print("Double Click")
        # print(event)
        self.orientation = 0 if self.orientation == 1 else 1
        self.flip_view(orientation=self.orientation)

    def flip_view(self, orientation=0):
        if orientation == 0:
            self.canvas.view.camera.up = '+z'
        else:
            self.canvas.view.camera.up = '-z'

    def set_layer_visible(self, tag, visible):
        if tag in self.meshes.keys():
            self.meshes[tag].visible = visible

    def set_path_visible(self, tag, visible):
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                p.visible = visible

    def set_gcode_visible(self, tag, visible):
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                p.visible = visible

    def get_layers_tag(self):
        return self.meshes.keys()

    def get_paths_tag(self):
        return self.paths.keys()

    def remove_layer(self, tag):
        if tag in self.meshes.keys():
            to_remove = self.meshes[tag]
            # self.canvas.events.draw.disconnect(to_remove.on_draw)
            to_remove.parent = None
            del self.meshes[tag]

    def remove_path(self, tag):
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                to_remove = p
                # self.canvas.events.draw.disconnect(to_remove.on_draw)
                to_remove.parent = None
                del p
            del self.paths[tag]

    def add_layer(self, tag, geom_list, color=None, holes=False):
        ldata = [[], []]
        triangulizer = GLUTess()
        order = 0
        order_d = self.TOP_ORDER if self.canvas.view.camera.up == '+z' else self.BTM_ORDER
        if tag in order_d:
            order = order_d[tag]

        for g in geom_list:
            # tri, pts = triangulizer.triangulate(g.geom, self.z)
            tri, pts = triangulizer.triangulate(g.geom, 0)
            tri_off = list(np.array(tri[:]) + len(ldata[1]))
            ldata[0] += tri_off
            ldata[1] += pts[:]
            if holes:
                # tri, pts = triangulizer.triangulate(g.geom, self.DELTA)
                tri, pts = triangulizer.triangulate(g.geom, 0)
                tri_off = list(np.array(tri[:]) + len(ldata[1]))
                ldata[0] += tri_off
                ldata[1] += pts[:]
                order = 0
        self.create_mesh(tag, ldata, color, order)
        # print("END")
        # self.z -= self.DELTA
        # self.z += self.DELTA

    def add_path(self, tag, geom_list, color=None):
        # todo: add zbuffer controll
        if geom_list:
            ldata = []
            order = 0
            for d in geom_list:
                gl = d[1]
                for g in gl:
                    if g.type == "LineString":
                        # print(">>>>>>>>>> Line String")
                        # print(list(g.coords))
                        ldata.append(list(g.coords))
                    if g.type == "LinearRing":
                        # print(list(g.coords))
                        # print("<<<<<<<<<< Linear Ring")
                        ldata.append(list(g.coords))
                self.create_line(tag, ldata, color, order)
            # print("END")
            # self.z -= self.DELTA
            # self.z += self.DELTA
        else:
            print("Cannot Visualize an Empty Path")

    def add_gcode(self, tag, gcode_list, color=('white', 'orange')):
        if gcode_list:
            order = 0
            gcode_paths = {}
            pre_d = gcode_list.pop(0)
            coords = [pre_d.coords]
            pre_d = gcode_list[0]
            for d in gcode_list:
                if d.type == pre_d.type:
                    coords.append(d.coords)
                else:
                    c = color[1] if pre_d.type == pre_d.TRAVEL else color[0]
                    if c not in gcode_paths.keys():
                        gcode_paths[c] = [coords]
                    else:
                        gcode_paths[c].append(coords)
                    coords = [pre_d.coords]
                    coords.append(d.coords)
                pre_d = d
            c = color[1] if pre_d.type == pre_d.TRAVEL else color[0]
            if c not in gcode_paths.keys():
                gcode_paths[c] = [coords]
            else:
                gcode_paths[c].append(coords)

            for color in gcode_paths.keys():
                self.create_line(tag, gcode_paths[color], color, order)
        else:
            print("Cannot Visualize an Empty GCode")

    def remove_gcode(self, tag):
        self.remove_path(tag)

    def add_triploy(self, tri, pts):
        self.canvas.unfreeze()
        mesh = visuals.Mesh()
        mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)))
        mesh._bounds_changed()
        self.canvas.view.add(mesh)
        self.canvas.freeze()
        visuals.XYZAxis(parent=self.canvas.view.scene)

    def create_line(self, tag, ldata, color=None, order=0):
        self.canvas.unfreeze()
        connect = []
        coords = []
        p = -1
        for l in ldata:
            p += 1
            c = l[0]
            coords.append(c)
            for j in range(1, len(l)):
                c = l[j]
                coords.append(c)
                connect.append((p, p+1))
                p += 1
        coords = np.array(coords)
        connect = np.array(connect)

        # print(coords)
        # print(connect)

        line = visuals.Line(pos=coords, connect=connect, width=0.1, color=color, parent=self.canvas.view)
        line.order = order
        if tag in list(self.paths.keys()):
            self.paths[tag] += [line]
        else:
            self.paths[tag] = [line]
        #self.paths[tag] = line
        self.canvas.view.add(line)
        self.canvas.view.camera.set_range()
        self.canvas.freeze()

    def create_mesh(self, tag, ldata, color=None, order=0):

        self.canvas.unfreeze()
        mesh = visuals.Mesh(parent=self.canvas.view.scene)
        # mesh = visuals.Mesh(shading='flat', parent=self.canvas.view.scene)
        # mesh.unfreeze()
        # mesh.filter = self.translucent_filter
        # mesh.attach(self.translucent_filter)
        # mesh.freeze()
        # mesh.filter.alpha = 0.3
        # mesh.shading = None
        mesh.set_gl_state('translucent', cull_face=False)
        mesh.order = order

        tri = ldata[0]
        pts = ldata[1]

        # print(order)
        # new_pts = []
        # for p in pts:
        #     new_pts.append((p[0], p[1], order))
        # pts = new_pts

        if color:
            mesh_colors = [Color(color).rgba] * int(len(tri) / 3)
            mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)),
                          face_colors=np.asarray(mesh_colors))
        else:
            mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)))
        mesh._bounds_changed()
        self.meshes[tag] = mesh
        self.canvas.view.add(mesh)

        self.canvas.view.camera.set_range()

        self.canvas.freeze()
        #visuals.XYZAxis(parent=self.canvas.view.scene)

        #
        # gloo.set_clear_color('white')
        # gloo.set_state('opaque')
        # gloo.set_polygon_offset(1, 1)
        #
        # # gloo.set_state(blend=False, depth_test=True, polygon_offset_fill=True)
        # gloo.set_state(blend=True, depth_test=True, polygon_offset_fill=False)
        # gloo.set_depth_mask(True)
        #
