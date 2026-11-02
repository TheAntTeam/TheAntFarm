"""Tests for the macro start flow of the controller worker.

A tool change must start only when the machine has executed every previously
streamed line, and a macro that cannot run must stop the job instead of being
silently skipped (the tool length offset would be wrong).
"""

import queue
from unittest.mock import MagicMock

import pytest


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
