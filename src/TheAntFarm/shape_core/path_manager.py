import logging
import time
from collections import OrderedDict
from typing import List, Tuple, Dict, Any, Optional, Union

import numpy as np
import shapely.geometry
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import substring

from .geometry_manager import (
    fill_holes_sh,
    get_bbox_area_sh,
    get_poly_diameter,
    is_overlaping_multiple_polygons,
    merge_polygons_path,
    offset_polygon,
    offset_polygon_holes,
)
from .drill_path_optimizer import DrillPathOptimizer
from .gerber_path_optimizer import GerberPathOptimizer

logger = logging.getLogger(__name__)


class Gapper:
    """
    Manages the creation of gaps (tabs) in the toolpath to hold the PCB in place during machining.
    """

    DEFAULT_STRATEGIES = ("none", "2h", "2v", "4p", "4h", "4v", "8p", "4x")

    def __init__(self, path: LineString, cfg: Dict[str, Any]) -> None:
        """
        Initialize the Gapper.

        :param path: The input path (LineString) to add gaps to.
        :param cfg: Configuration dictionary containing 'taps_length' and 'tool_diameter'.
        """
        self.cfg = cfg
        self.in_path = path
        self.gap_dim = self.cfg.get("taps_length", 0.5) + self.cfg.get("tool_diameter", 0.2)

    @staticmethod
    def rotate(el: List[Any], idx: int) -> List[Any]:
        """Rotates a list by a given index."""
        return el[idx:] + el[:idx]

    def get_available_strategies(self) -> Tuple[str, ...]:
        """Returns the list of available gap placement strategies."""
        return self.DEFAULT_STRATEGIES

    def add_taps_on_external_path(self, strategy: str = "4p") -> List[LineString]:
        """
        Adds gaps to the external path based on the selected strategy.

        :param strategy: The strategy to use (e.g., '4p', '2h', '8p').
        :return: A list of LineStrings representing the path with gaps.
        """
        ex_path = self.in_path
        b = ex_path.bounds

        xm = (b[2] + b[0]) / 2.0
        ym = (b[3] + b[1]) / 2.0

        x2 = np.linspace(b[0], b[2], 4)[1:3]
        y2 = np.linspace(b[1], b[3], 4)[1:3]

        v2l = [LineString(((x2[0], b[1]), (x2[0], b[3]))), LineString(((x2[1], b[1]), (x2[1], b[3])))]
        h2l = [LineString(((b[0], y2[0]), (b[2], y2[0]))), LineString(((b[0], y2[1]), (b[2], y2[1])))]

        # straight cross
        vl = LineString(((xm, b[1]), (xm, b[3])))
        hl = LineString(((b[0], ym), (b[2], ym)))

        # 45 degree cross
        lrl = LineString(((b[0], b[1]), (b[2], b[3])))
        rll = LineString(((b[2], b[1]), (b[0], b[3])))

        lines_list: Optional[List[LineString]] = None

        if strategy == "8p":
            # find intersection points between
            # v2l h2l and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = v2l + h2l

        if strategy == "4p":
            # find intersection points between
            # vl hl and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [vl, hl]

        if strategy == "4x":
            # find intersection points between
            # lrl rll and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [lrl, rll]

        if strategy == "2h":
            # find intersection points between
            # hl and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [hl]

        if strategy == "4h":
            # find intersection points between
            # h2l and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = h2l

        if strategy == "2v":
            # find intersection points between
            # vl and the external perimeter.
            # extract indices of the segments crossed by.
            # following the external linestring create the segment with
            # the length of taps_length

            lines_list = [vl]

        if strategy == "4v":
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

    def get_tappered_path(self, ex_path: LineString, intersect_line: List[LineString]) -> List[LineString]:
        """
        Splits the path at intersection points with the strategy lines and creates gaps.
        """
        points = list(ex_path.coords)
        pts = []
        for line in intersect_line:
            lb = line.boundary
            if hasattr(lb, 'geoms'):
                pts += [lb.geoms[0], lb.geoms[1]]
            else:
                # Handle case where boundary might be a MultiPoint or similar
                pts += list(lb) if hasattr(lb, '__iter__') else []

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

        if not lids:
            return [ex_path]

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
                while c < len(ids) and ids[c - 1] == ids[c]:
                    lsl.append(ls + [pids[c]])
                    ls = [pids[c]]
                    c += 1

        if lsl:
            lsl[0] = ls + lsl[0]
        else:
            lsl = [ls]

        nl = []
        for ll in lsl:
            ls_geom = LineString(ll)
            if self.gap_dim < ls_geom.length:
                nls = substring(ls_geom, start_dist=self.gap_dim / 2.0, end_dist=ls_geom.length - self.gap_dim / 2.0)
                nl.append(nls)

        return nl


class MachinePath:
    """
    Generates toolpaths (G-code geometry) for various machining operations:
    Gerber (isolation), Profile (cutout), Pocketing, and Drilling.
    """

    MIN_AREA = 0.1e-1
    TD_COEFF = 0.999
    
    # Machining Types
    TYPE_GERBER = "gerber"
    TYPE_PROFILE = "profile"
    TYPE_POCKETING = "pocketing"
    TYPE_DRILL = "drill"

    def __init__(self, tag: str, machining_type: str = TYPE_GERBER) -> None:
        """
        Initialize the MachinePath generator.

        :param tag: Identifier for the path.
        :param machining_type: Type of operation ('gerber', 'profile', 'pocketing', 'drill').
        """
        self.tag = tag
        self.geom_list: List[Any] = []
        self.cfg: Dict[str, Any] = {}
        
        if machining_type == self.TYPE_GERBER:
            self.cfg = {"tool_diameter": 0.2, "passages": 3, "overlap": 0.3}
            if self.cfg["passages"] < 1:
                logger.warning("At Least One Pass required. Setting passages to 1.")
                self.cfg["passages"] = 1
        elif machining_type == self.TYPE_PROFILE:
            self.cfg = {"tool_diameter": 1.0, "margin": 0.1, "taps_type": 3, "taps_length": 1.0}
        elif machining_type == self.TYPE_POCKETING:
            self.cfg = {"tool_diameter": 1.0}
        elif machining_type == self.TYPE_DRILL:
            self.cfg = {"tool_diameter": None, "bits_diameter": [0.8], "optimize": False}
        
        self.type = machining_type
        self.path: Optional[List[Tuple[Tuple[float, str], List[Any], Optional[List[int]]]]] = None

    def load_cfg(self, cfg: Dict[str, Any]) -> None:
        """Loads configuration settings."""
        logger.debug(f"Loading Config: {cfg}")
        self.cfg = cfg

    def get_path(self) -> Optional[List[Any]]:
        """Returns the generated path."""
        return self.path

    def load_geom(self, geom_list: List[Any]) -> None:
        """Loads the geometry to be processed."""
        self.geom_list = geom_list

    def execute(self) -> Optional[List[bool]]:
        """
        Executes the path generation based on the machining type.
        Returns a list of booleans indicating processed elements (for drilling/pocketing).
        """
        elabs: Optional[List[bool]] = None
        if self.type == self.TYPE_GERBER:
            self.execute_gerber()
        elif self.type == self.TYPE_PROFILE:
            self.execute_profile()
        elif self.type == self.TYPE_POCKETING:
            elabs = self.execute_pocketing()
        elif self.type == self.TYPE_DRILL:
            # if there is a valid pocketing tool, the pocketing process is performed
            # otherwise only the holes are drilled
            elabs_p = None
            if self.cfg.get("tool_diameter") is not None and self.cfg.get("milling_tool"):
                elabs_p = self.execute_pocketing()

            # if a pocketing process was performed, elabs will contain a list of bools
            # which identify the performed holes to be discarded in the next drilling phase
            elabs_d = self.execute_drill(not_to_drill=elabs_p)

            elabs = []
            if elabs_p is not None:
                for i in range(len(elabs_d)):
                    elabs.append(elabs_p[i] or elabs_d[i])
            else:
                elabs = elabs_d # If no pocketing, elabs is just drill results

            if elabs is not None:
                if not all(elabs):
                    logger.warning("Not all holes are computed, please add bits with correct diameter")

        return elabs

    def execute_gerber(self) -> None:
        """Generates isolation paths for Gerber files."""
        t0 = time.time()
        og_list = []
        prev_poly = []
        td = self.cfg["tool_diameter"] * self.TD_COEFF
        
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, td / 2.0)
            if og is not None:
                og_list.append(og)

        pre_len = len(og_list)
        og_list = merge_polygons_path(og_list)

        invalid_path_ids = []
        # Check for invalid paths (overlapping original geometry)
        if len(og_list) < pre_len:
            prev_sh_poly = shapely.geometry.MultiPolygon(prev_poly)
            for i, g in enumerate(og_list):
                check = is_overlaping_multiple_polygons(g, prev_sh_poly, shapely_poly=True)
                if check:
                    invalid_path_ids.append(i)

        # Generate multiple passes
        for i in range(self.cfg["passages"] - 1):
            sub_og_list = self._subpath_execute(og_list)
            og_list += sub_og_list

        t1 = time.time()
        logger.info(f"Path Generation Done in {t1 - t0:.4f} sec")
        if invalid_path_ids:
            logger.warning(f"DRC Check Output: {len(invalid_path_ids)} invalid paths {invalid_path_ids}")

        og_list = self.check_min_area(og_list)

        # Extract LineStrings from polygons
        path = []
        path_counter = 0
        invalid_paths = []
        for j, g in enumerate(og_list):
            ex_path = g.exterior
            if ex_path.geom_type in ["LinearRing", "LineString"]:
                path.append(ex_path)
                if j in invalid_path_ids:
                    invalid_paths.append(path_counter)
                path_counter += 1
            for i in g.interiors:
                if i.geom_type in ["LinearRing", "LineString"]:
                    path.append(i)
                    path_counter += 1
        
        # OPTIMIZATION: Reorder Gerber paths to minimize travel distance
        if path:
            logger.info("Optimizing Gerber path...")
            optimizer = GerberPathOptimizer(path)
            path = optimizer.optimize()

        t_d = self.cfg["tool_diameter"]
        # Structure: (tool_info, path_geometry, invalid_indices)
        self.path = [((t_d, self.TYPE_GERBER), path, invalid_paths)]

    def check_min_area(self, og_list: List[Polygon]) -> List[Polygon]:
        """Filters out polygons smaller than MIN_AREA."""
        big_poly = []
        old_poly_count = 0
        new_poly_count = 0
        
        for p in og_list:
            old_poly_count += 1
            new_inners = []
            for inner in p.interiors:
                old_poly_count += 1
                if abs(Polygon(inner).area) >= self.MIN_AREA:
                    new_inners.append(inner)
            
            if abs(Polygon(p.exterior).area) >= self.MIN_AREA:
                p = Polygon(p.exterior, new_inners)
                new_poly_count += 1 + len(p.interiors)
                big_poly.append(p)

        removed_count = old_poly_count - new_poly_count
        if removed_count > 0:
            logger.info(f"REMOVED small polygons: {removed_count}")
        return big_poly

    def execute_pocketing(self) -> List[bool]:
        """Generates pocketing paths (clearing area inside polygons)."""
        logger.info("Pocketing")
        t0 = time.time()
        og_list = []
        milled_list = []
        td = self.cfg["tool_diameter"] * self.TD_COEFF
        
        for g in self.geom_list:
            # Offset inwards by tool radius
            og = offset_polygon(g, -td / 2.0)
            if og is not None:
                if not og.is_empty:
                    og_list.append(og)
                    milled_list.append(True)
                else:
                    milled_list.append(False)
            else:
                milled_list.append(False)

        # TODO: Implement multi-pass pocketing logic here (currently just one pass)

        t1 = time.time()
        logger.info(f"Path Generation Done in {t1 - t0:.4f} sec")

        path = []
        for g in og_list:
            ex_path = g.exterior
            if ex_path.geom_type in ["LinearRing", "LineString"]:
                path.append(ex_path)
            for i in g.interiors:
                if i.geom_type in ["LinearRing", "LineString"]:
                    path.append(i)
        
        t_d = self.cfg["tool_diameter"]
        self.path = [((t_d, self.TYPE_POCKETING), path)]

        return milled_list

    def execute_drill(self, not_to_drill: Optional[List[bool]] = None) -> List[bool]:
        """Generates drilling paths, optimizing tool changes and travel distance."""
        logger.info("Drilling")
        t0 = time.time()
        bd = self.cfg.get("bits_diameter", [])[:]
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
                # Select the best bit: closest diameter <= hole diameter
                for j, d in enumerate(ds):
                    drills.append([i, c.coords[j], d])
            else:
                drilled_list.append(False)

        drills.sort(key=lambda x: x[2], reverse=True)

        drill_per_bit = OrderedDict()
        if not bd:
             logger.warning("No drill bits defined in configuration.")
             return drilled_list

        b = bd[0]
        c = 1
        for dd in drills:
            d = dd[2]
            while b > d and c < len(bd):
                b = bd[c]
                c += 1
            if b not in drill_per_bit:
                drill_per_bit[b] = []
            drill_per_bit[b].append(dd[1])

        # Optimize path for each bit
        for bit_k in drill_per_bit.keys():
            bit_points = drill_per_bit[bit_k]
            if "optimize" in self.cfg:
                optimize_cfg = self.cfg["optimize"]
                # Check if optimization is enabled (can be boolean or int index)
                if optimize_cfg is not False: 
                    opt = DrillPathOptimizer(bit_points)
                    available_opt_types = opt.get_optimization_types()
                    
                    # Handle integer index for optimization type (Backward Compatibility)
                    if isinstance(optimize_cfg, int) and 0 <= optimize_cfg < len(available_opt_types):
                        opt_type = available_opt_types[optimize_cfg]
                        opt.set_optimization_type(opt_type)
                    # Handle string name for optimization type (Preferred)
                    elif isinstance(optimize_cfg, str) and optimize_cfg in available_opt_types:
                         opt.set_optimization_type(optimize_cfg)
                    # Handle True boolean (Default to a good optimizer)
                    elif optimize_cfg is True:
                        # Default to hybrid_ils if available, else nearest_insertion
                        default_opt = "hybrid_ils" if "hybrid_ils" in available_opt_types else "nearest_insertion"
                        opt.set_optimization_type(default_opt)

                    optimized_bit_points = opt.get_optimized_path()
                    drill_per_bit[bit_k] = optimized_bit_points
                else:
                    pass

        paths = []
        for k in drill_per_bit:
            # Convert points back to LineString for consistency
            paths.append(((k, self.TYPE_DRILL), [LineString(drill_per_bit[k])]))

        if not_to_drill is not None:
            if any(not_to_drill) and self.path is not None:
                self.path += paths
            else:
                self.path = paths
        else:
            self.path = paths

        t1 = time.time()
        logger.info(f"Path Generation Done in {t1 - t0:.4f} sec")

        return drilled_list

    def execute_profile(self) -> None:
        """Generates profile cutout paths with tabs (gaps)."""
        t0 = time.time()
        og_list = []
        td = self.cfg["tool_diameter"] * self.TD_COEFF
        
        # Uniqueness check of the profile
        if len(self.geom_list) == 1:
            # Unique profile
            ext_path = offset_polygon(
                fill_holes_sh(self.geom_list[0].geom), td / 2.0 + self.cfg["margin"], shapely_poly=True
            )
            if ext_path is not None:
                og_list.append(ext_path)
        else:
            # Profile composed by multiple polygons
            # Identify the external profile (largest bbox area)
            geoms = [g.geom for g in self.geom_list]
            if not geoms:
                return

            bba = get_bbox_area_sh(geoms[0])
            idx = 0

            for i, p in enumerate(geoms):
                a = get_bbox_area_sh(p)
                if a > bba:
                    bba = a
                    idx = i

            ext_p = self.geom_list[idx]
            ext_path = offset_polygon(fill_holes_sh(ext_p.geom), td / 2.0 + self.cfg["margin"], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)

            for i, g in enumerate(self.geom_list):
                if i != idx:
                    og = offset_polygon_holes(g, -(td / 2.0 + self.cfg["margin"]))
                    if og is not None:
                        og_list.append(og)

        t1 = time.time()
        logger.info(f"Path Generation Done in {t1 - t0:.4f} sec")

        # Extracting linestring from the polygon path
        path = []
        for g in og_list:
            ex_path = g.exterior
            if ex_path.geom_type in ["LinearRing", "LineString"]:
                path.append(ex_path)
            for i in g.interiors:
                if i.geom_type in ["LinearRing", "LineString"]:
                    path.append(i)

        if not path:
            return

        # Add taps (gaps) based on the selected strategy
        t = Gapper(path[0], self.cfg)
        stl = t.get_available_strategies()
        
        taps_type_idx = self.cfg.get("taps_type", 0)
        if 0 <= taps_type_idx < len(stl):
            st = stl[taps_type_idx]
            logger.info(f"Strategy: {st}")
            new_ext = t.add_taps_on_external_path(strategy=st)
            path.pop(0)
            path = new_ext + path
        else:
            logger.warning(f"Invalid taps_type index: {taps_type_idx}")

        t_d = self.cfg["tool_diameter"]
        self.path = [((t_d, self.TYPE_PROFILE), path)]

    def _subpath_execute(self, ppg_list: List[Polygon]) -> List[Polygon]:
        """Helper to generate subsequent passes for Gerber milling."""
        ov = self.cfg["overlap"]
        td = self.cfg["tool_diameter"] * self.TD_COEFF
        pre_offset = td / 2.0 * (1 + 0.5 - ov)
        og_list = []

        for g in ppg_list:
            og = offset_polygon(g, pre_offset, shapely_poly=True)
            if og is not None:
                if og.geom_type == "MultiPolygon":
                    for sog in og.geoms:
                        og_list.append(sog)
                else:
                    og_list.append(og)
        
        mg_list = merge_polygons_path(og_list)

        mog_list = []
        for g in mg_list:
            mog = offset_polygon(g, -pre_offset, shapely_poly=True)
            if mog is not None:
                if mog.geom_type == "MultiPolygon":
                    for smog in mog.geoms:
                        mog_list.append(smog)
                else:
                    mog_list.append(mog)

        ng_list = []
        for g in mog_list:
            ng = offset_polygon(g, td / 2.0 * (1 + 0.5 - ov), shapely_poly=True)
            if ng is not None:
                if ng.geom_type == "MultiPolygon":
                    for sng in ng.geoms:
                        ng_list.append(sng)
                else:
                    ng_list.append(ng)

        fmg_list = merge_polygons_path(ng_list)

        return fmg_list
