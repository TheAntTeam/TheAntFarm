import sys
from pathlib import Path
from queue import Queue
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtSerialPort import QSerialPort


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests."""
    app = QCoreApplication([])
    yield app
    app.quit()


# Add the src directory and TheAntFarm package to PYTHONPATH
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(src_path / "TheAntFarm"))


@pytest.fixture
def sample_gerber_path():
    """Fixture providing path to test gerber files"""
    return Path(__file__).parent / "test_data" / "gerbers"


@pytest.fixture
def sample_config_path():
    """Fixture providing path to test configuration files"""
    return Path(__file__).parent / "test_data" / "config"


@pytest.fixture
def mock_serial_port(mocker):
    """Fixture providing a mocked QSerialPort"""
    mock_serial = mocker.Mock(spec=QSerialPort)
    mock_serial.isOpen.return_value = True
    mock_serial.open.return_value = True
    mock_serial.setBaudRate.return_value = True
    mock_serial.setPortName = mocker.Mock()
    mock_serial.errorOccurred = mocker.Mock()
    mock_serial.error.return_value = QSerialPort.NoError
    return mock_serial


@pytest.fixture
def controller_worker(qapp):
    settings = MagicMock()
    settings.local_path = "."

    machine_settings = MagicMock()
    machine_settings.tool_probe_rel_flag = True
    machine_settings.tool_probe_offset_x_wpos = 0.0
    machine_settings.tool_probe_offset_y_wpos = 0.0
    machine_settings.tool_probe_offset_z_wpos = 0.0
    machine_settings.tool_probe_offset_x_mpos = 0.0
    machine_settings.tool_probe_offset_y_mpos = 0.0
    machine_settings.tool_probe_offset_z_mpos = 0.0
    machine_settings.tool_change_offset_x_mpos = 0.0
    machine_settings.tool_change_offset_y_mpos = 0.0
    machine_settings.tool_change_offset_z_mpos = 0.0
    machine_settings.tool_probe_z_limit = -1.0
    machine_settings.feedrate_xy = 100.0
    machine_settings.feedrate_z = 50.0
    machine_settings.feedrate_probe = 25.0
    machine_settings.hold_on_probe_flag = False
    machine_settings.zeroing_after_probe_flag = False
    settings.machine_settings = machine_settings

    rx_queue = Queue()
    tx_queue = Queue()

    view = MagicMock()
    align = MagicMock()
    control = MagicMock()
    control.status_report_od = {"state": "Idle"}
    control.workspace_params_od = {}
    control.prb_val = []
    control.parse_bracket_angle.return_value = {"state": "Idle"}
    control.process_probe_and_abl.return_value = [False, False, False, False]

    gcr = MagicMock()
    gcr.load_cfg = MagicMock()
    gcr.user_cmd.get_command_str.return_value = []

    from controller.controller_manager import ControllerWorker

    worker = ControllerWorker(
        rx_queue,
        tx_queue,
        settings,
        view_controller=view,
        control_controller=control,
        align_controller=align,
        gcr=gcr,
    )

    return worker, control, rx_queue
