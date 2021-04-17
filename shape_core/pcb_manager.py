
import os
import gerber as gbr
import gerber.primitives
import numpy as np
import math
from gerber.utils import convex_hull
from collections import OrderedDict as Od

from .geometry_manager import Geom, merge_polygons
# from .plot_stuff import plot_vertices, plot_shapely


class PcbObj:

    GBR_KEYS = ["top", "bottom", "profile"]
    EXN_KEYS = ["drill"]
    DEFAULT_ARC_SUBDIVISIONS = 64
    MAX_ARC_CHORD_LEN = 0.2  # mm
    MIN_ARC_CHORD_LEN = 0.02  # mm

    def __init__(self):

        self.gerbers = Od({})
        self.excellons = Od({})
        self.init_data()
        self.arc_angle = 2.0 * math.pi / self.DEFAULT_ARC_SUBDIVISIONS
        self.arc_max_len = self.MAX_ARC_CHORD_LEN
        self.arc_min_len = self.MIN_ARC_CHORD_LEN
        self.layers = Od({})

    def get_arc_subdivisions(self):
        return int(2.0 * math.pi / self.arc_angle)

    def set_arc_subdivisions(self, arc_sub):
        self.arc_angle = 2.0 * math.pi / arc_sub

    def init_data(self):
        for k in self.GBR_KEYS:
            self.gerbers[k] = None

        for k in self.EXN_KEYS:
            self.excellons[k] = None

    def get_gerber(self, tag):
        if tag in self.GBR_KEYS:
            if self.gerbers[tag] is not None:
                return self.gerbers[tag]
            else:
                pass
        print("[ERROR] GERBER NOT FOUND")
        return None

    def get_excellon(self, tag):
        if tag in self.EXN_KEYS:
            if self.excellons[tag] is not None:
                return self.excellons[tag]
            else:
                pass
        print("[ERROR] GERBER NOT FOUND")
        return None

    def load_gerber(self, path, tag):
        if tag not in self.GBR_KEYS:
            print("[ERROR] GERBER TAG NOT RECOGNIZED")
            return False
        if not os.path.isfile(path):
            print("[ERROR] GERBER FILE NOT FOUND")
            return False
        tmp = gbr.read(path)
        self.gerbers[tag] = tmp
        self.gerbers[tag].to_metric()

    def load_excellon(self, path, tag):
        if tag not in self.EXN_KEYS:
            print("[ERROR] EXCELLON TAG NOT RECOGNIZED")
            return False
        if not os.path.isfile(path):
            print("[ERROR] EXCELLON FILE NOT FOUND")
            return False

        self.excellons[tag] = gbr.read(path)
        self.excellons[tag].to_metric()

    def get_gerber_layer(self, tag):
        g = self.get_gerber(tag)
        mp = []
        for primitive in g.primitives:
            gdata = self._primitive_paths(primitive)
            for gd in gdata:
                g = Geom(gd)
                if g.closed:
                    mp.append(g)
        self.layers[tag] = merge_polygons(mp)
        return self.layers[tag]

    def get_excellon_layer(self, tag):
        g = self.get_excellon(tag)
        mp = []
        for primitive in g.primitives:
            gdata = self._primitive_paths(primitive)
            for gd in gdata:
                g = Geom(gd)
                if g.closed:
                    mp.append(g)
        self.layers[tag] = merge_polygons(mp)
        return self.layers[tag]

    def _arc_segmentation(self, center, radius, start_angle, end_angle, forced_divisions=None):

        if forced_divisions is None:
            divisions = int(abs(end_angle - start_angle) / self.arc_angle)

            # The coordinates of the arc
            # theta = np.radians(np.linspace(start_angle, end_angle, self.arc_subdivisions))

            # chord length 2 * r * sin(theta/2)
            clen = abs(2.0 * radius * math.sin(0.5 * self.arc_angle))
            # print(clen)

            if clen < self.arc_min_len:
                min_theta = self.arc_min_len / radius
                divisions = int(abs(end_angle - start_angle) / min_theta)

            elif clen > self.arc_max_len:
                max_theta = self.arc_max_len / radius
                divisions = int(abs(end_angle - start_angle) / max_theta)

            divisions = max(divisions, 4)
        else:
            divisions = forced_divisions



        theta = np.linspace(start_angle, end_angle, divisions)

        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        arc_discretization = np.column_stack((x, y))
        arc_discretization = [tuple(x) for x in arc_discretization]
        return arc_discretization

    def _get_enhanced_line(self, primitive):
        if primitive.start[0] - primitive.end[0] >= 0:
            start = primitive.start
            end = primitive.end
        else:
            start = primitive.end
            end = primitive.start

        radius = 0.0
        if isinstance(primitive.aperture, gbr.primitives.Rectangle):
            radius = primitive.aperture.height / 4.0
            subdivisions = 2
        elif isinstance(primitive.aperture, gbr.primitives.Circle):
            radius = primitive.aperture.radius
            #print("Radius: " + str(radius))
            subdivisions = 60

        if radius != 0.0:
            # print(radius)
            # print(start)
            # print(end)
            sr = abs(complex(*start) - complex(*end))
            if sr == 0.0:
                sr += 2.0 * math.pi
            theta_sin = math.asin((start[1] - end[1]) / sr)
            theta_cos = math.acos((start[0] - end[0]) / sr)
            theta = theta_sin

            if abs(theta_sin) < 1e-15:
                theta = theta_cos
            start_theta = math.pi / 2.0 + theta
            end_theta = - math.pi / 2.0 + theta
            points = self._arc_segmentation(start, radius, start_theta, end_theta,
                                            forced_divisions=subdivisions)
            start_theta = math.pi / 2.0 + theta + math.pi
            end_theta = - math.pi / 2.0 + theta + math.pi
            points += self._arc_segmentation(end, radius, end_theta, start_theta,
                                             forced_divisions=subdivisions)
            # if isinstance(primitive.aperture, gbr.primitives.Rectangle) and False:
            #     fig, ax = plt.subplots(1, 1)
            #     ax.plot(*zip(*points))
            #     pts = convex_hull(points)
            #     ax.plot(*zip(*pts))
            #     line = [start, end]
            #     ax.plot(*zip(*line), '-o')
            #     ax.set_aspect('equal', 'box')
            #     fig.tight_layout()
            #     plt.show()
            return convex_hull(points)
        else:
            return [primitive.start, primitive.end]

    @staticmethod
    def _get_region_polygon(gdata):
        # poligono di timpo EAGLE
        points = []
        for g in gdata:
            points += g["points"]
        return points

    def _primitive_paths(self, primitive, region=False):
            gdata = []
            verbose_flag = False
            if isinstance(primitive, gbr.primitives.Outline):
                # tipo closed line
                if verbose_flag:
                    print("Closed line")
                points = primitive.vertices
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Line):
                closed_flag = True
                # tipo open line
                if verbose_flag:
                    print("Open line")
                points = primitive.vertices
                if isinstance(primitive.aperture, gbr.primitives.Circle):
                    if verbose_flag:
                        print("\t with rounded end")
                        pts = [primitive.start, primitive.end]
                        print(pts)
                    if not region:
                        # print("\t with flat end")
                        points = self._get_enhanced_line(primitive)
                    else:
                        points = [primitive.start, primitive.end]
                        closed_flag = False
                if isinstance(primitive.aperture, gbr.primitives.Rectangle):
                    if not region:
                        # print("\t with flat end")
                        points = self._get_enhanced_line(primitive)
                    else:
                        points = [primitive.start, primitive.end]
                        closed_flag = False
                        # print("\t with point end")
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': closed_flag}]
                if points is None:
                    points = [primitive.start, primitive.end]
                    gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': False}]
            elif isinstance(primitive, gbr.primitives.Arc):
                # tipo open line arc
                if verbose_flag:
                    print("Arc")
                p = primitive
                points = self._arc_segmentation(p.center, p.radius, p.start_angle, p.end_angle)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': False}]
            elif isinstance(primitive, gbr.primitives.Rectangle):
                # tipo polygon
                if verbose_flag:
                    print("Rectangle")
                points = primitive.vertices
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Polygon):
                # tipo polygon
                if verbose_flag:
                    print("Polygon")
                points = primitive.vertices
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Circle):
                # tipo polygon
                if verbose_flag:
                    print("Circle")
                p = primitive
                points = self._arc_segmentation(p.position, p.radius, 0, 2 * math.pi)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Obround):
                # tipo polygon
                if verbose_flag:
                    print("Obround")
                p = primitive
                circle1 = p.subshapes["circle1"]
                circle2 = p.subshapes["circle2"]
                points1 = self._arc_segmentation(circle1.position, circle1.radius, 0, 2 * math.pi)
                points2 = self._arc_segmentation(circle2.position, circle2.radius, 0, 2 * math.pi)
                points = convex_hull(points1 + points2)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Region) or isinstance(primitive, gbr.primitives.AMGroup):
                # tipo group
                if verbose_flag:
                    if region:
                        print("Region of Region")
                    else:
                        if isinstance(primitive, gbr.primitives.AMGroup):
                            print("AMGroup")
                        else:
                            print("REGION")
                if primitive.primitives is not None:
                    lines_flag = True
                    for p in primitive.primitives:
                        gdata += self._primitive_paths(p, region=True)
                        lines_flag &= isinstance(p, gbr.primitives.Line)
                    if lines_flag:
                        # controllo che la linea sia chiusa
                        p0 = primitive.primitives[0]
                        p1 = primitive.primitives[-1]
                        if p0.start != p1.end:
                            points = [p1.end, p0.start]
                            gd = [{'points': points, 'polarity': primitive.level_polarity, 'closed': False}]
                            gdata += gd

                        points = self._get_region_polygon(gdata)
                        gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Drill):
                # tipo drill
                if verbose_flag:
                    print("Drill")
                p = primitive
                points = self._arc_segmentation(p.position, p.radius, 0, 2 * math.pi)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]

            # elif isinstance(primitive, gbr.primitives.AMGroup):
            #     # tipo group
            #     if verbose_flag:
            #         print("AMGroup")
            #     if primitive.primitives is not None:
            #         lines_flag = True
            #         for p in primitive.primitives:
            #             gdata += self._primitive_paths(p, region=True)
            #             lines_flag &= isinstance(p, gbr.primitives.Line)
            #         if lines_flag:
            #             points = self._get_region_polygon(gdata)
            #             gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]

            else:
                print("[ERROR] PRIMITIVE NOT RECOGNIZED")
                print(primitive)
            return gdata

# -----------------------------------------------------------------------------


if __name__ == '__main__':

    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test1\\gerbers_file\\copper_top.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test1\\gerbers_file\\copper_bottom.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test2\\gerbers_file\\copper_bottom.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test2\\gerbers_file\\profile.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test3\\gerbers_file\\JST_motor_breakout_board-F_Cu.gbr"

    pcb = PcbObj()
    pcb.load_gerber(gerber_path, 'top')
    gtop = pcb.get_gerber('top')
    pcb.get_gerber_layer('top')
