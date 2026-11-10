# To convert ui to py from the "src/TheAntFarm" folder
# do: PySide6-uic the_ant_farm.ui > ui_the_ant_farm.py
# or: python .\build.py ui
# Whenever you change resources in qrc, go into the "src/TheAntFarm" folder
# convert qrc to py: PySide6-rcc app_resources.qrc -o app_resources_rc.py
# or:                python .\build.py res

import logging.handlers
import os
import platform
import sys
from queue import Queue
from typing import Any

from controller.controller_manager import ControllerWorker
from executable_path_checker import ExecutablePathChecker
from log_manager import FileLogHandler, LogHandler
from PySide6.QtCore import QDeadlineTimer, QMetaObject, QResource, Qt, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from serial_manager import SerialWorker
from settings_manager.settings_manager import SettingsHandler
from style_manager import StyleManager
from ui_manager.ui_manager import UiManager
from ui_the_ant_farm import Ui_MainWindow


def config_os():
    pys2_path = os.path.dirname(sys.modules["PySide6"].__file__)
    if os.path.isdir(os.path.join(pys2_path, "Qt")):
        pys2_path = os.path.join(pys2_path, "Qt")

    # Simple mod to set the QT environment data just for python
    # avoiding conflict with other applications using Qt
    os.environ["QT_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins")

    sys_name = platform.system()
    print(sys_name)
    if sys_name == "Windows":
        print("Windows Env")
        # https://bugreports.qt.io/browse/PYSIDE-2935: the PySide6 DLLs are in the folder of its module, also in
        # the executable built with PyInstaller
        os.add_dll_directory(os.path.dirname(sys.modules["PySide6"].__file__))
    elif sys_name == "Darwin":
        print("Mac Env")
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins", "platforms")
    else:
        print("Linux Env")
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins", "platforms")
        os.environ.setdefault("QT_QPA_PLATFORM", "wayland;xcb")
        # GTK3 (Qt's GNOME theme) aborts on Wayland with gnome-settings-daemon 50: let it use XWayland
        os.environ.setdefault("GDK_BACKEND", "x11")


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu: Queue[Any] = Queue()  # serial FIFO RX Queue
    serialTxQu: Queue[Any] = Queue()  # serial FIFO TX Queue
    THREAD_STOP_TIMEOUT_MS = 3000  # shared by the threads, more than a blocking serial write (1 s)

    def __init__(self, local_path="", style_manager=None):
        super(MainWindow, self).__init__()

        self.local_path = local_path
        self.style_manager = style_manager

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if platform.system() == "Darwin":
            StyleManager.scale_fixed_font_sizes(self, StyleManager.MACOS_FONT_SCALE)

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
        # Timers can only be stopped from their own thread: the control thread stops its own ones
        # right before it finishes (finished is emitted from that thread).
        self.control_thread.finished.connect(self.controlWo.stop_timers, Qt.DirectConnection)
        self.control_thread.start()

        # Serial Worker Thread.
        self.serial_thread = QThread(self)
        self.serial_thread.setObjectName("serial_T")
        self.serialWo = SerialWorker(self.serialRxQu, self.serialTxQu)
        self.serialWo.moveToThread(self.serial_thread)
        self.serial_thread.start()

        # Important: this call should be after the thread creations.
        self.ui_manager = UiManager(self, self.ui, self.controlWo, self.serialWo, self.settings, self.style_manager)

    def closeEvent(self, event):
        """Before closing the application stop all threads and return ok code."""
        if not self.confirm_close():
            event.ignore()
            return
        already_saved = False
        if self.ui_manager.ui_settings_tab_m.has_unsaved_changes():
            msg = QMessageBox(self)
            msg.setWindowTitle("Unsaved Settings")
            msg.setText("You have unsaved changes in the Settings/Preferences tab.")
            msg.setInformativeText("Do you want to save your changes before closing?")
            save_btn = msg.addButton("Save", QMessageBox.ActionRole)
            msg.addButton("Discard", QMessageBox.DestructiveRole)  # neither Save nor Cancel
            cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
            msg.setDefaultButton(cancel_btn)
            msg.exec()

            clicked = msg.clickedButton()
            if clicked == cancel_btn:
                event.ignore()
                return
            elif clicked == save_btn:
                self.ui_manager.ui_settings_tab_m.save_settings_preferences()
                already_saved = True

        if not already_saved:
            logger.info("Saving settings")
            self.ui_manager.save_all_settings()
            logger.info("Settings saved")
        self.stop_threads()
        self.close()

    def confirm_close(self) -> bool:
        """Ask before closing while connected to the machine, and stop a running job if the user confirms.

        Closing only closes the serial port: a running job would go on with the lines the machine already
        has, with the spindle still on. Returns ``False`` when the user cancels.
        """
        control_tab = self.ui_manager.ui_control_tab_m
        if control_tab.job_running:
            text = "A job is running."
            informative_text = "Closing stops it: the machine is put on feed hold and reset."
            close_label = "Stop and Close"
        elif control_tab.serial_connection_status:
            text = "Close The Ant Farm?"
            informative_text = "The machine will be disconnected."
            close_label = "Close"
        else:
            return True
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Close The Ant Farm")
        msg.setText(text)
        msg.setInformativeText(informative_text)
        close_btn = msg.addButton(close_label, QMessageBox.AcceptRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
        msg.setDefaultButton(cancel_btn)
        msg.setEscapeButton(cancel_btn)
        msg.exec()
        if msg.clickedButton() != close_btn:
            return False
        if control_tab.job_running:
            # Blocking: the hold and reset are queued to the serial thread before the port is closed.
            logger.info("Stopping the running job before closing")
            QMetaObject.invokeMethod(self.controlWo, "stop_job_for_close", Qt.BlockingQueuedConnection)
        return True

    def stop_threads(self) -> None:
        """Close the serial port and stop the worker threads, waiting for them up to a shared deadline.

        ``quit()`` does not interrupt a slot that is running: the thread stops when the slot returns. A
        thread still running at the deadline is logged and left behind rather than terminated, which could
        leave the serial port or Qt in a broken state.
        """
        logger.info("Stopping threads")
        self.ui.camera_list_cb.setCurrentIndex(0)  # Select NO CAMERA before closing
        QMetaObject.invokeMethod(self.serialWo, "close_port", Qt.BlockingQueuedConnection)
        self.controlWo.stop_timers()  # the timers of the GUI thread
        self.serial_thread.quit()
        self.control_thread.quit()
        deadline = QDeadlineTimer(self.THREAD_STOP_TIMEOUT_MS)
        for name, thread in (("Serial", self.serial_thread), ("Control", self.control_thread)):
            if thread.wait(deadline):
                logger.info(f"{name} thread stopped")
            else:
                logger.warning(f"{name} thread still running {self.THREAD_STOP_TIMEOUT_MS} ms after the close")


def main(local_path=""):
    app = QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow(local_path=local_path, style_manager=style_man)

    h = LogHandler(window.ui_manager.update_logging_status)
    h.set_handler_features()
    h.connect_log_actions(window.ui)

    fh = FileLogHandler(window.settings.app_settings)
    fh.set_handler_features()

    root = logging.getLogger()
    root.addHandler(h)
    root.addHandler(fh)
    root.setLevel(logging.DEBUG)  # Set root log level to the lowest between the log lever of the handlers.

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    config_os()
    epc = ExecutablePathChecker()
    local_path = epc.create_data_folders()
    print("The Ant Farm Path")
    print(local_path)
    main(local_path)
