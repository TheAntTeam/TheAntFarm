"""
Machine Service – GRBL protocol state machine (pure Python).

Design contract
---------------
- No Qt imports anywhere in this file.
- Handles all *stateful* protocol logic: position tracking, probe/ABL
  state, G-code file registry and GRBL response parsing.
- The async transport layer (buffered send, flow-control timers, Qt
  signals) stays in ``controller_manager.py``; it delegates every
  stateful decision to this service.

Migration path from ControlController
--------------------------------------
Phase 1 (this file)
    ``ControlController`` keeps working unchanged.
    Gradually redirect its methods to delegate here.

Phase 2
    ``ControlController`` reduced to Qt boilerplate only::

        def parse_bracket_angle(self, line):
            return self._service.parse_status_report(line)
"""
from __future__ import annotations

import logging
import random
import re
import string
import traceback
from collections import OrderedDict, deque
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from shape_core.gcode_manager import GCoder, GCodeAlignment, GCodeLeveler, GCodeParser

from app.events import MachineStatus

logger = logging.getLogger(__name__)

# Pattern shared with ControlController – matches the delimiters used
# inside GRBL square/angle bracket responses.
_SPLIT_PAT = re.compile(r"[:|,]")


class MachineService:
    """
    Pure-Python GRBL state machine.

    Replaces the stateful parts of :class:`controller.ControlController`
    without inheriting from ``QObject``, making it:

    - directly unit-testable (no Qt event-loop needed)
    - usable from a CLI or headless script
    - the single source-of-truth for machine state

    No Qt types are imported or returned.
    """

    def __init__(self) -> None:
        # ---- position ------------------------------------------------
        self.mpos_a: np.ndarray = np.array([0.0, 0.0, 0.0])
        self.wco_a: np.ndarray = np.array([0.0, 0.0, 0.0])
        self.wpos_a: np.ndarray = np.array([0.0, 0.0, 0.0])

        # ---- status --------------------------------------------------
        self.status: str = ""
        self.status_report_od: Dict[str, Any] = OrderedDict()
        self.workspace_params_od: Dict[str, Any] = OrderedDict()

        # ---- probe / ABL --------------------------------------------
        self.prb_val: deque = deque([[-1.0, -1.0, -1.0], [-1.0, -1.0, -1.0]], maxlen=2)
        self.abl_val: List[Any] = []
        self.prb_activated: bool = False
        self.abl_activated: bool = False
        self.prb_updated: bool = False
        self.abl_updated: bool = False
        self.prb_num_todo: int = 0
        self.prb_num_done: int = 0
        self.prb_reps_todo: int = 1
        self.abl_cmd_ls: List[str] = []
        self.abl_steps: Tuple[int, int] = (0, 0)

        # ---- alignment -----------------------------------------------
        self.align_data: List[Any] = []

        # ---- G-code file registry ------------------------------------
        self.gcodes_od: Dict[str, Any] = OrderedDict()

    # ================================================================= #
    #  GRBL response parsing  (ported from ControlController verbatim)
    # ================================================================= #

    def parse_status_report(self, line: str) -> Dict[str, Any]:
        """
        Parse a GRBL ``<…>`` status line and update internal state.

        Returns the updated ``status_report_od`` dict so the Qt adapter
        can emit it via signal without needing to read state directly.
        """
        line_stripped = line.strip()
        fields = line_stripped[1:-1].split("|")
        self.status = fields[0]
        self.status_report_od["state"] = fields[0]
        self.status_report_od["pins"] = ""  # reset limit-pin status

        for field in fields[1:]:
            word = _SPLIT_PAT.split(field.strip())
            try:
                if word[0] == "MPos":
                    self.mpos_a = np.array([float(word[1]), float(word[2]), float(word[3])])
                    self.status_report_od["mpos"] = self.mpos_a.copy()
                elif word[0] == "WCO":
                    self.wco_a = np.array([float(word[1]), float(word[2]), float(word[3])])
                    self.status_report_od["wco"] = self.wco_a.copy()
                elif word[0] == "Pn":
                    self.status_report_od["pins"] = word[1]
                elif word[0] == "F":
                    self.status_report_od["curfeed"] = float(word[1])
                elif word[0] == "FS":
                    self.status_report_od["curfeed"] = float(word[1])
                    self.status_report_od["curspindle"] = float(word[2])
                elif word[0] == "Bf":
                    self.status_report_od["planner"] = int(word[1])
                    self.status_report_od["rxbytes"] = int(word[2])
                elif word[0] == "Ov":
                    self.status_report_od["OvFeed"] = int(word[1])
                    self.status_report_od["OvRapid"] = int(word[2])
                    self.status_report_od["OvSpindle"] = int(word[3])
            except (ValueError, IndexError) as e:
                logger.error("Error parsing GRBL field %r: %s", field, e)

        self.wpos_a = self.mpos_a - self.wco_a
        self.status_report_od["wpos"] = self.wpos_a.copy()
        return self.status_report_od

    def parse_bracket_square(self, line: str) -> None:
        """
        Parse a GRBL ``[…]`` parameter response (probe, workspace offsets, TLO…).
        """
        word = _SPLIT_PAT.split(line.rstrip()[1:-1])
        try:
            if word[0] == "PRB":
                self.prb_val.appendleft([float(word[1]), float(word[2]), float(word[3])])
                self.prb_updated = True
            elif word[0] in ("G54", "G55", "G56", "G57", "G58", "G59", "G28", "G30", "G92"):
                self.workspace_params_od[word[0]] = np.array(
                    [float(word[1]), float(word[2]), float(word[3])]
                )
            elif word[0] == "TLO":
                self.workspace_params_od["TLO"] = float(word[1])
        except (ValueError, IndexError) as e:
            logger.error("Error parsing GRBL bracket-square %r: %s", line, e)

    # ================================================================= #
    #  Probe / ABL state machine
    # ================================================================= #

    def process_probe_and_abl(self) -> Tuple[bool, bool, bool, bool]:
        """
        Decide what to acknowledge after a ``[PRB:…]`` response.

        Returns
        -------
        (ack_prb, ack_abl, send_next, other)
            Tuple of boolean flags consumed by the Qt adapter to emit
            the appropriate signals.
        """
        ack_prb = ack_abl = send_next = other = False

        if self.prb_activated and self.prb_updated:
            self.prb_activated = False
            self.prb_updated = False
            ack_prb = True
        elif self.abl_activated:
            ack_abl, send_next = self._update_abl()
        else:
            other = True

        return ack_prb, ack_abl, send_next, other

    def arm_probe(self) -> None:
        """Mark a single Z-probe operation as pending."""
        self.prb_updated = False
        self.prb_activated = True
        self.prb_num_todo = 1
        self.prb_reps_todo = 1

    def arm_auto_bed_levelling(
        self,
        abl_cmd_ls: List[str],
        prb_num_todo: int,
        steps: Tuple[int, int],
    ) -> None:
        """Initialise ABL state (called by the Qt adapter after building the command list)."""
        self.abl_cmd_ls = abl_cmd_ls
        self.prb_num_todo = prb_num_todo
        self.abl_steps = steps
        self.abl_val = []
        self.prb_num_done = 0
        self.prb_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.abl_activated = True

    @staticmethod
    def get_grid_coords(bbox_t: Tuple[float, float, float, float, float, float], steps_t: Tuple[int, int]):
        xmin = bbox_t[0]
        ymin = bbox_t[1]
        xmax = bbox_t[3]
        ymax = bbox_t[4]
        x_step = steps_t[0]
        y_step = steps_t[1]
        xc = np.linspace(xmin, xmax, x_step)
        yc = np.linspace(ymin, ymax, y_step)
        xi, yi = np.meshgrid(xc, yc)
        return list(zip(xi.ravel().tolist(), yi.ravel().tolist()))

    @staticmethod
    def make_cmd_auto_bed_levelling(
        xy_c_l: List[Tuple[float, float]],
        travel_z: float,
        probe_z_min: float,
        probe_feed_rate: float,
    ):
        gcr = GCoder("dummy", "commander")
        abl_cmd_ls, prb_num_todo = gcr.get_autobed_leveling_code(xy_c_l, travel_z, probe_z_min, probe_feed_rate)
        logger.debug("ABL routine: %s", str(abl_cmd_ls))
        logger.debug("ABL points to do: %s", str(prb_num_todo))
        return [abl_cmd_ls, prb_num_todo]

    def get_probe_value(self) -> List[float]:
        """Return the most recently received probe position."""
        return list(self.prb_val)[0] if self.prb_val else []

    def get_abl_value(self) -> List[Any]:
        return self.abl_val

    def get_next_abl_command(self) -> Optional[str]:
        """Return the next ABL probe command to send, or *None* when done."""
        if self.prb_num_done < len(self.abl_cmd_ls):
            return self.abl_cmd_ls[self.prb_num_done]
        return None

    def _update_abl(self) -> Tuple[bool, bool]:
        """Internal ABL step – called by :meth:`process_probe_and_abl`."""
        ack_flag = send_next = False
        if self.prb_updated:
            self.prb_updated = False
            self.prb_num_done += 1
            self.abl_val.append(list(self.prb_val)[0])
            if self.prb_num_done >= self.prb_num_todo:
                ack_flag = True
                self.abl_activated = False
            else:
                send_next = True
        return ack_flag, send_next

    def update_abl(self) -> Tuple[bool, bool]:
        """Public wrapper for one ABL state step, used by migration adapters."""
        return self._update_abl()

    # ================================================================= #
    #  Alignment data
    # ================================================================= #

    def set_align_data(self, data: Any) -> None:
        if isinstance(data, (list, tuple)):
            self.align_data = data

    def get_align_data(self) -> Any:
        return self.align_data

    # ================================================================= #
    #  G-code file registry
    # ================================================================= #

    def load_gcode_file(self, cfg: Dict[str, Any], path: str) -> None:
        gcp = GCodeParser(cfg)
        gcp.load_gcode_file(path)
        gcp.interp()
        gcp.vectorize()
        self.register_gcode(path, gcp)

    def register_gcode(self, path: str, gcp: Any) -> str:
        """Store a loaded :class:`~shape_core.GCodeParser` and return its tag."""
        tag = self._new_tag()
        self.gcodes_od[path] = {"gcode": gcp, "tag": tag}
        return tag

    def deregister_gcode(self, path: str) -> None:
        self.gcodes_od.pop(path, None)

    def get_gcode_entry(self, path: str) -> Optional[Dict[str, Any]]:
        return self.gcodes_od.get(path)

    def get_gcode_gcp(self, path: str) -> Any:
        entry = self.get_gcode_entry(path)
        if entry is None:
            raise KeyError(path)
        return entry["gcode"]

    def get_gcode_lines(self, path: str):
        return self.get_gcode_gcp(path).recode_gcode()

    @staticmethod
    def get_change_tool_lines():
        gcp = GCodeParser(None)
        return gcp.get_change_tool_gcode()

    def get_boundary_box(self, path: str):
        return self.get_gcode_gcp(path).get_bbox()

    def apply_alignment(self, path: str) -> None:
        gcp = self.get_gcode_gcp(path)
        align = GCodeAlignment(gcp.gc)
        align.update_align_info(self.align_data.copy())
        align.apply_align()

    def remove_alignment(self, path: str) -> bool:
        gcp = self.get_gcode_gcp(path)
        if gcp.gc.aligned_vectors:
            gcp.gc.aligned_vectors = []
            return True
        return False

    def apply_abl(self, path: str) -> None:
        gcp = self.get_gcode_gcp(path)
        abl = GCodeLeveler(gcp.gc)
        abl_val = self.abl_val.copy()
        if abl_val != [] or True:
            last_probe = abl_val.pop()
            abl.get_grid_data(abl_val, self.abl_steps, last_probe, self.wco_a)
        abl.interp_grid_data()
        abl.apply_abl()

    def remove_abl(self, path: str) -> bool:
        gcp = self.get_gcode_gcp(path)
        if gcp.gc.modified_vectors:
            gcp.gc.modified_vectors = []
            return True
        return False

    def _new_tag(self, size: int = 4) -> str:
        existing = {v["tag"] for v in self.gcodes_od.values()}
        chars = string.ascii_uppercase + string.digits
        while True:
            candidate = "".join(random.choices(chars, k=size))
            if candidate not in existing:
                return candidate
