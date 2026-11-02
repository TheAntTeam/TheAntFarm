import logging
import os
import time
from collections import OrderedDict as Od
from typing import Any, Optional

from gerbyx import logger as gerbyx_logger
from gerbyx.excellon import (
    ExcellonParser,
    ExcellonProcessor,
    ExcellonState,
    tokenize_excellon,
)
from gerbyx.parser import GerberParser
from gerbyx.processor import GerberProcessor
from gerbyx.tokenizer import tokenize_gerber

from .geometry_manager import Geom

# gerbyx is verbose at INFO level: keep its output out of the application log
gerbyx_logger.set_level("WARNING")

logger = logging.getLogger(__name__)


def _shapes_to_geoms(shapes):
    """Wrap the shapely geometries of a layer into Geom objects.

    A MultiPolygon is split into its parts: the rest of the CAM works one
    polygon at a time (offset, toolpath, drilling).
    """
    geoms = []
    for shape in shapes:
        if shape.geom_type == "MultiPolygon":
            geoms.extend(Geom.from_shapely(part) for part in shape.geoms)
        else:
            geoms.append(Geom.from_shapely(shape))
    return geoms


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

        # a new file invalidates the geometry computed from the previous one
        self.layers.pop(tag, None)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as gerber_file:
                gerber_source = gerber_file.read()

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

        # a new file invalidates the geometry computed from the previous one
        self.layers.pop(tag, None)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as excellon_file:
                excellon_source = excellon_file.read()

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
        """Return the geometries of a loaded Gerber layer.

        The result is cached: the conversion of the primitives to ``Geom``
        is needed every time a job is created from the layer, while the layer
        itself only changes when a new file is loaded.
        """
        if tag in self.layers and self.layers[tag] is not None:
            return self.layers[tag]

        logger.info(f"Processing Gerber Layer: {tag}")
        start_time = time.perf_counter()
        g = self.get_gerber(tag)
        if g is None:
            return None

        self.layers[tag] = (_shapes_to_geoms(g.geometries), ())
        logger.debug("Gerber layer %s geometries: %s", tag, self.layers[tag])
        logger.info(f"Gerber Layer {tag} processed in {time.perf_counter() - start_time:.4f} seconds")

        return self.layers[tag]

    def get_excellon_layer(self, tag: str) -> Any:
        """Return the geometries of a loaded Excellon layer (cached, see above)."""
        if tag in self.layers and self.layers[tag] is not None:
            return self.layers[tag]

        logger.info(f"Processing Excellon Layer: {tag}")
        start_time = time.perf_counter()
        g = self.get_excellon(tag)

        logger.debug("Excellon processor: %s", g)

        if g is None:
            return None

        self.layers[tag] = (_shapes_to_geoms(g.geometries), ())
        logger.debug("Excellon layer %s geometries: %s", tag, self.layers[tag])
        logger.info(f"Excellon Layer {tag} processed in {time.perf_counter() - start_time:.4f} seconds")

        return self.layers[tag]

