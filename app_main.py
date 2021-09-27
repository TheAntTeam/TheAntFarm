import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtCore import QThread, QSettings, QPoint, QSize
from queue import Queue
from ui_newCNC import Ui_MainWindow  # convert like this: pyside2-uic newCNC.ui > ui_newCNC.py
""" Custom imports """
from serial_manager import SerialWorker
from controller.controller_manager import ControllerWorker
from style_manager import StyleManager
from ui_manager.ui_manager import UiManager
from settings_manager import SettingsHandler
from log_manager import LogHandler
import logging.handlers


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue
    serialTxQu = Queue()                   # serial FIFO TX Queue

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
                                                    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = SettingsHandler(self)
        self.settings.read_all_settings()  # TODO: manage exceptions with a try except

        # Control Worker Thread, started as soon as the thread pool is started.
        self.control_thread = QThread(self)
        self.control_thread.setObjectName("control_T")
        self.controlWo = ControllerWorker(self.serialRxQu, self.serialTxQu, self.settings)
        self.controlWo.moveToThread(self.control_thread)
        self.controlWo.init_timers()
        self.control_thread.start()

        # Serial Worker Thread.
        self.serial_thread = QThread(self)
        self.serial_thread.setObjectName("serial_T")
        self.serialWo = SerialWorker(self.serialRxQu, self.serialTxQu)
        self.serialWo.moveToThread(self.serial_thread)
        self.serial_thread.start()

        # Important: this call should be after the thread creations.
        self.ui_manager = UiManager(self, self.ui, self.controlWo, self.serialWo, self.settings)

    def closeEvent(self, event):
        """Before closing the application stop all threads and return ok code."""
        # all_settings_od = {"jobs_settings": self.ui_manager.ui_create_job_m.get_all_settings()}
        # self.settings.write_all_settings(all_settings_od)  # write_settings()
        self.ui_manager.save_all_settings()
        self.serialWo.close_port()
        self.serial_thread.quit()
        self.control_thread.quit()
        app.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow()

    h = LogHandler(window.ui_manager.update_logging_status)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(module)s %(funcName)s %(message)s')
    h.setFormatter(formatter)
    h.setLevel(logging.INFO)
    h.connect_log_actions(window.ui)

    fh = logging.handlers.RotatingFileHandler('./program.log', maxBytes=1000000, backupCount=10)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    root = logging.getLogger()
    root.addHandler(h)
    root.addHandler(fh)
    root.setLevel(logging.DEBUG)  # Set root log level to the lowest between the log lever of the handlers.

    style_man.change_style("Fusion")
    style_man.set_dark_palette()

    window.show()
    sys.exit(app.exec_())

