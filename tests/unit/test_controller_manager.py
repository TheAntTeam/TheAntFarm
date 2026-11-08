"""Tests for the macro start flow of the controller worker.

A tool change must start only when the machine has executed every previously
streamed line, and a macro that cannot run must stop the job instead of being
silently skipped (the tool length offset would be wrong).
"""

import queue
from typing import Any, List, Optional, Tuple
from unittest.mock import MagicMock

import pytest
from PySide6.QtTest import QTest


@pytest.fixture
def settings():
    settings = MagicMock()
    settings.local_path = ""
    machine = MagicMock()
    machine.tool_probe_rel_flag = True
    machine.tool_probe_offset_x_wpos = 10.0
    machine.tool_probe_offset_y_wpos = 20.0
    machine.tool_probe_offset_z_wpos = -5.0
    machine.tool_probe_offset_x_mpos = 10.0
    machine.tool_probe_offset_y_mpos = 20.0
    machine.tool_probe_offset_z_mpos = -5.0
    machine.tool_change_offset_x_mpos = -41.2
    machine.tool_change_offset_y_mpos = -120.88
    machine.tool_change_offset_z_mpos = -1.0
    machine.tool_probe_z_limit = -11.0
    machine.feedrate_xy = 300.0
    machine.feedrate_z = 80.0
    machine.feedrate_probe = 50.0
    machine.hold_on_probe_flag = False
    machine.zeroing_after_probe_flag = False
    machine.safe_z = -1.0
    machine.tool_change_mode = "wcs"
    machine.tool_setter_x = -200.0
    machine.tool_setter_y = -150.0
    machine.tool_setter_rel_flag = False
    machine.tool_probe_backoff = 1.5
    machine.spindle_stop_dwell = 1.0
    settings.machine_settings = machine
    return settings


@pytest.fixture
def worker(settings, qapp):
    # imported here on purpose: importing the controller package at collection
    # time changes the import order that test_controller_align relies on
    from controller.controller_manager import ControllerWorker

    return ControllerWorker(queue.Queue(), queue.Queue(), settings)


def _start_macro(worker):
    """Put the worker in the state where the next file line is processed."""
    worker.ack_lines = worker.sent_lines = 0
    worker.tot_lines = 10
    return worker.macro_check("M6")


class TestMacroStart:
    def test_regular_line_is_returned_unchanged(self, worker):
        assert worker.macro_check("G21") == "G21"
        assert worker.macro_on is False

    def test_macro_waits_for_the_machine_to_be_idle(self, worker):
        """The M6 line must not be consumed while unacked lines are pending."""
        worker.ack_lines = 1
        worker.sent_lines = 3

        assert worker.macro_check("M6") is None
        assert worker.macro_on is False
        assert worker.wait_tag_decoding is True

    def test_macro_starts_when_the_machine_is_idle(self, worker):
        assert _start_macro(worker) == "$#\n"
        assert worker.macro_on is True
        assert worker.macro_obj is not None
        assert worker.macro_obj.ok is True
        assert worker.wait_tag_decoding is False
        # the $# line is sent in addition to the file lines
        assert worker.tot_lines == 11

    def test_macro_lines_are_streamed_and_the_file_goes_on(self, worker):
        _start_macro(worker)

        first_line = worker.get_next_macro_line()
        assert first_line.rstrip("\n") == "(The Ant Tool Change)"

        worker.macro_obj.id = len(worker.macro_obj.macro_lines)
        assert worker.get_next_macro_line() is None
        assert worker.job_aborted is False


class TestBrokenMacro:
    @pytest.fixture
    def broken_macro_folder(self, tmp_path):
        macros = tmp_path / "macros"
        macros.mkdir()
        (macros / "tool_change_wcs.gcode").write_text("G01 Z@NOT_A_TAG@\n", encoding="utf-8")
        return tmp_path

    def test_broken_template_aborts_the_job(self, worker, broken_macro_folder):
        worker.settings.local_path = str(broken_macro_folder)
        messages = []
        worker.update_console_text_s.connect(messages.append)

        assert _start_macro(worker) is None

        assert worker.job_aborted is True
        assert worker.macro_on is False
        assert worker.macro_obj is None
        assert worker.sending_file is False
        assert messages and "NOT_A_TAG" in messages[-1]

    def test_no_macro_line_is_streamed_after_the_abort(self, worker, broken_macro_folder):
        worker.settings.local_path = str(broken_macro_folder)
        _start_macro(worker)

        assert worker.get_next_macro_line() is None
        assert worker.job_aborted is True

    def test_unresolvable_line_mid_macro_aborts_the_job(self, worker):
        _start_macro(worker)
        worker.macro_obj.macro_lines = ["G01 Z@NOT_A_TAG@"]
        worker.macro_obj.id = 0

        assert worker.get_next_macro_line() is None
        assert worker.job_aborted is True
        assert worker.macro_on is False

    def test_file_streaming_stops_when_the_macro_is_broken(self, worker, broken_macro_folder, qapp):
        worker.settings.local_path = str(broken_macro_folder)
        worker.send_gcode_lines(["G21", "M6", "G00 X10"])

        # the first line is streamed and the machine acknowledges it
        assert worker.serialTxQueue.qsize() == 1
        assert worker.job_aborted is False

        worker.serialRxQueue.put("ok\n")
        worker.parse_rx_queue()

        # the M6 line is reached, the macro cannot start and the job is stopped
        assert worker.job_aborted is True
        assert worker.sending_file is False
        assert worker.content_line == 1  # the M6 line has not been consumed
        assert worker.serialTxQueue.qsize() == 1  # nothing else has been queued


JOB = [
    "G21\n",
    "M3 S1000.0\n",
    "G0 X1.000 Y1.000 Z1.000\n",
    "G1 F100.0\n",
    "G1 X1.000 Y1.000 Z-0.100\n",
    "G1 F300.0\n",
    "G1 X2.000 Y1.000 Z-0.100\n",
    "G1 X2.000 Y2.000 Z-0.100\n",
    "G1 X3.000 Y2.000 Z-0.100\n",
    "G1 X3.000 Y3.000 Z-0.100\n",
    "G1 X4.000 Y3.000 Z-0.100\n",
    "G1 X4.000 Y4.000 Z-0.100\n",
    "G0 X4.000 Y4.000 Z1.000\n",
    "M5\n",
]
FEED_HOLD = b"!"
CYCLE_START = b"~"
SOFT_RESET = b"\030"
SPINDLE_STOP_TOGGLE = b"\x9e"
STATUS_LINE = "<{}|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>\n"


def _wait_for_cycle_start(rig: "StreamRig", timeout_ms: int = 2000) -> None:
    """Process events until the delayed cycle start of a resume is sent."""
    waited = 0
    while CYCLE_START not in rig.realtime and waited < timeout_ms:
        QTest.qWait(5)
        waited += 5


class StreamRig:
    """Drive the real streaming code with the responses of the machine."""

    def __init__(self, worker: Any, lines: Optional[List[str]] = None) -> None:
        self.worker = worker
        self.stops: List[int] = []
        self.console: List[str] = []
        self.prompts: List[Tuple[str, str]] = []
        self.realtime: List[bytes] = []
        worker.stop_send_s.connect(lambda: self.stops.append(1))
        worker.update_console_text_s.connect(self.console.append)
        worker.line_rejected_s.connect(lambda error, line: self.prompts.append((error, line)))
        worker.serial_send_s.connect(self.realtime.append)
        if lines is not None:
            worker.send_gcode_lines(list(lines))

    def feed(self, *responses: str) -> None:
        for response in responses:
            self.worker.serialRxQueue.put(response)
            self.worker.parse_rx_queue()

    def run_until_line(self, line_index: int) -> None:
        self.feed(*["ok\n"] * line_index)

    def status(self, state: str) -> None:
        self.feed(STATUS_LINE.format(state))

    def hold_and_prompt(self, line_index: int = 7) -> None:
        self.run_until_line(line_index)
        self.feed("error:20\n")
        self.status("Hold:0")

    def sent(self) -> List[str]:
        lines = []
        while not self.worker.serialTxQueue.empty():
            lines.append(self.worker.serialTxQueue.get())
        return lines


class TestRejectedLine:
    """A line rejected by the machine holds the job until the user decides."""

    @pytest.mark.parametrize("line_index", range(len(JOB)))
    def test_any_line_holds_the_machine(self, worker, line_index):
        rig = StreamRig(worker, JOB)
        rig.run_until_line(line_index)

        rig.feed("error:20\n")

        assert rig.realtime == [FEED_HOLD]
        assert rig.sent()[-1] == JOB[line_index]
        assert worker.sending_file is True
        assert worker.job_aborted is False
        assert rig.stops == []

    def test_prompt_and_spindle_stop_wait_for_the_end_of_the_hold(self, worker):
        rig = StreamRig(worker, JOB)
        rig.run_until_line(7)
        rig.feed("error:20\n")

        rig.status("Hold:1")
        assert rig.prompts == []
        assert rig.realtime == [FEED_HOLD]

        rig.status("Hold:0")
        assert rig.prompts == [("error:20", JOB[7].strip())]
        assert rig.realtime == [FEED_HOLD, SPINDLE_STOP_TOGGLE]

    def test_spindle_toggle_is_sent_only_once(self, worker):
        rig = StreamRig(worker, JOB)
        rig.hold_and_prompt()

        rig.status("Hold:0")
        rig.status("Hold:0")

        assert rig.realtime == [FEED_HOLD, SPINDLE_STOP_TOGGLE]
        assert len(rig.prompts) == 1

    def test_ok_during_the_hold_does_not_advance_the_job(self, worker):
        rig = StreamRig(worker, JOB)
        rig.hold_and_prompt()
        rig.sent()

        rig.feed("ok\n", "error:20\n")

        assert rig.sent() == []
        assert rig.realtime == [FEED_HOLD, SPINDLE_STOP_TOGGLE]

    def test_error_without_a_job_changes_nothing(self, worker):
        rig = StreamRig(worker)

        rig.feed("error:20\n")

        assert rig.realtime == []
        assert worker.job_aborted is False
        assert rig.stops == []

    def test_locked_machine_stops_the_job(self, worker):
        rig = StreamRig(worker, JOB)
        rig.run_until_line(7)

        rig.feed("error:9\n")

        assert worker.job_aborted is True
        assert rig.stops == [1]
        assert rig.realtime == []

    def test_rejected_macro_line_stops_the_job(self, worker):
        rig = StreamRig(worker, ["G21\n", "M6\n", "G1 X1.000 Y1.000 Z-0.100\n"])
        rig.feed("ok\n")
        assert rig.sent()[-1] == "$#\n"

        rig.feed("error:20\n")

        assert worker.job_aborted is True
        assert worker.macro_on is False
        assert rig.stops == [1]

    def test_pause_button_cannot_release_the_hold(self, worker):
        rig = StreamRig(worker, JOB)
        rig.run_until_line(7)
        rig.feed("error:20\n")
        rig.status("Hold:1")

        worker.pause_resume()

        assert rig.realtime == [FEED_HOLD]

    def test_alarm_during_the_hold_stops_the_job(self, worker):
        rig = StreamRig(worker, JOB)
        rig.hold_and_prompt()

        rig.feed("ALARM:1\n")

        assert worker.job_aborted is True
        assert worker.rejected_line_pending is False
        assert rig.stops == [1]

    def test_disconnection_clears_the_hold(self, worker):
        worker.poll_timer = MagicMock()
        rig = StreamRig(worker, JOB)
        rig.hold_and_prompt()

        worker.on_controller_connection(False)

        assert worker.rejected_line_pending is False


class TestResumeAfterRejectedLine:
    @pytest.fixture
    def rig(self, worker):
        worker.SPINDLE_RESTART_DELAY_MS = 1
        rig = StreamRig(worker, JOB)
        rig.hold_and_prompt()
        return rig

    def test_spindle_restarts_before_any_motion(self, worker, rig):
        rig.sent()
        worker.SPINDLE_RESTART_DELAY_MS = 60000

        worker.resume_after_rejected_line()

        assert rig.realtime == [FEED_HOLD, SPINDLE_STOP_TOGGLE, SPINDLE_STOP_TOGGLE]
        assert rig.sent() == []

    def test_job_continues_without_the_rejected_line(self, worker, rig):
        rig.sent()

        worker.resume_after_rejected_line()
        _wait_for_cycle_start(rig)

        assert rig.realtime == [FEED_HOLD, SPINDLE_STOP_TOGGLE, SPINDLE_STOP_TOGGLE, CYCLE_START]
        assert rig.sent() == [JOB[8]]
        assert worker.rejected_line_pending is False

    def test_job_finishes_after_resuming(self, worker, rig):
        worker.resume_after_rejected_line()
        _wait_for_cycle_start(rig)

        rig.feed(*["ok\n"] * (len(JOB) - 8))
        rig.status("Idle")

        assert rig.sent() == JOB
        assert rig.stops == [1]
        assert worker.job_aborted is False

    def test_rejected_last_line_ends_the_job_after_resuming(self, worker):
        worker.SPINDLE_RESTART_DELAY_MS = 1
        rig = StreamRig(worker, JOB)
        rig.hold_and_prompt(len(JOB) - 1)

        worker.resume_after_rejected_line()
        _wait_for_cycle_start(rig)
        rig.status("Idle")

        assert rig.stops == [1]

    def test_resume_is_ignored_before_the_prompt(self, worker):
        rig = StreamRig(worker, JOB)
        rig.run_until_line(7)
        rig.feed("error:20\n")

        worker.resume_after_rejected_line()

        assert rig.realtime == [FEED_HOLD]

    def test_second_resume_is_ignored(self, worker, rig):
        worker.resume_after_rejected_line()
        worker.resume_after_rejected_line()
        _wait_for_cycle_start(rig)

        assert rig.realtime.count(SPINDLE_STOP_TOGGLE) == 2
        assert rig.realtime.count(CYCLE_START) == 1

    def test_stop_during_the_spindle_restart_cancels_the_resume(self, worker, rig):
        rig.sent()
        worker.resume_after_rejected_line()

        worker.stop_gcode_file()
        QTest.qWait(20)

        assert CYCLE_START not in rig.realtime
        assert rig.sent() == []
        assert worker.rejected_line_pending is False

    def test_stop_from_the_prompt_resets_the_machine(self, worker, rig):
        worker.stop_gcode_file()

        assert rig.realtime[-2:] == [FEED_HOLD, SOFT_RESET]
        assert worker.rejected_line_pending is False
        assert worker.buffered_cmds == []
        assert worker.cmds_to_ack == 0


class TestAlarm:
    def test_alarm_always_resets_the_machine(self, worker):
        rig = StreamRig(worker)
        worker.send_soft_reset = False
        worker.send_gcode_lines(["G21\n", "M3 S1000.0\n"])

        rig.feed("ALARM:1\n")
        worker.stop_gcode_file()

        assert rig.realtime == [FEED_HOLD, SOFT_RESET]

    def test_alarm_during_the_job_stops_it(self, worker):
        rig = StreamRig(worker, JOB)
        rig.run_until_line(7)

        rig.feed("ALARM:1\n")

        assert worker.job_aborted is True
        assert worker.sending_file is False
        assert rig.stops == [1]
        assert any("ALARM:1" in message and "job stopped" in message.lower() for message in rig.console)

    def test_alarm_while_waiting_for_the_last_moves_stops_the_job(self, worker):
        rig = StreamRig(worker, JOB)
        rig.feed(*["ok\n"] * len(JOB))
        assert worker.eof_wait_for_idle is True

        rig.feed("ALARM:1\n")

        assert worker.eof_wait_for_idle is False
        assert rig.stops == [1]

    def test_alarm_without_a_job_changes_nothing(self, worker):
        rig = StreamRig(worker)

        rig.feed("ALARM:1\n")

        assert worker.job_aborted is False
        assert rig.stops == []
        assert "ALARM:1\n" in rig.console


class TestLineTooLong:
    LONG_LINE = "G1 X1 ; " + "c" * 130 + "\n"

    def test_job_is_refused_before_anything_is_sent(self, worker):
        rig = StreamRig(worker, ["G21\n", self.LONG_LINE, "M5\n"])

        assert rig.sent() == []
        assert worker.sending_file is False
        assert rig.stops == [1]
        assert any("Line 2" in message for message in rig.console)

    def test_refused_job_does_not_reset_the_machine(self, worker, qapp):
        rig = StreamRig(worker)

        worker.send_gcode_lines([self.LONG_LINE])
        worker.stop_gcode_file()

        assert rig.realtime == []
        assert rig.stops == [1]
        assert worker.send_soft_reset is True


class TestToolChangeSettings:
    """The tool change procedure settings reach the macro configuration."""

    def test_update_gerber_cfg_passes_the_procedure_settings(self, worker):
        settings = worker.settings.machine_settings
        settings.safe_z = 12.5
        settings.tool_change_mode = "setter"
        settings.tool_setter_x = -200.0
        settings.tool_setter_y = -150.5
        settings.tool_setter_rel_flag = False
        settings.tool_probe_backoff = 2.0
        settings.spindle_stop_dwell = 3.0

        worker.update_gerber_cfg()

        cfg = worker.gcr.cfg
        assert cfg["safe_pos"] == (0.0, 0.0, 12.5)
        assert cfg["tool_change_mode"] == "setter"
        assert cfg["tool_setter_pos"] == (-200.0, -150.5)
        assert cfg["tool_setter_working"] is False
        assert cfg["tool_probe_backoff"] == 2.0
        assert cfg["spindle_stop_dwell"] == 3.0

    def test_the_macro_configuration_matches_the_settings(self, worker):
        settings = worker.settings.machine_settings
        settings.tool_change_mode = "tlo"
        settings.safe_z = 5.0

        worker.update_gerber_cfg()

        assert worker.gcr.macro.get_mode("M6") == "tlo"
        assert worker.gcr.macro.cfg["safe_pos"] == (0.0, 0.0, 5.0)

    def test_an_invalid_mode_is_rejected_by_the_macro(self, worker):
        from shape_core.macros_manager import MacroError

        worker.settings.machine_settings.tool_change_mode = "not_a_mode"
        worker.update_gerber_cfg()

        with pytest.raises(MacroError, match="available modes"):
            worker.gcr.macro.get_macro_string("M6")
