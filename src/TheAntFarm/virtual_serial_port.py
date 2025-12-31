"""Virtual Serial Port - Simulates GRBL controller behavior for testing/demonstration."""

from PySide6.QtCore import QObject, Signal
import logging
import time
from threading import Lock
import re

logger = logging.getLogger(__name__)


class VirtualSerialPort(QObject):
    """Simulated GRBL serial port for development/demonstration without hardware."""
    
    readyRead = Signal()
    errorOccurred = Signal()
    
    class SerialPortError:
        NoError = 0
        ResourceError = 1
        PermissionError = 2
        OpenError = 3
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_open = False
        self._port_name = ""
        self._baud_rate = 0
        self._read_buffer = b""
        self._write_buffer = b""
        self._error = self.SerialPortError.NoError
        self._lock = Lock()
        
        # Virtual machine state
        self._mpos = [0.0, 0.0, 0.0]
        self._wpos = [0.0, 0.0, 0.0]
        self._wco = [0.0, 0.0, 0.0]
        self._status = "Idle"
        self._simulation_delay = 0.01  # Simulate realistic response time
        self._g28_position = [0.0, 0.0, 0.0]
        self._g30_position = [0.0, 0.0, 0.0]
        self._g92_position = [0.0, 0.0, 0.0]
        
        logger.info("VirtualSerialPort initialized")
    
    def setPortName(self, name):
        """Set the virtual port name (for display)."""
        self._port_name = name
    
    def portName(self):
        """Get the virtual port name."""
        return self._port_name
    
    def setBaudRate(self, rate):
        """Set baud rate (ignored in simulation)."""
        self._baud_rate = rate
    
    def open(self, mode):
        """Open the virtual port."""
        if self._port_name:
            self._is_open = True
            logger.info(f"Virtual serial port opened: {self._port_name} at {self._baud_rate} baud")
            return True
        return False
    
    def isOpen(self):
        """Check if port is open."""
        return self._is_open
    
    def close(self):
        """Close the virtual port."""
        self._is_open = False
        logger.info(f"Virtual serial port closed: {self._port_name}")
    
    def write(self, data):
        """Write data to virtual port and simulate response."""
        if not self._is_open:
            return -1
        
        if isinstance(data, str):
            data = data.encode()
        
        with self._lock:
            self._write_buffer += data
        
        # Parse and respond to command
        self._process_command(data)
        
        return len(data)
    
    def readAll(self):
        """Read all buffered data."""
        class BytesData:
            def __init__(self, data):
                self._data = data
            
            def data(self):
                return self._data
        
        with self._lock:
            result = BytesData(self._read_buffer)
            self._read_buffer = b""
        
        return result
    
    def canReadLine(self):
        """Check if there's a complete line in buffer."""
        with self._lock:
            return b"\n" in self._read_buffer
    
    def waitForBytesWritten(self, msecs=None):
        """Simulate write delay."""
        time.sleep(self._simulation_delay)
        return True
    
    def flush(self):
        """Flush buffers (no-op for simulation)."""
        pass
    
    def error(self):
        """Get error code."""
        return self._error
    
    def errorString(self):
        """Get error message."""
        return "Virtual serial port error"
    
    def _process_command(self, command):
        """Parse incoming G-code and queue appropriate response."""
        cmd_str = command.decode().strip()
        if cmd_str:
            logger.debug(f"Virtual port received: {cmd_str}")
        
        # Status query
        if cmd_str == "?":
            status_line = (
                f"<{self._status},MPos:{self._mpos[0]:.3f},"
                f"{self._mpos[1]:.3f},{self._mpos[2]:.3f},"
                f"WPos:{self._wpos[0]:.3f},"
                f"{self._wpos[1]:.3f},{self._wpos[2]:.3f}>"
            )
            self._queue_response(status_line.encode() + b"\n")
        
        # Soft reset
        elif cmd_str == "!" or cmd_str == "\x18":
            self._status = "Idle"
            self._queue_response(b"[Reset to continue]\n")
        
        # Unlock
        elif cmd_str == "$X":
            self._queue_response(b"ok\n")
        
        # Home (G28)
        elif cmd_str in ["$H", "G28"]:
            self._mpos = [0.0, 0.0, 0.0]
            self._wpos = [0.0, 0.0, 0.0]
            self._status = "Idle"
            self._queue_response(b"ok\n")
        
        # Set position (G92)
        elif cmd_str.upper().startswith("G92"):
            self._parse_g92(cmd_str)
            self._status = "Idle"
            self._queue_response(b"ok\n")
        
        # Probe command (G38.2 or similar)
        elif "G38" in cmd_str.upper():
            self._probe_command(cmd_str)
        
        # Movement commands (G0/G1)
        elif "G0" in cmd_str.upper() or "G1" in cmd_str.upper():
            self._parse_movement(cmd_str)
            self._status = "Idle"
            self._queue_response(b"ok\n")
        
        # Settings query ($#)
        elif cmd_str == "$#":
            self._queue_settings_response()
        
        # Generic $ settings
        elif cmd_str.startswith("$") and cmd_str != "$X" and cmd_str != "$H":
            # Return dummy settings or acknowledgement
            self._queue_response(b"ok\n")
        
        # Any other command: respond with ok
        elif cmd_str:
            self._queue_response(b"ok\n")
        
        if cmd_str:
            self.readyRead.emit()
    
    def _parse_movement(self, cmd_str):
        """Parse G0/G1 command and update virtual position."""
        try:
            # Simple parser: look for X, Y, Z values
            for token in cmd_str.split():
                token_upper = token.upper()
                if token_upper.startswith('X'):
                    self._mpos[0] = float(token[1:])
                    self._wpos[0] = self._mpos[0] - self._wco[0]
                elif token_upper.startswith('Y'):
                    self._mpos[1] = float(token[1:])
                    self._wpos[1] = self._mpos[1] - self._wco[1]
                elif token_upper.startswith('Z'):
                    self._mpos[2] = float(token[1:])
                    self._wpos[2] = self._mpos[2] - self._wco[2]
        except (ValueError, IndexError) as e:
            logger.debug(f"Error parsing movement command '{cmd_str}': {e}")
    
    def _parse_g92(self, cmd_str):
        """Parse G92 (set position) command."""
        try:
            for token in cmd_str.split():
                token_upper = token.upper()
                if token_upper.startswith('X'):
                    self._g92_position[0] = float(token[1:])
                elif token_upper.startswith('Y'):
                    self._g92_position[1] = float(token[1:])
                elif token_upper.startswith('Z'):
                    self._g92_position[2] = float(token[1:])
        except (ValueError, IndexError) as e:
            logger.debug(f"Error parsing G92 command '{cmd_str}': {e}")
    
    def _probe_command(self, cmd_str):
        """Handle probe command (G38.2)."""
        # Simulate probe touching at slightly different position
        probe_pos = [
            self._mpos[0] + 0.5,
            self._mpos[1] + 0.5,
            self._mpos[2] - 5.0
        ]
        probe_response = f"[PRB:{probe_pos[0]:.3f},{probe_pos[1]:.3f},{probe_pos[2]:.3f}:1]\n"
        self._queue_response(probe_response.encode())
        self._queue_response(b"ok\n")
    
    def _queue_settings_response(self):
        """Queue GRBL settings response for $# query."""
        settings = [
            f"[G28:{self._g28_position[0]:.3f},{self._g28_position[1]:.3f},{self._g28_position[2]:.3f}]\n".encode(),
            f"[G30:{self._g30_position[0]:.3f},{self._g30_position[1]:.3f},{self._g30_position[2]:.3f}]\n".encode(),
            f"[G92:{self._g92_position[0]:.3f},{self._g92_position[1]:.3f},{self._g92_position[2]:.3f}]\n".encode(),
        ]
        for setting in settings:
            self._queue_response(setting)
        self._queue_response(b"ok\n")
    
    def _queue_response(self, response):
        """Queue a response to be read."""
        with self._lock:
            self._read_buffer += response
    
    def set_simulation_delay(self, delay_ms):
        """Set response delay in milliseconds."""
        self._simulation_delay = delay_ms / 1000.0
    
    def get_virtual_position(self):
        """Get current virtual machine position."""
        return {
            "mpos": self._mpos.copy(),
            "wpos": self._wpos.copy(),
            "wco": self._wco.copy(),
            "status": self._status
        }
    
    def set_virtual_position(self, mpos=None, wco=None):
        """Manually set virtual machine state."""
        if mpos:
            self._mpos = list(mpos)
        if wco:
            self._wco = list(wco)
            self._wpos = [
                self._mpos[0] - self._wco[0],
                self._mpos[1] - self._wco[1],
                self._mpos[2] - self._wco[2]
            ]
