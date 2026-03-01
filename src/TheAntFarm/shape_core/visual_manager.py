#
# https://programtalk.com/vs2/python/7189/phy/phy/plot/tests/test_panzoom.py/
# https://stackoverflow.com/questions/33942728/how-to-get-world-coordinates-from-screen-coordinates-in-vispy

import logging
import random
import string
from collections import OrderedDict
from typing import List, Tuple, Dict, Optional, Any, Union

import numpy as np
import shapely as sh
from OpenGL import GLU
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.strtree import STRtree
from vispy.color import Color
from vispy.scene import visuals, PanZoomCamera
from vispy.visuals.filters import Alpha

logger = logging.getLogger(__name__)


class GLUTess:
    """
    Handles the tessellation of complex 2D polygons into triangles using the OpenGL GLU library.
    This is necessary because GPUs render triangles, but Shapely handles arbitrary polygons
    (potentially with holes).
    """

    def __init__(self) -> None:
        """
        Initialize the GLU triangulation class.
        """
        self.tris: List[Any] = []
        self.pts: List[Tuple[float, float, float]] = []
        self.vertex_index: int = 0

    def _on_begin_primitive(self, type: int) -> None:
        """Callback for the beginning of a primitive (e.g., GL_TRIANGLES)."""
        pass

    def _on_new_vertex(self, vertex: Any) -> None:
        """Callback for when a new vertex is generated."""
        self.tris.append(vertex)

    # Force GLU to return separate triangles (GLU_TRIANGLES)
    def _on_edge_flag(self, flag: int) -> None:
        """Callback for edge flags (unused but required to force specific GLU behavior)."""
        pass

    def _on_combine(self, coords: Tuple[float, float, float], data: Any, weight: Any) -> Tuple[float, float, float]:
        """
        Callback for when GLU needs to create a new vertex at an intersection.
        Returns the coordinates of the new vertex.
        """
        return coords[0], coords[1], coords[2]

    def _on_error(self, errno: int) -> None:
        """
        Callback for GLU errors.
        Logs the error code and its string representation.
        """
        err_str = GLU.gluErrorString(errno)
        logger.error(f"GLUTess error: {errno} ({err_str})")

    def _on_end_primitive(self) -> None:
        """Callback for the end of a primitive."""
        pass

    def triangulate(self, polygon: Polygon, z: float = 0.0) -> Tuple[List[int], List[Tuple[float, float, float]]]:
        """
        Triangulates a Shapely polygon.

        :param polygon: shapely.geometry.polygon.Polygon
            The polygon to tessellate.
        :param z: float
            The Z-coordinate to assign to the vertices.
        :return: tuple(list, list)
            - Array of triangle vertex indices [t0i0, t0i1, t0i2, ... ]
            - Array of polygon points [(x0, y0, z), (x1, y1, z), ... ]
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

        # Reset data buffers
        del self.tris[:]
        del self.pts[:]
        self.vertex_index = 0

        # Define polygon
        GLU.gluTessBeginPolygon(tess, None)

        def define_contour(contour: Any) -> None:
            """Helper to define a single contour (exterior or hole) for GLU."""
            vertices = list(contour.coords)  # Get vertices coordinates

            if vertices[0] == vertices[-1]:  # Open ring if closed
                vertices = vertices[:-1]

            # Store 3D vertices
            vertices3d = [(v[0], v[1], z) for v in vertices]
            self.pts += vertices3d

            GLU.gluTessBeginContour(tess)  # Start contour

            # Pass vertices to GLU
            for vertex in vertices:
                point = (vertex[0], vertex[1], z)
                GLU.gluTessVertex(tess, point, self.vertex_index)
                self.vertex_index += 1

            GLU.gluTessEndContour(tess)  # End contour

        # Process Polygon exterior
        define_contour(polygon.exterior)

        # Process Interiors (holes)
        for interior in polygon.interiors:
            define_contour(interior)

        # Start tessellation processing
        GLU.gluTessEndPolygon(tess)

        # Free resources
        GLU.gluDeleteTess(tess)

        # Post-process indices to handle new vertices created by GLU (intersections)
        id_counter = len(self.pts)
        new_tris = self.tris[:]
        for i, t in enumerate(self.tris):
            if not isinstance(t, int):
                # If t is not an int, it's a coordinate tuple from _on_combine
                self.pts.append((t[0], t[1], z))
                new_tris[i] = id_counter
                id_counter += 1

        self.tris = new_tris

        return self.tris, self.pts


class VisualLayer:
    """
    Manages the visualization of geometric layers on a VisPy canvas.
    Handles rendering, camera control (Top/Bottom views), and user interaction (selection).
    """

    # --- Constants ---
    # Layer Tags
    SELECTED_TAG = "selected"
    DRILL_TAG = "drill"
    PROFILE_TAG = "profile"
    TOP_TAG = "top"
    BOTTOM_TAG = "bottom"
    NC_TOP_TAG = "nc_top"
    NC_BOTTOM_TAG = "nc_bottom"
    POINTER_TAG = "POINTER"

    # View Order (Rendering priority)
    # Defines which layers are drawn on top based on the camera orientation
    TOP_ORDER = {
        SELECTED_TAG: 1,
        DRILL_TAG: 2,
        PROFILE_TAG: 3,
        TOP_TAG: 5,
        BOTTOM_TAG: 6,
        NC_TOP_TAG: 4,
        NC_BOTTOM_TAG: 7,
    }
    BTM_ORDER = {
        SELECTED_TAG: 1,
        DRILL_TAG: 2,
        PROFILE_TAG: 3,
        TOP_TAG: 6,
        BOTTOM_TAG: 5,
        NC_TOP_TAG: 7,
        NC_BOTTOM_TAG: 4,
    }

    # Pointer settings
    POINTER_RADIUS = 0.5
    POINTER_COLOR = "yellow"
    POINTER_SEGMENTS = 20

    DELTA = 1

    def __init__(self, canvas: Any, selectable: bool = False) -> None:
        """
        Initialize the VisualLayer manager.

        :param canvas: vispy.scene.SceneCanvas
            The canvas where the visualization will be drawn.
        :param selectable: bool
            Whether the layers should be interactive (selectable via double-click).
        """
        self.canvas = canvas
        self.canvas.view.camera = PanZoomCamera(aspect=1)
        self.translucent_filter = Alpha()

        # Data storage
        self.meshes: OrderedDict[str, visuals.Mesh] = OrderedDict({})
        self.paths: OrderedDict[str, List[visuals.Line]] = OrderedDict({})
        self.meshes_geom: OrderedDict[str, List[Any]] = OrderedDict({})
        self.paths_geom: OrderedDict[str, List[Any]] = OrderedDict({})

        # Spatial Index for fast selection
        self.tree: Optional[STRtree] = None
        self.indexed_geoms: List[Any] = []
        self.geom_id_to_shape: Dict[int, Any] = {}

        # State
        self.orientation: int = 0
        self.pointer_tag: str = ""
        self.selectable: bool = selectable
        self.selected_object: Optional[Any] = None

        if selectable:
            self.canvas.events.mouse_double_click.connect(self.on_mouse_double_click)

    def _rebuild_index(self) -> None:
        """
        Rebuilds the STRtree spatial index.
        This is called whenever layers are added or removed to ensure efficient selection queries.
        """
        self.indexed_geoms = []
        self.geom_id_to_shape = {}
        geoms = []

        # Collect all geometries from all layers except the selection layer itself
        for tag, shapes in self.meshes_geom.items():
            if tag == self.SELECTED_TAG:
                continue
            for shape in shapes:
                if hasattr(shape, 'geom') and shape.geom:
                    geoms.append(shape.geom)
                    # Map the geometry ID back to the shape object wrapper
                    self.geom_id_to_shape[id(shape.geom)] = shape

        self.indexed_geoms = geoms
        if self.indexed_geoms:
            try:
                # Build the R-tree
                self.tree = STRtree(self.indexed_geoms)
            except Exception as e:
                logger.error(f"Failed to build STRtree: {e}")
                self.tree = None
        else:
            self.tree = None

    def compute_pointer(self, coords: Tuple[float, float, float]) -> List[List[float]]:
        """
        Computes the vertices for a circular pointer marker.
        """
        segments = self.POINTER_SEGMENTS
        xc, yc, zc = coords

        radius = self.POINTER_RADIUS
        theta = np.linspace(0, 2 * np.pi, segments)
        x = xc + radius * np.cos(theta)
        y = yc + radius * np.sin(theta)
        z = np.ones((segments,)) * zc
        pointer_coords = np.vstack((x, y, z)).transpose().tolist()
        return pointer_coords

    def create_pointer(self, coords: Tuple[float, float, float]) -> None:
        """Creates a visual pointer at the specified coordinates."""
        pointer_coords = self.compute_pointer(coords)
        chars = string.ascii_uppercase + string.digits
        tag = self.POINTER_TAG + "_" + "".join(random.choice(chars) for _ in range(4))
        self.pointer_tag = tag
        self.create_line(tag, [pointer_coords], colors=self.POINTER_COLOR, order=0, width=0.1)

    def update_pointer(self, coords: Tuple[float, float, float]) -> None:
        """Updates the position of the existing pointer."""
        if self.pointer_tag:
            pointer_coords = self.compute_pointer(coords)
            path = self.paths[self.pointer_tag][0]
            path.set_data(pos=np.array(pointer_coords))

    def remove_pointer(self) -> None:
        """Removes the pointer from the scene."""
        if self.pointer_tag:
            self.remove_path(self.pointer_tag)
            self.pointer_tag = ""

    def set_pointer_visible(self, visible: bool) -> None:
        """Toggles pointer visibility."""
        if self.pointer_tag:
            self.set_path_visible(self.pointer_tag, visible)

    def update_order(self) -> None:
        """Updates the rendering order based on the current camera orientation."""
        if self.canvas.view.camera.up == "+z":
            self.top_view()
        else:
            self.bottom_view()

    def top_view(self) -> None:
        """Sets the camera to Top View (+Z up) and adjusts layer order."""
        self.canvas.view.camera.up = "+z"
        self.canvas.view.camera.flip = (False, False, False)

        for m in self.meshes.keys():
            self.meshes[m].order = self.TOP_ORDER[m]

        self.canvas._draw_order.clear()
        self.canvas.update()

    def bottom_view(self) -> None:
        """Sets the camera to Bottom View (-Z up) and adjusts layer order."""
        self.canvas.view.camera.up = "-z"
        self.canvas.view.camera.flip = (True, False, True)

        for m in self.meshes.keys():
            self.meshes[m].order = self.BTM_ORDER[m]

        self.canvas._draw_order.clear()
        self.canvas.update()

    def flip_camera(self, flipped: Tuple[bool, bool, bool]) -> None:
        """Manually flips the camera."""
        self.canvas.view.camera.up = "+z"
        self.canvas.view.camera.flip = (flipped)

        for m in self.meshes.keys():
            self.meshes[m].order = self.TOP_ORDER[m]

        self.canvas._draw_order.clear()
        self.canvas.update()

    def on_mouse_double_click(self, event: Any) -> None:
        """
        Handles double-click events for object selection.
        Uses the spatial index (STRtree) for efficient querying.
        """
        if event.button == 1:  # left click
            self.remove_layer(self.SELECTED_TAG)
            self.canvas.view.interactive = False

            # Transform screen coordinates to world coordinates
            tr = self.canvas.scene.node_transform(self.canvas.view.scene)
            pos = tr.map(event.pos)
            self.canvas.view.interactive = True

            # Create a point from the click position
            point = Point(pos[0:2])
            found_shape = None

            # 1. Broad Phase: Use R-tree to find candidate geometries near the point
            if self.tree:
                candidates = self.tree.query(point)
                for candidate in candidates:
                    # Handle different return types from STRtree versions
                    if isinstance(candidate, (int, np.integer)):
                        geom = self.indexed_geoms[candidate]
                    else:
                        geom = candidate

                    # 2. Narrow Phase: Precise 'contains' check
                    if geom.contains(point):
                        found_shape = self.geom_id_to_shape.get(id(geom))
                        if found_shape:
                            break

            # If an object is found, highlight it
            if found_shape:
                self.add_layer(tag=self.SELECTED_TAG, geom_list=[found_shape], color="yellow", holes=False,
                               auto_range=False)

    def on_mouse_click(self, event: Any) -> None:
        """Handles single click events (toggles view orientation)."""
        self.orientation = 0 if self.orientation == 1 else 1
        self.flip_view(orientation=self.orientation)

    def flip_view(self, orientation: int = 0) -> None:
        """Flips the view based on orientation index."""
        if orientation == 0:
            self.canvas.view.camera.up = '+z'
        else:
            self.canvas.view.camera.up = '-z'

    def set_layer_visible(self, tag: str, visible: bool) -> None:
        """Sets the visibility of a mesh layer."""
        if tag in self.meshes.keys():
            self.meshes[tag].visible = visible

    def set_path_visible(self, tag: str, visible: bool) -> None:
        """Sets the visibility of a path layer."""
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                p.visible = visible

    def set_gcode_visible(self, tag: str, visible: bool) -> None:
        """Sets the visibility of a GCode layer."""
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                p.visible = visible

    def get_layers_tag(self) -> List[str]:
        """Returns a list of all mesh layer tags."""
        return list(self.meshes.keys())

    def get_paths_tag(self) -> List[str]:
        """Returns a list of all path layer tags."""
        return list(self.paths.keys())

    def remove_layer(self, tag: str) -> None:
        """
        Removes a mesh layer by tag and rebuilds the spatial index.
        """
        if tag in self.meshes.keys():
            to_remove = self.meshes[tag]
            # self.canvas.events.draw.disconnect(to_remove.on_draw)
            to_remove.parent = None
            del self.meshes[tag]
            del self.meshes_geom[tag]
            self._rebuild_index()

    def remove_path(self, tag: str) -> None:
        """Removes a path layer by tag."""
        if tag in self.paths.keys():
            for p in self.paths[tag]:
                to_remove = p
                # self.canvas.events.draw.disconnect(to_remove.on_draw)
                to_remove.parent = None
                del p
            if tag in self.paths.keys():
                del self.paths[tag]
            if tag in self.paths_geom.keys():
                del self.paths_geom[tag]

    def add_layer(self, tag: str, geom_list: List[Any], color: Optional[Any] = None, holes: bool = False,
                  auto_range: bool = True) -> None:
        """
        Adds a new geometric layer to the scene.
        Triangulates the Shapely geometries and creates a VisPy mesh.
        """
        ldata: List[List[Any]] = [[], []]
        triangulizer = GLUTess()
        order = 0
        order_d = self.TOP_ORDER if self.canvas.view.camera.up == '+z' else self.BTM_ORDER
        if tag in order_d:
            order = order_d[tag]

        # Batch triangulation: Process all geometries in the list
        for g in geom_list:
            tri, pts = triangulizer.triangulate(g.geom, 0)
            # Offset triangle indices to match the current vertex buffer position
            tri_off = list(np.array(tri[:]) + len(ldata[1]))
            ldata[0] += tri_off
            ldata[1] += pts[:]

        self.create_mesh(tag, ldata, color, order, auto_range=auto_range)
        self.meshes_geom[tag] = geom_list
        self._rebuild_index()

    def get_selected_centroid(self) -> Optional[List[float]]:
        """Returns the centroid of the currently selected object."""
        if self.SELECTED_TAG in self.meshes_geom.keys():
            sel_geom_list = self.meshes_geom[self.SELECTED_TAG]
            if len(sel_geom_list) > 0:
                centroid = list(sel_geom_list[0].geom.centroid.xy)
                centroid = [centroid[0][0], centroid[1][0]]
                return centroid
            else:
                logger.warning("No Active Selection found. Please select a Drill Position from the Alignment View")
        else:
            logger.warning("No Drill Information Loaded. Please Load a GCODE or EXCELLON file in the Alignment View")
        return None

    def add_path(self, tag: str, geom_list: List[Any], color: Optional[Any] = None,
                 warning_color: str = 'red') -> None:
        """Adds a path (line) layer to the scene."""
        # todo: add zbuffer controll
        if geom_list:
            order = 0
            for d in geom_list:
                ldata = []
                gl = d[1]
                special_gl_ids = []
                if len(d) > 2:
                    special_gl_ids = d[2]
                colors = []
                for i, g in enumerate(gl):
                    if g.geom_type == "LineString":
                        ldata.append(list(g.coords))
                    if g.geom_type == "LinearRing":
                        ldata.append(list(g.coords))
                    if i in special_gl_ids:
                        colors.append(warning_color)
                    else:
                        colors.append(color)
                self.create_line(tag, ldata, colors, order)
            self.paths_geom[tag] = geom_list
        else:
            logger.warning("Cannot Visualize an Empty Path")
        self.update_order()

    def add_gcode(self, tag: str, gcode_list: List[Any], color: Tuple[str, str] = ('white', 'orange')) -> None:
        """Adds a GCode path visualization, distinguishing between travel and cut moves."""
        if gcode_list:
            order = 0
            gcode_paths: Dict[str, List[Any]] = {}
            pre_d = gcode_list.pop(0)
            coords = [pre_d.coords]
            pre_d = gcode_list[0]

            # Group segments by type (Travel vs Cut) to optimize rendering
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

            # Handle the last segment
            c = color[1] if pre_d.type == pre_d.TRAVEL else color[0]
            if c not in gcode_paths.keys():
                gcode_paths[c] = [coords]
            else:
                gcode_paths[c].append(coords)

            for col in gcode_paths.keys():
                self.create_line(tag, gcode_paths[col], col, order)
            self.paths_geom[tag] = gcode_list
        else:
            logger.warning("Cannot Visualize an Empty GCode")

    def remove_gcode(self, tag: str) -> None:
        """Removes a GCode layer."""
        self.remove_path(tag)

    def add_triploy(self, tri: List[Any], pts: List[Any]) -> None:
        """Directly adds a mesh from triangles and points (debug utility)."""
        self.canvas.unfreeze()
        mesh = visuals.Mesh()
        mesh.set_data(np.asarray(pts), np.asarray(tri, dtype=np.uint32).reshape((-1, 3)))
        mesh._bounds_changed()
        self.canvas.view.add(mesh)
        self.canvas.freeze()
        visuals.XYZAxis(parent=self.canvas.view.scene)

    def create_line(self, tag: str, ldata: List[Any], colors: Optional[Union[List[Any], Any]] = None, order: int = 0,
                    width: float = 0.1) -> None:
        """
        Creates a VisPy Line visual from a list of segments.
        Optimized to create a single Line object with 'connect' array instead of multiple objects.
        """
        if colors is not None:
            if not isinstance(colors, list):
                colors_list = [colors for i in range(len(ldata))]
            else:
                colors_list = colors
        else:
            colors_list = None
            logger.error("Path Colors List not Set")

        self.canvas.unfreeze()
        connect = []
        coords = []
        p = -1
        all_colors = []

        # Flatten all segments into a single coordinate array and connection array
        for i, l in enumerate(ldata):
            p += 1
            c = l[0]
            coords.append(c)
            for j in range(1, len(l)):
                c = l[j]
                coords.append(c)
                connect.append((p, p+1))
                p += 1
            if colors_list:
                all_colors += [colors_list[i]] * len(l)
        
        coords_arr = np.array(coords)
        connect_arr = np.array(connect)

        line = visuals.Line(pos=coords_arr, connect=connect_arr, width=width, color=all_colors,
                            parent=self.canvas.view, antialias=True)
        line.order = order
        if tag in list(self.paths.keys()):
            self.paths[tag] += [line]
        else:
            self.paths[tag] = [line]
        self.canvas.view.add(line)
        self.canvas.view.camera.set_range()
        self.canvas.freeze()

    def create_mesh(self, tag: str, ldata: List[Any], color: Optional[Any] = None, order: int = 0,
                    auto_range: bool = True) -> None:
        """
        Creates a VisPy Mesh visual from triangle data.
        """
        self.canvas.unfreeze()
        mesh = visuals.Mesh(parent=self.canvas.view)
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
