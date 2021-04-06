import os
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import Signal, Slot, QObject, Qt
from PySide2.QtGui import QPixmap
from shape_core.visual_manager import VisualLayer
from collections import OrderedDict as Od
import logging

logger = logging.getLogger(__name__)


class UiManager(QObject):
    """Manage UI objects, signals and slots"""
    L_TAGS = ("top", "bottom", "profile", "drill", "no_copper_top", "no_copper_bottom")
    L_NAMES = ("TOP", "BOTTOM", "PROFILE", "DRILL", "NO COPPER TOP", "NO COPPER BOTTOM")
    L_COLORS = ["red", "blue", "black", "green", "purple", "brown"]
    LOG_COLORS = {
        logging.DEBUG:    'white',
        logging.INFO:     'light blue',
        logging.WARNING:  'orange',
        logging.ERROR:    'red',
        logging.CRITICAL: 'purple',
    }

    def __init__(self, main_win, ui, control_worker, serial_worker, settings):
        super(UiManager, self).__init__()
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.settings = settings

        # UI Sub-Managers
        self.ui_load_layer_m = UiViewLoadLayerTab(main_win, control_worker, settings)
        self.ui_control_tab_m = UiControlTab(ui, control_worker, serial_worker, settings)
        self.ui_align_tab_m = UiAlignTab(ui, control_worker, settings)

        [self.ui.layer_choice_cb.addItem(x) for x in self.L_NAMES]   # todo: the loaded list depends on the layer actually loaded.

        self.ui.layer_choice_cb.currentIndexChanged.connect(self.change_job_page)

        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)

    def change_job_page(self):
        current_text_cb = self.ui.layer_choice_cb.currentText()
        idx = self.L_NAMES.index(current_text_cb)
        self.ui.jobs_sw.setCurrentIndex(idx)

    @Slot(str, logging.LogRecord)
    def update_logging_status(self, status, record):
        color = self.LOG_COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.ui.logging_plain_te.appendHtml(s)

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()


class UiViewLoadLayerTab(QObject):
    """Class dedicated to UI <--> Control interactions. """
    L_TAGS = ("top", "bottom", "profile", "drill", "no_copper_top", "no_copper_bottom")
    L_NAMES = ("TOP", "BOTTOM", "PROFILE", "DRILL", "NO COPPER TOP", "NO COPPER BOTTOM")
    L_COLORS = ["red", "blue", "black", "green", "purple", "brown"]

    load_layer_s = Signal(str, str)

    def __init__(self, main_win, control_worker, settings):
        super(UiViewLoadLayerTab, self).__init__()
        self.main_win = main_win
        self.ui = main_win.ui
        self.controlWo = control_worker
        self.settings = settings

        self.vis_layer = VisualLayer(self.ui.viewCanvasWidget)
        self.layer_colors = Od([(k, v) for k, v in zip(self.L_TAGS, self.L_COLORS)])
        self.L_TEXT = [self.ui.top_file_le, self.ui.bottom_file_le, self.ui.profile_file_le,
                       self.ui.drill_file_le, self.ui.no_copper_1_le, self.ui.no_copper_2_le]
        self.layers_te = Od([(k, t) for k, t in zip(self.L_TAGS, self.L_TEXT)])
        self.L_CHECKBOX = [self.ui.top_view_chb, self.ui.bottom_view_chb, self.ui.profile_view_chb,
                           self.ui.drill_view_chb, self.ui.no_copper_1_chb, self.ui.no_copper_2_chb]
        self.layers_chb = Od([(k, t) for k, t in zip(self.L_TAGS, self.L_CHECKBOX)])

        # Load Layer TAB related controls.
        self.load_layer_s.connect(self.controlWo.load_new_layer)
        self.controlWo.update_layer_s.connect(self.visualize_new_layer)
        self.ui.top_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[0], "Load Top Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.bottom_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[1], "Load Bottom Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.profile_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[2], "Load Profile Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.drill_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[3], "Load Drill Excellon File", "Excellon (*.xln *.XLN)"))
        self.ui.no_copper_1_pb.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[4], "Load No Copper TOP Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.no_copper_2_pb.clicked.connect(
            lambda: self.load_gerber_file(self.L_TAGS[5], "Load No Copper BOTTOM Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.top_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.L_TAGS[0], self.ui.top_view_chb.isChecked()))
        self.ui.bottom_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.L_TAGS[1], self.ui.bottom_view_chb.isChecked()))
        self.ui.profile_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.L_TAGS[2], self.ui.profile_view_chb.isChecked()))
        self.ui.drill_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.L_TAGS[3], self.ui.drill_view_chb.isChecked()))
        self.ui.no_copper_1_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.L_TAGS[4], self.ui.no_copper_1_chb.isChecked()))
        self.ui.no_copper_2_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.L_TAGS[5], self.ui.no_copper_2_chb.isChecked()))
        self.ui.all_view_chb.stateChanged.connect(lambda: self.hide_show_layers(self.ui.all_view_chb.isChecked()))
        self.ui.clear_views_pb.clicked.connect(self.remove_all_vis_layers)

    def load_gerber_file(self, layer="top", load_text="Load File", extensions=""):
        filters = extensions + ";;All files (*.*)"
        load_file_path = QFileDialog.getOpenFileName(self.main_win, load_text, self.settings.layer_last_dir, filters)
        if load_file_path[0]:
            self.vis_layer.remove_layer(layer)
            self.settings.layer_last_dir = os.path.dirname(load_file_path[0])
            logging.info("Loading " + load_file_path[0])
            self.load_layer_s.emit(layer, load_file_path[0])

    def remove_all_vis_layers(self):
        loaded_views = list(self.vis_layer.get_layers_tag())
        for view in loaded_views:
            self.vis_layer.remove_layer(view)
        for layer in self.layers_te:
            self.layers_te[layer].setText("")

    def hide_show_layers(self, checked):
        for cb in self.layers_chb:
            self.layers_chb[cb].setChecked(checked)

    @Slot(str, bool)
    def set_layer_visible(self, tag, visible):
        self.vis_layer.set_layer_visible(tag, visible)

    @Slot(Od, str, str, bool)
    def visualize_new_layer(self, loaded_layer, layer, layer_path, holes):
        self.vis_layer.add_layer(layer, loaded_layer[0], self.layer_colors[layer], holes)
        self.layers_te[layer].setText(layer_path)


class UiControlTab(QObject):
    """Class dedicated to UI <--> Control interactions on Control Tab. """
    serial_send_s = Signal(str)

    def __init__(self, ui, control_worker, serial_worker, settings):
        super(UiControlTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.settings = settings

        self.serial_connection_status = False
        self.serial_send_s.connect(self.serialWo.send)
        self.controlWo.update_status_s.connect(self.update_status)
        self.controlWo.update_console_text_s.connect(self.update_console_text)

        # From Controller Manager to Serial Manager
        self.controlWo.serial_send_s.connect(self.serialWo.send)

        # From Serial Manager to UI Manager
        self.serialWo.update_console_text_s.connect(self.update_console_text)

        # From Serial Manager to Control Manager
        self.serialWo.rx_queue_not_empty_s.connect(self.controlWo.parse_rx_queue)

        self.ui.send_text_edit.setPlaceholderText('input here')
        self.ui.send_text_edit.hide()
        self.ui.send_push_button.hide()

        self.ui.refresh_button.clicked.connect(self.handle_refresh_button)
        self.ui.connect_button.clicked.connect(self.handle_connect_button)
        self.ui.clear_terminal_button.clicked.connect(self.handle_clear_terminal)
        self.ui.send_push_button.clicked.connect(self.send_input)
        self.ui.send_text_edit.returnPressed.connect(self.send_input)
        self.ui.unlockButton.clicked.connect(self.handle_unlock)
        self.ui.homingButton.clicked.connect(self.handle_homing)
        self.ui.xMinusButton.clicked.connect(self.handle_x_minus)

    @Slot(list)
    def update_status(self, status_l):
        self.ui.statusLabel.setText(status_l[0])
        self.ui.mpos_x_label.setText(status_l[1][0])
        self.ui.mpos_y_label.setText(status_l[1][1])
        self.ui.mpos_z_label.setText(status_l[1][2])

    @Slot(str)
    def update_console_text(self, new_text):
        self.ui.serial_te.append(new_text)

    def send_input(self):
        """Send input to the serial port."""
        # self.serialTxQu.put(self.ui.send_text_edit.text() + "\n")
        self.serial_send_s.emit(self.ui.send_text_edit.text() + "\n")
        self.ui.send_text_edit.clear()

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        ls = self.serialWo.get_port_list()
        if ls:
            logger.debug("Available ports: " + str(ls))
            self.ui.serial_ports_cb.clear()
            self.ui.serial_ports_cb.addItems(ls)
        else:
            logger.info('No serial ports available.')
            self.ui.serial_te.append('No serial ports available.')
            self.ui.serial_ports_cb.clear()

    def handle_connect_button(self):
        """Connect/Disconnect button opens/closes the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        if not self.serial_connection_status:
            if self.serialWo.open_port(self.ui.serial_ports_cb.currentText()):
                self.serial_connection_status = True
                self.ui.connect_button.setText("Disconnect")
                self.ui.serial_ports_cb.hide()
                self.ui.serial_baud_cb.hide()
                self.ui.refresh_button.hide()
                self.ui.send_text_edit.show()
                self.ui.send_push_button.show()
        else:
            self.serialWo.close_port()
            self.serial_connection_status = False
            self.ui.connect_button.setText("Connect")
            self.ui.serial_ports_cb.show()
            self.ui.serial_baud_cb.show()
            self.ui.refresh_button.show()
            self.ui.send_text_edit.hide()
            self.ui.send_push_button.hide()
            self.ui.statusLabel.setText("Not Connected")

    def handle_clear_terminal(self):
        self.ui.serial_te.clear()

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()

    def handle_unlock(self):
        logging.debug("Unlock Command")
        self.serial_send_s.emit("$X\n")

    def handle_homing(self):
        logging.debug("Homing Command")
        self.serial_send_s.emit("$H\n")

    def handle_x_minus(self):
        logging.debug("X_minus Command")
        # self.serialTxQu.put("$J=G91 X-10 F100000\n") #todo: change this, just for test
        self.serial_send_s.emit("$J=G91 X-10 F100000\n")  # todo: change this, just for test


class UiAlignTab(QObject):
    """Class dedicated to UI <--> Control interactions on Align Tab. """
    align_active_s = Signal(bool)
    update_threshold_s = Signal(int)

    def __init__(self, ui, control_worker, settings):
        super(UiAlignTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker
        self.settings = settings

        # Align TAB related controls.
        self.ui.main_tab_widget.currentChanged.connect(self.check_align_is_active)
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.ui.verticalSlider.valueChanged.connect(self.update_threshold)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)

        self.controlWo.update_camera_image_s.connect(self.update_camera_image)

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        self.ui.label_2.setPixmap(pixmap)

    def check_align_is_active(self):
        self.align_active_s.emit(self.ui.main_tab_widget.currentWidget().objectName() == "align_tab")

    def update_threshold(self):
        self.update_threshold_s.emit(self.ui.verticalSlider.value())


if __name__ == "__main__":
    pass
