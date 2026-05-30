"""
PCB Service – layer loading, tool-path computation and G-code generation.

Design contract
---------------
- No Qt imports anywhere in this file.
- Mirrors the logic of :class:`controller.ViewController` but without
  ``QObject`` inheritance, making it directly testable and CLI-callable.
- All results are plain Python dataclasses (see :mod:`app.events`).

Migration path
--------------
Phase 1 (this file)
    ``ViewController`` keeps working unchanged.
    Gradually move its business logic here; ``ViewController`` becomes a
    thin Qt adapter that delegates to ``PcbService`` and emits signals.

Phase 2
    ``ViewController`` reduced to:
    ::

        def generate_new_path(self, tag, cfg, mtype):
            result = self._service.generate_path(tag, cfg, mtype)
            return result.paths           # Qt adapter emits signal
"""
from __future__ import annotations

import logging
import os
import traceback
from typing import Any, Dict, List, Optional

from shape_core.gcode_manager import GCoder
from shape_core.path_manager import MachinePath
from shape_core.pcb_manager import PcbObj

from app.events import GCodeResult, LayerResult, PathResult

logger = logging.getLogger(__name__)


class PcbService:
    """
    Pure-Python PCB processing service.

    Responsibilities
    ~~~~~~~~~~~~~~~~
    - Load Gerber and Excellon files via :class:`~shape_core.PcbObj`.
    - Compute tool paths via :class:`~shape_core.MachinePath`.
    - Generate G-code files via :class:`~shape_core.GCoder`.

    No Qt types are imported or returned.
    """

    def __init__(self) -> None:
        self._pcb = PcbObj()

    # ------------------------------------------------------------------ #
    #  Layer loading
    # ------------------------------------------------------------------ #

    def load_layer(self, layer_type: str, file_path: str) -> LayerResult:
        """
        Load a Gerber or Excellon layer.

        Parameters
        ----------
        layer_type:
            One of ``PcbObj.GBR_KEYS`` (``"top"``, ``"bottom"``, …)
            or ``PcbObj.EXN_KEYS`` (``"drill"``).
        file_path:
            Absolute or relative path to the source file.

        Returns
        -------
        :class:`~app.events.LayerResult`
            ``ok=False`` on any failure; ``layer_data=None`` when no
            geometry was found.
        """
        try:
            grb_keys = self._pcb.GBR_KEYS
            exc_keys = self._pcb.EXN_KEYS

            if layer_type in grb_keys:
                self._pcb.load_gerber(file_path, layer_type)
                layer_data = self._pcb.get_gerber_layer(layer_type)
                has_drill = False
            elif layer_type in exc_keys:
                self._pcb.load_excellon(file_path, layer_type)
                layer_data = self._pcb.get_excellon_layer(layer_type)
                has_drill = True
            else:
                logger.error("Unknown layer type: %s", layer_type)
                return LayerResult(None, layer_type, file_path, False, False)

            if layer_data is None or not layer_data[0]:
                logger.warning("No geometry found in %s", file_path)
                return LayerResult(None, layer_type, file_path, has_drill, False)

            return LayerResult(layer_data, layer_type, file_path, has_drill, True)

        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logger.error("Error loading layer %s from %s: %s", layer_type, file_path, e, exc_info=True)
        except Exception:
            logger.error("Uncaught exception loading layer: %s", traceback.format_exc())

        return LayerResult(None, layer_type, file_path, False, False)

    # ------------------------------------------------------------------ #
    #  Path computation
    # ------------------------------------------------------------------ #

    def generate_path(self, tag: str, cfg: Dict[str, Any], machining_type: str) -> PathResult:
        """
        Compute tool paths for a previously loaded layer.

        Parameters
        ----------
        tag:
            Layer tag matching the value used in :meth:`load_layer`.
        cfg:
            Machining configuration dict (cut depth, feedrates, …).
        machining_type:
            ``"gerber"``, ``"profile"``, ``"drill"``, or ``"pocketing"``.
        """
        try:
            if machining_type in ("gerber", "profile"):
                layer = self._pcb.get_gerber_layer(tag)
            elif machining_type == "drill":
                layer = self._pcb.get_excellon_layer(tag)
            else:
                logger.error("Unknown machining type: %s", machining_type)
                return PathResult(tag, [])

            path = MachinePath(tag, machining_type)
            path.load_geom(layer[0])
            path.load_cfg(cfg)
            path.execute()
            return PathResult(tag, path.get_path())

        except Exception:
            logger.error("Uncaught exception computing path: %s", traceback.format_exc())
            return PathResult(tag, [])

    # ------------------------------------------------------------------ #
    #  G-code generation
    # ------------------------------------------------------------------ #

    def generate_gcode(
        self,
        tag: str,
        cfg: Dict[str, Any],
        machining_type: str,
        paths: List[Any],
        output_folder: str,
        mirror_type: str = "x",
    ) -> GCodeResult:
        """
        Generate a G-code file from pre-computed paths.

        Parameters
        ----------
        tag:
            Layer tag used as G-code file identifier.
        cfg:
            Machining configuration dict.
        machining_type:
            ``"gerber"``, ``"profile"``, ``"drill"``, or ``"pocketing"``.
        paths:
            Path list returned by :meth:`generate_path`.
        output_folder:
            Directory where the ``.gcode`` file will be written.
        mirror_type:
            ``"x"`` (mirror Y values) or ``"y"`` (mirror X values).

        Returns
        -------
        :class:`~app.events.GCodeResult`
            ``gcode_path`` is an empty string on failure.
        """
        try:
            gcoder = GCoder(tag, machining_type, mirror_type=mirror_type)
            gcoder.load_cfg(cfg)
            gcoder.load_path(paths)

            if not gcoder.compute():
                logger.error("G-code computation failed for tag %s", tag)
                return GCodeResult(tag, "")

            gcode_filename = gcoder.get_file_name()
            gcode_path = os.path.join(output_folder, gcode_filename)
            gcoder.write(gcode_path)
            logger.info("G-code written to %s", gcode_path)
            return GCodeResult(tag, gcode_path)

        except Exception:
            logger.error("Uncaught exception generating G-code: %s", traceback.format_exc())
            return GCodeResult(tag, "")
