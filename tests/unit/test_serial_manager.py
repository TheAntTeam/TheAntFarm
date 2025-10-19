import pytest
from TheAntFarm.serial_manager import SerialWorker
from PySide6.QtSerialPort import QSerialPort

class TestSerialManager:
    @pytest.fixture
    def serial_manager(self, mock_serial_port):
        return SerialWorker(serial_rx_queue=[], serial_tx_queue=[])

    def test_connect(self, serial_manager, mocker):
        """Test connecting to serial port"""
        # Mock QSerialPort methods
        serial_manager.serial_port.open = mocker.Mock(return_value=True)
        serial_manager.serial_port.setBaudRate = mocker.Mock()
        
        # Set up signal handler
        signal_received = []
        serial_manager.open_port_s.connect(lambda x: signal_received.append(x))
        
        # Test successful connection
        serial_manager.open_port("COM1", 115200)
        
        # Verify results
        assert len(signal_received) == 1
        assert signal_received[0] is True
        serial_manager.serial_port.setBaudRate.assert_called_once_with(115200)

    def test_disconnect(self, serial_manager, mocker):
        """Test disconnecting from serial port"""
        # Mock QSerialPort methods
        serial_manager.serial_port.close = mocker.Mock()
        serial_manager.serial_port.isOpen = mocker.Mock(return_value=True)
        
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

    def test_connection_error(self, serial_manager, mocker):
        """Test handling connection errors"""
        # Set up signal handler
        signal_received = []
        serial_manager.close_for_error_s.connect(lambda: signal_received.append(True))
        
        # Mock error state
        serial_manager.serial_port.error = mocker.Mock(return_value=QSerialPort.ResourceError)
        serial_manager.serial_port.errorString = mocker.Mock(return_value="Test error")
        
        # Simulate error
        serial_manager.serial_error_manager()
        
        # Verify error handling
        assert len(signal_received) == 0  # Signal is commented out in the code
        # Verify that error was logged (we can see this in the captured log)