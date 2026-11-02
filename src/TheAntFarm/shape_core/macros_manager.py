"""Macro system of The Ant Farm.

A macro is a plain G-code template stored in ``macros/*.gcode`` (or in the user
data folder) whose variable parts are written as ``@TAG@`` placeholders, e.g.::

    G53 G00 Z@SAFE_POS_Z@
    G38.2 Z@PROBE_POS_MIN@ F@PROBE_FEED_SLOW@

The placeholders are resolved **at streaming time** by :meth:`Macros.expand`
using the current machine state (:class:`MacroContext`), so a tag like
``@PROBE_VALUE_PREZ@`` can be filled with the probe value measured by a
previous line of the same macro.

Design notes
------------
* every available placeholder is declared once in :data:`TAGS` (name, resolver
  and description); there is no other place to update when a tag is added;
* a template is validated against :data:`TAGS` before the job starts, so a
  typo raises an error instead of sending invalid G-code to the machine;
* unknown or malformed placeholders raise :class:`MacroError`, they are never
  sent to the controller as literal text.
"""

import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple

logger = logging.getLogger(__name__)

AXES = ("X", "Y", "Z")

#: ``@NAME@`` placeholder. Only text wrapped in two ``@`` is substituted, so a
#: plain comment containing the word "probe" can never be mistaken for a tag.
TAG_PATTERN = re.compile(r"@([A-Za-z0-9_]+)@")

_MISSING = object()


class MacroError(Exception):
    """Base class for the macro errors."""


class UnknownMacroTag(MacroError):
    """The template contains a placeholder that is not declared in TAGS."""


class MacroSyntaxError(MacroError):
    """The template contains a malformed placeholder (unbalanced ``@``)."""


class MacroDataError(MacroError):
    """The machine state needed to resolve a placeholder is not available."""


@dataclass(frozen=True)
class MacroContext:
    """Machine state used to resolve the placeholders of a macro.

    Parameters
    ----------
    cfg : mapping
        Macro/commander configuration (probe position, feed rates, safe position,
        spindle speed, ...). Missing keys fall back to :data:`DEFAULT_CFG`.
    wsp : mapping
        Workspace parameters read from the ``$#`` report (``G54``.., ``TLO``...).
    dro : mapping
        Digital read out frozen at the moment the macro started
        (``WPO`` = work position, ``MPO`` = machine position).
    probe_data : sequence
        Probe results, newest first: ``probe_data[0]`` is the last probing
        point, ``probe_data[1]`` the one before it (machine coordinates).
    digits : int
        Number of decimals used to format the values.
    """

    cfg: Mapping[str, Any]
    wsp: Mapping[str, Any]
    dro: Mapping[str, Any]
    probe_data: Sequence[Sequence[float]]
    digits: int = 4

    # -- formatting ---------------------------------------------------------
    def fmt(self, value: float) -> str:
        """Format a value the same way the G-code writer does."""
        value = float(value)
        return f"{round(value, self.digits):.{self.digits}f}"

    # -- configuration ------------------------------------------------------
    def cfg_value(self, key: str, default: Any = _MISSING) -> Any:
        """Return a configuration value, with an explicit error when missing."""
        if key in self.cfg:
            return self.cfg[key]
        if default is not _MISSING:
            return default
        raise MacroDataError(f"Missing configuration key for the macro: {key}")

    # -- machine state ------------------------------------------------------
    @property
    def wco(self) -> List[float]:
        """Work coordinate offset (machine position - work position)."""
        try:
            return [self.dro["MPO"][i] - self.dro["WPO"][i] for i in range(len(AXES))]
        except (KeyError, IndexError, TypeError) as exc:
            raise MacroDataError("Machine position (WPO/MPO) not available") from exc

    def probe(self, when: str, axis: str) -> float:
        """Probe value for ``axis`` in work coordinates.

        ``when="ACT"`` is the last probing cycle, ``when="PRE"`` the previous one.
        """
        index = 0 if when == "ACT" else 1
        try:
            value = self.probe_data[index][AXES.index(axis)]
        except (IndexError, KeyError, TypeError) as exc:
            raise MacroDataError(f"Probe value {when}_{axis} not available") from exc
        return float(value) - self.wco[AXES.index(axis)]

    def tlo(self) -> float:
        """Tool length offset currently applied by the controller."""
        try:
            return float(self.wsp["TLO"])
        except (KeyError, TypeError, ValueError) as exc:
            raise MacroDataError("Tool length offset not available in the $# report") from exc

    def tlo_delta(self) -> float:
        """Tool length difference between the last and the previous probing cycle."""
        try:
            return float(self.probe_data[0][2]) - float(self.probe_data[1][2])
        except (IndexError, KeyError, TypeError) as exc:
            raise MacroDataError("Two probing cycles are needed to compute the tool length") from exc


#: Default configuration of the macros. The values provided by the application
#: (machine settings) override them, see :meth:`Macros.load_cfg`.
DEFAULT_CFG: Dict[str, Any] = {
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
    "tool_setter_pos": None,  # (X, Y) of the fixed tool setter, see load_cfg
    "tool_setter_working": False,  # False: machine position, True: working position
}


@dataclass(frozen=True)
class Tag:
    """A placeholder available in the macro templates."""

    name: str
    resolve: Callable[[MacroContext], str]
    description: str = ""


def _pos(axis: str) -> int:
    return AXES.index(axis)


def _cfg_pos(key: str, axis: str) -> Callable[[MacroContext], str]:
    return lambda ctx: ctx.fmt(ctx.cfg_value(key)[_pos(axis)])


def _cfg_scalar(key: str) -> Callable[[MacroContext], str]:
    return lambda ctx: ctx.fmt(ctx.cfg_value(key))


def _feed(index: int) -> Callable[[MacroContext], str]:
    return lambda ctx: ctx.fmt(ctx.cfg_value("tool_probe_feedrate")[index])


def _probe_value(when: str, axis: str) -> Callable[[MacroContext], str]:
    return lambda ctx: ctx.fmt(ctx.probe(when, axis))


def _setter_pos(axis: str) -> Callable[[MacroContext], str]:
    return lambda ctx: ctx.fmt(ctx.cfg_value("tool_setter_pos")[_pos(axis)])


def _setter_type(ctx: MacroContext) -> str:
    return "G54" if ctx.cfg_value("tool_setter_working") else "G53"


def _probe_type(ctx: MacroContext) -> str:
    return "G54" if ctx.cfg_value("tool_probe_working") else "G53"


def _probe_hold(ctx: MacroContext) -> str:
    return "M0" if ctx.cfg_value("tool_probe_hold") else "(NO HOLD)"


def _change_type(ctx: MacroContext) -> str:
    # The tool change position can be expressed in a different coordinate system
    # than the probe position; when not configured, follow the probe setting.
    working = ctx.cfg_value("tool_change_working", ctx.cfg_value("tool_probe_working"))
    return "G54" if working else "G53"


def _change_feed(index: int) -> Callable[[MacroContext], str]:
    def resolve(ctx: MacroContext) -> str:
        feedrates = ctx.cfg_value("tool_change_feedrate", ctx.cfg_value("tool_probe_feedrate"))
        return ctx.fmt(feedrates[index])

    return resolve


def _tlo(mode: str) -> Callable[[MacroContext], str]:
    if mode == "A":
        # add the measured difference to the offset currently applied
        return lambda ctx: ctx.fmt(ctx.tlo() + ctx.tlo_delta())
    # replace the offset with the measured difference
    return lambda ctx: ctx.fmt(ctx.tlo_delta())


def _spindle_stop(ctx: MacroContext) -> str:
    # One tag must expand to one line: the G-code streamer sends (and waits the
    # ack of) a single line at a time. The dwell is a separate tag.
    return "M5"


def _spindle_start(ctx: MacroContext) -> str:
    speed = ctx.cfg.get("spindle")
    if speed is None:
        # No speed configured: do not overwrite the spindle speed of the job.
        return "M3"
    return f"M3 S{ctx.fmt(speed)}"


TAGS: Dict[str, Tag] = {
    tag.name: tag
    for tag in (
        # -- probe position / feed rates ------------------------------------
        Tag("PROBE_POS_X", _cfg_pos("tool_probe_pos", "X"), "Probe X coordinate"),
        Tag("PROBE_POS_Y", _cfg_pos("tool_probe_pos", "Y"), "Probe Y coordinate"),
        Tag("PROBE_POS_MIN", _cfg_scalar("tool_probe_min"), "Lowest Z allowed while probing"),
        Tag("PROBE_TYPE_POS", _probe_type, "Coordinate system of the probe position (G54/G53)"),
        Tag("PROBE_FEED_XY", _feed(0), "Feed rate for the XY travel"),
        Tag("PROBE_FEED_FAST", _feed(1), "Feed rate for the fast approach"),
        Tag("PROBE_FEED_SLOW", _feed(2), "Feed rate for the measuring move"),
        Tag("PROBE_HOLD_BEFORE", _probe_hold, "Optional M0 before the probing move"),
        Tag("PROBE_BACKOFF", _cfg_scalar("tool_probe_backoff"), "Retract distance between the two probes"),
        # -- fixed tool setter ----------------------------------------------
        Tag("SETTER_POS_X", _setter_pos("X"), "Tool setter X coordinate"),
        Tag("SETTER_POS_Y", _setter_pos("Y"), "Tool setter Y coordinate"),
        Tag("SETTER_TYPE_POS", _setter_type, "Coordinate system of the tool setter (G54/G53)"),
        # -- measured values (work coordinates) -----------------------------
        Tag("PROBE_VALUE_PREX", _probe_value("PRE", "X"), "Previous probe, X"),
        Tag("PROBE_VALUE_PREY", _probe_value("PRE", "Y"), "Previous probe, Y"),
        Tag("PROBE_VALUE_PREZ", _probe_value("PRE", "Z"), "Previous probe, Z"),
        Tag("PROBE_VALUE_ACTX", _probe_value("ACT", "X"), "Last probe, X"),
        Tag("PROBE_VALUE_ACTY", _probe_value("ACT", "Y"), "Last probe, Y"),
        Tag("PROBE_VALUE_ACTZ", _probe_value("ACT", "Z"), "Last probe, Z"),
        # -- tool change position -------------------------------------------
        Tag("CHANGE_POS_X", _cfg_pos("tool_change_pos", "X"), "Tool change X coordinate"),
        Tag("CHANGE_POS_Y", _cfg_pos("tool_change_pos", "Y"), "Tool change Y coordinate"),
        Tag("CHANGE_POS_Z", _cfg_pos("tool_change_pos", "Z"), "Tool change Z coordinate"),
        Tag("CHANGE_TYPE_POS", _change_type, "Coordinate system of the change position (G54/G53)"),
        Tag("CHANGE_FEED_SLOW", _change_feed(2), "Slow feed rate for the tool change moves"),
        Tag("CHANGE_FEED_FAST", _change_feed(1), "Fast feed rate for the tool change moves"),
        # -- safety / machine ----------------------------------------------
        Tag("SAFE_POS_Z", _cfg_pos("safe_pos", "Z"), "Safe Z coordinate"),
        Tag("PRE_POS_X", lambda ctx: ctx.fmt(ctx.dro["WPO"][0]), "Work X position before the macro"),
        Tag("PRE_POS_Y", lambda ctx: ctx.fmt(ctx.dro["WPO"][1]), "Work Y position before the macro"),
        Tag("PRE_POS_Z", lambda ctx: ctx.fmt(ctx.dro["WPO"][2]), "Work Z position before the macro"),
        Tag("SPINDLE_STOP", _spindle_stop, "Stop the spindle before the tool change"),
        Tag("SPINDLE_DWELL", _cfg_scalar("spindle_stop_dwell"), "Dwell used to wait the spindle spin down"),
        Tag("SPINDLE_START", _spindle_start, "Restart the spindle at the job speed"),
        # -- tool length offset --------------------------------------------
        Tag("TLO_TYPE_A", _tlo("A"), "Tool length offset to apply (add to the current one)"),
        Tag("TLO_TYPE_N", _tlo("N"), "Tool length offset measured by the last two probes"),
    )
}


@dataclass(frozen=True)
class MacroSpec:
    """A macro supported by the application."""

    id: str
    variants: Mapping[str, str]
    default_variant: str
    mode_key: Optional[str] = None
    description: str = ""


#: Supported macros. ``variants`` maps a mode to a template file so that the
#: procedure can be selected from the settings (e.g. WCS re-datum vs TLO).
MACROS: Dict[str, MacroSpec] = {
    "M6": MacroSpec(
        id="M6",
        variants={
            "wcs": "tool_change_wcs.gcode",  # probe the workpiece, re-datum G54
            "tlo": "tool_change_tlo.gcode",  # probe the workpiece, apply a TLO
            "setter": "tool_change_setter.gcode",  # probe the fixed tool setter
        },
        default_variant="wcs",
        mode_key="tool_change_mode",
        description="Tool change with tool length correction",
    ),
}


def find_tags(text: str) -> List[str]:
    """Return the names of the placeholders used by ``text``, in order."""
    return TAG_PATTERN.findall(text)


def validate_template(text: str) -> List[Tuple[int, str]]:
    """Check a template against the tag catalog.

    Returns
    -------
    list of (int, str)
        One ``(line number, problem)`` item for every unknown placeholder and for
        every unbalanced ``@``. An empty list means the template is valid.
    """
    problems: List[Tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for name in find_tags(line):
            if name.upper() not in TAGS:
                problems.append((line_no, f"unknown tag @{name}@"))
        leftover = TAG_PATTERN.sub("", line)
        if "@" in leftover:
            problems.append((line_no, "unbalanced '@'"))
    return problems


class Macros:
    """Loads the macro templates and resolves their placeholders."""

    MACRO_FOLDER_NAME = "macros"

    def __init__(self, parent=None):
        self.parent = parent

        self.cfg: Dict[str, Any] = dict(DEFAULT_CFG)
        self.load_cfg()

        self.macros_default_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", self.MACRO_FOLDER_NAME)
        )

    # -- configuration ------------------------------------------------------
    def load_cfg(self, cfg: Optional[Mapping[str, Any]] = None) -> None:
        """Merge ``cfg`` on top of :data:`DEFAULT_CFG`.

        The configuration is copied, so that the macro manager never modifies the
        dictionary owned by the caller and missing keys always fall back to a
        default value.
        """
        merged = dict(DEFAULT_CFG)
        if cfg is not None:
            merged.update(cfg)
        if merged.get("tool_setter_pos") is None:
            # A setter that is not configured falls back to the probe position,
            # which is a position the user already trusts, instead of failing
            # in the middle of a tool change.
            merged["tool_setter_pos"] = tuple(merged["tool_probe_pos"])[:2]
            if str(merged.get("tool_change_mode", "")).lower() == "setter":
                logger.warning("tool_setter_pos not configured: probing the probe position instead")
        self.cfg = merged

    @property
    def digits(self) -> int:
        return int(getattr(self.parent, "DIGITS", 4))

    def format_float(self, value: float) -> str:
        """Format a value: delegated to the G-code writer when available."""
        parent = getattr(self, "parent", None)
        if parent is not None and hasattr(parent, "format_float"):
            return parent.format_float(value)
        return f"{round(float(value), self.digits):.{self.digits}f}"

    # -- templates ----------------------------------------------------------
    def is_macro(self, cmd: str) -> bool:
        return str(cmd).strip().upper() in MACROS

    def get_mode(self, macro: str) -> str:
        """Return the selected variant (mode) of ``macro``."""
        spec = MACROS[str(macro).strip().upper()]
        if spec.mode_key is None:
            return spec.default_variant
        mode = str(self.cfg.get(spec.mode_key, spec.default_variant)).lower()
        if mode not in spec.variants:
            raise MacroError(
                f"Unknown mode '{mode}' for macro {spec.id}: "
                f"available modes are {sorted(spec.variants)}"
            )
        return mode

    def get_macro_path(self, macro: str, local_path: str = "") -> str:
        spec = MACROS.get(str(macro).strip().upper())
        if spec is None:
            raise MacroError(f"Command {macro!r} is not a macro")
        file_name = spec.variants[self.get_mode(macro)]
        macros_path = self.macros_default_path
        if local_path and os.path.isdir(local_path):
            local_macros_path = os.path.join(local_path, self.MACRO_FOLDER_NAME)
            if os.path.isfile(os.path.join(local_macros_path, file_name)):
                macros_path = local_macros_path
        return os.path.join(macros_path, file_name)

    def get_macro_string(self, macro: str, local_path: str = "") -> str:
        """Return the validated template of ``macro``.

        Raises
        ------
        MacroError
            When the command is not a macro, the file is missing or the template
            uses unknown/malformed placeholders.
        """
        macro_path = self.get_macro_path(macro, local_path=local_path)
        if not os.path.isfile(macro_path):
            raise MacroError(f"Macro file not found: {macro_path}")

        with open(macro_path, "r", encoding="utf-8", errors="replace") as macro_file:
            text = macro_file.read()

        problems = validate_template(text)
        if problems:
            details = ", ".join(f"line {line}: {problem}" for line, problem in problems)
            raise MacroError(f"Invalid macro template {os.path.basename(macro_path)}: {details}")
        return text

    # -- expansion ----------------------------------------------------------
    def make_context(self, wsp, probe_data, dro) -> MacroContext:
        return MacroContext(cfg=self.cfg, wsp=wsp, dro=dro, probe_data=probe_data, digits=self.digits)

    def expand(self, text: str, context: MacroContext) -> str:
        """Replace every ``@TAG@`` of ``text`` with its value."""

        def replace(match: "re.Match[str]") -> str:
            name = match.group(1).upper()
            tag = TAGS.get(name)
            if tag is None:
                raise UnknownMacroTag(f"Unknown macro tag @{name}@ (available: {', '.join(sorted(TAGS))})")
            return tag.resolve(context)

        expanded = TAG_PATTERN.sub(replace, text)
        if "@" in TAG_PATTERN.sub("", expanded):
            raise MacroSyntaxError("Unbalanced '@' in the macro template")
        return expanded

    def expand_lines(self, lines: Sequence[str], context: MacroContext) -> Iterator[str]:
        """Expand a template line by line (used for the preview)."""
        for line in lines:
            yield self.expand(line, context)

    def compute_tag(self, gc_str: str, wsp, probe_data, dro) -> str:
        """Expand one line of a macro (used while streaming the job)."""
        return self.expand(gc_str, self.make_context(wsp, probe_data, dro))

    def check_tag_in_string(self, gc_str: str) -> bool:
        return bool(find_tags(str(gc_str)))
