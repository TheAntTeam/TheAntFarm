"""
Qt Signal Bridge – the ONLY place where Qt types are created from service data.

Responsibility
--------------
Convert pure-Python results returned by ``app/services/`` into Qt types
and emit them as signals.  Nothing outside this file should import
``QPixmap``, ``QImage`` or similar types for the purpose of wrapping
service results.

Current Qt-type conversions
----------------------------
- :class:`~app.events.CameraFrame` (numpy BGR array) → ``QPixmap``
- :class:`~app.events.LayerResult`                   → signal arguments
- :class:`~app.events.MachineStatus`                 → ``OrderedDict``

Usage pattern
-------------
The existing controllers call service methods and pass results here::

    # Inside ControllerWorker (controller_manager.py) – after migration:

    from app.adapters.qt_signal_bridge import camera_frame_to_pixmap

    def on_camera_timeout(self):
        frame = self.align_service.get_camera_frame(self.camera_zoom)
        if frame:
            self.update_camera_image_s.emit(camera_frame_to_pixmap(frame))
        else:
            self.update_camera_image_s.emit(QPixmap())

Before this bridge existed, the conversion lived directly inside
``AlignController.camera_new_frame()`` via ``qimage2ndarray.array2qimage``,
mixing Qt and domain concerns.  Moving it here makes the services
independently testable without a Qt application.
"""
from __future__ import annotations

import logging
from typing import Optional

import qimage2ndarray
from PySide6.QtGui import QPixmap

from app.events import CameraFrame, LayerResult

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
#  Camera
# ------------------------------------------------------------------ #


def camera_frame_to_pixmap(frame: Optional[CameraFrame]) -> QPixmap:
    """
    Convert a :class:`~app.events.CameraFrame` to a ``QPixmap``.

    Returns an empty ``QPixmap`` when *frame* is *None* or has zero size,
    matching the current behaviour of ``ControllerWorker.on_camera_timeout``.
    """
    if frame is None or frame.width == 0 or frame.height == 0:
        return QPixmap()
    qimage = qimage2ndarray.array2qimage(frame.data)
    return QPixmap.fromImage(qimage)


# ------------------------------------------------------------------ #
#  Layer result → signal arguments
# ------------------------------------------------------------------ #


def layer_result_to_signal_args(result: LayerResult):
    """
    Unpack a :class:`~app.events.LayerResult` into the tuple expected by the
    ``update_layer_s`` / ``update_align_layer_s`` signals::

        Signal(Od, str, str, bool)
        → (layer_data, layer_type, layer_path, has_drill_exceptions)

    Returns the "failure" tuple ``(None, layer_type, "", False)`` when
    ``result.ok`` is *False*, keeping the same behaviour as the current
    ``ControllerWorker.load_new_layer`` implementation.
    """
    if result.ok and result.layer_data is not None:
        return result.layer_data, result.layer_type, result.layer_path, result.has_drill_exceptions
    logger.warning("Invalid layer data for %s (%s)", result.layer_type, result.layer_path)
    return None, result.layer_type, "", False
