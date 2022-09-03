
import os
import time
import gerber as gbr
import gerber.primitives
from gerber.excellon_statements import ToolSelectionStmt, CoordinateStmt, EndOfProgramStmt, SlotStmt, FormatStmt
# from gerber.render.cairo_backend import GerberCairoContext
from gerber.excellon import DrillSlot, DrillHit, ExcellonParser
from gerber.excellon import loads as exc_load
from gerber.cam import FileSettings

import numpy as np
import math
from gerber.utils import convex_hull
from collections import OrderedDict as Od

from .geometry_manager import Geom, merge_polygons
# import matplotlib.pyplot as plt


class PcbObj:

    GBR_KEYS = ["top", "bottom", "profile"]
    EXN_KEYS = ["drill"]
    DEFAULT_ARC_SUBDIVISIONS = 64
    MAX_ARC_CHORD_LEN = 0.5  # mm
    MIN_ARC_CHORD_LEN = 0.1  # mm

    def __init__(self):

        self.gerbers = Od({})
        self.excellons = Od({})
        self.init_data()
        self.arc_angle = 2.0 * math.pi / self.DEFAULT_ARC_SUBDIVISIONS
        self.arc_max_len = self.MAX_ARC_CHORD_LEN
        self.arc_min_len = self.MIN_ARC_CHORD_LEN
        self.layers = Od({})
        self.am_group = False

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
        # unit conversion used to FIX bug in pcb-tools
        if tmp.units == 'inch':
            self.gerbers[tag].to_metric()
            self.gerbers[tag] = gbr.loads(self.dump_str(tmp))

        # self.render_layer(tmp)

    @staticmethod
    def dump_str(gerber_obj, data_type="gerber", ext_settings=None):
        # used to FIX bug in pcb-tools that doesn't work properly
        # tip: file conversion to metric before geom parser
        print("Converting file units to metric")
        string = ""
        if ext_settings is not None:
            settings = ext_settings
        else:
            settings = gerber_obj.settings

        if data_type == "gerber":
            for stmt in gerber_obj.statements:
                string += str(stmt.to_gerber(gerber_obj.settings)) + "\n"
        else:
            # for stmt in gerber_obj.statements:
            #     string += str(stmt.to_excellon(settings)) + "\n"

            for statement in gerber_obj.statements:
                if not isinstance(statement, ToolSelectionStmt) and not isinstance(statement, FormatStmt):
                    string += statement.to_excellon(settings) + '\n'
                else:
                    if isinstance(statement, FormatStmt):
                        pass
                    else:
                        break

            k = 25.4
            # Write out coordinates for drill hits by tool
            for tool in iter(gerber_obj.tools.values()):
                data = ToolSelectionStmt(tool.number)
                string += data.to_excellon(settings) + '\n'
                for hit in gerber_obj.hits:
                    if hit.tool.number == tool.number:
                        if isinstance(hit, DrillHit):
                            string += CoordinateStmt(hit.position[0] * k, hit.position[1] * k).to_excellon(settings) + '\n'
                        elif isinstance(hit, DrillSlot):
                            string += CoordinateStmt(hit.start[0] * k, hit.start[1] * k).to_excellon(
                                settings) + '\n'
                            string += CoordinateStmt(hit.end[0] * k, hit.end[1] * k).to_excellon(
                                settings) + '\n'
                            # string += SlotStmt(hit.start[0]*1e3, hit.start[1]*1e3, hit.end[0]*1e3, hit.end[1]*1e3).to_excellon(settings) + '\n'
            string += EndOfProgramStmt().to_excellon() + '\n'
        return string

    def load_excellon(self, path, tag):
        if tag not in self.EXN_KEYS:
            print("[ERROR] EXCELLON TAG NOT RECOGNIZED")
            return False
        if not os.path.isfile(path):
            print("[ERROR] EXCELLON FILE NOT FOUND")
            return False

        tmp = gbr.read(path)
        self.excellons[tag] = tmp
        if tmp.units == 'inch':
            self.excellons[tag].to_metric()  # pcb-tools has a bug related to the inch -> metric conversion
                                             # a workaround is applied, during the dump process all the xy points
                                             # coordinates are converted in metric by default

            settings = FileSettings(format=(3, 3), zero_suppression='leading', units='metric', notation='absolute',
                                    angle_units='degrees')
            data = self.dump_str(self.excellons[tag], data_type="excellon", ext_settings=settings)
            self.excellons[tag] = exc_load(data, settings=settings)

    # def render_layer(self, layer):
    #
    #     # Create a new drawing context
    #     ctx = GerberCairoContext(1200)
    #     ctx.color = (80. / 255, 80 / 255., 154 / 255.)
    #     ctx.drill_color = ctx.color
    #
    #     # Draw the layer, and specify the rendering settings to use
    #     layer.render(ctx)
    #
    #     outfile = os.path.join(os.path.dirname(__file__), 'pcb_top.png')
    #
    #     # Write output to png file
    #     print("Writing output to: {}".format(outfile))
    #     ctx.dump(os.path.join(os.path.dirname(__file__), 'outputs', outfile))

    def get_gerber_layer(self, tag):
        print("Get Gerber Layer")
        start_time = time.time()
        g = self.get_gerber(tag)
        mp = []
        print("*** %s seconds ---" % (time.time() - start_time))
        for primitive in g.primitives:
            primitive.to_metric()
            gdata = self._primitive_paths(primitive)
            for gd in gdata:
                g = Geom(gd)
                if g.closed:
                    mp.append(g)

        print("**- %s seconds ---" % (time.time() - start_time))
        self.layers[tag] = merge_polygons(mp)
        print("*-- %s seconds ---" % (time.time() - start_time))
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

    def _arc_segmentation(self, center, radius, arc_start_angle, arc_end_angle, direction='clockwise', forced_divisions=None):

        start_angle = arc_start_angle
        end_angle = arc_end_angle

        if direction == 'clockwise':
            if start_angle < end_angle:
                start_angle += 2 * math.pi
        else:
            # counterclockwise doesn't check
            if start_angle > end_angle:
                end_angle += 2 * math.pi

        circle = False
        if start_angle == end_angle:
            # bad circle definition
            circle = True

        if forced_divisions is None:
            if not circle:
                divisions = int(abs(end_angle - start_angle) / self.arc_angle)
            else:
                divisions = int(2.0 * math.pi / self.arc_angle)

            # The coordinates of the arc
            # theta = np.radians(np.linspace(start_angle, end_angle, self.arc_subdivisions))

            # chord length 2 * r * sin(theta/2)
            clen = abs(2.0 * radius * math.sin(0.5 * self.arc_angle))

            if clen < self.arc_min_len:
                min_theta = self.arc_min_len / radius
                if not circle:
                    divisions = int(abs(end_angle - start_angle) / min_theta)
                else:
                    divisions = int(2.0 * math.pi / min_theta)

            elif clen > self.arc_max_len:
                max_theta = self.arc_max_len / radius
                if not circle:
                    divisions = int(abs(end_angle - start_angle) / max_theta)
                else:
                    divisions = int(2.0 * math.pi / max_theta)

            divisions = max(divisions, 4)
        else:
            divisions = forced_divisions

        if not circle:
            theta = np.linspace(start_angle, end_angle, divisions)
        else:
            theta = np.linspace(0, 2.0 * math.pi, divisions)

        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        arc_discretization = np.column_stack((x, y))
        arc_discretization = [tuple(x) for x in arc_discretization]
        return arc_discretization

    def _get_enhanced_line(self, l_start, l_end, aperture):
        if l_start[0] - l_end[0] >= 0:
            start = l_start
            end = l_end
        else:
            start = l_end
            end = l_start

        radius = 0.0

        if isinstance(aperture, gbr.primitives.Rectangle):
            #radius = max(aperture.height, aperture.width) / 4.0
            print(aperture.height)
            print(aperture.width)
            radius = aperture.height / 4.0
            subdivisions = 4
        elif isinstance(aperture, gbr.primitives.Circle):
            radius = aperture.radius
            subdivisions = 60

        if radius != 0.0:
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
                                            forced_divisions=int(subdivisions/2))

            # sign inverted (Geekoid testcase)
            start_theta = - math.pi / 2.0 + theta + math.pi
            end_theta = math.pi / 2.0 + theta + math.pi
            points += self._arc_segmentation(end, radius, end_theta, start_theta,
                                             forced_divisions=int(subdivisions/2))

            return convex_hull(points)
        else:
            return [l_start, l_end]

    @staticmethod
    def _get_region_polygon(gdata, vectors=False):
        points = []
        if not vectors:
            # EAGLE type polygon
            flag = False
            for g in gdata:
                if flag:
                    if points[-1] == g["points"][0]:
                        points += g["points"][1:]
                    else:
                        points += g["points"]
                else:
                    points += g["points"]
                flag = True
        else:
            # AM Group Outline Vectors Description
            gd = gdata.copy()
            last = gd.pop()["points"][-1]
            for g in gd:
                for p in g["points"]:
                    if p != last:
                        points.append(p)
            points += [last]
            points.append(last)
        return points

    def _primitive_paths(self, primitive, region=False):
            gdata = []
            verbose_flag = False

            if isinstance(primitive, gbr.primitives.Line):
                closed_flag = True
                # open line type
                if verbose_flag:
                    print("Open line")
                points = primitive.vertices
                avaible_type = ()

                if isinstance(primitive.aperture, gbr.primitives.Circle) or \
                        isinstance(primitive.aperture, gbr.primitives.Rectangle):
                    # if verbose_flag:
                    #     print("\t with rounded end")
                    #     pts = [primitive.start, primitive.end]
                    #     print(pts)
                    if not region or self.am_group:
                        points = self._get_enhanced_line(primitive.start, primitive.end, primitive.aperture)
                    else:
                        points = [primitive.start, primitive.end]
                        closed_flag = False
                    #print(points)

                # if isinstance(primitive.aperture, gbr.primitives.Rectangle):
                #     if not region:
                #         points = self._get_enhanced_line(primitive.start, primitive.end, primitive.aperture)
                #     else:
                #         points = [primitive.start, primitive.end]
                #         closed_flag = False
                #     #print(points)

                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': closed_flag}]
                if points is None:
                    points = [primitive.start, primitive.end]
                    gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': False}]

            elif isinstance(primitive, gbr.primitives.Arc):
                # open line arc type
                if verbose_flag:
                    print("Arc")
                p = primitive
                points = self._arc_segmentation(p.center, p.radius, p.start_angle, p.end_angle, direction=p.direction)

                if isinstance(primitive.aperture, gbr.primitives.Circle) or \
                        isinstance(primitive.aperture, gbr.primitives.Rectangle) and not region:
                        pts = points.copy()
                        pp = pts.pop(0)
                        gdata = []
                        for np in pts:
                            l_points = self._get_enhanced_line(pp, np, primitive.aperture)
                            gdata.append({'points': l_points, 'polarity': primitive.level_polarity, 'closed': True})
                            pp = np
                else:
                    gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': False}]

            elif isinstance(primitive, gbr.primitives.Rectangle):
                # rectangle type
                if verbose_flag:
                    print("Rectangle")
                points = primitive.vertices
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Polygon):
                # polygon type
                if verbose_flag:
                    print("Polygon")
                points = primitive.vertices
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Circle):
                # circle type
                if verbose_flag:
                    print("Circle")
                p = primitive
                points = self._arc_segmentation(p.position, p.radius, 0, 2 * math.pi)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
            elif isinstance(primitive, gbr.primitives.Obround):
                # obround type
                if verbose_flag:
                    print("Obround")
                p = primitive
                circle1 = p.subshapes["circle1"]
                circle2 = p.subshapes["circle2"]
                points1 = self._arc_segmentation(circle1.position, circle1.radius, 0, 2 * math.pi)
                points2 = self._arc_segmentation(circle2.position, circle2.radius, 0, 2 * math.pi)
                points = convex_hull(points1 + points2)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]

            elif isinstance(primitive, gbr.primitives.Region) or \
                    isinstance(primitive, gbr.primitives.AMGroup) \
                    or isinstance(primitive, gbr.primitives.Outline):
                # group type

                am_group = False
                if isinstance(primitive, gbr.primitives.AMGroup):
                    self.am_group = True
                    am_group = True

                if verbose_flag:
                    if region:
                        print("Region of Region")
                    else:
                        if isinstance(primitive, gbr.primitives.AMGroup):
                            print("AMGroup")
                            print("Primitives: " + str(primitive.primitives))
                        else:
                            print("REGION")

                if primitive.primitives is not None:
                    lines_flag = True
                    pp = primitive.primitives.copy()
                    for p in pp:
                        gdata += self._primitive_paths(p, region=True)
                        lines_flag &= isinstance(p, gbr.primitives.Line) or isinstance(p, gbr.primitives.Arc)
                    if lines_flag:
                        # check if the line is closed
                        p0 = primitive.primitives[0]
                        p1 = primitive.primitives[-1]
                        if p0.start != p1.end:
                            points = [p1.end, p0.start]
                            gd = [{'points': points, 'polarity': primitive.level_polarity, 'closed': False}]
                            gdata += gd

                        vectors = False
                        if self.am_group and isinstance(primitive, gbr.primitives.Outline):
                            vectors = p1.start == p1.end

                        points = self._get_region_polygon(gdata, vectors)
                        gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]
                if am_group:
                    self.am_group = False

            elif isinstance(primitive, gbr.primitives.Drill):
                # drill type
                if verbose_flag:
                    print("Drill")
                p = primitive
                points = self._arc_segmentation(p.position, p.radius, 0, 2 * math.pi)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]

            elif isinstance(primitive, gbr.primitives.Slot):
                # drill type
                if verbose_flag:
                    print("Slot")
                p = primitive
                points1 = self._arc_segmentation(p.start, p.diameter/2.0, 0, 2 * math.pi)
                points2 = self._arc_segmentation(p.end, p.diameter/2.0, 0, 2 * math.pi)
                points = convex_hull(points1 + points2)
                gdata = [{'points': points, 'polarity': primitive.level_polarity, 'closed': True}]

            # elif isinstance(primitive, gbr.primitives.AMGroup):
            #     # group type
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

            return gdata


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test1\\gerbers_file\\copper_top.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test1\\gerbers_file\\copper_bottom.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test2\\gerbers_file\\copper_bottom.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test2\\gerbers_file\\profile.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test3\\gerbers_file\\JST_motor_breakout_board-F_Cu.gbr"
    gerber_path = "C:\\Users\\mmatt\\Desktop\\Gerber\\LedKeyring-F_Cu.gbr"

    pcb = PcbObj()
    pcb.load_gerber(gerber_path, 'top')
    gtop = pcb.get_gerber('top')
    pcb.get_gerber_layer('top')
