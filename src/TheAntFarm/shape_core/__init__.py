"""Core of The Ant Farm: Gerber/Excellon parsing, toolpath generation, G-code.

The module can be imported in a headless process: the visualization layer
(:mod:`shape_core.visual_manager`) depends on vispy and OpenGL and is imported
lazily, on first access to ``VisualLayer`` or ``GLUTess``::

    from TheAntFarm.shape_core import GCoder, MachinePath

    gcoder = GCoder("top", "gerber")
"""

from .align_manager import AlignManager, TpsCoefficients
from .commands_manager import CommandManager
from .config import (
    GCODE_DEFAULTS,
    PATH_DEFAULTS,
    PROBE_DEFAULTS,
    default_config,
    merge_config,
)
from .gcode_drill_converter import DrillGcodeConverter
from .gcode_manager import (
    POSITION_DIGITS,
    GCode,
    GCodeAlignment,
    GCoder,
    GCodeLeveler,
    GCodeMacro,
    GCodeParser,
    GcodeLine,
    GcodePoint,
)
from .geometry_manager import (
    Geom,
    get_poly_diameter,
    get_poly_parts,
    merge_polygons,
    merge_polygons_path,
    offset_polygon,
    offset_polygon_holes,
)
from .macros_manager import (
    MACROS,
    TAGS,
    MacroContext,
    MacroDataError,
    MacroError,
    Macros,
    MacroSyntaxError,
    UnknownMacroTag,
    find_tags,
    validate_template,
)
from .path_manager import Gapper, MachinePath, remap_invalid_ids
from .path_types import ToolPath
from .pcb_manager import PcbObj

__all__ = [
    "GCODE_DEFAULTS",
    "MACROS",
    "PATH_DEFAULTS",
    "POSITION_DIGITS",
    "PROBE_DEFAULTS",
    "TAGS",
    "AlignManager",
    "CommandManager",
    "DrillGcodeConverter",
    "GCode",
    "GCodeAlignment",
    "GCoder",
    "GCodeLeveler",
    "GCodeMacro",
    "GCodeParser",
    "Gapper",
    "Geom",
    "GcodeLine",
    "GcodePoint",
    "MachinePath",
    "MacroContext",
    "MacroDataError",
    "MacroError",
    "Macros",
    "MacroSyntaxError",
    "PcbObj",
    "ToolPath",
    "TpsCoefficients",
    "UnknownMacroTag",
    "default_config",
    "find_tags",
    "get_poly_diameter",
    "get_poly_parts",
    "merge_config",
    "merge_polygons",
    "merge_polygons_path",
    "offset_polygon",
    "offset_polygon_holes",
    "remap_invalid_ids",
    "validate_template",
]

#: Names of the visualization layer, imported on demand (vispy/OpenGL).
_LAZY_EXPORTS = ("GLUTess", "VisualLayer")


def __getattr__(name):
    if name in _LAZY_EXPORTS:
        from . import visual_manager

        return getattr(visual_manager, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(__all__) | set(_LAZY_EXPORTS))
