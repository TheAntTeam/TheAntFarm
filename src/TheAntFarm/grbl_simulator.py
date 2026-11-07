"""Simulated GRBL 1.1 controller, to use and test The Ant Farm without a machine.

The simulator follows GRBL 1.1h (gnea/grbl): ``ok`` is sent when a line has been
queued in the planner, not when it has been executed; real-time commands are
handled as soon as they arrive; a machine on hold stops reading new lines; and a
soft reset while moving raises ``ALARM:3``.

It is simplified: the motion runs at constant speed (no acceleration), an arc
moves along its chord in the time of the arc, and limit switches, safety door,
check mode, sleep and startup lines are not simulated. Homing is enabled
(``$22=1``) but the machine starts unlocked.

Lines starting with ``$SIM=`` control the simulator and get no ``ok``:

- ``$SIM=ERROR:<code>``: the next G-code line is rejected with ``error:<code>``.
- ``$SIM=ALARM:<code>``: raise ``ALARM:<code>`` now.
- ``$SIM=PROBE:<z>``: the probe touches at machine Z ``<z>``.
"""

import logging
import math
import re
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable, Deque, Dict, List, Optional, Tuple, Union

from PySide6.QtCore import QByteArray, QElapsedTimer, QObject, QTimer, Signal
from PySide6.QtSerialPort import QSerialPort

logger = logging.getLogger(__name__)

SIMULATOR_PORT_NAME = "GRBL simulator"

AXES = "XYZ"
Vector = List[float]

STATUS_EXPECTED_COMMAND_LETTER = 1
STATUS_BAD_NUMBER_FORMAT = 2
STATUS_INVALID_STATEMENT = 3
STATUS_NEGATIVE_VALUE = 4
STATUS_SETTING_DISABLED = 5
STATUS_IDLE_ERROR = 8
STATUS_SYSTEM_GC_LOCK = 9
STATUS_OVERFLOW = 11
STATUS_INVALID_JOG_COMMAND = 16
STATUS_GCODE_UNSUPPORTED_COMMAND = 20
STATUS_GCODE_MODAL_GROUP_VIOLATION = 21
STATUS_GCODE_UNDEFINED_FEED_RATE = 22
STATUS_GCODE_COMMAND_VALUE_NOT_INTEGER = 23
STATUS_GCODE_AXIS_COMMAND_CONFLICT = 24
STATUS_GCODE_WORD_REPEATED = 25
STATUS_GCODE_NO_AXIS_WORDS = 26
STATUS_GCODE_INVALID_LINE_NUMBER = 27
STATUS_GCODE_VALUE_WORD_MISSING = 28
STATUS_GCODE_UNSUPPORTED_COORD_SYS = 29
STATUS_GCODE_G53_INVALID_MOTION_MODE = 30
STATUS_GCODE_AXIS_WORDS_EXIST = 31
STATUS_GCODE_INVALID_TARGET = 33
STATUS_GCODE_NO_OFFSETS_IN_PLANE = 35
STATUS_GCODE_UNUSED_WORDS = 36
STATUS_GCODE_G43_DYNAMIC_AXIS_ERROR = 37
STATUS_GCODE_MAX_VALUE_EXCEEDED = 38

ALARM_HARD_LIMIT = 1
ALARM_SOFT_LIMIT = 2
ALARM_ABORT_CYCLE = 3
ALARM_PROBE_FAIL_INITIAL = 4
ALARM_PROBE_FAIL_CONTACT = 5
ALARM_HOMING_FAIL_RESET = 6

RT_STATUS = 0x3F
RT_FEED_HOLD = 0x21
RT_CYCLE_START = 0x7E
RT_RESET = 0x18
RT_JOG_CANCEL = 0x85
RT_SPINDLE_STOP = 0x9E

DEFAULT_SETTINGS: Dict[int, float] = {
    0: 10,
    1: 25,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    10: 1,
    11: 0.010,
    12: 0.002,
    13: 0,
    20: 0,
    21: 0,
    22: 1,
    23: 0,
    24: 25.0,
    25: 500.0,
    26: 250,
    27: 1.0,
    30: 1000,
    31: 0,
    32: 0,
    100: 250.0,
    101: 250.0,
    102: 250.0,
    110: 500.0,
    111: 500.0,
    112: 500.0,
    120: 10.0,
    121: 10.0,
    122: 10.0,
    130: 200.0,
    131: 200.0,
    132: 200.0,
}
FLOAT_SETTINGS = {11, 12, 24, 25, 27, 100, 101, 102, 110, 111, 112, 120, 121, 122, 130, 131, 132}
RPM_SETTINGS = {30, 31}

G_GROUPS = {
    "4": 0,
    "10": 0,
    "28": 0,
    "28.1": 0,
    "30": 0,
    "30.1": 0,
    "53": 0,
    "92": 0,
    "92.1": 0,
    "0": 1,
    "1": 1,
    "2": 1,
    "3": 1,
    "38.2": 1,
    "38.3": 1,
    "38.4": 1,
    "38.5": 1,
    "80": 1,
    "17": 2,
    "18": 2,
    "19": 2,
    "90": 3,
    "91": 3,
    "91.1": 4,
    "93": 5,
    "94": 5,
    "20": 6,
    "21": 6,
    "40": 7,
    "43.1": 8,
    "49": 8,
    "54": 12,
    "55": 12,
    "56": 12,
    "57": 12,
    "58": 12,
    "59": 12,
    "61": 13,
}
M_GROUPS = {"0": 4, "1": 4, "2": 4, "30": 4, "3": 7, "4": 7, "5": 7, "8": 8, "9": 8}
ARC_PLANES = {17: (0, 1, "IJ"), 18: (2, 0, "KI"), 19: (1, 2, "JK")}
NUMBER = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)")
SETTING = re.compile(r"(\d+)=(.*)")
SIM_COMMAND = re.compile(r"(ERROR|ALARM|PROBE):([-+]?(?:\d+\.?\d*|\.\d+))")


def _format_axes(values: Vector) -> str:
    return ",".join(f"{0.0 if abs(v) < 0.0005 else v:.3f}" for v in values)


def _code(value: float) -> str:
    integer = int(value)
    mantissa = round((value - integer) * 100)
    if mantissa == 0:
        return str(integer)
    if mantissa % 10:
        return f"{integer}.{mantissa:02d}"
    return f"{integer}.{mantissa // 10}"


@dataclass
class _ParserState:
    motion: str = "0"
    coord_select: int = 0
    plane: int = 17
    units: int = 21
    distance: int = 90
    feed_mode: int = 94
    spindle: int = 5
    coolant: bool = False
    tool: int = 0
    feed_rate: float = 0.0
    spindle_speed: float = 0.0
    tool_length_offset: float = 0.0
    coord_offset: Vector = field(default_factory=lambda: [0.0, 0.0, 0.0])
    position: Vector = field(default_factory=lambda: [0.0, 0.0, 0.0])


@dataclass
class _Motion:
    start: Vector
    target: Vector
    length: float
    kind: str
    feed_rate: float
    rate_limit: float
    probe_away: bool = False
    probe_no_error: bool = False
    done: float = 0.0

    def position(self, distance: float) -> Vector:
        ratio = min(distance / self.length, 1.0)
        return [s + (t - s) * ratio for s, t in zip(self.start, self.target)]


@dataclass
class _Block:
    state: _ParserState
    sync: bool = False
    motions: List[_Motion] = field(default_factory=list)
    dwell: float = 0.0
    probe: Optional[_Motion] = None
    program_flow: str = ""
    store_coord: Optional[Tuple[int, Vector]] = None
    messages: List[str] = field(default_factory=list)
    action: Optional[Callable[[], None]] = None
    home: bool = False
    jog: bool = False
    wco_change: bool = False
    silent: bool = False


@dataclass
class _Wait:
    kind: str
    seconds: float = 0.0
    motions: List[_Motion] = field(default_factory=list)
    flow: str = ""
    probe_no_error: bool = False
    probe_contact: Optional[Vector] = None


@dataclass
class _Line:
    text: str
    raw_length: int
    overflow: bool = False


class GrblSimulator:
    """GRBL 1.1 controller driven by bytes in and simulated time."""

    VERSION = "1.1h"
    BUILD = "20190830"
    LINE_BUFFER_SIZE = 80
    PLANNER_BLOCKS = 15
    RX_BUFFER_SIZE = 128
    HOLD_DECELERATION_S = 0.2
    BUSY_STATES = ("Run", "Hold", "Jog", "Home")
    WCO_REFRESH = (10, 30)
    OVR_REFRESH = (10, 20)

    def __init__(self, probe_contact_z: float = -5.0) -> None:
        self.settings: Dict[int, float] = dict(DEFAULT_SETTINGS)
        self.coord_data: List[Vector] = [[0.0, 0.0, 0.0] for _ in range(8)]
        self.probe_contact_z = probe_contact_z
        self.rx_overflows = 0
        self.power_cycle()

    def power_cycle(self) -> None:
        """Start as GRBL does after power-up: position lost, settings and offsets kept."""
        self.mpos: Vector = [0.0, 0.0, 0.0]
        self.state = "Idle"
        self._output = bytearray()
        self._reset_volatile()
        self._write_welcome()

    def _reset_volatile(self) -> None:
        self.parser = _ParserState(position=list(self.mpos))
        self.hold_complete = False
        self.spindle_stop_override = False
        self.feed_override = 100
        self.rapid_override = 100
        self.spindle_override = 100
        self.probe_position: Vector = [0.0, 0.0, 0.0]
        self.probe_succeeded = False
        self._planner: Deque[_Motion] = deque()
        self._lines: Deque[_Line] = deque()
        self._partial = ""
        self._partial_raw = 0
        self._partial_flags = ""
        self._partial_overflow = False
        self._wait: Optional[_Wait] = None
        self._decel_left: Optional[float] = None
        self._jog_cancel = False
        self._critical = False
        self._injected_errors: Deque[int] = deque()
        self._wco_counter = 0
        self._ovr_counter = 1

    def _write(self, text: str) -> None:
        self._output += (text + "\r\n").encode()

    def _write_welcome(self) -> None:
        self._output += f"\r\nGrbl {self.VERSION} ['$' for help]\r\n".encode()
        if self.state == "Alarm":
            self._write("[MSG:'$H'|'$X' to unlock]")

    def read_output(self) -> bytes:
        """Return and clear what the controller has sent."""
        data = bytes(self._output)
        self._output.clear()
        return data

    @property
    def wco(self) -> Vector:
        """Work coordinate offset, as GRBL reports it."""
        coord_system = self.coord_data[self.parser.coord_select]
        wco = [c + o for c, o in zip(coord_system, self.parser.coord_offset)]
        wco[2] += self.parser.tool_length_offset
        return wco

    @property
    def wpos(self) -> Vector:
        return [m - w for m, w in zip(self.mpos, self.wco)]

    @property
    def probe_triggered(self) -> bool:
        return self.mpos[2] <= self.probe_contact_z + 1e-9

    @property
    def spindle_running(self) -> bool:
        stopped = self.spindle_stop_override and self.state == "Hold" and self.hold_complete
        return self.parser.spindle in (3, 4) and not stopped

    @property
    def planner_blocks(self) -> int:
        return len(self._planner)

    def inject_error(self, code: int) -> None:
        """Reject the next G-code line with ``error:<code>``."""
        self._injected_errors.append(code)

    def trigger_alarm(self, code: int) -> None:
        """Raise ``ALARM:<code>`` now, as a limit switch or a failure would."""
        self._stop_motion()
        self.state = "Alarm"
        self._write(f"ALARM:{code}")
        if code in (ALARM_HARD_LIMIT, ALARM_SOFT_LIMIT):
            self._write("[MSG:Reset to continue]")
            self._critical = True

    def receive(self, data: bytes) -> None:
        """Handle bytes sent by the host."""
        for byte in data:
            if self._critical and byte != RT_RESET:
                continue
            if byte == RT_STATUS:
                self._write(self.status_report())
            elif byte == RT_FEED_HOLD:
                self.feed_hold()
            elif byte == RT_CYCLE_START:
                self.cycle_start()
            elif byte == RT_RESET:
                self.soft_reset()
            elif byte >= 0x80:
                self._realtime_extended(byte)
            elif byte in (0x0A, 0x0D):
                self._end_line()
                self._service()
            else:
                self._add_char(chr(byte))
        self._service()

    def _rx_buffer_used(self) -> int:
        lines = list(self._lines)
        if lines and self._wait is None and not self._suspended():
            lines = lines[1:]
        return sum(line.raw_length for line in lines) + self._partial_raw

    def _add_char(self, char: str) -> None:
        if self._rx_buffer_used() >= self.RX_BUFFER_SIZE - 1:
            self.rx_overflows += 1
            logger.warning("Simulated GRBL serial buffer full: a character from the host has been lost.")
            return
        self._partial_raw += 1
        if self._partial_flags:
            if char == ")" and self._partial_flags == "(":
                self._partial_flags = ""
        elif char <= " " or char == "/":
            pass
        elif char == "(":
            self._partial_flags = "("
        elif char == ";":
            self._partial_flags = ";"
        elif len(self._partial) >= self.LINE_BUFFER_SIZE - 1:
            self._partial_overflow = True
        else:
            self._partial += char.upper()

    def _end_line(self) -> None:
        self._lines.append(_Line(self._partial, self._partial_raw + 1, self._partial_overflow))
        self._partial = ""
        self._partial_raw = 0
        self._partial_flags = ""
        self._partial_overflow = False

    def _realtime_extended(self, byte: int) -> None:
        if byte == RT_JOG_CANCEL:
            if self.state == "Jog" and self._decel_left is None:
                self._start_deceleration()
        elif byte == RT_SPINDLE_STOP:
            if self.state == "Hold":
                self.spindle_stop_override = not self.spindle_stop_override
        elif 0x90 <= byte <= 0x94:
            steps = {0x90: 100 - self.feed_override, 0x91: 10, 0x92: -10, 0x93: 1, 0x94: -1}
            self._set_overrides(feed=min(max(self.feed_override + steps[byte], 10), 200))
        elif 0x95 <= byte <= 0x97:
            self._set_overrides(rapid={0x95: 100, 0x96: 50, 0x97: 25}[byte])
        elif 0x99 <= byte <= 0x9D:
            steps = {0x99: 100 - self.spindle_override, 0x9A: 10, 0x9B: -10, 0x9C: 1, 0x9D: -1}
            self._set_overrides(spindle=min(max(self.spindle_override + steps[byte], 10), 200))

    def _set_overrides(
        self, feed: Optional[int] = None, rapid: Optional[int] = None, spindle: Optional[int] = None
    ) -> None:
        new = (
            self.feed_override if feed is None else feed,
            self.rapid_override if rapid is None else rapid,
            self.spindle_override if spindle is None else spindle,
        )
        if new != (self.feed_override, self.rapid_override, self.spindle_override):
            self.feed_override, self.rapid_override, self.spindle_override = new
            self._ovr_counter = 0

    def feed_hold(self) -> None:
        """Real-time ``!``."""
        if self.state in ("Run", "Jog"):
            if self._decel_left is None:
                self._start_deceleration()
        elif self.state == "Idle":
            self.state = "Hold"
            self.hold_complete = True

    def _start_deceleration(self) -> None:
        self._decel_left = self.HOLD_DECELERATION_S
        if self.state == "Jog":
            self._jog_cancel = True
        else:
            self.state = "Hold"
            self.hold_complete = False

    def cycle_start(self) -> None:
        """Real-time ``~``: honoured only when idle or when the hold is complete."""
        if self.state != "Hold" or not self.hold_complete:
            return
        self.spindle_stop_override = False
        self.hold_complete = False
        self.state = "Run" if self._planner else "Idle"
        if self._wait is not None and self._wait.kind == "pause":
            self._wait = None
            self._write("ok")
        self._service()

    def soft_reset(self) -> None:
        """Real-time ctrl-x: stop everything, raising ``ALARM:3`` if the machine was moving."""
        moving = self.state in ("Run", "Jog", "Home") or (self.state == "Hold" and not self.hold_complete)
        was_alarm = self.state == "Alarm"
        alarm = None
        if moving:
            alarm = ALARM_HOMING_FAIL_RESET if self.state == "Home" else ALARM_ABORT_CYCLE
        self._reset_volatile()
        if alarm is not None:
            self._write(f"ALARM:{alarm}")
        self.state = "Alarm" if alarm is not None or was_alarm else "Idle"
        self._write_welcome()

    def _stop_motion(self) -> None:
        self._planner.clear()
        self._wait = None
        self._decel_left = None
        self._jog_cancel = False
        self.hold_complete = False
        self.parser.position = list(self.mpos)

    def _suspended(self) -> bool:
        return self.state == "Hold" and self.hold_complete

    def _buffer_empty(self) -> bool:
        return not self._planner and self.state not in ("Run", "Jog", "Home")

    def _service(self) -> None:
        while self._lines and self._wait is None and not self._suspended() and not self._critical:
            line = self._lines[0]
            result = self._interpret_line(line)
            if isinstance(result, int):
                self._lines.popleft()
                self._write("ok" if result == 0 else f"error:{result}")
                continue
            if result.sync and not self._buffer_empty():
                return
            if len(self._planner) + len(result.motions) > self.PLANNER_BLOCKS:
                return
            self._lines.popleft()
            self._commit(result)

    def _interpret_line(self, line: _Line) -> Union[int, _Block]:
        if line.overflow:
            return STATUS_OVERFLOW
        text = line.text
        if not text:
            return 0
        if text.startswith("$"):
            return self._system_line(text)
        if self.state in ("Alarm", "Jog"):
            return STATUS_SYSTEM_GC_LOCK
        if self._injected_errors:
            return self._injected_errors.popleft()
        return self._interpret_gcode(text)

    def _commit(self, block: _Block) -> None:
        if block.store_coord is not None:
            index, values = block.store_coord
            self.coord_data[index] = values
        self.parser = block.state
        if block.wco_change:
            self._wco_counter = 0
        if block.action is not None:
            block.action()
        for message in block.messages:
            self._write(message)
        if block.home:
            self._start_homing()
            return
        if block.dwell > 0:
            self._wait = _Wait("dwell", seconds=block.dwell, motions=block.motions, flow=block.program_flow)
            return
        if block.probe is not None:
            self._start_probe(block.probe)
            return
        self._queue(block.motions, jog=block.jog)
        if block.program_flow:
            self._wait = _Wait("flow", flow=block.program_flow)
            self._check_wait()
            return
        if not block.silent:
            self._write("ok")

    def _queue(self, motions: List[_Motion], jog: bool = False) -> None:
        self._planner.extend(motions)
        if self._planner and self.state == "Idle":
            self.state = "Jog" if jog else "Run"

    def _start_homing(self) -> None:
        target = [-self.settings[27]] * 3
        length = math.dist(self.mpos, target)
        self.state = "Home"
        self._wait = _Wait("home")
        if length > 0:
            rate = self.settings[25]
            self._planner.append(_Motion(list(self.mpos), target, length, "home", rate, rate))
        self._check_wait()

    def _start_probe(self, motion: _Motion) -> None:
        self.probe_succeeded = False
        triggered = self.probe_triggered
        if triggered != motion.probe_away:
            self.state = "Alarm"
            self._write(f"ALARM:{ALARM_PROBE_FAIL_INITIAL}")
            self._write("ok")
            return
        self._wait = _Wait("probe", probe_no_error=motion.probe_no_error)
        self._planner.append(motion)
        self.state = "Run"

    def _check_wait(self) -> None:
        wait = self._wait
        if wait is None:
            return
        if wait.kind == "home" and not self._planner:
            self.mpos = [-self.settings[27]] * 3
            self.parser.position = list(self.mpos)
            self.state = "Idle"
            self._wait = None
            self._write("ok")
        elif wait.kind == "probe" and self._buffer_empty():
            self._wait = None
            self._finish_probe(wait)
        elif wait.kind == "flow" and self._buffer_empty():
            self._wait = None
            self._program_flow(wait.flow)

    def _finish_probe(self, wait: _Wait) -> None:
        self.parser.position = list(self.mpos)
        if wait.probe_contact is not None:
            self.probe_position = wait.probe_contact
            self.probe_succeeded = True
        else:
            self.probe_position = list(self.mpos)
            if not wait.probe_no_error:
                self.state = "Alarm"
                self._write(f"ALARM:{ALARM_PROBE_FAIL_CONTACT}")
        self._write(self._probe_report())
        self._write("ok")

    def _program_flow(self, flow: str) -> None:
        if flow == "pause":
            self.state = "Hold"
            self.hold_complete = True
            self._wait = _Wait("pause")
            return
        position = list(self.parser.position)
        self.parser = _ParserState(
            motion="1",
            tool=self.parser.tool,
            feed_rate=self.parser.feed_rate,
            spindle_speed=self.parser.spindle_speed,
            tool_length_offset=self.parser.tool_length_offset,
            coord_offset=self.parser.coord_offset,
            units=self.parser.units,
            position=position,
        )
        self._wco_counter = 0
        self._write("[MSG:Pgm End]")
        self._write("ok")

    def advance(self, seconds: float) -> None:
        """Let ``seconds`` of simulated time pass."""
        if self._critical:
            return
        remaining = seconds
        while remaining > 1e-9:
            if not self._planner or not self._moving():
                break
            step = remaining if self._decel_left is None else min(remaining, self._decel_left)
            used = self._move(step)
            if self._decel_left is not None:
                self._decel_left -= used
                if self._decel_left <= 1e-9:
                    self._finish_deceleration()
            remaining -= used
        if not self._planner:
            self._cycle_stop()
        self._advance_dwell(seconds)
        self._check_wait()
        self._service()

    def _moving(self) -> bool:
        return self.state in ("Run", "Jog", "Home") or (self.state == "Hold" and not self.hold_complete)

    def _speed(self, motion: _Motion) -> float:
        if motion.kind == "rapid":
            return motion.rate_limit * self.rapid_override / 100
        if motion.kind == "feed":
            return min(motion.feed_rate * self.feed_override / 100, motion.rate_limit)
        return min(motion.feed_rate, motion.rate_limit)

    def _current_rate(self) -> float:
        if self._planner and self._moving():
            return self._speed(self._planner[0])
        return 0.0

    def _move(self, seconds: float) -> float:
        motion = self._planner[0]
        speed = self._speed(motion) / 60
        left = motion.length - motion.done
        used = min(seconds, left / speed)
        travelled = motion.done + speed * used
        position = motion.position(travelled)
        if motion.kind == "probe":
            contact = self._probe_crossing(motion, travelled)
            if contact is not None:
                distance, position = contact
                used = (distance - motion.done) / speed
                motion.done = motion.length
                self.mpos = position
                self._planner.clear()
                if self._wait is not None:
                    self._wait.probe_contact = list(position)
                return max(used, 0.0)
        motion.done = travelled
        self.mpos = position
        if motion.done >= motion.length - 1e-9:
            self.mpos = list(motion.target)
            self._planner.popleft()
        return used

    def _probe_crossing(self, motion: _Motion, travelled: float) -> Optional[Tuple[float, Vector]]:
        z_start = motion.position(motion.done)[2]
        z_end = motion.position(travelled)[2]
        contact_z = self.probe_contact_z
        crosses = z_end <= contact_z < z_start if not motion.probe_away else z_start <= contact_z < z_end
        if not crosses:
            return None
        ratio = (contact_z - z_start) / (z_end - z_start)
        distance = motion.done + (travelled - motion.done) * ratio
        position = motion.position(distance)
        position[2] = contact_z if not motion.probe_away else contact_z + 1e-6
        return distance, position

    def _finish_deceleration(self) -> None:
        self._decel_left = None
        if self._jog_cancel:
            self._jog_cancel = False
            self._planner.clear()
            self.parser.position = list(self.mpos)
            self.state = "Idle"
        else:
            self.hold_complete = True

    def _cycle_stop(self) -> None:
        if self.state in ("Run", "Jog"):
            self.state = "Idle"
            self._decel_left = None
            self._jog_cancel = False
        elif self.state == "Hold" and not self.hold_complete:
            self._decel_left = None
            self.hold_complete = True

    def _advance_dwell(self, seconds: float) -> None:
        wait = self._wait
        if wait is None or wait.kind != "dwell" or self._suspended():
            return
        if not self._buffer_empty():
            return
        wait.seconds -= seconds
        if wait.seconds <= 1e-9:
            self._wait = None
            self._queue(wait.motions)
            if wait.flow:
                self._wait = _Wait("flow", flow=wait.flow)
                self._check_wait()
            else:
                self._write("ok")

    def status_report(self) -> str:
        """The ``<...>`` real-time status report."""
        if self.state == "Hold":
            state = f"Hold:{0 if self.hold_complete else 1}"
        else:
            state = self.state
        busy = self.state in self.BUSY_STATES
        mask = int(self.settings[10])
        if mask & 1:
            fields = [state, f"MPos:{_format_axes(self.mpos)}"]
        else:
            fields = [state, f"WPos:{_format_axes(self.wpos)}"]
        if mask & 2:
            rx_free = self.RX_BUFFER_SIZE - 1 - self._rx_buffer_used()
            fields.append(f"Bf:{self.PLANNER_BLOCKS - len(self._planner)},{rx_free}")
        fields.append(f"FS:{self._current_rate():.0f},{self._spindle_rpm():.0f}")
        if self.probe_triggered:
            fields.append("Pn:P")
        fields += self._refreshed_fields(busy)
        return "<" + "|".join(fields) + ">"

    def _refreshed_fields(self, busy: bool) -> List[str]:
        fields = []
        if self._wco_counter > 0:
            self._wco_counter -= 1
        else:
            self._wco_counter = self.WCO_REFRESH[busy] - 1
            if self._ovr_counter == 0:
                self._ovr_counter = 1
            fields.append(f"WCO:{_format_axes(self.wco)}")
        if self._ovr_counter > 0:
            self._ovr_counter -= 1
        else:
            self._ovr_counter = self.OVR_REFRESH[busy] - 1
            fields.append(f"Ov:{self.feed_override},{self.rapid_override},{self.spindle_override}")
            accessories = ""
            if self.spindle_running:
                accessories += "S" if self.parser.spindle == 3 else "C"
            if self.parser.coolant:
                accessories += "F"
            if accessories:
                fields.append(f"A:{accessories}")
        return fields

    def _spindle_rpm(self) -> float:
        if not self.spindle_running or self.parser.spindle_speed <= 0:
            return 0.0
        rpm = self.parser.spindle_speed * self.spindle_override / 100
        return min(max(rpm, self.settings[31]), self.settings[30])

    def _probe_report(self) -> str:
        return f"[PRB:{_format_axes(self.probe_position)}:{int(self.probe_succeeded)}]"

    def _system_line(self, text: str) -> Union[int, _Block]:
        command = text[1:]
        if command.startswith("SIM="):
            return self._simulator_command(command[4:])
        if command == "":
            return self._message_block(["[HLP:$$ $# $G $I $N $x=val $Nx=line $J=line $SLP $C $X $H ~ ! ? ctrl-x]"])
        if command.startswith("J"):
            if self.state not in ("Idle", "Jog"):
                return STATUS_IDLE_ERROR
            if command[1:2] != "=":
                return STATUS_INVALID_STATEMENT
            return self._interpret_gcode(command[2:], jog=True)
        if command[0] in "$GCX":
            return self._anytime_command(command)
        if self.state not in ("Idle", "Alarm"):
            return STATUS_IDLE_ERROR
        return self._idle_command(command)

    def _anytime_command(self, command: str) -> Union[int, _Block]:
        if len(command) != 1:
            return STATUS_INVALID_STATEMENT
        if command == "$":
            if self.state in ("Run", "Hold"):
                return STATUS_IDLE_ERROR
            return self._message_block(self._settings_report())
        if command == "G":
            return self._message_block([self._gcode_modes_report()])
        if command == "X":
            if self.state != "Alarm":
                return 0
            block = self._message_block(["[MSG:Caution: Unlocked]"])
            block.action = self._unlock
            return block
        return STATUS_INVALID_STATEMENT

    def _idle_command(self, command: str) -> Union[int, _Block]:
        if command == "#":
            return self._message_block(self._parameters_report())
        if command == "H":
            if not self.settings[22]:
                return STATUS_SETTING_DISABLED
            return _Block(state=deepcopy(self.parser), home=True)
        if command == "I":
            return self._message_block([f"[VER:{self.VERSION}.{self.BUILD}:]", "[OPT:V,15,128]"])
        if command == "N":
            return self._message_block(["$N0=", "$N1="])
        return self._store_setting(command)

    def _unlock(self) -> None:
        self.state = "Idle"

    def _message_block(self, messages: List[str]) -> _Block:
        return _Block(state=deepcopy(self.parser), messages=messages)

    def _store_setting(self, command: str) -> Union[int, _Block]:
        match = SETTING.fullmatch(command)
        if match is None:
            return STATUS_BAD_NUMBER_FORMAT if not command[:1].isdigit() else STATUS_INVALID_STATEMENT
        number = int(match.group(1))
        if not NUMBER.fullmatch(match.group(2)):
            return STATUS_BAD_NUMBER_FORMAT
        value = float(match.group(2))
        if value < 0:
            return STATUS_NEGATIVE_VALUE
        if number not in self.settings:
            return STATUS_INVALID_STATEMENT
        block = _Block(state=deepcopy(self.parser))
        block.action = lambda: self.settings.__setitem__(number, value)
        return block

    def _simulator_command(self, command: str) -> Union[int, _Block]:
        match = SIM_COMMAND.fullmatch(command)
        if match is None:
            return STATUS_INVALID_STATEMENT
        name, value = match.group(1), float(match.group(2))
        block = _Block(state=deepcopy(self.parser), silent=True)
        if name == "ERROR":
            block.action = lambda: self.inject_error(int(value))
            block.messages = [f"[MSG:Simulator: the next G-code line gets error:{int(value)}]"]
        elif name == "ALARM":
            block.action = lambda: self.trigger_alarm(int(value))
        else:
            block.action = lambda: setattr(self, "probe_contact_z", value)
            block.messages = [f"[MSG:Simulator: the probe touches at machine Z {value:.3f}]"]
        return block

    def _settings_report(self) -> List[str]:
        lines = []
        for number, value in self.settings.items():
            if number in FLOAT_SETTINGS:
                lines.append(f"${number}={value:.3f}")
            elif number in RPM_SETTINGS:
                lines.append(f"${number}={value:.0f}")
            else:
                lines.append(f"${number}={int(value)}")
        return lines

    def _gcode_modes_report(self) -> str:
        p = self.parser
        modes = [
            f"G{p.motion}",
            f"G{p.coord_select + 54}",
            f"G{p.plane}",
            f"G{p.units}",
            f"G{p.distance}",
            f"G{p.feed_mode}",
            f"M{p.spindle}",
            "M8" if p.coolant else "M9",
        ]
        return f"[GC:{' '.join(modes)} T{p.tool} F{p.feed_rate:.0f} S{p.spindle_speed:.0f}]"

    def _parameters_report(self) -> List[str]:
        names = ["G54", "G55", "G56", "G57", "G58", "G59", "G28", "G30"]
        lines = [f"[{name}:{_format_axes(values)}]" for name, values in zip(names, self.coord_data)]
        lines.append(f"[G92:{_format_axes(self.parser.coord_offset)}]")
        lines.append(f"[TLO:{self.parser.tool_length_offset:.3f}]")
        lines.append(self._probe_report())
        return lines

    def _parse_words(self, text: str) -> Union[int, List[Tuple[str, float]]]:
        words = []
        position = 0
        while position < len(text):
            letter = text[position]
            if not "A" <= letter <= "Z":
                return STATUS_EXPECTED_COMMAND_LETTER
            match = NUMBER.match(text, position + 1)
            if match is None:
                return STATUS_BAD_NUMBER_FORMAT
            words.append((letter, float(match.group())))
            position = match.end()
        return words

    def _interpret_gcode(self, text: str, jog: bool = False) -> Union[int, _Block]:
        words = self._parse_words(text)
        if isinstance(words, int):
            return words
        classified = self._classify_words(words)
        if isinstance(classified, int):
            return classified
        g_codes, m_codes, values = classified
        if jog:
            return self._interpret_jog(g_codes, m_codes, values)
        if values.get("N", 0) > 9999999:
            return STATUS_GCODE_INVALID_LINE_NUMBER
        if values.get("T", 0) > 255:
            return STATUS_GCODE_MAX_VALUE_EXCEEDED
        return self._build_block(g_codes, m_codes, values)

    def _classify_words(
        self, words: List[Tuple[str, float]]
    ) -> Union[int, Tuple[Dict[int, str], Dict[int, str], Dict[str, float]]]:
        g_codes: Dict[int, str] = {}
        m_codes: Dict[int, str] = {}
        values: Dict[str, float] = {}
        for letter, value in words:
            if letter in "GM":
                key = _code(value)
                group = (G_GROUPS if letter == "G" else M_GROUPS).get(key)
                codes = g_codes if letter == "G" else m_codes
                if group is None:
                    return STATUS_GCODE_UNSUPPORTED_COMMAND
                if group in codes:
                    return STATUS_GCODE_MODAL_GROUP_VIOLATION
                codes[group] = key
            elif letter in "FIJKLNPRSTXYZ":
                if letter in values:
                    return STATUS_GCODE_WORD_REPEATED
                if value < 0 and letter in "FNPST":
                    return STATUS_NEGATIVE_VALUE
                values[letter] = value
            else:
                return STATUS_GCODE_UNSUPPORTED_COMMAND
        return g_codes, m_codes, values

    def _interpret_jog(
        self, g_codes: Dict[int, str], m_codes: Dict[int, str], values: Dict[str, float]
    ) -> Union[int, _Block]:
        if m_codes or any(group not in (0, 3, 6) for group in g_codes) or g_codes.get(0, "53") != "53":
            return STATUS_INVALID_JOG_COMMAND
        if "F" not in values:
            return STATUS_GCODE_UNDEFINED_FEED_RATE
        if set(values) - set("XYZFN"):
            return STATUS_GCODE_UNUSED_WORDS
        if not set(values) & set(AXES):
            return STATUS_GCODE_NO_AXIS_WORDS
        jog_state = deepcopy(self.parser)
        if 6 in g_codes:
            jog_state.units = int(g_codes[6])
        if 3 in g_codes:
            jog_state.distance = int(g_codes[3])
        scale = 25.4 if jog_state.units == 20 else 1.0
        target = self._target(values, jog_state, scale, g_codes.get(0) == "53")
        state = deepcopy(self.parser)
        state.position = target
        motion = self._line_motion(self.parser.position, target, "jog", values["F"] * scale)
        return _Block(state=state, motions=[motion] if motion else [], jog=True)

    def _target(self, values: Dict[str, float], state: _ParserState, scale: float, machine: bool) -> Vector:
        coord_system = self.coord_data[state.coord_select]
        target = list(state.position)
        for index, axis in enumerate(AXES):
            if axis not in values:
                continue
            value = values[axis] * scale
            if machine:
                target[index] = value
            elif state.distance == 90:
                target[index] = value + coord_system[index] + state.coord_offset[index]
                if index == 2:
                    target[index] += state.tool_length_offset
            else:
                target[index] = state.position[index] + value
        return target

    def _rate_limit(self, start: Vector, target: Vector, length: float) -> float:
        limit = math.inf
        for index in range(3):
            delta = abs(target[index] - start[index])
            if delta > 1e-12:
                limit = min(limit, self.settings[110 + index] * length / delta)
        return limit

    def _line_motion(
        self, start: Vector, target: Vector, kind: str, feed_rate: float, length: Optional[float] = None
    ) -> Optional[_Motion]:
        chord = math.dist(start, target)
        if chord < 1e-9 and not length:
            return None
        length = length or chord
        limit = self._rate_limit(start, target, chord) if chord > 1e-9 else self.settings[110]
        return _Motion(list(start), list(target), length, kind, feed_rate, limit)

    def _build_block(
        self, g_codes: Dict[int, str], m_codes: Dict[int, str], values: Dict[str, float]
    ) -> Union[int, _Block]:
        state = deepcopy(self.parser)
        block = _Block(state=state)
        scale = self._apply_modal_words(state, block, g_codes, m_codes, values)
        used = set("FNST")
        axis_words = [axis for axis in AXES if axis in values]
        non_modal = g_codes.get(0, "")
        result = self._check_axis_users(g_codes, non_modal, axis_words)
        if not result and non_modal == "4":
            result = self._dwell(values, block, used)
        if not result and 8 in g_codes:
            result = self._tool_length(g_codes[8], state, values, scale, block, used)
        if not result and non_modal:
            result = self._non_modal(non_modal, state, values, scale, block, used)
        if result:
            return result
        self._program_flow_word(m_codes, block)
        if non_modal == "53" and state.motion not in ("0", "1"):
            return STATUS_GCODE_G53_INVALID_MOTION_MODE
        if any(axis not in used for axis in axis_words):
            result = self._motion(state, values, scale, non_modal == "53", block, used)
        elif 1 in g_codes and state.motion.startswith("38"):
            result = STATUS_GCODE_NO_AXIS_WORDS
        if result:
            return result
        if set(values) - used:
            return STATUS_GCODE_UNUSED_WORDS
        return block

    def _apply_modal_words(
        self,
        state: _ParserState,
        block: _Block,
        g_codes: Dict[int, str],
        m_codes: Dict[int, str],
        values: Dict[str, float],
    ) -> float:
        if 6 in g_codes:
            state.units = int(g_codes[6])
        if 5 in g_codes:
            state.feed_mode = int(g_codes[5])
        scale = 25.4 if state.units == 20 else 1.0
        if "F" in values:
            state.feed_rate = values["F"] if state.feed_mode == 93 else values["F"] * scale
        elif state.feed_mode == 93:
            state.feed_rate = 0.0
        self._apply_spindle_words(state, block, m_codes, values)
        for group, name in ((2, "plane"), (3, "distance")):
            if group in g_codes:
                setattr(state, name, int(g_codes[group]))
        state.motion = g_codes.get(1, state.motion)
        if 12 in g_codes:
            state.coord_select = int(g_codes[12]) - 54
            if state.coord_select != self.parser.coord_select:
                block.sync = block.wco_change = True
        return scale

    def _apply_spindle_words(
        self, state: _ParserState, block: _Block, m_codes: Dict[int, str], values: Dict[str, float]
    ) -> None:
        old = self.parser
        state.spindle_speed = values.get("S", state.spindle_speed)
        state.tool = int(values.get("T", state.tool))
        state.spindle = int(m_codes.get(7, state.spindle))
        if 8 in m_codes:
            state.coolant = m_codes[8] == "8"
        speed_change = state.spindle_speed != old.spindle_speed and old.spindle != 5
        if speed_change or state.spindle != old.spindle or state.coolant != old.coolant:
            block.sync = True

    def _check_axis_users(self, g_codes: Dict[int, str], non_modal: str, axis_words: List[str]) -> int:
        axis_users = int(non_modal in ("10", "28", "30", "92")) + int(g_codes.get(8) == "43.1")
        if axis_users > 1 or (axis_users and 1 in g_codes and axis_words):
            return STATUS_GCODE_AXIS_COMMAND_CONFLICT
        return 0

    def _dwell(self, values: Dict[str, float], block: _Block, used: set) -> int:
        if "P" not in values:
            return STATUS_GCODE_VALUE_WORD_MISSING
        block.dwell = values["P"]
        block.sync = True
        used.add("P")
        return 0

    def _tool_length(
        self, code: str, state: _ParserState, values: Dict[str, float], scale: float, block: _Block, used: set
    ) -> int:
        if code == "43.1":
            if [axis for axis in AXES if axis in values] != ["Z"]:
                return STATUS_GCODE_G43_DYNAMIC_AXIS_ERROR
            state.tool_length_offset = values["Z"] * scale
            used.add("Z")
        else:
            state.tool_length_offset = 0.0
        if state.tool_length_offset != self.parser.tool_length_offset:
            block.sync = block.wco_change = True
        return 0

    def _program_flow_word(self, m_codes: Dict[int, str], block: _Block) -> None:
        flow = {"0": "pause", "2": "end", "30": "end"}.get(m_codes.get(4, ""), "")
        if flow:
            block.program_flow = flow
            block.sync = True

    def _non_modal(
        self, command: str, state: _ParserState, values: Dict[str, float], scale: float, block: _Block, used: set
    ) -> int:
        if command in ("10", "28", "30", "92"):
            used.update(axis for axis in AXES if axis in values)
        if command == "10":
            return self._set_coordinate_data(state, values, scale, block, used)
        if command == "92":
            return self._set_coordinate_offset(state, values, scale, block)
        if command in ("28", "30"):
            self._go_predefined_position(command, state, values, scale, block)
        elif command in ("28.1", "30.1"):
            block.store_coord = (6 if command == "28.1" else 7, list(state.position))
            block.sync = True
        elif command == "92.1":
            state.coord_offset = [0.0, 0.0, 0.0]
            block.sync = block.wco_change = True
        return 0

    def _set_coordinate_data(
        self, state: _ParserState, values: Dict[str, float], scale: float, block: _Block, used: set
    ) -> int:
        if "L" not in values or "P" not in values:
            return STATUS_GCODE_VALUE_WORD_MISSING
        if values["L"] not in (2, 20):
            return STATUS_GCODE_UNSUPPORTED_COMMAND
        if values["P"] != int(values["P"]) or not 0 <= values["P"] <= 6:
            return STATUS_GCODE_UNSUPPORTED_COORD_SYS
        index = state.coord_select if values["P"] == 0 else int(values["P"]) - 1
        coord = list(self.coord_data[index])
        for axis_index, axis in enumerate(AXES):
            if axis in values:
                value = values[axis] * scale
                if values["L"] == 20:
                    value = state.position[axis_index] - state.coord_offset[axis_index] - value
                    value -= state.tool_length_offset if axis_index == 2 else 0.0
                coord[axis_index] = value
        block.store_coord = (index, coord)
        block.sync = True
        block.wco_change = index == state.coord_select
        used.update("LP")
        return 0

    def _set_coordinate_offset(self, state: _ParserState, values: Dict[str, float], scale: float, block: _Block) -> int:
        if not any(axis in values for axis in AXES):
            return STATUS_GCODE_NO_AXIS_WORDS
        coord_system = self.coord_data[state.coord_select]
        for axis_index, axis in enumerate(AXES):
            if axis in values:
                offset = state.position[axis_index] - coord_system[axis_index] - values[axis] * scale
                offset -= state.tool_length_offset if axis_index == 2 else 0.0
                state.coord_offset[axis_index] = offset
        block.sync = block.wco_change = True
        return 0

    def _go_predefined_position(
        self, command: str, state: _ParserState, values: Dict[str, float], scale: float, block: _Block
    ) -> None:
        stored = list(self.coord_data[6 if command == "28" else 7])
        points = [stored]
        if any(axis in values for axis in AXES):
            points.insert(0, self._target(values, state, scale, False))
        start = list(state.position)
        for point in points:
            motion = self._line_motion(start, point, "rapid", 0.0)
            if motion:
                block.motions.append(motion)
            start = point
        state.position = stored

    def _motion(
        self, state: _ParserState, values: Dict[str, float], scale: float, machine: bool, block: _Block, used: set
    ) -> int:
        motion_mode = state.motion
        if motion_mode == "80":
            return STATUS_GCODE_AXIS_WORDS_EXIST
        used.update(AXES)
        if motion_mode != "0" and (state.feed_rate <= 0 or (state.feed_mode == 93 and "F" not in values)):
            return STATUS_GCODE_UNDEFINED_FEED_RATE
        start = list(state.position)
        target = self._target(values, state, scale, machine)
        length = None
        if motion_mode in ("2", "3"):
            arc = self._arc_length(state, values, scale, start, target, motion_mode == "2")
            if isinstance(arc, int):
                return arc
            length = arc
            used.update("IJKR")
        feed_rate = state.feed_rate
        if state.feed_mode == 93:
            feed_rate = (length or math.dist(start, target)) * state.feed_rate
        state.position = target
        if motion_mode.startswith("38"):
            return self._probe_motion(start, target, motion_mode, feed_rate, block)
        motion = self._line_motion(start, target, "rapid" if motion_mode == "0" else "feed", feed_rate, length)
        if motion:
            block.motions.append(motion)
        return 0

    def _probe_motion(self, start: Vector, target: Vector, motion_mode: str, feed_rate: float, block: _Block) -> int:
        motion = self._line_motion(start, target, "probe", feed_rate)
        if motion is None:
            return STATUS_GCODE_INVALID_TARGET
        motion.probe_away = motion_mode in ("38.4", "38.5")
        motion.probe_no_error = motion_mode in ("38.3", "38.5")
        block.probe = motion
        block.sync = True
        return 0

    def _arc_length(
        self,
        state: _ParserState,
        values: Dict[str, float],
        scale: float,
        start: Vector,
        target: Vector,
        clockwise: bool,
    ) -> Union[int, float]:
        axis_0, axis_1, offset_letters = ARC_PLANES[state.plane]
        dx = target[axis_0] - start[axis_0]
        dy = target[axis_1] - start[axis_1]
        linear = target[3 - axis_0 - axis_1] - start[3 - axis_0 - axis_1]
        if "R" in values:
            radius = abs(values["R"] * scale)
            chord = math.hypot(dx, dy)
            if radius < 1e-9 or chord < 1e-9 or chord > 2 * radius + 1e-6:
                return STATUS_GCODE_INVALID_TARGET
            angle = 2 * math.asin(min(chord / (2 * radius), 1.0))
            if values["R"] < 0:
                angle = 2 * math.pi - angle
        else:
            if not any(letter in values for letter in offset_letters):
                return STATUS_GCODE_NO_OFFSETS_IN_PLANE
            i = values.get(offset_letters[0], 0.0) * scale
            j = values.get(offset_letters[1], 0.0) * scale
            radius = math.hypot(i, j)
            end_radius = math.hypot(dx - i, dy - j)
            if abs(end_radius - radius) > 0.005 and abs(end_radius - radius) > 0.001 * radius:
                return STATUS_GCODE_INVALID_TARGET
            start_angle = math.atan2(-j, -i)
            end_angle = math.atan2(dy - j, dx - i)
            angle = end_angle - start_angle
            if clockwise and angle >= -1e-9:
                angle -= 2 * math.pi
            elif not clockwise and angle <= 1e-9:
                angle += 2 * math.pi
            angle = abs(angle)
        return math.hypot(radius * angle, linear)


class SimulatedSerialPort(QObject):
    """The part of ``QSerialPort`` used by ``SerialWorker``, connected to a ``GrblSimulator``."""

    readyRead = Signal()
    errorOccurred = Signal(QSerialPort.SerialPortError)
    TICK_MS = 20

    def __init__(self, parent: Optional[QObject] = None, speed: float = 1.0) -> None:
        super().__init__(parent)
        self.simulator = GrblSimulator()
        self.speed = speed
        self._port_name = SIMULATOR_PORT_NAME
        self._baud_rate = 115200
        self._is_open = False
        self._buffer = bytearray()
        self._notify_pending = False
        self._clock = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setInterval(self.TICK_MS)
        self._timer.timeout.connect(self._tick)

    def setPortName(self, name: str) -> None:
        self._port_name = name

    def portName(self) -> str:
        return self._port_name

    def setBaudRate(self, baud_rate: int) -> bool:
        self._baud_rate = baud_rate
        return True

    def baudRate(self) -> int:
        return self._baud_rate

    def open(self, mode: object) -> bool:
        """Open the port: like an Arduino, the controller restarts on connection."""
        self._is_open = True
        self._buffer.clear()
        self.simulator.power_cycle()
        self._clock.start()
        self._timer.start()
        self._collect()
        logger.info(f"GRBL simulator connected, running at {self.speed:g}x speed.")
        return True

    def isOpen(self) -> bool:
        return self._is_open

    def close(self) -> None:
        self._timer.stop()
        self._is_open = False

    def write(self, data: bytes) -> int:
        if not self._is_open:
            return -1
        payload = bytes(data)
        self.simulator.receive(payload)
        self._collect()
        return len(payload)

    def waitForBytesWritten(self, msecs: int = 30000) -> bool:
        return self._is_open

    def flush(self) -> bool:
        return self._is_open

    def canReadLine(self) -> bool:
        return b"\n" in self._buffer

    def bytesAvailable(self) -> int:
        return len(self._buffer)

    def readAll(self) -> QByteArray:
        data = QByteArray(bytes(self._buffer))
        self._buffer.clear()
        return data

    def error(self) -> QSerialPort.SerialPortError:
        return QSerialPort.SerialPortError.NoError

    def errorString(self) -> str:
        return "No error"

    def _tick(self) -> None:
        elapsed = self._clock.restart() / 1000.0
        self.simulator.advance(elapsed * self.speed)
        self._collect()

    def _collect(self) -> None:
        output = self.simulator.read_output()
        if output:
            self._buffer += output
            if not self._notify_pending:
                self._notify_pending = True
                QTimer.singleShot(0, self._notify)

    def _notify(self) -> None:
        self._notify_pending = False
        if self._buffer:
            self.readyRead.emit()
