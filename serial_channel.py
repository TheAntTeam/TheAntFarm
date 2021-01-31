import serial
from serial.tools.list_ports import comports


class SerialChannel:
    """Serial Channel utilities"""

    SERIAL_TIMEOUT = 5

    def __init__(self, speed=115200):
        self.serials = self._get_serial_ports()
        self.speed = speed
        self.active_port = None

    def get_active_port_name(self):
        """Get active serial port name."""
        if self.active_port is not None:
            if self.active_port.is_open:
                return self.active_port.name
        return None

    def open(self, com_name):
        """Tries to open the serial port with the com name given."""
        open_flag = False
        if self.active_port is None:
            open_flag = True
        else:
            if self.active_port.is_open:
                if self.active_port.name != com_name:
                    self.active_port.close()
                    open_flag = True
                else:
                    if self.active_port.baudrate != self.speed:
                        self.active_port.close()
                        open_flag = True
            else:
                open_flag = True

        if open_flag:
            self.active_port = serial.Serial(None,
                                             self.speed,
                                             bytesize=serial.EIGHTBITS,
                                             parity=serial.PARITY_NONE,
                                             stopbits=serial.STOPBITS_ONE,
                                             timeout=self.SERIAL_TIMEOUT,
                                             xonxoff=False,
                                             rtscts=False,
                                             dsrdtr=False)
            self.active_port.port = com_name
            self.active_port.open()

    def close(self):
        """Close serial port if active and opened."""
        if self.active_port is not None:
            if self.active_port.is_open:
                self.active_port.close()

    def set_speed(self, speed):
        """Changes serial port baudrate."""
        self.speed = speed

    @staticmethod
    def _get_serial_ports():
        """ Lists serial port names """
        # print(sorted([x[0] for x in comports()])) #debug print
        return sorted([port.device for port in comports()])

    def get_available_ports(self):
        """Returns a lists of available serial port names."""
        return self._get_serial_ports()

    def active_port_is_open(self):
        """Return true if the active port is open, false otherwise."""
        return self.active_port.is_open


if __name__ == "__main__":
    pass
