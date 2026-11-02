"""Default configuration of the CAM pipeline.

The toolpath generator (``MachinePath``) and the G-code writer (``GCoder``)
need different values for the same job, and the probe/tool change settings are
needed by the macro and command managers: keeping the defaults in one place
means that a value is defined once, and that a configuration coming from the
application can always be merged on top of a complete set (no ``KeyError`` for
a missing key).
"""

from typing import Any, Dict, Mapping, Optional

#: Values used by every G-code job.
COMMON_GCODE: Dict[str, Any] = {
    "cut": -0.07,
    "travel": 0.7,
    "xy_feedrate": 250.0,
    "z_feedrate": 40.0,
    "spindle": 1000.0,
    "mirror": False,
}

#: Probe position, tool change position and feed rates (machine settings).
PROBE_DEFAULTS: Dict[str, Any] = {
    "tool_probe_pos": (-1.0, -1.0, -11.0),
    "tool_probe_working": True,  # False: machine position, True: working position
    "tool_probe_min": -11.0,
    "tool_change_pos": (-41.2, -120.88, -1.0),
    "tool_probe_feedrate": (300.0, 80.0, 50.0),  # XY, fast, slow
    "tool_probe_hold": False,
    "tool_probe_zero": False,
    "safe_pos": (-1.0, -1.0, -1.0),
    "tool_probe_backoff": 1.5,
    "spindle_stop_dwell": 1.0,
    "tool_setter_pos": None,  # (X, Y), falls back to the probe position
    "tool_setter_working": False,
}

#: Defaults of the G-code writer, per machining type.
GCODE_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "gerber": dict(COMMON_GCODE),
    "profile": {**COMMON_GCODE, "cut": -1.8, "multi_depth": True, "depth_per_pass": 0.6},
    "pocketing": {**COMMON_GCODE, "multi_depth": False, "depth_per_pass": 0.0},
    "drill": {**COMMON_GCODE, "cut": -2.1},
    "commander": dict(PROBE_DEFAULTS),
}

#: Defaults of the toolpath generator, per machining type.
PATH_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "gerber": {"tool_diameter": 0.2, "passages": 3, "overlap": 0.3},
    "profile": {"tool_diameter": 1.0, "margin": 0.1, "taps_type": 3, "taps_length": 1.0},
    "pocketing": {"tool_diameter": 1.0},
    "drill": {"tool_diameter": None, "bits_diameter": [0.8], "optimize": False, "milling_tool": False},
}


def default_config(kind: str, machining_type: str) -> Dict[str, Any]:
    """Return a copy of the defaults of ``kind`` for ``machining_type``.

    Parameters
    ----------
    kind : str
        ``"path"`` for :class:`~shape_core.path_manager.MachinePath`,
        ``"gcode"`` for :class:`~shape_core.gcode_manager.GCoder`.
    machining_type : str
        ``gerber``, ``profile``, ``pocketing``, ``drill`` or ``commander``.

    Returns
    -------
    dict
        An empty dictionary for an unknown machining type, so that the caller
        can add new tools without touching this module.
    """
    defaults = PATH_DEFAULTS if kind == "path" else GCODE_DEFAULTS
    return dict(defaults.get(machining_type, {}))


def merge_config(kind: str, machining_type: str, cfg: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Merge ``cfg`` on top of the defaults.

    ``None`` values in ``cfg`` are ignored, so that a settings file with an empty
    entry does not override a meaningful default.
    """
    merged = default_config(kind, machining_type)
    if cfg:
        merged.update({key: value for key, value in cfg.items() if value is not None})
    return merged
