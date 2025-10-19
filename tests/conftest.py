import pytest
import sys
import os
from pathlib import Path

# Add the src directory to PYTHONPATH
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

@pytest.fixture
def sample_gerber_path():
    """Fixture providing path to test gerber files"""
    return Path(__file__).parent / 'test_data' / 'gerbers'

@pytest.fixture
def sample_config_path():
    """Fixture providing path to test configuration files"""
    return Path(__file__).parent / 'test_data' / 'config'

@pytest.fixture
def mock_serial_port(mocker):
    """Fixture providing a mocked serial port"""
    mock_serial = mocker.patch('serial.Serial')
    mock_serial.return_value.is_open = True
    return mock_serial