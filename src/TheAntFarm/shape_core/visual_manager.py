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
import string
import random
from shapely.geometry import Point
import shapely as sh

print(sh.__version__)




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
                self.pts.append((t[0], t[1], z))
                new_tris[i] = id
                id += 1

        self.tris = new_tris

        return self.tris, self.pts


class VisualLayer:

    DELTA = 1
    TOP_ORDER = {'selected': 1, 'drill': 2, 'profile': 3, 'top': 5, 'bottom': 6, 'nc_top': 4, 'nc_bottom': 7}
    BTM_ORDER = {'selected': 1, 'drill': 2, 'profile': 3, 'top': 6, 'bottom': 5, 'nc_top': 7, 'nc_bottom': 4}
    POINTER_RADIUS = 0.5
    POINTER_TAG = "POINTER"
    POINTER_COLOR = "orange"
    POINTER_SEGMENTS = 20

    def __init__(self, canvas, selectable=False):
        self.canvas = canvas
        self.canvas.view.camera = PanZoomCamera(aspect=1)
        self.translucent_filter = Alpha()
        self.meshes = OrderedDict({})
        self.paths = OrderedDict({})
        self.meshes_geom = OrderedDict({})
        self.paths_geom = OrderedDict({})

        # self.view = 0
        self.orientation = 0
        self.pointer_tag = ""
        self.selectable = selectable

        self.selected_object = None

        if selectable:
            self.canvas.events.mouse_double_click.connect(self.on_mouse_double_click)

    def compute_pointer(self, coords):
        segments = self.POINTER_SEGMENTS
        xc, yc, zc = coords

        radius = self.POINTER_RADIUS
        theta = np.linspace(0, 2 * np.pi, segments)
        x = xc + radius * np.cos(theta)
        y = yc + radius * np.sin(theta)
        z = np.ones((segments,)) * zc
        pointer_coords = np.vstack((x, y, z)).transpose().tolist()
        return pointer_coords

    def create_pointer(self, coords):
        pointer_coords = self.compute_pointer(coords)
        chars = string.ascii_uppercase + string.digits
        tag = self.POINTER_TAG + "_" + "".join(random.choice(chars) for _ in range(4))
        self.pointer_tag = tag
        self.create_line(tag, [pointer_coords], color=self.POINTER_COLOR, order=0, width=0.1)

    def update_pointer(self, coords):
        if self.pointer_tag:
            pointer_coords = self.compute_pointer(coords)
            path = self.paths[self.pointer_tag][0]
            path.set_data(pos=np.array(pointer_coords))

    def remove_pointer(self):
        if self.pointer_tag:
            self.remove_path(self.pointer_tag)
            self.pointer_tag = ""

    def set_pointer_visible(self, visible):
        if self.pointer_tag:
            self.set_path_visible(self.pointer_tag, visible)

    def update_order(self):
        if self.canvas.view.camera.up == "+z":
            self.top_view()
        else:
            self.bottom_view()

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

    def flip_camera(self, flipped):
        self.canvas.view.camera.up = "+z"
        self.canvas.view.camera.flip = (flipped)

        for m in self.meshes.keys():
            self.meshes[m].order = self.TOP_ORDER[m]

        self.canvas._draw_order.clear()
        self.canvas.update()

    def on_mouse_double_click(self, event):
        if event.button == 1:  # left click
            self.remove_layer("selected")
            self.canvas.view.interactive = False
            tr = self.canvas.scene.node_transform(self.canvas.view.scene)
            pos = tr.map(event.pos)
            self.canvas.view.interactive = True

            # get selected polygon using shapely
            point = Point(pos)
            for gk in self.meshes_geom.keys():
                if gk != "selected":
                    geom_list = self.meshes_geom[gk].copy()
                    contain_flag = False
                    shape = None
                    while geom_list and not contain_flag:
                        shape = geom_list.pop()
                        contain_flag = shape.geom.contains(point)

                    # ToDo: to parametrize color of selection
                    if contain_flag:
                        self.add_layer(tag="selected", geom_list=[shape], color="yellow", holes=False, auto_range=False)
                        break

    def on_mouse_click(self, event):
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
            del self.meshes_geom[tag]

    def remove_path(self, tag):
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                to_remove = p
                # self.canvas.events.draw.disconnect(to_remove.on_draw)
                to_remove.parent = None
                del p
            del self.paths[tag]
            del self.paths_geom[tag]

    def add_layer(self, tag, geom_list, color=None, holes=False, auto_range=True):
        ldata = [[], []]
        triangulizer = GLUTess()
        order = 0
        order_d = self.TOP_ORDER if self.canvas.view.camera.up == '+z' else self.BTM_ORDER
        if tag in order_d:
            order = order_d[tag]

        for g in geom_list:
            tri, pts = triangulizer.triangulate(g.geom, 0)
            tri_off = list(np.array(tri[:]) + len(ldata[1]))
            ldata[0] += tri_off
            ldata[1] += pts[:]
            # if holes:
            #     tri, pts = triangulizer.triangulate(g.geom, 0)
            #     tri_off = list(np.array(tri[:]) + len(ldata[1]))
            #     ldata[0] += tri_off
            #     ldata[1] += pts[:]
                #order = 0
        self.create_mesh(tag, ldata, color, order, auto_range=auto_range)
        self.meshes_geom[tag] = geom_list

    def add_path(self, tag, geom_list, color=None):
        # todo: add zbuffer controll
        if geom_list:
            ldata = []
            order = 0
            for d in geom_list:
                gl = d[1]
                for g in gl:
                    if g.geom_type == "LineString":
                        ldata.append(list(g.coords))
                    if g.geom_type == "LinearRing":
                        ldata.append(list(g.coords))
                self.create_line(tag, ldata, color, order)
            self.paths_geom[tag] = geom_list
        else:
            print("Cannot Visualize an Empty Path")

        self.update_order()

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
            self.paths_geom[tag] = gcode_list
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

    def create_line(self, tag, ldata, color=None, order=0, width=0.1):
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

        line = visuals.Line(pos=coords, connect=connect, width=width, color=color, parent=self.canvas.view, antialias=True)
        line.order = order
        if tag in list(self.paths.keys()):
            self.paths[tag] += [line]
        else:
            self.paths[tag] = [line]
        self.canvas.view.add(line)
        self.canvas.view.camera.set_range()
        self.canvas.freeze()

    def create_mesh(self, tag, ldata, color=None, order=0, auto_range=True):

        self.canvas.unfreeze()
        mesh = visuals.Mesh(parent=self.canvas.view)
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

        if color:
            mesh_colors = [Color(color).rgba] * int(len(tri) / 3)
            mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)),
                          face_colors=np.asarray(mesh_colors))
        else:
            mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)))
        mesh._bounds_changed()
        self.meshes[tag] = mesh
        self.canvas.view.add(mesh)

        if auto_range:
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
