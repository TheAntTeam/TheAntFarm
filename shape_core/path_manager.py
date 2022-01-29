#
import time
from shapely.geometry import Polygon, LineString, MultiLineString, Point, MultiPoint
from shapely.ops import substring
from collections import OrderedDict
from .geometry_manager import merge_polygons_path, offset_polygon, offset_polygon_holes, get_bbox_area_sh, fill_holes_sh, get_poly_diameter
from .path_optimizer import Optimizer
import numpy as np


class Gapper:

    DEFAULT_STRATEGIES = (
        "none",
        "2h",
        "2v",
        "4p",
        "4h",
        "4v",
        "8p",
        "4x"
    )

    def __init__(self, path, cfg):
        self.cfg = cfg
        self.in_path = path
        self.gap_dim = self.cfg['taps_length'] + self.cfg['tool_diameter']

    @staticmethod
    def rotate(l, n):
        return l[n:] + l[:n]

    def get_available_strategies(self):
        return self.DEFAULT_STRATEGIES

    def add_taps_on_external_path(self, strategy='4p'):
        ex_path = self.in_path
        b = ex_path.bounds

        xm = (b[2] + b[0]) / 2.0
        ym = (b[3] + b[1]) / 2.0

        x2 = np.linspace(b[0], b[2], 4)[1:3]
        y2 = np.linspace(b[1], b[3], 4)[1:3]

        v2l = [
            LineString(((x2[0], b[1]), (x2[0], b[3]))),
            LineString(((x2[1], b[1]), (x2[1], b[3])))
        ]

        h2l = [
            LineString(((b[0], y2[0]), (b[2], y2[0]))),
            LineString(((b[0], y2[1]), (b[2], y2[1])))
        ]

        # straight cross
        vl = LineString(((xm, b[1]), (xm, b[3])))
        hl = LineString(((b[0], ym), (b[2], ym)))

        # 45 degree cross
        lrl = LineString(((b[0], b[1]), (b[2], b[3])))
        rll = LineString(((b[2], b[1]), (b[0], b[3])))

        lines_list = None

        if strategy == '8p':
            # find intersection points between
            # v2l h2l and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = v2l + h2l

        if strategy == '4p':
            # find intersection points between
            # vl hl and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [vl, hl]

        if strategy == '4x':
            # find intersection points between
            # lrl rll and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [lrl, rll]

        if strategy == '2h':
            # find intersection points between
            # hl and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [hl]

        if strategy == '4h':
            # find intersection points between
            # h2l and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = h2l

        if strategy == '2v':
            # find intersection points between
            # vl and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [vl]

        if strategy == '4v':
            # find intersection points between
            # v2l and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = v2l

        if lines_list is not None:
            tappered = self.get_tappered_path(ex_path, lines_list)
            return tappered
        else:
            return [ex_path]

    def get_tappered_path(self, ex_path, intersect_line):
        points = list(ex_path.coords)
        pts = []
        for line in intersect_line:
            lb = line.boundary
            pts += [lb[0], lb[1]]
        pts_ll = []
        ids = []
        pids = []
        lids = []
        for p in pts:
            d = ex_path.project(p)
            pt = ex_path.interpolate(d)
            pts_ll.append(pt)
            c = 0
            for i, j in zip(points, points[1:]):
                if LineString((i, j)).distance(pt) < 1e-8:
                    ids.append(c)
                    pids.append(pt)
                    lids.append(d)
                c += 1

        temp = sorted(zip(lids, ids, pids), key=lambda x: x[0])
        lids, ids, pids = map(list, zip(*temp))

        ids.append(ids[0])
        pids.append(pids[0])

        c = 0
        lsl = []
        ls = []
        points.pop()
        for j, p in enumerate(points):
            ls.append(p)
            if j == ids[c]:
                ls.append(pids[c])
                lsl.append(ls)
                ls = [pids[c]]
                c += 1
                while ids[c-1] == ids[c]:
                    lsl.append(ls + [pids[c]])
                    ls = [pids[c]]
                    c += 1

        lsl[0] = ls + lsl[0]
        nl = []
        for ll in lsl:
            ls = LineString(ll)
            if self.gap_dim < ls.length:
                nls = substring(ls, start_dist=self.gap_dim / 2.0, end_dist=ls.length - self.gap_dim / 2.0)
                nl.append(nls)

        return nl


class MachinePath:

    MIN_AREA = 0.1e-1
    TD_COEFF = 0.999

    def __init__(self, tag, machining_type='gerber'):
        # machining type
        # gerber, profile

        self.tag = tag

        self.geom_list = []
        if machining_type == 'gerber':
            self.cfg = {'tool_diameter': 0.2, 'passages': 3, 'overlap': 0.3}
            if self.cfg['passages'] < 1:
                print("[WARNING] At Least One Pass")
                self.cfg['passages'] = 1
        elif machining_type == 'profile':
            self.cfg = {'tool_diameter': 1.0, 'margin': 0.1, 'taps_type': 3, 'taps_length': 1.0}
        elif machining_type == 'pocketing':
            self.cfg = {'tool_diameter': 1.0}
        elif machining_type == 'drill':
            # self.cfg = {'tool_diameter': 1.0, 'bits_diameter': [1.0, 0.8, 0.6, 0.4]}
            self.cfg = {'tool_diameter': None, 'bits_diameter': [0.8], 'optimize': False}
        else:
            self.cfg = {}
        self.type = machining_type
        self.path = None

    def load_cfg(self, cfg):
        print("Cfg")
        print(cfg)
        self.cfg = cfg

    def get_path(self):
        return self.path

    def load_geom(self, geom_list):
        self.geom_list = geom_list

    def execute(self):
        elabs = None
        if self.type == 'gerber':
            self.execute_gerber()
        elif self.type == 'profile':
            self.execute_profile()
        elif self.type == 'pocketing':
            elabs = self.execute_pocketing()
        elif self.type == 'drill':
            # if there is a valid pocketing tool
            # the pocketing process is performed
            # otherwise only the holes are drilled
            elabs_p = None
            if self.cfg['tool_diameter'] is not None and self.cfg['milling_tool']:
                elabs_p = self.execute_pocketing()

            # if a pocketing process was performed
            # elabs will contain a list of bools which identify the performed holes
            # to be discaded in the next drilling phase
            elabs_d = self.execute_drill(not_to_drill=elabs_p)

            # at the end, checking the elabs list, it will possible notice to the
            # user which holes were not drilled
            elabs = []

            if elabs_p is not None:
                for i in range(len(elabs_d)):
                    elabs.append(elabs_p[i] or elabs_d[i])

            if elabs is not None:
                if not all(elabs):
                    print("Not all holes are computed, please add bits with correct diameter")

        return elabs

    def execute_gerber(self):
        # the first pass performed is the one closest to the PCB traces
        t0 = time.time()
        og_list = []
        prev_poly = []
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, td/2.0)
            if og is not None:
                og_list.append(og)

        og_list = merge_polygons_path(og_list, as_list=True)

        # for the next steps, starting from the previous path, enlarge it by the tool radius
        # make bollean or on it and then reduce it by the tool radius
        # at that point it is enlarged by the <diameter of the tool> * (1 - <overlap_percentage>)
        # todo: check the formula
        for i in range(self.cfg['passages']-1):
            sub_og_list = self._subpath_execute(og_list)
            og_list += sub_og_list

        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")

        og_list = self.check_min_area(og_list)

        # extract the linestring from paths polygons
        path = []
        for g in og_list:
            ex_path = g.exterior
            if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                path.append(ex_path)
            for i in g.interiors:
                if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                    path.append(i)
        t_d = self.cfg['tool_diameter']
        self.path = [((t_d, "gerber"), path)]

    def check_min_area(self, og_list):
        big_poly = []
        old_poly = 0
        new_poly = 0
        for p in og_list:
            old_poly += 1
            new_inners = []
            for inner in p.interiors:
                old_poly += 1
                # need to make a polygon of the linearring to get the _filled_ area of
                # the closed ring.
                if abs(Polygon(inner).area) >= self.MIN_AREA:
                    new_inners.append(inner)
            if abs(Polygon(p.exterior).area) >= self.MIN_AREA:
                p = Polygon(p.exterior, new_inners)
                new_poly += 1 + len(p.interiors)
                big_poly.append(p)

        print("REMOVED: " + str(old_poly - new_poly))

        return big_poly

    def execute_pocketing(self):
        print("Pocketing")
        # the first pass performed is the one closest to the hole perimeter
        t0 = time.time()
        og_list = []
        prev_poly = []
        milled_list = []
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, - td / 2.0)
            if og is not None:
                if not og.is_empty:
                    og_list.append(og)
                    milled_list.append(True)
                else:
                    milled_list.append(False)
            else:
                milled_list.append(False)

        # for the next steps, starting from the previous path, enlarge it by the tool radius
        # make bollean or on it and then reduce it by the tool radius
        # at that point it is enlarged by the <diameter of the tool> * (1 - <overlap_percentage>)
        # todo: check the formula

        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")

        # extract the linestring from paths polygons
        path = []
        for g in og_list:
            ex_path = g.exterior
            if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                path.append(ex_path)
            for i in g.interiors:
                if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                    path.append(i)
        t_d = self.cfg['tool_diameter']
        self.path = [((t_d, "pocketing"), path)]

        return milled_list

    def execute_drill(self, not_to_drill=None):
        print("Drilling")
        t0 = time.time()
        bd = self.cfg['bits_diameter'][:]
        bd.sort(reverse=True)

        to_drill = [True] * len(self.geom_list)
        if not_to_drill is not None:
            to_drill = [not elem for elem in not_to_drill]

        drilled_list = []
        drills = []
        for i, g in enumerate(self.geom_list):
            if to_drill[i]:
                drilled_list.append(True)
                c = g.geom.centroid
                ds = get_poly_diameter(g.geom)
                # with the diameter of the hole,
                # it is possible to select the bit to be used for drilling
                # among those available.
                # the tip with the diameter closest to that of the hole
                # but never greater than it will be selected
                for j, d in enumerate(ds):
                    drills.append([i, c.coords[j], d])
            else:
                drilled_list.append(False)

        drills.sort(key=lambda x: x[2], reverse=True)

        drill_per_bit = OrderedDict()
        b = bd[0]
        c = 1
        for dd in drills:
            d = dd[2]
            while b > d and c < len(bd):
                b = bd[c]
                c += 1
            if b not in drill_per_bit.keys():
                drill_per_bit[b] = []
            drill_per_bit[b].append(dd[1])

        for bit_k in drill_per_bit.keys():
            bit_points = drill_per_bit[bit_k]
            if 'optimize' in self.cfg.keys():
                if self.cfg['optimize']:
                    opt = Optimizer(bit_points)
                    optimized_bit_points = opt.get_optimized_path()
                    drill_per_bit[bit_k] = optimized_bit_points
                    #print("Bit " + str(bit_k) + " " + str(optimized_bit_points))
                else:
                    #print("Bit " + str(bit_k) + " " + str(bit_points))
                    pass

        paths = []
        for k in drill_per_bit:
            paths.append(((k, "drill"), [LineString(drill_per_bit[k])]))

        # if holes have already been performed by the pocketing procedure,
        # the drilling path will be append to the pocketing one

        if not_to_drill is not None:
            if any(not_to_drill) and self.path is not None:
                self.path += paths
            else:
                self.path = paths
        else:
            self.path = paths

        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")

        return drilled_list

    def execute_profile(self):
        # to compute the profile path, the external perimeter of the board need to be
        # detected. The perimeter of the geom that contains all the other geom
        # will be chose as profile perimeter.
        # If the external geom is unique its holes will be considered otherwise multiple external
        # geoms are present, their perimeters will be considered as contours of holes

        t0 = time.time()
        og_list = []
        prev_poly = [g.geom for g in self.geom_list]
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        # uniqueness check of the profile
        if len(self.geom_list) == 1:
            # unique profile
            ext_path = offset_polygon(fill_holes_sh(self.geom_list[0].geom),
                                      td / 2.0 + self.cfg['margin'], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)
        else:
            # profile composed by multiple polygons
            # to identify the external profile I calculate the areas of the bboxes of each polygon.
            # the polygon with the largest bbox will be the outer one.
            geoms = [g.geom for g in self.geom_list]
            bba = get_bbox_area_sh(geoms.pop(0))
            id = 0

            for i, p in enumerate(geoms):
                a = get_bbox_area_sh(p)
                if a > bba:
                    bba = a
                    id = i + 1

            # id contains the index of the polygon with biggest bbox
            # todo: check, are all the remaining polygons contained in the biggest one?

            ext_p = self.geom_list[id]
            ext_path = offset_polygon(fill_holes_sh(ext_p.geom),
                                      td / 2.0 + self.cfg['margin'], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)

            for i, g in enumerate(self.geom_list):
                if i != id:
                    og = offset_polygon_holes(g, - (td / 2.0 + self.cfg['margin']))
                    if og is not None:
                        og_list.append(og)

        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")

        # extracting linestring from the polygon path
        path = []
        for g in og_list:
            ex_path = g.exterior
            if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                path.append(ex_path)
            for i in g.interiors:
                if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                    path.append(i)

        # add taps
        # based on the selected tap strategy
        t = Gapper(path[0], self.cfg)
        stl = t.get_available_strategies()
        st = stl[self.cfg["taps_type"]]
        print("Strategy")
        print(st)
        new_ext = t.add_taps_on_external_path(strategy=st)
        path.pop(0)
        path = new_ext + path

        # todo: add the option to make tap for the perimeter holes
        # I was thinking of something that would put at least 2 gaps
        # in case the hole had a perimeter greater than a fixed parameter such as 30mm
        # parameter could be set by GUI or settings page

        t_d = self.cfg['tool_diameter']
        self.path = [((t_d, "profile"), path)]

    def _subpath_execute(self, ppg_list):

        ov = self.cfg['overlap']

        # ppg_list pre path list
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        pre_offset = td/2.0 * (1 + 0.5 - ov)
        og_list = []

        for g in ppg_list:
            og = offset_polygon(g, pre_offset, shapely_poly=True)
            if og is not None:
                if og.geom_type == 'MultiPolygon':
                    for sog in og:
                        og_list.append(sog)
                else:
                    og_list.append(og)
        mg_list = merge_polygons_path(og_list)

        mog_list = []
        for g in mg_list:
            mog = offset_polygon(g, -pre_offset, shapely_poly=True)
            if mog is not None:
                if mog.geom_type == 'MultiPolygon':
                    for smog in mog:
                        mog_list.append(smog)
                else:
                    mog_list.append(mog)

        # the last operation is defined based on the tool diameter and the overlap value

        ng_list = []
        for g in mog_list:
            ng = offset_polygon(g, td / 2.0 * (1 + 0.5 - ov), shapely_poly=True)
            if ng is not None:
                if ng.geom_type == 'MultiPolygon':
                    for sng in ng:
                        ng_list.append(sng)
                else:
                    ng_list.append(ng)

        fmg_list = merge_polygons_path(ng_list)

        return fmg_list
