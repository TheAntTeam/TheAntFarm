"""Tests for the simulated GRBL 1.1 controller."""

from queue import Queue
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QIODevice

from TheAntFarm.grbl_simulator import SIMULATOR_PORT_NAME, GrblSimulator, SimulatedSerialPort


@pytest.fixture
def sim():
    simulator = GrblSimulator()
    simulator.read_output()
    return simulator


def send(sim, data, seconds=0.0):
    sim.receive(data.encode() if isinstance(data, str) else data)
    if seconds:
        sim.advance(seconds)
    return sim.read_output().decode().splitlines()


def status(sim):
    return send(sim, "?")[-1]


class TestStartup:
    def test_power_up_prints_the_welcome_message(self):
        simulator = GrblSimulator()

        assert simulator.read_output() == b"\r\nGrbl 1.1h ['$' for help]\r\n"

    def test_first_report_has_the_offsets_and_the_next_the_overrides(self, sim):
        assert status(sim) == "<Idle|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>"
        assert status(sim) == "<Idle|MPos:0.000,0.000,0.000|FS:0,0|Ov:100,100,100>"
        assert status(sim) == "<Idle|MPos:0.000,0.000,0.000|FS:0,0>"

    def test_status_reports_work_position_when_asked(self, sim):
        send(sim, "$10=0\n")
        send(sim, "G10 L2 P1 X5\n")

        assert status(sim).startswith("<Idle|WPos:-5.000,0.000,0.000|")


class TestOkTiming:
    def test_ok_is_sent_when_the_line_is_queued_not_executed(self, sim):
        assert send(sim, "G0 X10\n") == ["ok"]
        assert status(sim).startswith("<Run|")
        assert sim.mpos == [0.0, 0.0, 0.0]

    def test_motion_runs_at_the_axis_limit(self, sim):
        send(sim, "G0 X10\n")

        sim.advance(0.6)

        assert status(sim).startswith("<Run|MPos:5.000,0.000,0.000|FS:500,0")
        sim.advance(1.0)
        assert status(sim).startswith("<Idle|MPos:10.000,0.000,0.000|FS:0,0")

    def test_ok_is_withheld_while_the_planner_is_full(self, sim):
        moves = "".join(f"G1 X{i + 1} F500\n" for i in range(17))

        assert send(sim, moves) == ["ok"] * GrblSimulator.PLANNER_BLOCKS
        assert send(sim, "", 0.13) == ["ok"]

    def test_empty_line_and_comment_get_ok(self, sim):
        assert send(sim, "\n(only a comment)\n") == ["ok", "ok"]


class TestErrors:
    @pytest.mark.parametrize(
        "line,code",
        [
            ("G5", 20),
            ("M6", 20),
            ("G1 X1", 22),
            ("G0 G1 X1", 21),
            ("G0 X1 X2", 25),
            ("G4", 28),
            ("G92", 26),
            ("G43.1 X1", 37),
            ("G10 L20 P9 X0", 29),
            ("G80 X1", 31),
            ("G0 P1 X1", 36),
            ("X1.2.3", 1),
            ("X", 2),
            ("$ABC", 2),
            ("$999=1", 3),
        ],
    )
    def test_invalid_line_is_rejected(self, sim, line, code):
        assert send(sim, line + "\n") == [f"error:{code}"]

    def test_line_longer_than_the_line_buffer_overflows(self, sim):
        assert send(sim, "G0 X" + "1" * 80 + "\n") == ["error:11"]

    def test_spaces_do_not_count_in_the_line_buffer(self, sim):
        assert send(sim, "G0" + " " * 100 + "X1\n") == ["ok"]

    def test_parameters_are_refused_while_moving(self, sim):
        send(sim, "G0 X10\n")

        assert send(sim, "$#\n") == ["error:8"]
        sim.advance(2.0)
        assert send(sim, "$#\n")[-1] == "ok"


class TestFeedHold:
    def test_hold_decelerates_then_completes(self, sim):
        send(sim, "G0 X10\n", 0.5)

        send(sim, "!")
        assert status(sim).startswith("<Hold:1|")
        sim.advance(GrblSimulator.HOLD_DECELERATION_S)
        assert status(sim).startswith("<Hold:0|")

    def test_hold_from_idle_completes_at_once(self, sim):
        send(sim, "!")

        assert status(sim).startswith("<Hold:0|")

    def test_cycle_start_is_ignored_while_decelerating(self, sim):
        send(sim, "G0 X10\n", 0.5)
        send(sim, "!~")

        sim.advance(GrblSimulator.HOLD_DECELERATION_S)

        assert status(sim).startswith("<Hold:0|")

    def test_no_line_is_read_while_the_hold_is_complete(self, sim):
        send(sim, "G0 X10\n", 0.5)
        send(sim, "!", GrblSimulator.HOLD_DECELERATION_S)
        position = list(sim.mpos)

        assert send(sim, "G0 X20\n", 1.0) == []
        assert sim.mpos == position
        assert send(sim, "~") == ["ok"]
        assert status(sim).startswith("<Run|")


class TestSpindleStop:
    def test_spindle_stop_is_ignored_out_of_hold(self, sim):
        send(sim, "M3 S500\n\x9e")

        assert sim.spindle_running

    def test_spindle_stops_in_hold_and_restarts_with_cycle_start(self, sim):
        send(sim, "M3 S500\nG1 X10 F300\n", 0.5)
        send(sim, "!\x9e", GrblSimulator.HOLD_DECELERATION_S)

        assert not sim.spindle_running
        assert "FS:0,0" in status(sim)
        send(sim, "~")
        assert sim.spindle_running
        assert "FS:300,500" in status(sim)


class TestSoftReset:
    def test_reset_while_moving_raises_alarm_3(self, sim):
        send(sim, "G0 X10\n", 0.5)

        assert send(sim, "\x18") == ["ALARM:3", "", "Grbl 1.1h ['$' for help]", "[MSG:'$H'|'$X' to unlock]"]
        assert status(sim).startswith("<Alarm|")
        assert send(sim, "G0 X0\n") == ["error:9"]
        assert send(sim, "$X\n") == ["[MSG:Caution: Unlocked]", "ok"]
        assert status(sim).startswith("<Idle|")

    def test_reset_after_a_complete_hold_raises_no_alarm(self, sim):
        send(sim, "G0 X10\n", 0.5)
        send(sim, "!", GrblSimulator.HOLD_DECELERATION_S)

        assert send(sim, "\x18") == ["", "Grbl 1.1h ['$' for help]"]
        assert status(sim).startswith("<Idle|")

    def test_reset_clears_g92_and_keeps_g54(self, sim):
        send(sim, "G10 L2 P1 X1\nG92 Y2\n")

        send(sim, "\x18")

        assert sim.wco == [1.0, 0.0, 0.0]


class TestProbe:
    def test_probe_reports_the_contact_then_ok(self, sim):
        assert send(sim, "G38.2 Z-11 F300\n") == []
        assert send(sim, "", 2.0) == ["[PRB:0.000,0.000,-5.000:1]", "ok"]
        assert "Pn:P" in status(sim)

    def test_probe_without_contact_raises_alarm_5(self, sim):
        sim.probe_contact_z = -20.0

        assert send(sim, "G38.2 Z-11 F300\n", 3.0) == ["ALARM:5", "[PRB:0.000,0.000,-11.000:0]", "ok"]
        assert status(sim).startswith("<Alarm|")

    def test_probe_g38_3_without_contact_does_not_alarm(self, sim):
        sim.probe_contact_z = -20.0

        assert send(sim, "G38.3 Z-11 F300\n", 3.0) == ["[PRB:0.000,0.000,-11.000:0]", "ok"]

    def test_probe_already_touching_raises_alarm_4(self, sim):
        sim.probe_contact_z = 1.0

        assert send(sim, "G38.2 Z-11 F300\n") == ["ALARM:4", "ok"]


class TestProgramFlow:
    def test_m0_gets_ok_after_cycle_start(self, sim):
        assert send(sim, "M0\n") == []
        assert status(sim).startswith("<Hold:0|")
        assert send(sim, "~") == ["ok"]

    def test_m2_resets_the_modes(self, sim):
        send(sim, "G91 G55 M3 S100\n")

        assert send(sim, "M2\n") == ["[MSG:Pgm End]", "ok"]
        assert send(sim, "$G\n")[0] == "[GC:G1 G54 G17 G21 G90 G94 M5 M9 T0 F0 S100]"


class TestOffsets:
    def test_g10_l20_sets_the_current_position_as_zero(self, sim):
        send(sim, "G0 X10 Y5\n", 3.0)

        send(sim, "G10 L20 P1 X0 Y0\n")

        assert sim.wco == [10.0, 5.0, 0.0]
        assert sim.wpos == [0.0, 0.0, 0.0]

    def test_offset_change_waits_for_the_motion(self, sim):
        send(sim, "G0 X10\n")

        assert send(sim, "G10 L20 P1 X0\n") == []
        assert send(sim, "", 2.0) == ["ok"]

    def test_tool_length_offset_moves_the_work_z(self, sim):
        send(sim, "G43.1 Z2.5\n")

        assert sim.wco == [0.0, 0.0, 2.5]
        assert send(sim, "$#\n")[-3] == "[TLO:2.500]"


class TestJog:
    def test_jog_runs_in_jog_state_and_locks_gcode(self, sim):
        assert send(sim, "$J=G91 X5 F300\n") == ["ok"]
        assert status(sim).startswith("<Jog|")
        assert send(sim, "G0 X0\n") == ["error:9"]
        assert send(sim, "", 2.0) == []
        assert sim.mpos == [5.0, 0.0, 0.0]

    def test_jog_cancel_stops_and_flushes(self, sim):
        send(sim, "$J=G91 X50 F300\n$J=G91 Y50 F300\n", 0.5)

        send(sim, "\x85", GrblSimulator.HOLD_DECELERATION_S)

        assert status(sim).startswith("<Idle|")
        assert sim.planner_blocks == 0
        assert sim.mpos[1] == 0.0

    def test_jog_needs_a_feed_rate(self, sim):
        assert send(sim, "$J=G91 X5\n") == ["error:22"]


class TestDwell:
    def test_ok_comes_after_the_dwell(self, sim):
        assert send(sim, "G4 P1\n", 0.5) == []
        assert send(sim, "", 0.6) == ["ok"]


class TestHoming:
    def test_homing_moves_to_the_pull_off_position(self, sim):
        assert send(sim, "$H\n") == []
        assert status(sim).startswith("<Home|")
        assert send(sim, "", 1.0) == ["ok"]
        assert sim.mpos == [-1.0, -1.0, -1.0]


class TestSimulatorCommands:
    def test_injected_error_rejects_the_next_gcode_line(self, sim):
        assert send(sim, "$SIM=ERROR:20\n") == ["[MSG:Simulator: the next G-code line gets error:20]"]
        assert send(sim, "G0 X1\n") == ["error:20"]
        assert send(sim, "G0 X1\n") == ["ok"]

    def test_injected_hard_limit_alarm_needs_a_reset(self, sim):
        assert send(sim, "$SIM=ALARM:1\n") == ["ALARM:1", "[MSG:Reset to continue]"]
        assert send(sim, "?$X\n") == []
        assert send(sim, "\x18")[-1] == "[MSG:'$H'|'$X' to unlock]"

    def test_probe_contact_can_be_moved(self, sim):
        send(sim, "$SIM=PROBE:-2\n")

        assert send(sim, "G38.2 Z-11 F300\n", 1.0)[0] == "[PRB:0.000,0.000,-2.000:1]"


class TestSerialBuffer:
    def test_characters_beyond_the_serial_buffer_are_lost(self, sim):
        send(sim, "G4 P10\n")

        send(sim, "G0 X1\n" * 30)

        assert sim.rx_overflows > 0


@pytest.mark.usefixtures("qapp")
class TestSimulatedSerialPort:
    @pytest.fixture
    def port(self):
        port = SimulatedSerialPort(speed=50.0)
        yield port
        port.close()

    def test_opening_restarts_the_controller(self, port, qtbot):
        with qtbot.waitSignal(port.readyRead, timeout=1000):
            assert port.open(QIODevice.ReadWrite)

        assert port.canReadLine()
        assert port.readAll().data() == b"\r\nGrbl 1.1h ['$' for help]\r\n"

    def test_written_lines_are_answered_and_executed(self, port, qtbot):
        port.open(QIODevice.ReadWrite)
        port.readAll()

        assert port.write(b"G0 X10\n") == 7
        qtbot.waitUntil(lambda: port.simulator.state == "Idle", timeout=2000)

        assert port.readAll().data() == b"ok\r\n"
        assert port.simulator.mpos == [10.0, 0.0, 0.0]

    def test_closed_port_refuses_writes(self, port):
        assert port.write(b"?") == -1


def a_real_port(mocker):
    real = mocker.Mock()
    real.portName.return_value = "COM3"
    real.hasVendorIdentifier.return_value = True
    real.standardBaudRates.return_value = [9600, 115200]
    mocker.patch("PySide6.QtSerialPort.QSerialPortInfo.availablePorts", return_value=[real])


@pytest.mark.usefixtures("qapp")
class TestSerialWorkerWithSimulator:
    @pytest.fixture
    def worker(self, mock_serial_port):
        from TheAntFarm.serial_manager import SerialWorker

        worker = SerialWorker(Queue(), Queue())
        worker.serial_port = mock_serial_port
        worker.set_simulator(True, 20.0)
        yield worker
        if worker.simulated_port is not None:
            worker.simulated_port.close()

    def test_simulator_is_listed_last(self, worker, mocker, qtbot):
        a_real_port(mocker)

        with qtbot.waitSignal(worker.get_port_list_s, timeout=1000) as blocker:
            worker.get_port_list()

        assert blocker.args == [["COM3", SIMULATOR_PORT_NAME], [9600, 115200]]

    def test_simulator_is_listed_without_any_port(self, worker, mocker, qtbot):
        mocker.patch("PySide6.QtSerialPort.QSerialPortInfo.availablePorts", return_value=[])

        with qtbot.waitSignal(worker.get_port_list_s, timeout=1000) as blocker:
            worker.get_port_list()

        assert blocker.args[0] == [SIMULATOR_PORT_NAME]
        assert 115200 in blocker.args[1]

    def test_opening_the_simulator_and_then_a_real_port(self, worker, mock_serial_port, qtbot):
        with qtbot.waitSignal(worker.open_port_s, timeout=1000) as blocker:
            worker.open_port(SIMULATOR_PORT_NAME, 115200)

        assert blocker.args == [True]
        assert worker.serial_port is worker.simulated_port
        assert worker.simulated_port.speed == 20.0
        qtbot.waitUntil(lambda: not worker.serialRxQueue.empty(), timeout=1000)
        mock_serial_port.setPortName.assert_not_called()

        worker.close_port()
        worker.open_port("COM3", 115200)

        assert worker.serial_port is mock_serial_port
        mock_serial_port.setPortName.assert_called_once_with("COM3")

    def test_the_simulator_is_created_only_when_opened(self, worker):
        assert worker.simulated_port is None

    def test_a_new_speed_reaches_the_open_simulator(self, worker, qtbot):
        worker.open_port(SIMULATOR_PORT_NAME, 115200)

        worker.set_simulator(True, 5.0)

        assert worker.simulated_port.speed == 5.0

    def test_disabled_simulator_is_not_listed_or_opened(self, worker, mock_serial_port, mocker, qtbot):
        a_real_port(mocker)
        worker.set_simulator(False, 1.0)

        with qtbot.waitSignal(worker.get_port_list_s, timeout=1000) as blocker:
            worker.get_port_list()
        worker.open_port(SIMULATOR_PORT_NAME, 115200)

        assert blocker.args[0] == ["COM3"]
        assert worker.serial_port is mock_serial_port
        assert worker.simulated_port is None

    def test_no_simulator_by_default(self, mocker, qtbot):
        from TheAntFarm.serial_manager import SerialWorker

        a_real_port(mocker)
        worker = SerialWorker(Queue(), Queue())

        with qtbot.waitSignal(worker.get_port_list_s, timeout=1000) as blocker:
            worker.get_port_list()

        assert not worker.simulator_enabled
        assert blocker.args[0] == ["COM3"]

    def test_the_signal_sets_the_simulator(self, worker, qtbot):
        worker.set_simulator_s.emit(False, 3.0)

        assert not worker.simulator_enabled
        assert worker.simulator_speed == 3.0


JOB = [
    "G21\n",
    "G90\n",
    "M3 S1000.0\n",
    "G0 X1.000 Y1.000 Z1.000\n",
    "G1 F100.0\n",
    "G1 X1.000 Y1.000 Z-0.100\n",
    "G1 F300.0\n",
    "G1 X2.000 Y1.000 Z-0.100\n",
    "G1 X2.000 Y2.000 Z-0.100\n",
    "G1 X3.000 Y2.000 Z-0.100\n",
    "G0 X3.000 Y2.000 Z1.000\n",
    "M5\n",
]


@pytest.fixture
def controller_worker(qapp):
    from controller.controller_manager import ControllerWorker

    settings = MagicMock()
    settings.local_path = ""
    return ControllerWorker(Queue(), Queue(), settings)


class Link:
    """Carry bytes between the worker queues and the simulator, as SerialWorker does."""

    STEP_S = 0.05

    def __init__(self, worker):
        self.worker = worker
        self.sim = GrblSimulator()
        self.console = []
        self.stopped = 0
        worker.serial_send_s.connect(self._to_simulator)
        worker.update_console_text_s.connect(self.console.append)
        worker.stop_send_s.connect(self._on_stop)
        self._deliver()

    def _on_stop(self):
        self.stopped += 1

    def _to_simulator(self, data):
        self.sim.receive(data if isinstance(data, bytes) else data.encode())

    def _deliver(self):
        for line in self.sim.read_output().decode().splitlines(True):
            self.worker.serialRxQueue.put(line)
            self.worker.parse_rx_queue()

    def run(self, seconds):
        for _ in range(round(seconds / self.STEP_S)):
            while not self.worker.serialTxQueue.empty():
                self._to_simulator(self.worker.serialTxQueue.get())
            self._deliver()
            self.sim.receive(b"?")
            self.sim.advance(self.STEP_S)
            self._deliver()
            if self.stopped:
                return


class TestStreamToSimulator:
    def test_job_runs_to_the_end(self, controller_worker):
        link = Link(controller_worker)

        controller_worker.send_gcode_lines(list(JOB))
        link.run(30.0)

        assert link.stopped == 1
        assert controller_worker.ack_lines == len(JOB)
        assert link.sim.mpos == pytest.approx([3.0, 2.0, 1.0])
        assert link.sim.state == "Idle"
        assert not [text for text in link.console if "error" in text.lower()]

    def test_spindle_stop_waits_for_the_motion(self, controller_worker):
        link = Link(controller_worker)

        controller_worker.send_gcode_lines(list(JOB))
        link.run(1.0)

        assert controller_worker.ack_lines == len(JOB) - 1
        assert link.stopped == 0
        assert link.sim.state == "Run"

    def test_stopping_a_running_job_leaves_the_machine_locked(self, controller_worker):
        link = Link(controller_worker)
        controller_worker.send_gcode_lines(list(JOB))
        link.run(1.0)

        controller_worker.stop_gcode_file()
        link.run(0.1)

        assert link.sim.state == "Alarm"
        assert "ALARM:3\r\n" in link.console
