from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QIODevice, Signal, Slot, QObject
import logging
import traceback

logger = logging.getLogger(__name__)


class SerialWorker(QObject):
    open_port_s = Signal(bool)
    update_console_text_s = Signal(str)
    rx_queue_not_empty_s = Signal()
    refresh_port_list_s = Signal()
    get_port_list_s = Signal(list, list)
    close_for_error_s = Signal()

    def __init__(self, serial_rx_queue, serial_tx_queue):
        super(SerialWorker, self).__init__()
        self.serial_port = QSerialPort(self)
        self.serial_port.readyRead.connect(self.receive)
        self.serial_port.errorOccurred.connect(self.serial_error_manager)
        self.refresh_port_list_s.connect(self.get_port_list)

        self.serialRxQueue = serial_rx_queue  # FIFO RX Queue to pass data to control thread
        self.serialTxQueue = serial_tx_queue  # FIFO TX Queue to get data from control thread
        self.residual_string = ""

        self.count_queue_sent = 0
        self.count_sent = 0

    @Slot()
    def get_port_list(self):
        """Return serial port list."""
        port_l = QSerialPortInfo().availablePorts()
        port_name_l = [port.portName() for port in port_l]
        port_name_l.sort()
        if port_l:
            bauds_ls = port_l[0].standardBaudRates()
            self.get_port_list_s.emit(port_name_l, bauds_ls)

    def open_port(self, port, baud_rate):
        """Open passed serial port. Return outcome of operation. True if success, otherwise False. """
        if port:
            logger.debug("Opening " + port)
            self.update_console_text_s.emit("Opening " + port)
            try:
                self.serial_port.setPortName(port)
                if self.serial_port.open(QIODevice.ReadWrite):
                    self.serial_port.setBaudRate(baud_rate)
                    self.open_port_s.emit(True)
                else:
                    self.update_console_text_s.emit("COM port could not be opened." + self.serial_port.errorString())
                    self.open_port_s.emit(False)
            except IOError:
                logger.debug("COM port already in use.")
                self.update_console_text_s.emit("COM port already in use.")
                self.open_port_s.emit(False)
        else:
            self.update_console_text_s.emit("No port selected.")
            self.open_port_s.emit(False)

    def close_port(self):
        """Close serial port."""
        logger.debug("Closing " + self.serial_port.portName())
        self.update_console_text_s.emit("Closing " + self.serial_port.portName())
        self.serial_port.close()

    @Slot()
    def receive(self):
        if self.serial_port.canReadLine():
            data_out = self.serial_port.readAll().data().decode()
            if data_out:
                # logger.debug("data in: " + data_out)
                self.residual_string = self.residual_string + data_out
                # logger.debug("Residual string: " + self.residual_string)
                res_split = self.residual_string.splitlines(True)
                self.residual_string = ""
                while res_split:
                    element = res_split.pop(0)
                    if '\n' in element:
                        self.serialRxQueue.put(element)
                        # logger.debug("RXelem: " + element)
                        self.rx_queue_not_empty_s.emit()
                    else:
                        self.residual_string = element
                # logger.debug("Final residual string: " + self.residual_string)

    @Slot(bytes)
    def send(self, data):
        if self.serial_port.isOpen():
            try:
                # logger.debug("data sent: " + str(data))
                self.count_sent += 1
                # logger.debug("Sent count: " + str(self.count_sent))
                if isinstance(data, bytes):
                    self.serial_port.write(data)
                    self.serial_port.waitForBytesWritten(msecs=200)
                elif isinstance(data, int):
                    pass  # do nothing, this should not happen
                else:
                    self.serial_port.write(data.encode())
                    self.serial_port.waitForBytesWritten(msecs=200)
            except AttributeError as e:
                logger.error(e, exc_info=True)
            except Exception:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    @Slot()
    def send_from_queue(self):
        if self.serial_port.isOpen():
            try:
                if not self.serialTxQueue.empty():
                    data = self.serialTxQueue.get()
                    # logger.debug("data sent: " + str(data))
                    self.count_queue_sent += 1
                    logger.debug("Sent count: " + str(self.count_queue_sent))
                    if isinstance(data, bytes):
                        self.serial_port.write(data)
                        self.serial_port.waitForBytesWritten(msecs=1000)
                    elif isinstance(data, int):
                        pass  # do nothing, this should not happen
                        # self.serial_port.write(data)
                    else:
                        self.serial_port.write(data.encode("utf-8"))
                        self.serial_port.waitForBytesWritten(msecs=1000)
                    # if not self.serial_port.waitForBytesWritten(msecs=10):
                    #     logger.debug("data not completely sent: " + str(data))
                    self.serial_port.flush()
            except AttributeError as e:
                logger.error(e, exc_info=True)
            except Exception:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    @Slot()
    def serial_error_manager(self):
        error_type = self.serial_port.error()
        if error_type != 0:
            logger.error(self.serial_port.error())
            logger.error(self.serial_port.errorString())
            # if error_type == QSerialPort.ResourceError:
            #     self.close_for_error_s.emit()
