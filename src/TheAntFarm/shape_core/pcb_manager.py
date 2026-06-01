import logging
import math
import os
import time
from collections import OrderedDict as Od
from typing import Any, Dict, List, Optional, Tuple, Union

from gerbyx import logger as gerbyx_logger
from gerbyx.tokenizer import tokenize_gerber
from gerbyx.parser import GerberParser
from gerbyx.processor import GerberProcessor


from gerbyx.excellon import (
    ExcellonState,
    ExcellonParser,
    ExcellonProcessor,
    tokenize_excellon,
)

gerbyx_logger.set_level('WARNING')  # or 'INFO' (default), 'WARNING', 'ERROR'
import numpy as np

import gerber as gbr
import gerber.primitives
from gerber.cam import FileSettings
from gerber.excellon import DrillHit, DrillSlot
from gerber.excellon import loads as exc_load
from gerber.excellon_statements import CoordinateStmt, EndOfProgramStmt, FormatStmt, ToolSelectionStmt
from gerber.utils import convex_hull
from shapely.geometry.multipolygon import MultiPolygon

from .geometry_manager import Geom, FakeGeom, merge_polygons

logger = logging.getLogger(__name__)


# workaround for pcb-tools read function
def _new_pcb_tools_read_function(filename: str) -> Any:
    with open(filename, "r") as f:
        data = f.read()
    return gbr.loads(data, filename)


gbr.read = _new_pcb_tools_read_function


class PcbObj:
    """
    Manages PCB data loaded from Gerber and Excellon files.
    Handles parsing, unit conversion, and geometric conversion of PCB layers.
    """

    GBR_KEYS = ["top", "bottom", "profile", "noncopper_top", "noncopper_bottom"]
    EXN_KEYS = ["drill"]
    DEFAULT_ARC_SUBDIVISIONS = 64
    MAX_ARC_CHORD_LEN = 0.5  # mm
    MIN_ARC_CHORD_LEN = 0.1  # mm

    def __init__(self) -> None:
        self.gerbers: Od[str, Any] = Od({})
        self.excellons: Od[str, Any] = Od({})
        self.init_data()
        self.arc_angle = 2.0 * math.pi / self.DEFAULT_ARC_SUBDIVISIONS
        self.arc_max_len = self.MAX_ARC_CHORD_LEN
        self.arc_min_len = self.MIN_ARC_CHORD_LEN
        self.layers: Od[str, Any] = Od({})
        self.am_group = False

    def get_arc_subdivisions(self) -> int:
        return int(2.0 * math.pi / self.arc_angle)

    def set_arc_subdivisions(self, arc_sub: int) -> None:
        self.arc_angle = 2.0 * math.pi / arc_sub

    def init_data(self) -> None:
        for k in self.GBR_KEYS:
            self.gerbers[k] = None

        for k in self.EXN_KEYS:
            self.excellons[k] = None

    def get_gerber(self, tag: str) -> Optional[Any]:
        if tag in self.GBR_KEYS:
            if self.gerbers[tag] is not None:
                return self.gerbers[tag]
        logger.error(f"GERBER NOT FOUND: {tag}")
        return None

    def get_excellon(self, tag: str) -> Optional[Any]:
        if tag in self.EXN_KEYS:
            if self.excellons[tag] is not None:
                return self.excellons[tag]
        logger.error(f"EXCELLON NOT FOUND: {tag}")
        return None

    def load_gerber(self, path: str, tag: str) -> bool:
        if tag not in self.GBR_KEYS:
            logger.error(f"GERBER TAG NOT RECOGNIZED: {tag}")
            return False
        if not os.path.isfile(path):
            logger.error(f"GERBER FILE NOT FOUND: {path}")
            return False

        try:
            gerbyx_logger.set_level('INFO')  # or 'INFO' (default), 'WARNING', 'ERROR'

            # Parse Gerber file
            with open(path, 'r') as f:
                gerber_source = f.read()

            processor = GerberProcessor()
            parser = GerberParser(processor)
            tokens = tokenize_gerber(gerber_source)
            parser.parse(tokens)
            self.gerbers[tag] = processor
            return True

        except Exception as e:
            logger.error(f"Failed to load Gerber file {path}: {e}")
            return False

    @staticmethod
    def dump_str(gerber_obj: Any, data_type: str = "gerber", ext_settings: Optional[FileSettings] = None) -> str:
        # used to FIX bug in pcb-tools that doesn't work properly
        # tip: file conversion to metric before geom parser
        string = ""
        if ext_settings is not None:
            settings = ext_settings
        else:
            settings = gerber_obj.settings

        if data_type == "gerber":
            for stmt in gerber_obj.statements:
                string += str(stmt.to_gerber(gerber_obj.settings)) + "\n"
        else:
            for statement in gerber_obj.statements:
                if not isinstance(statement, ToolSelectionStmt) and not isinstance(statement, FormatStmt):
                    string += statement.to_excellon(settings) + "\n"
                else:
                    if isinstance(statement, FormatStmt):
                        pass
                    else:
                        break

            k = 25.4
            # Write out coordinates for drill hits by tool
            for tool in iter(gerber_obj.tools.values()):
                data = ToolSelectionStmt(tool.number)
                string += data.to_excellon(settings) + "\n"
                for hit in gerber_obj.hits:
                    if hit.tool.number == tool.number:
                        if isinstance(hit, DrillHit):
                            string += (
                                CoordinateStmt(hit.position[0] * k, hit.position[1] * k).to_excellon(settings) + "\n"
                            )
                        elif isinstance(hit, DrillSlot):
                            string += CoordinateStmt(hit.start[0] * k, hit.start[1] * k).to_excellon(settings) + "\n"
                            string += CoordinateStmt(hit.end[0] * k, hit.end[1] * k).to_excellon(settings) + "\n"
            string += EndOfProgramStmt().to_excellon() + "\n"
        return string

    def load_excellon_old(self, path: str, tag: str) -> bool:
        if tag not in self.EXN_KEYS:
            logger.error(f"EXCELLON TAG NOT RECOGNIZED: {tag}")
            return False
        if not os.path.isfile(path):
            logger.error(f"EXCELLON FILE NOT FOUND: {path}")
            return False

        try:
            tmp = gbr.read(path)
            self.excellons[tag] = tmp
            if tmp.units == "inch":
                logger.info(f"Converting Excellon {tag} from inch to metric")
                self.excellons[tag].to_metric()
                """ Note: pcb-tools has a bug related to the inch -> metric conversion
                    a workaround is applied, during the dump process all the xy points
                    coordinates are converted in metric by default """

                settings = FileSettings(
                    format=(3, 3),
                    zero_suppression="leading",
                    units="metric",
                    notation="absolute",
                    angle_units="degrees",
                )
                data = self.dump_str(self.excellons[tag], data_type="excellon", ext_settings=settings)
                self.excellons[tag] = exc_load(data, settings=settings)
            return True
        except Exception as e:
            logger.error(f"Failed to load Excellon file {path}: {e}")
            return False

    def load_excellon(self, path: str, tag: str) -> bool:

        if tag not in self.EXN_KEYS:
            logger.error(f"EXCELLON TAG NOT RECOGNIZED: {tag}")
            return False
        if not os.path.isfile(path):
            logger.error(f"EXCELLON FILE NOT FOUND: {path}")
            return False

        try:
            # Parse Excellon file
            with open(path, 'r') as f:
                excellon_source = f.read()

            state = ExcellonState(output_units="MM")  # oppure "INCH"
            parser = ExcellonParser(state, auto_detect_coord_format=True)  # hint_units="INCH" se il file non dichiara le unità
            parser.parse(tokenize_excellon(excellon_source))

            proc = ExcellonProcessor(state)
            proc.process(parser.primitives)

            self.excellons[tag] = proc  # proc.geometries → lista di Shapely Polygon
            return True
        except Exception as e:
            logger.error(f"Failed to load Excellon file {path}: {e}")
            return False

    def get_gerber_layer(self, tag: str) -> Any:
        logger.info(f"Processing Gerber Layer: {tag}")
        start_time = time.time()
        g = self.get_gerber(tag)
        if g is None:
            return None

        self.layers[tag] = ([FakeGeom(x) for x in g.geometries], ())
        print(self.layers[tag])
        logger.info(f"Gerber Layer {tag} processed in {time.time() - start_time:.4f} seconds")

        return self.layers[tag]

    def get_excellon_layer_old(self, tag: str) -> Any:
        g = self.get_excellon(tag)
        if g is None:
            return None

        mp = []
        for primitive in g.primitives:
            gdata = self._primitive_paths(primitive)
            for gd in gdata:
                g_geom = Geom(gd)
                if g_geom.closed:
                    mp.append(g_geom)
        self.layers[tag] = merge_polygons(mp)
        return self.layers[tag]

    def get_excellon_layer(self, tag: str) -> Any:
        logger.info(f"Processing Excellon Layer: {tag}")
        start_time = time.time()
        g = self.get_excellon(tag)

        print("Excellon:", g)
        print(" - Geometries:", g.geometries)

        if g is None:
            return None

        self.layers[tag] = ([FakeGeom(x) for x in g.geometries], ())
        print(self.layers[tag])
        logger.info(f"Excellon Layer {tag} processed in {time.time() - start_time:.4f} seconds")

        return self.layers[tag]

    def _arc_segmentation(
        self,
        center: Tuple[float, float],
        radius: float,
        arc_start_angle: float,
        arc_end_angle: float,
        direction: str = "clockwise",
        forced_divisions: Optional[int] = None,
    ) -> List[Tuple[float, float]]:

        start_angle = arc_start_angle
        end_angle = arc_end_angle

        if direction == "clockwise":
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
        return [tuple(x) for x in arc_discretization]

    def _get_enhanced_line(
        self, l_start: Tuple[float, float], l_end: Tuple[float, float], aperture: Any
    ) -> List[Tuple[float, float]]:
        if l_start[0] - l_end[0] >= 0:
            start = l_start
            end = l_end
        else:
            start = l_end
            end = l_start

        radius = 0.0
        subdivisions = 4

        if isinstance(aperture, gbr.primitives.Rectangle):
            # radius = max(aperture.height, aperture.width) / 4.0
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
            end_theta = -math.pi / 2.0 + theta
            points = self._arc_segmentation(
                start, radius, start_theta, end_theta, forced_divisions=int(subdivisions / 2)
            )

            # sign inverted (Geekoid testcase)
            start_theta = -math.pi / 2.0 + theta + math.pi
            end_theta = math.pi / 2.0 + theta + math.pi
            points += self._arc_segmentation(
                end, radius, end_theta, start_theta, forced_divisions=int(subdivisions / 2)
            )

            return convex_hull(points)
        else:
            return [l_start, l_end]

    @staticmethod
    def _get_region_polygon(gdata: List[Dict[str, Any]], vectors: bool = False) -> List[Tuple[float, float]]:
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

    def _process_line(self, primitive: Any, region: bool) -> List[Dict[str, Any]]:
        closed_flag = True
        points = primitive.vertices

        if isinstance(primitive.aperture, (gbr.primitives.Circle, gbr.primitives.Rectangle)):
            if not region or self.am_group:
                points = self._get_enhanced_line(primitive.start, primitive.end, primitive.aperture)
            else:
                points = [primitive.start, primitive.end]
                closed_flag = False

        gdata = [{"points": points, "polarity": primitive.level_polarity, "closed": closed_flag}]
        if points is None:
            points = [primitive.start, primitive.end]
            gdata = [{"points": points, "polarity": primitive.level_polarity, "closed": False}]
        return gdata

    def _process_arc(self, primitive: Any, region: bool) -> List[Dict[str, Any]]:
        points = self._arc_segmentation(
            primitive.center,
            primitive.radius,
            primitive.start_angle,
            primitive.end_angle,
            direction=primitive.direction,
        )

        if isinstance(primitive.aperture, (gbr.primitives.Circle, gbr.primitives.Rectangle)) and not region:
            pts = points.copy()
            pp = pts.pop(0)
            gdata = []
            for npp in pts:
                l_points = self._get_enhanced_line(pp, npp, primitive.aperture)
                gdata.append({"points": l_points, "polarity": primitive.level_polarity, "closed": True})
                pp = npp
            return gdata
        else:
            return [{"points": points, "polarity": primitive.level_polarity, "closed": False}]

    def _process_region(self, primitive: Any, region: bool) -> List[Dict[str, Any]]:
        gdata = []
        am_group = False
        if isinstance(primitive, gbr.primitives.AMGroup):
            self.am_group = True
            am_group = True

        if primitive.primitives is not None:
            lines_flag = True
            pp = primitive.primitives.copy()
            for p in pp:
                gdata += self._primitive_paths(p, region=True)
                lines_flag &= isinstance(p, (gbr.primitives.Line, gbr.primitives.Arc))

            if lines_flag and primitive.primitives:
                # check if the line is closed
                p0 = primitive.primitives[0]
                p1 = primitive.primitives[-1]
                if p0.start != p1.end:
                    points = [p1.end, p0.start]
                    gd = [{"points": points, "polarity": primitive.level_polarity, "closed": False}]
                    gdata += gd

                vectors = False
                if self.am_group and isinstance(primitive, gbr.primitives.Outline):
                    vectors = p1.start == p1.end

                points = self._get_region_polygon(gdata, vectors)
                gdata = [{"points": points, "polarity": primitive.level_polarity, "closed": True}]

        if am_group:
            self.am_group = False
        return gdata

    def _primitive_paths(self, primitive: Any, region: bool = False) -> List[Dict[str, Any]]:
        if isinstance(primitive, gbr.primitives.Line):
            return self._process_line(primitive, region)

        elif isinstance(primitive, gbr.primitives.Arc):
            return self._process_arc(primitive, region)

        elif isinstance(primitive, (gbr.primitives.Region, gbr.primitives.AMGroup, gbr.primitives.Outline)):
            return self._process_region(primitive, region)

        elif isinstance(primitive, gbr.primitives.Rectangle):
            return [{"points": primitive.vertices, "polarity": primitive.level_polarity, "closed": True}]

        elif isinstance(primitive, gbr.primitives.Polygon):
            return [{"points": primitive.vertices, "polarity": primitive.level_polarity, "closed": True}]

        elif isinstance(primitive, gbr.primitives.Circle):
            points = self._arc_segmentation(primitive.position, primitive.radius, 0, 2 * math.pi)
            return [{"points": points, "polarity": primitive.level_polarity, "closed": True}]

        elif isinstance(primitive, gbr.primitives.Obround):
            circle1 = primitive.subshapes["circle1"]
            circle2 = primitive.subshapes["circle2"]
            points1 = self._arc_segmentation(circle1.position, circle1.radius, 0, 2 * math.pi)
            points2 = self._arc_segmentation(circle2.position, circle2.radius, 0, 2 * math.pi)
            points = convex_hull(points1 + points2)
            return [{"points": points, "polarity": primitive.level_polarity, "closed": True}]

        elif isinstance(primitive, gbr.primitives.Drill):
            points = self._arc_segmentation(primitive.position, primitive.radius, 0, 2 * math.pi)
            return [{"points": points, "polarity": primitive.level_polarity, "closed": True}]

        elif isinstance(primitive, gbr.primitives.Slot):
            points1 = self._arc_segmentation(primitive.start, primitive.diameter / 2.0, 0, 2 * math.pi)
            points2 = self._arc_segmentation(primitive.end, primitive.diameter / 2.0, 0, 2 * math.pi)
            points = convex_hull(points1 + points2)
            return [{"points": points, "polarity": primitive.level_polarity, "closed": True}]

        else:
            logger.warning(f"PRIMITIVE NOT RECOGNIZED: {type(primitive)}")
            return []


if __name__ == "__main__":

    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test1\\gerbers_file\\copper_top.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test1\\gerbers_file\\copper_bottom.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test2\\gerbers_file\\copper_bottom.gbr"
    gerber_path = "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test2\\gerbers_file\\profile.gbr"
    gerber_path = (
        "C:\\Users\\mmatt\\Documents\\prj\\new_cnc\\cam_data\\test3\\gerbers_file\\JST_motor_breakout_board-F_Cu.gbr"
    )
    gerber_path = "C:\\Users\\mmatt\\Desktop\\Gerber\\LedKeyring-F_Cu.gbr"

    pcb = PcbObj()
    pcb.load_gerber(gerber_path, "top")
    gtop = pcb.get_gerber("top")
    pcb.get_gerber_layer("top")
