from PySide6.QtCore import Signal, QObject
import logging
import logging.handlers

logger = logging.getLogger(__name__)


class Signaller(QObject):
    """
    Since the Log Handler classes are not derived from QObject, they cannot
    contain signals, this is why this class exists.
    """
    signal = Signal(str, logging.LogRecord)


class LogHandler(logging.Handler):
    """
    Logging Handler class, that is responsible for the configuration of logs and
    the redirection from non-main threads to main thread, where the app can display
    the messages in the GUI.
    The working logic of this class is derived from the following example:
    http://plumberjack.blogspot.com/2019/11/a-qt-gui-for-logging.html
    """
    def __init__(self, slot_func, *args, **kwargs):
        super(LogHandler, self).__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slot_func)

    def emit(self, record):
        s = self.format(record)
        self.signaller.signal.emit(s, record)

    def set_handler_features(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(module)s %(funcName)s %(message)s')
        self.setFormatter(formatter)
        self.setLevel(logging.INFO)

    def connect_log_actions(self, ui):
        ui.action_critical.triggered.connect(lambda: self.setLevel(logging.CRITICAL))
        ui.action_error.triggered.connect(lambda: self.setLevel(logging.ERROR))
        ui.action_warning.triggered.connect(lambda: self.setLevel(logging.WARNING))
        ui.action_info.triggered.connect(lambda: self.setLevel(logging.INFO))
        ui.action_debug.triggered.connect(lambda: self.setLevel(logging.DEBUG))


class FileLogHandler(logging.handlers.RotatingFileHandler):
    """
    File Logging Handler class, that is responsible for the configuration of logs saved in files.
    """
    def __init__(self, app_settings):
        super(FileLogHandler, self).__init__(app_settings.logs_file,
                                             maxBytes=app_settings.logs_max_bytes,
                                             backupCount=app_settings.logs_backup_count)

    def set_handler_features(self):
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(threadName)s %(module)s %(funcName)s %(message)s')
        self.setFormatter(formatter)
        self.setLevel(logging.DEBUG)
