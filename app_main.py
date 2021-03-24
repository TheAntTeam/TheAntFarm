import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtCore import QThread, QSettings, QPoint, QSize
from queue import Queue
from ui_newCNC import Ui_MainWindow  # convert like this: pyside2-uic newCNC.ui > ui_newCNC.py
""" Custom imports """
from serial_manager import SerialWorker
from controller_manager import ControllerWorker
from style_manager import StyleManager
from ui_manager import UiManager
from settings_manager import SettingsHandler
from log_manager import LogHandler
import logging


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Control Worker Thread, started as soon as the thread pool is started.
        self.control_thread = QThread(self)
        self.control_thread.start()
        self.controlWo = ControllerWorker(self.serialRxQu)
        self.controlWo.moveToThread(self.control_thread)

        # Serial Worker Thread.
        self.serial_thread = QThread(self)
        self.serial_thread.start()
        self.serialWo = SerialWorker(self.serialRxQu)
        self.serialWo.moveToThread(self.serial_thread)

        self.settings = SettingsHandler("The Ant Team", "newCNC", self)
        self.settings.read_all_settings()  # TODO: manage exceptions with a try except

        # Important: this call should be after the thread creations.
        self.ui_manager = UiManager(self, self.ui, self.controlWo, self.serialWo, self.settings)

    def closeEvent(self, event):
        """Before closing the application stop all threads and return ok code."""
        self.settings.write_all_settings()  # write_settings()
        self.serialWo.close_port()
        self.serial_thread.quit()
        self.control_thread.quit()
        app.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow()

    h = LogHandler(window.ui_manager.update_logging_status)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')
    h.setFormatter(formatter)
    root = logging.getLogger()
    h.setLevel(logging.INFO)
    root.addHandler(h)
    root.setLevel(logging.DEBUG)  # Set root log level to the lowest between the log lever of the handlers.

    style_man.change_style("Fusion")
    style_man.set_dark_palette()

    window.show()
    sys.exit(app.exec_())

