"""
Align Service – alignment layer loading, camera capture and alignment points.

Design contract
---------------
- No Qt imports anywhere in this file.
- Camera frames are returned as :class:`~app.events.CameraFrame`
  (numpy array). The Qt adapter in ``app/adapters/qt_signal_bridge.py``
  converts them to ``QPixmap`` at the UI boundary.  A CLI or headless
  test can consume the raw array directly.

Migration path from AlignController
------------------------------------
``AlignController`` keeps working unchanged.  Gradually replace its body
with delegation to ``AlignService``::

    # controller_align.py (after migration)
    def camera_new_frame(self, zoom=1):
        frame = self._service.get_camera_frame(zoom)
        if frame:
            return array2qimage(frame.data)   # Qt conversion stays here
        return None
"""
from __future__ import annotations

import logging
import os
import traceback
from typing import List, Optional, Tuple

from double_side_manager import DoubleSideManager
from shape_core.gcode_drill_converter import DrillGcodeConverter
from shape_core.pcb_manager import PcbObj

from app.events import CameraFrame, LayerResult

logger = logging.getLogger(__name__)


class AlignService:
    """
    Pure-Python alignment service.

    Responsibilities
    ~~~~~~~~~~~~~~~~
    - Load Excellon / G-code drill layers for alignment reference.
    - Capture and process camera frames (returns numpy arrays, not Qt types).
    - Manage alignment point pairs (geometry point ↔ machine working position).

    No Qt types are imported or returned.
    """

    EXCELLON_EXTENSIONS = (".xln", ".drl")

    def __init__(
        self,
        camera_rotation: float = 0.0,
        flip_h: bool = False,
        flip_v: bool = False,
        drill_diameter: float = 0.7,
    ) -> None:
        self._pcb = PcbObj()
        dd = drill_diameter if drill_diameter else 0.7
        self._dgc = DrillGcodeConverter(cfg={"default_gcode_drill_size": dd})
        self._dsm = DoubleSideManager()
        self._dsm.set_camera_rotation(camera_rotation)
        self._dsm.set_camera_flip(flip_h, flip_v)

        self.threshold_value: int = 0
        self.flipping_view: List[bool] = [False, False, False]
        self.align_data: List[Tuple] = []

    # ------------------------------------------------------------------ #
    #  Layer loading
    # ------------------------------------------------------------------ #

    def load_align_layer(self, layer_type: str, file_path: str) -> LayerResult:
        """
        Load an alignment reference layer from an Excellon or G-code drill file.

        Resets :attr:`align_data` on success so stale points are not mixed
        with a new reference layer.
        """
        try:
            exc_keys = self._pcb.EXN_KEYS
            if layer_type in exc_keys:
                ext = os.path.splitext(file_path)[1].lower()
                if ext in self.EXCELLON_EXTENSIONS:
                    self._pcb.load_excellon(file_path, layer_type)
                    layer_data = self._pcb.get_excellon_layer(layer_type)
                else:
                    self._dgc.load_gcode(file_path)
                    self._dgc.convert()
                    layer_data = self._dgc.get_drill_layer()

                if layer_data and layer_data[0]:
                    self.align_data = []
                    return LayerResult(layer_data, layer_type, file_path, True, True)

        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logger.error("Error loading align layer %s: %s", file_path, e, exc_info=True)
        except Exception:
            logger.error("Uncaught exception: %s", traceback.format_exc())

        return LayerResult(None, layer_type, file_path, False, False)

    # ------------------------------------------------------------------ #
    #  Camera
    # ------------------------------------------------------------------ #

    def get_camera_frame(self, zoom: float = 1.0) -> Optional[CameraFrame]:
        """
        Capture and process the latest camera frame.

        Returns
        -------
        :class:`~app.events.CameraFrame`
            Contains a BGR numpy array. Returns *None* when no camera frame
            is available (camera disconnected, etc.).

        The Qt UI adapter converts this to ``QPixmap``; a CLI or test can
        save it to disk with ``cv2.imwrite`` or ``PIL.Image.fromarray``.
        """
        frame = self._dsm.get_webcam_frame()
        if frame is None:
            return None
        processed = self._dsm.detect_holes(frame, self.threshold_value, zoom_f=zoom)
        h, w = processed.shape[:2]
        return CameraFrame(data=processed, width=w, height=h)

    def get_camera_list(self) -> List[int]:
        """Return list of detected camera indexes."""
        return self._dsm.list_cameras_indexes()

    def update_camera(self, index: int) -> None:
        """Select the active camera by index (-1 = none)."""
        self._dsm.update_camera(index)

    # ------------------------------------------------------------------ #
    #  Alignment points
    # ------------------------------------------------------------------ #

    def add_align_point(
        self,
        geom_point: List[float],
        working_position: List[float],
    ) -> List[Tuple]:
        """
        Register an alignment point pair and return the updated list.

        Parameters
        ----------
        geom_point:
            [x, y] coordinates selected on the PCB geometry view.
        working_position:
            [x, y] machine working-coordinate position at the time of capture.
        """
        if geom_point is not None and working_position is not None:
            self.align_data.append((geom_point, working_position))
        return self.align_data

    def remove_align_points(self, rows: List[int]) -> List[Tuple]:
        """Remove alignment points by row index (supports multi-select)."""
        for r in sorted(rows, reverse=True):
            if r < len(self.align_data):
                del self.align_data[r]
            else:
                logger.error("Invalid alignment row %d", r)
        return self.align_data

    # ------------------------------------------------------------------ #
    #  Camera settings
    # ------------------------------------------------------------------ #

    def set_camera_rotation(self, angle: float) -> None:
        self._dsm.set_camera_rotation(angle)

    def set_camera_flip_h(self, flip_h: bool) -> None:
        self._dsm.flip_h = flip_h

    def set_camera_flip_v(self, flip_v: bool) -> None:
        self._dsm.flip_v = flip_v

    def set_threshold(self, value: int) -> None:
        self.threshold_value = value

    # ------------------------------------------------------------------ #
    #  Layer flipping (view transform, not data transform)
    # ------------------------------------------------------------------ #

    def flip_horizontally(self, flipped: bool) -> None:
        self.flipping_view[0] = flipped

    def flip_vertically(self, flipped: bool) -> None:
        self.flipping_view[1] = flipped
