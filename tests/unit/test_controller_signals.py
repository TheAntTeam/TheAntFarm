import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock, patch


@pytest.fixture(scope="module")
def signals():
    with patch("PySide6.QtCore.QObject"):
        from controller.controller_signals import ControllerSignals
        return ControllerSignals()


def test_signal_update_layer_s(signals):
    assert hasattr(signals, "update_layer_s")


def test_signal_update_align_layer_s(signals):
    assert hasattr(signals, "update_align_layer_s")


def test_signal_update_align_layer_view_s(signals):
    assert hasattr(signals, "update_align_layer_view_s")


def test_signal_update_path_s(signals):
    assert hasattr(signals, "update_path_s")


def test_signal_update_camera_image_s(signals):
    assert hasattr(signals, "update_camera_image_s")


def test_signal_update_camera_list_s(signals):
    assert hasattr(signals, "update_camera_list_s")


def test_signal_update_status_s(signals):
    assert hasattr(signals, "update_status_s")


def test_signal_update_console_text_s(signals):
    assert hasattr(signals, "update_console_text_s")


def test_signal_serial_send_s(signals):
    assert hasattr(signals, "serial_send_s")


def test_signal_serial_tx_available_s(signals):
    assert hasattr(signals, "serial_tx_available_s")


def test_signal_update_align_points_s(signals):
    assert hasattr(signals, "update_align_points_s")


def test_signal_touched_probe_s(signals):
    assert hasattr(signals, "touched_probe_s")


def test_signal_update_probe_s(signals):
    assert hasattr(signals, "update_probe_s")


def test_signal_send_abl_s(signals):
    assert hasattr(signals, "send_abl_s")


def test_signal_update_abl_s(signals):
    assert hasattr(signals, "update_abl_s")


def test_signal_update_bbox_s(signals):
    assert hasattr(signals, "update_bbox_s")


def test_signal_update_gcode_s(signals):
    assert hasattr(signals, "update_gcode_s")


def test_signal_gcode_vectorized_s(signals):
    assert hasattr(signals, "gcode_vectorized_s")


def test_signal_update_file_progress_s(signals):
    assert hasattr(signals, "update_file_progress_s")


def test_signal_reset_controller_status_s(signals):
    assert hasattr(signals, "reset_controller_status_s")


def test_signal_stop_send_s(signals):
    assert hasattr(signals, "stop_send_s")


def test_signal_send_tool_change_s(signals):
    assert hasattr(signals, "send_tool_change_s")


def test_signal_report_status_report_s(signals):
    assert hasattr(signals, "report_status_report_s")