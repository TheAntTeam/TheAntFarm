import sys
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import QThreadPool
from queue import Queue
from ui_newCNC import Ui_MainWindow  # convert like this: pyside2-uic newCNC.ui > ui_newCNC.py
""" Custom imports """
from serial_thread import SerialWorker
from controller_thread import ControllerWorker
from style_manager import StyleManager
# from PySide2.QtOpenGLWidgets import *
from PySide2.QtOpenGL import *


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue
    serialTxQu = Queue()                   # serial FIFO TX Queue

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.connection_status = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.refreshButton.clicked.connect(self.handle_refresh_button)
        self.ui.connectButton.clicked.connect(self.handle_connect_button)
        self.ui.unlockButton.clicked.connect(self.handle_unlock)
        self.ui.homingButton.clicked.connect(self.handle_homing)
        self.ui.xMinusButton.clicked.connect(self.handle_x_minus)
        self.ui.clearTerminalButton.clicked.connect(self.handle_clear_terminal)
        self.ui.send_text_edit.hide()
        self.ui.send_push_button.hide()

        # Visualization Worker Thread, started as soon as the thread pool is started. Pass the figure to plot on.
        self.controlWo = ControllerWorker(self.serialRxQu, self.serialTxQu, self.ui)

        # serial Worker Thread
        self.serialWo = SerialWorker(self.serialRxQu, self.serialTxQu, self.ui.textEdit)

        self.threadpool = QThreadPool()
        self.threadpool.start(self.controlWo)

    def set_finish_signal(self):
        """Send signals to stop all threads."""
        self.controlWo.terminate_thread()
        self.serialWo.terminate_thread()

    def closeEvent(self, event):
        """Before closing the application stop all threads and return ok code."""
        self.set_finish_signal()
        app.exit(0)

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        ls = self.serialWo.get_port_list()
        if ls:
            # print(ls)
            # self.ui.textEdit.append("Listing serial ports: ")
            # self.ui.textEdit.append(str(ls))
            self.ui.serialPortsComboBox.clear()
            self.ui.serialPortsComboBox.addItems(ls)
        else:
            # print('No serial ports available.')
            self.ui.textEdit.append('No serial ports available.')
            self.ui.serialPortsComboBox.clear()

    def handle_connect_button(self):
        """Connect button opens the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        if self.connection_status == False:
            # print(self.serialPortsComboBox.currentText())
            if self.serialWo.open_port(self.ui.serialPortsComboBox.currentText()):
                if self.serialWo.no_serial_worker:
                    self.serialWo.revive_it()
                    self.threadpool.start(self.serialWo)
                    self.serialWo.thread_is_started()
                if self.serialWo.is_paused:
                    self.serialWo.revive_it()
                self.connection_status = True
                self.ui.connectButton.setText("Disconnect")
                self.ui.serialPortsComboBox.hide()
                self.ui.refreshButton.hide()
                self.ui.send_text_edit.show()
                self.ui.send_push_button.show()
        else:
            self.serialWo.close_port()
            self.connection_status = False
            self.ui.connectButton.setText("Connect")
            self.ui.serialPortsComboBox.show()
            self.ui.refreshButton.show()
            self.ui.send_text_edit.hide()
            self.ui.send_push_button.hide()


    def handle_disconnect_button(self):
        """Disconnect button closes the serial port."""
        self.serialWo.close_port()

    def handle_unlock(self):
        print("unlock")
        self.serialTxQu.put("$X\n")

    def handle_homing(self):
        print("homing")
        self.serialTxQu.put("$H\n")

    def handle_x_minus(self):
        print("x_minus")
        self.serialTxQu.put("$J=G91 X-10 F100000\n") #todo: change this, just for test

    def handle_clear_terminal(self):
        self.ui.textEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow()

    style_man.change_style("Fusion")
    style_man.set_dark_palette()

    window.show()
    # app.exec_()  # todo: use for debugger only
    sys.exit(app.exec_())
