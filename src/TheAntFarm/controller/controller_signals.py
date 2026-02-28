from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap
from collections import OrderedDict as Od


class ControllerSignals(QObject):
    """Base class containing all signals for ControllerWorker."""

    # View signals
    update_layer_s = Signal(Od, str, str, bool)  # Update layer visualization
    update_align_layer_s = Signal(Od, str, str, bool)  # Update align layer visualization
    update_align_layer_view_s = Signal(list)  # Update align layer visualization (flipping)
    update_path_s = Signal(str, list)  # Update path visualization
    update_camera_image_s = Signal(QPixmap)  # Update Camera Image
    update_camera_list_s = Signal(list)  # Update Camera list detected
    update_status_s = Signal(Od)  # Update controller status
    update_console_text_s = Signal(str)  # Send text to the console textEdit

    # Serial signals
    serial_send_s = Signal(bytes)  # Send text to the serial
    serial_tx_available_s = Signal()  # Send text to the serial

    # Alignment signals
    update_align_points_s = Signal(list)  # Update the list of alignment points

    # Probe signals
    touched_probe_s = Signal()  # Signal the probe touched
    update_probe_s = Signal(list)  # Update probe value

    # Auto-Bed-Levelling signals
    send_abl_s = Signal(tuple, tuple)
    update_abl_s = Signal(list)  # Update Auto-Bed-Levelling value

    # GCode signals
    update_bbox_s = Signal(tuple)
    update_gcode_s = Signal(str, list, bool, bool)
    gcode_vectorized_s = Signal(str)
    update_file_progress_s = Signal(float, str)  # Update progress info

    # Control signals
    reset_controller_status_s = Signal()
    stop_send_s = Signal()
    send_tool_change_s = Signal()  # Start the tool change procedure

    # Status report signal
    report_status_report_s = Signal(Od)
