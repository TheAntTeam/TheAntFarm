from PySide2.QtCore import Signal, Slot, QObject
import logging

logger = logging.getLogger(__name__)


# Signals need to be contained in a QObject or subclass in order to be correctly initialized.
class Signaller(QObject):
    signal = Signal(str, logging.LogRecord)


# Output to a Qt GUI is only supposed to happen on the main thread. So, this
# handler is designed to take a slot function which is set up to run in the main
# thread. In this example, the function takes a string argument which is a
# formatted log message, and the log record which generated it. The formatted
# string is just a convenience - you could format a string for output any way
# you like in the slot function itself.
#
# You specify the slot function to do whatever GUI updates you want. The handler
# doesn't know or care about specific UI elements.
#
class LogHandler(logging.Handler):
    def __init__(self, slot_func, *args, **kwargs):
        super(LogHandler, self).__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slot_func)

    def emit(self, record):
        s = self.format(record)
        self.signaller.signal.emit(s, record)

    def connect_log_actions(self, ui):
        ui.action_critical.triggered.connect(lambda: self.setLevel(logging.CRITICAL))
        ui.action_error.triggered.connect(lambda: self.setLevel(logging.ERROR))
        ui.action_warning.triggered.connect(lambda: self.setLevel(logging.WARNING))
        ui.action_info.triggered.connect(lambda: self.setLevel(logging.INFO))
        ui.action_debug.triggered.connect(lambda: self.setLevel(logging.DEBUG))
