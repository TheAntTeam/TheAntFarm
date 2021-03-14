import sys
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import Signal, QThread
from queue import Queue
from ui_newCNC import Ui_MainWindow  # convert like this: pyside2-uic newCNC.ui > ui_newCNC.py
""" Custom imports """
from serial_manager import SerialWorker
from controller_manager import ControllerWorker
from style_manager import StyleManager
from shape_core.visual_manager import VisualLayer
from ui_manager import UiManager


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.connection_status = False
        self.last_open_dir = "."

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.vl = VisualLayer(self.ui.viewCanvasWidget)
        self.ui.refreshButton.clicked.connect(self.handle_refresh_button)
        self.ui.connectButton.clicked.connect(self.handle_connect_button)
        self.ui.clearTerminalButton.clicked.connect(self.handle_clear_terminal)
        self.ui.send_text_edit.setPlaceholderText('input here')
        self.ui.send_text_edit.hide()
        self.ui.send_push_button.hide()
        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)

        # Control Worker Thread, started as soon as the thread pool is started.
        self.control_thread = QThread(self)
        self.control_thread.start()
        self.controlWo = ControllerWorker(self.serialRxQu, self.vl)
        self.controlWo.moveToThread(self.control_thread)

        # Serial Worker Thread.
        self.serial_thread = QThread(self)
        self.serial_thread.start()
        self.serialWo = SerialWorker(self.serialRxQu)
        self.serialWo.moveToThread(self.serial_thread)

        self.ui_manager = UiManager(self, self.ui, self.controlWo, self.serialWo)

    def closeEvent(self, event):
        """Before closing the application stop all threads and return ok code."""
        self.serialWo.close_port()
        self.serial_thread.quit()
        self.control_thread.quit()
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
        """Connect/Disconnect button opens/closes the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        if not self.connection_status:
            # print(self.serialPortsComboBox.currentText())
            if self.serialWo.open_port(self.ui.serialPortsComboBox.currentText()):
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
            self.ui.statusLabel.setText("Not Connected")

    def handle_clear_terminal(self):
        self.ui.textEdit.clear()

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.consoleTextEdit.show()
        else:
            self.ui.consoleTextEdit.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow()

    style_man.change_style("Fusion")
    style_man.set_dark_palette()

    window.show()
    sys.exit(app.exec_())

