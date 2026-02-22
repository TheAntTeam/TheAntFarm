import pytest
import sys
from pathlib import Path
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
