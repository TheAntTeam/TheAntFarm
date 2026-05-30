from queue import Queue

import pytest
from PySide6.QtSerialPort import QSerialPort

from TheAntFarm.serial_manager import SerialWorker


class TestSerialManager:
    @pytest.fixture
    def serial_manager(self, mock_serial_port, qapp):
        rx_queue = Queue()
        tx_queue = Queue()
        worker = SerialWorker(rx_queue, tx_queue)
        worker.serial_port = mock_serial_port
        return worker

    def test_connect(self, serial_manager, qtbot):
        """Test connecting to serial port"""
        # Set up signal spy
        with qtbot.waitSignal(serial_manager.open_port_s, timeout=1000) as blocker:
            serial_manager.open_port("COM1", 115200)

        # Verify results
        assert blocker.args == [True]
        serial_manager.serial_port.setBaudRate.assert_called_once_with(115200)
        serial_manager.serial_port.setPortName.assert_called_once_with("COM1")

    def test_disconnect(self, serial_manager):
        """Test disconnecting from serial port"""
        # Setup mock port name
        serial_manager.serial_port.portName.return_value = "COM1"

        # Test disconnection
        serial_manager.close_port()
        serial_manager.serial_port.close.assert_called_once()

    def test_send_command(self, serial_manager, mocker):
        """Test sending G-code command"""
        # Mock write method
        serial_manager.serial_port.write = mocker.Mock()
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)

        # Test command sending
        test_command = "G0 X0 Y0"
        serial_manager.send(test_command)
        serial_manager.serial_port.write.assert_called_once_with(test_command.encode())

    def test_receive_response(self, serial_manager, mocker):
        """Test receiving response from machine"""
        # Mock readAll method
        mock_data = mocker.Mock()
        mock_data.data = mocker.Mock(return_value=b"ok\n")
        serial_manager.serial_port.readAll = mocker.Mock(return_value=mock_data)

        # Test receiving data
        serial_manager.receive()
        assert serial_manager.residual_string == ""  # Should be cleared after processing

    def test_connection_error_below_warning_threshold(self, serial_manager, qtbot, caplog):
        """Test error handling below warning threshold - error should not be logged"""
        error_string = "Test Error Message"
        serial_manager.serial_port.error.return_value = QSerialPort.ResourceError
        serial_manager.serial_port.errorString.return_value = error_string

        # Trigger error once (below warning threshold of 3)
        serial_manager.serial_error_manager()

        # Should not emit console update signal or log at error level yet
        assert serial_manager._consecutive_errors == 1
        # Should not log the error yet (below threshold)
        assert "Serial error:" not in caplog.text

    def test_connection_error_at_warning_threshold(self, serial_manager, qtbot, caplog):
        """Test error handling at warning threshold - should log warning"""
        error_string = "Test Error Message"
        serial_manager.serial_port.error.return_value = QSerialPort.ResourceError
        serial_manager.serial_port.errorString.return_value = error_string

        # Simulate reaching warning threshold (3 errors)
        with qtbot.waitSignal(serial_manager.update_console_text_s, timeout=1000) as blocker:
            for _ in range(3):
                serial_manager.serial_error_manager()

        # Should have logged warning and emitted console signal
        assert serial_manager._consecutive_errors == 3
        assert "Serial error:" in caplog.text or "Warning:" in blocker.args[0]

    def test_connection_error_at_critical_threshold(self, serial_manager, qtbot, caplog):
        """Test error handling at critical threshold - should close port"""
        error_string = "Test Error Message"
        serial_manager.serial_port.error.return_value = QSerialPort.ResourceError
        serial_manager.serial_port.errorString.return_value = error_string

        # Simulate reaching critical threshold (10 errors)
        with qtbot.waitSignal(serial_manager.close_for_error_s, timeout=1000):
            for _ in range(10):
                serial_manager.serial_error_manager()

        # Should have logged critical error and emitted close signal
        assert serial_manager._consecutive_errors == 10
        assert "Critical error:" in caplog.text

    def test_error_type_change_resets_counter(self, serial_manager):
        """Test that changing error type resets the consecutive error counter"""
        # Simulate first error type
        serial_manager.serial_port.error.return_value = QSerialPort.ResourceError
        serial_manager.serial_port.errorString.return_value = "Resource Error"
        serial_manager.serial_error_manager()
        serial_manager.serial_error_manager()

        assert serial_manager._consecutive_errors == 2
        assert serial_manager._last_error_type == QSerialPort.ResourceError

        # Change to different error type
        serial_manager.serial_port.error.return_value = QSerialPort.TimeoutError
        serial_manager.serial_port.errorString.return_value = "Timeout Error"
        serial_manager.serial_error_manager()

        # Counter should be reset to 1 (for the new error type)
        assert serial_manager._consecutive_errors == 1
        assert serial_manager._last_error_type == QSerialPort.TimeoutError

    def test_no_error_resets_counters(self, serial_manager):
        """Test that no error state resets the error counters"""
        # Simulate some errors
        serial_manager.serial_port.error.return_value = QSerialPort.ResourceError
        serial_manager.serial_port.errorString.return_value = "Resource Error"
        serial_manager.serial_error_manager()
        serial_manager.serial_error_manager()

        assert serial_manager._consecutive_errors == 2

        # Now simulate no error
        serial_manager.serial_port.error.return_value = QSerialPort.NoError
        serial_manager.serial_error_manager()

        # Counters should be reset
        assert serial_manager._consecutive_errors == 0
        assert serial_manager._last_error_type is None

    def test_reset_error_count_method(self, serial_manager):
        """Test the reset_error_count method"""
        # Simulate some errors
        serial_manager._consecutive_errors = 5
        serial_manager._last_error_type = QSerialPort.ResourceError

        # Call reset method
        serial_manager.reset_error_count()

        # Should be reset
        assert serial_manager._consecutive_errors == 0
        assert serial_manager._last_error_type is None

    def test_close_port_resets_error_count(self, serial_manager):
        """Test that closing port resets error count"""
        # Simulate some errors
        serial_manager._consecutive_errors = 5
        serial_manager._last_error_type = QSerialPort.ResourceError
        serial_manager.serial_port.portName.return_value = "COM1"

        # Close port
        serial_manager.close_port()

        # Error count should be reset
        assert serial_manager._consecutive_errors == 0
        assert serial_manager._last_error_type is None
        serial_manager.serial_port.close.assert_called_once()

    def test_get_port_list(self, serial_manager, mocker, qtbot):
        """Test getting available ports list"""
        # Mock QSerialPortInfo
        mock_port = mocker.Mock()
        mock_port.portName.return_value = "COM1"
        mock_port.description.return_value = "Test Port"
        mock_port.hasVendorIdentifier.return_value = True
        mock_port.standardBaudRates.return_value = [9600, 115200]

        # Mock the availablePorts method
        mocker.patch("PySide6.QtSerialPort.QSerialPortInfo.availablePorts", return_value=[mock_port])

        # Set up signal spy
        with qtbot.waitSignal(serial_manager.get_port_list_s, timeout=1000) as blocker:
            serial_manager.get_port_list()

        # Verify port list
        assert blocker.args == [["COM1"], [9600, 115200]]

    @pytest.mark.parametrize("platform,port_name,expected", [
        ("linux", "ttyS0", False),
        ("linux", "ttyUSB0", True),
        ("linux", "ttyACM0", True),
        ("linux", "ttyAMA0", True),
        ("darwin", "cu.usbmodem101", True),
        ("darwin", "cu.Bluetooth", False),
        ("darwin", "tty.Bluetooth", False),
        ("darwin", "tty.usbserial-1234", True),
        ("win32", "COM1", True),
        ("win32", "COM3", True),
    ])
    def test_get_port_list_filtering(self, serial_manager, mocker, qtbot, platform, port_name, expected):
        """Test filtering behavior on different platforms"""
        mock_port = mocker.Mock()
        mock_port.portName.return_value = port_name
        mock_port.hasVendorIdentifier.return_value = False
        mock_port.standardBaudRates.return_value = [9600, 115200]

        mocker.patch("PySide6.QtSerialPort.QSerialPortInfo.availablePorts", return_value=[mock_port])
        mocker.patch("serial_manager.sys.platform", platform)

        with qtbot.waitSignal(serial_manager.get_port_list_s, timeout=1000) as blocker:
            serial_manager.get_port_list()

        if expected:
            assert blocker.args[0] == [port_name]
        else:
            assert blocker.args[0] == []

    def test_get_port_list_vid_takes_priority(self, serial_manager, mocker, qtbot):
        """Verify VID/PID check takes priority over platform name filter"""
        mock_port = mocker.Mock()
        mock_port.portName.return_value = "ttyS0"
        mock_port.hasVendorIdentifier.return_value = True  # Has VID even though name is ttyS0
        mock_port.standardBaudRates.return_value = [9600, 115200]

        mocker.patch("PySide6.QtSerialPort.QSerialPortInfo.availablePorts", return_value=[mock_port])
        mocker.patch("serial_manager.sys.platform", "linux")

        with qtbot.waitSignal(serial_manager.get_port_list_s, timeout=1000) as blocker:
            serial_manager.get_port_list()

        # Should be included because it has vendor ID
        assert blocker.args[0] == ["ttyS0"]

    def test_queue_handling(self, serial_manager):
        """Test queue operations"""
        # Put test command in TX queue
        test_command = "G0 X10 Y10"
        serial_manager.serialTxQueue.put(test_command)

        # Process queue
        serial_manager.send_from_queue()

        # Verify command was sent
        serial_manager.serial_port.write.assert_called_once_with(test_command.encode())
        assert serial_manager.count_queue_sent == 1

    def test_open_port_no_port_selected(self, serial_manager, qtbot):
        """Test open_port when no port is selected"""
        serial_manager.serial_port.portName.return_value = ""

        with qtbot.waitSignal(serial_manager.open_port_s, timeout=1000) as blocker:
            serial_manager.open_port("", 115200)

        assert blocker.args == [False]

    def test_open_port_io_error(self, serial_manager, qtbot, mocker):
        """Test open_port when IOError occurs (port already in use)"""
        serial_manager.serial_port.open = mocker.Mock(side_effect=IOError("Port in use"))

        with qtbot.waitSignal(serial_manager.open_port_s, timeout=1000) as blocker:
            serial_manager.open_port("COM1", 115200)

        assert blocker.args == [False]

    def test_open_port_fails_to_open(self, serial_manager, qtbot, mocker):
        """Test open_port when port fails to open (open returns False)"""
        serial_manager.serial_port.open = mocker.Mock(return_value=False)
        serial_manager.serial_port.errorString = mocker.Mock(return_value="Permission denied")

        with qtbot.waitSignal(serial_manager.open_port_s, timeout=1000) as blocker:
            serial_manager.open_port("COM1", 115200)

        assert blocker.args == [False]

    def test_receive_unicode_decode_error(self, serial_manager, mocker):
        """Test receive when UnicodeDecodeError occurs"""
        mock_data = mocker.Mock()
        mock_data.data = mocker.Mock(return_value=b"\xff\xfe invalid")
        serial_manager.serial_port.readAll = mocker.Mock(return_value=mock_data)
        serial_manager.serial_port.canReadLine = mocker.Mock(return_value=True)

        serial_manager.receive()

        assert serial_manager.residual_string == ""

    def test_receive_partial_line(self, serial_manager, mocker):
        """Test receive with partial line (no newline)"""
        mock_data = mocker.Mock()
        mock_data.data = mocker.Mock(return_value=b"partial data")
        serial_manager.serial_port.readAll = mocker.Mock(return_value=mock_data)
        serial_manager.serial_port.canReadLine = mocker.Mock(return_value=True)

        serial_manager.receive()

        assert serial_manager.residual_string == "partial data"

    def test_send_bytes_data(self, serial_manager, mocker):
        """Test send with bytes data"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock()
        serial_manager.serial_port.waitForBytesWritten = mocker.Mock(return_value=True)

        test_data = b"G0 X0 Y0"
        serial_manager.send(test_data)

        serial_manager.serial_port.write.assert_called_once_with(test_data)

    def test_send_int_data(self, serial_manager, mocker):
        """Test send with int data (should do nothing)"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock()

        test_data = 123
        serial_manager.send(test_data)

        serial_manager.serial_port.write.assert_not_called()

    def test_send_port_not_open(self, serial_manager, mocker):
        """Test send when port is not open"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=False)
        serial_manager.serial_port.write = mocker.Mock()

        serial_manager.send("G0 X0")

        serial_manager.serial_port.write.assert_not_called()

    def test_send_exception_handling(self, serial_manager, mocker):
        """Test send exception handling"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock(side_effect=AttributeError("Port closed"))

        serial_manager.send("G0 X0")

    def test_send_generic_exception(self, serial_manager, mocker):
        """Test send generic exception handling"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock(side_effect=Exception("Unknown error"))

        serial_manager.send("G0 X0")

    def test_send_from_queue_bytes_data(self, serial_manager, mocker):
        """Test send_from_queue with bytes data"""
        serial_manager.serial_port.write = mocker.Mock()
        serial_manager.serial_port.waitForBytesWritten = mocker.Mock(return_value=True)

        test_data = b"G0 X0 Y0"
        serial_manager.serialTxQueue.put(test_data)

        serial_manager.send_from_queue()

        serial_manager.serial_port.write.assert_called_once_with(test_data)

    def test_send_from_queue_int_data(self, serial_manager, mocker):
        """Test send_from_queue with int data (should do nothing)"""
        serial_manager.serial_port.write = mocker.Mock()

        test_data = 456
        serial_manager.serialTxQueue.put(test_data)

        serial_manager.send_from_queue()

        serial_manager.serial_port.write.assert_not_called()

    def test_send_from_queue_port_not_open(self, serial_manager, mocker):
        """Test send_from_queue when port is not open"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=False)
        serial_manager.serial_port.write = mocker.Mock()

        serial_manager.serialTxQueue.put("G0 X0")

        serial_manager.send_from_queue()

        serial_manager.serial_port.write.assert_not_called()

    def test_send_from_queue_exception(self, serial_manager, mocker):
        """Test send_from_queue exception handling"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock(side_effect=Exception("Write error"))
        serial_manager.serial_port.flush = mocker.Mock()

        serial_manager.serialTxQueue.put("G0 X0")

        serial_manager.send_from_queue()

    def test_send_from_queue_generic_exception(self, serial_manager, mocker):
        """Test send_from_queue generic exception handling"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock(side_effect=Exception("Unknown"))
        serial_manager.serial_port.flush = mocker.Mock()

        serial_manager.serialTxQueue.put("G0 X0")

        serial_manager.send_from_queue()

    def test_send_from_queue_attribute_error(self, serial_manager, mocker):
        """Test send_from_queue AttributeError handling"""
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        serial_manager.serial_port.write = mocker.Mock(side_effect=AttributeError("No attribute"))
        serial_manager.serial_port.flush = mocker.Mock()

        serial_manager.serialTxQueue.put("G0 X0")

        serial_manager.send_from_queue()
