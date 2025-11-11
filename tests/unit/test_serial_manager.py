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

    def test_connection_error(self, serial_manager, caplog):
        """Test handling errors - verify errors are logged but port stays open"""
        # Setup error conditions
        error_string = "Test Error Message"
        serial_manager.serial_port.error.return_value = QSerialPort.ResourceError
        serial_manager.serial_port.errorString.return_value = error_string

        # Trigger error
        serial_manager.serial_error_manager()

        # Verify error was logged but port stays open
        assert "ResourceError" in caplog.text
        assert error_string in caplog.text
        assert serial_manager.serial_port.isOpen()

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