import pytest
from TheAntFarm.serial_manager import SerialWorker
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QIODevice
from queue import Queue

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
        with qtbot.waitSignal(serial_manager.close_for_error_s, timeout=1000) as blocker:
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
        mock_port.standardBaudRates.return_value = [9600, 115200]

        # Mock the availablePorts method
        mocker.patch('PySide6.QtSerialPort.QSerialPortInfo.availablePorts',
                    return_value=[mock_port])

        # Set up signal spy
        with qtbot.waitSignal(serial_manager.get_port_list_s, timeout=1000) as blocker:
            serial_manager.get_port_list()

        # Verify port list
        assert blocker.args == [["COM1"], [9600, 115200]]

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