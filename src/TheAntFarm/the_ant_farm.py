import os
import sys
import sysconfig
import platform
import shutil
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QThread, QResource
from queue import Queue
from ui_the_ant_farm import Ui_MainWindow
# To convert ui to py from the "src/TheAntFarm" folder
# do: PySide6-uic the_ant_farm.ui > ui_the_ant_farm.py
# or: python .\build.py ui
# Whenever you change resources in qrc, go into the "src/TheAntFarm" folder
# convert qrc to py: PySide6-rcc app_resources.qrc -o app_resources_rc.py
# or:                python .\build.py res
""" Custom imports """
from executable_path_checker import ExecutablePathChecker
from serial_manager import SerialWorker
from controller.controller_manager import ControllerWorker
from style_manager import StyleManager
from ui_manager.ui_manager import UiManager
from settings_manager.settings_manager import SettingsHandler
from log_manager import LogHandler, FileLogHandler
import logging.handlers


def config_os():
    pys2_path = os.path.dirname(sys.modules['PySide6'].__file__)
    if os.path.isdir(os.path.join(pys2_path, "Qt")):
        pys2_path = os.path.join(pys2_path, "Qt")

    # Simple mod to set the QT environment data just for python
    # avoiding conflict with other applications using Qt
    os.environ["QT_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins")

    sys_name = platform.system()
    print(sys_name)
    if sys_name == "Windows":
        print("Windows Env")
        # https://bugreports.qt.io/browse/PYSIDE-2935?attachmentViewMode=list
        pyside6_dll_lib_path = sysconfig.get_path('purelib') + '/PySide6/'
        os.add_dll_directory(pyside6_dll_lib_path)
    elif sys_name == 'Darwin':
        print("Mac Env")
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins", "platforms")
    else:
        print("Linux Env")
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins", "platforms")
        os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue
    serialTxQu = Queue()                   # serial FIFO TX Queue

    def __init__(self, local_path=""):
        super(MainWindow, self).__init__()

        self.local_path = local_path

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # After the UI is set up, register the resources root path relatively to this file path.
        resources_rel_path = os.path.normpath(os.path.join(os.path.dirname(__file__)))
        QResource.registerResource(resources_rel_path)

        self.settings = SettingsHandler(self)
        self.settings.read_all_settings()

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
        print("Saving Settings")
        self.ui_manager.save_all_settings()
        print("Settings Saved")
        print("Stopping Threads")
        self.ui.camera_list_cb.setCurrentIndex(0)  # Select NO CAMERA before closing
        self.serialWo.close_port()
        self.serial_thread.quit()
        self.control_thread.quit()
        self.serial_thread.wait(10)
        self.control_thread.wait(10)
        if self.serial_thread.isRunning():
            print("Serial Thread still running")
        else:
            print("Serial Thread stopped")
        if self.control_thread.isRunning():
            print("Control Thread still running")
        else:
            print("Control Thread stopped")
        self.close()


def main(local_path=""):
    app = QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow(local_path=local_path)

    h = LogHandler(window.ui_manager.update_logging_status)
    h.set_handler_features()
    h.connect_log_actions(window.ui)

    fh = FileLogHandler(window.settings.app_settings)
    fh.set_handler_features()

    root = logging.getLogger()
    root.addHandler(h)
    root.addHandler(fh)
    root.setLevel(logging.DEBUG)  # Set root log level to the lowest between the log lever of the handlers.

    style_man.change_style("Fusion")
    style_man.set_dark_palette()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    config_os()
    epc = ExecutablePathChecker()
    local_path = epc.create_data_folders()
    print("The Ant Farm Path")
    print(local_path)
    main(local_path)
