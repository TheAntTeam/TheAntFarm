import logging
import os
import time
from collections import OrderedDict as Od
from typing import Any, Optional

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
from .geometry_manager import FakeGeom

logger = logging.getLogger(__name__)


class PcbObj:
    """
    Manages PCB data loaded from Gerber and Excellon files.
    Handles parsing, unit conversion, and geometric conversion of PCB layers.
    """

    GBR_KEYS = ["top", "bottom", "profile", "noncopper_top", "noncopper_bottom"]
    EXN_KEYS = ["drill"]

    def __init__(self) -> None:
        self.gerbers: Od[str, Any] = Od({})
        self.excellons: Od[str, Any] = Od({})
        self.init_data()
        self.layers: Od[str, Any] = Od({})

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
        logger.debug("Gerber layer %s geometries: %s", tag, self.layers[tag])
        logger.info(f"Gerber Layer {tag} processed in {time.time() - start_time:.4f} seconds")

        return self.layers[tag]

    def get_excellon_layer(self, tag: str) -> Any:
        logger.info(f"Processing Excellon Layer: {tag}")
        start_time = time.time()
        g = self.get_excellon(tag)

        logger.debug("Excellon processor: %s", g)

        if g is None:
            return None

        self.layers[tag] = ([FakeGeom(x) for x in g.geometries], ())
        logger.debug("Excellon layer %s geometries: %s", tag, self.layers[tag])
        logger.info(f"Excellon Layer {tag} processed in {time.time() - start_time:.4f} seconds")

        return self.layers[tag]


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
