from PySide2.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide2.QtCore import QIODevice, Signal, Slot, QObject
import logging

logger = logging.getLogger(__name__)


class SerialWorker(QObject):
    update_console_text_s = Signal(str)
    rx_queue_not_empty_s = Signal()

    def __init__(self, serial_rx_queue):
        super(SerialWorker, self).__init__()
        self.serial_port = QSerialPort(self)
        self.serial_port.readyRead.connect(self.receive)
        self.serial_port.bytesWritten.connect(self.send)

        self.serialRxQueue = serial_rx_queue  # FIFO RX Queue to pass data to view thread
        self.residual_string = ""

    @staticmethod
    def get_port_list():
        """Return serial port list."""
        port_l = QSerialPortInfo().availablePorts()
        port_name_l = [port.portName() for port in port_l]
        port_name_l.sort()
        return port_name_l

    def open_port(self, port):
        """Open passed serial port. Return outcome of operation. True if success, otherwise False. """
        if port:
            logging.debug("Opening " + port)
            self.update_console_text_s.emit("Opening " + port)
            try:
                self.serial_port.setPortName(port)
                self.serial_port.open(QIODevice.ReadWrite)
                self.serial_port.setBaudRate(QSerialPort.Baud115200)  #todo: pass baudrate
                return True
            except IOError:
                logging.debug("COM port already in use.")
                self.update_console_text_s.emit("COM port already in use.")
                return False
        else:
            self.update_console_text_s.emit("No port selected.")
            return False

    def close_port(self):
        """Close serial port."""
        logging.debug("Closing " + self.serial_port.portName())
        self.update_console_text_s.emit("Closing " + self.serial_port.portName())
        self.serial_port.close()

    @Slot()
    def receive(self):
        if self.serial_port.canReadLine():
            data_out = self.serial_port.readLine().data().decode()
            if data_out:
                logging.debug("data in: " + data_out)
                self.residual_string = self.residual_string + data_out
                logging.debug("Residual string: " + self.residual_string)
                res_split = self.residual_string.splitlines(True)
                logging.debug("Res split: " + res_split)
                self.residual_string = ""
                while res_split:
                    element = res_split.pop(0)
                    if '\n' in element:
                        self.serialRxQueue.put(element)
                        self.rx_queue_not_empty_s.emit()
                    else:
                        self.residual_string = element
                logging.debug("Final residual string: " + self.residual_string)

    @Slot()
    def send(self, data):
        if self.serial_port.isOpen():
            self.serial_port.write(data.encode("utf-8"))
