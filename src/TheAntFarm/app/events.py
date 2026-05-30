"""
Pure-Python result / event types for inter-layer communication.

Rules
-----
- No Qt imports anywhere in this file.
- UI adapters (Qt, CLI, …) convert these types at their own boundary.
  e.g. :class:`CameraFrame` → ``QPixmap`` happens only inside
  ``app/adapters/qt_signal_bridge.py``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

import numpy as np


@dataclass
class LayerResult:
    """Result of loading a PCB layer (Gerber or Excellon)."""

    layer_data: Optional[Any]
    layer_type: str
    layer_path: str
    has_drill_exceptions: bool  # True when the layer carries drill/exception geometry
    ok: bool


@dataclass
class PathResult:
    """Result of tool-path computation."""

    tag: str
    paths: List[Any]


@dataclass
class GCodeResult:
    """Result of G-code generation."""

    tag: str
    gcode_path: str  # empty string on failure


@dataclass
class MachineStatus:
    """Machine state parsed from a GRBL ``<…>`` status report."""

    state: str = ""
    mpos: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    wco: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    wpos: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    feed: float = 0.0
    spindle: float = 0.0
    pins: str = ""


@dataclass
class ProbeResult:
    """Result of a Z-probe cycle."""

    position: List[float] = field(default_factory=list)
    success: bool = False


@dataclass
class CameraFrame:
    """
    Raw camera frame (numpy array, BGR or RGB).

    UI adapters convert this to ``QPixmap`` / PIL Image / saved file.
    The service layer never touches Qt image types.
    """

    data: np.ndarray
    width: int
    height: int

    @classmethod
    def empty(cls) -> CameraFrame:
        return cls(data=np.empty((0, 0, 3), dtype=np.uint8), width=0, height=0)
