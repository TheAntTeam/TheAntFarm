from PySide2.QtCore import Signal, Slot, QObject, QSize, Qt, QPersistentModelIndex
from PySide2.QtWidgets import QFileDialog, QLineEdit, QRadioButton, QTableWidgetItem, \
                              QHeaderView, QCheckBox, QButtonGroup
from style_manager import StyleManager
import os
import logging

logger = logging.getLogger(__name__)


class UiControlTab(QObject):
    """Class dedicated to UI <--> Control interactions on Control Tab. """
    controller_connected_s = Signal(bool)
    ui_serial_send_bytes_s = Signal(bytes)
    ui_serial_send_s = Signal(str)
    ui_serial_open_s = Signal(str)
    ui_serial_close_s = Signal()

    send_gcode_s = Signal(str)                   # Signal to start sending a gcode file
    stop_gcode_s = Signal()                      # Signal to stop sending a gcode file
    pause_resume_gcode_s = Signal()              # Signal to pause/resume sending a gcode file

    precalc_gcode_s = Signal(str)
    select_gcode_s = Signal(str)

    def __init__(self, ui, control_worker, serial_worker, ctrl_layer, app_settings):
        """
        Initialize ui elements of Control tab and connect signals coming and going to other classes/workers.

        Parameters
        ----------
        ui: Ui_MainWindow
            User interface object. Contains all user interface's children objects.
        control_worker: ControllerWorker
            Control thread worker object.
        serial_worker: SerialWorker
            Serial thread worker object.
        ctrl_layer: VisualLayer
            VisualLayer object that contain the openGL canvas.
        app_settings: SettingsHandler
            Handler object that allows the access to the application settings.
        """
        super(UiControlTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.ctrl_layer = ctrl_layer
        self.app_settings = app_settings

        self.serial_connection_status = False
        self.ui_serial_send_s.connect(self.serialWo.send)
        self.ui_serial_send_bytes_s.connect(self.serialWo.send)
        self.ui_serial_open_s.connect(self.serialWo.open_port)
        self.ui_serial_close_s.connect(self.serialWo.close_port)
        self.controlWo.reset_controller_status_s.connect(self.controlWo.reset_dro_status_updated)
        self.controlWo.update_status_s.connect(self.update_status)
        self.controlWo.update_probe_s.connect(self.update_probe)
        self.controlWo.send_abl_s.connect(self.controlWo.cmd_auto_bed_levelling)
        self.controlWo.update_bbox_s.connect(self.update_bbox)
        self.controlWo.update_console_text_s.connect(self.update_console_text)
        self.controlWo.update_file_progress_s.connect(self.update_progress_bar)

        self.send_gcode_s.connect(self.controlWo.send_gcode_file)
        self.stop_gcode_s.connect(self.controlWo.stop_gcode_file)
        self.pause_resume_gcode_s.connect(self.controlWo.pause_resume)

        # From Controller Manager to Serial Manager
        self.controlWo.serial_send_s.connect(self.serialWo.send)
        self.controlWo.serial_tx_available_s.connect(self.serialWo.send_from_queue)

        # From Serial Manager to UI Manager
        self.serialWo.open_port_s.connect(self.act_on_connection)
        self.serialWo.update_console_text_s.connect(self.update_console_text)

        # From Serial Manager to Control Manager
        self.serialWo.rx_queue_not_empty_s.connect(self.controlWo.parse_rx_queue)

        self.ui.open_gcode_tb.clicked.connect(self.open_gcode_files)

        self.ui.send_te.setPlaceholderText('input here')
        self.ui.send_te.hide()
        self.ui.send_pb.hide()

        self.ui.refresh_pb.clicked.connect(self.handle_refresh_button)
        self.ui.connect_pb.clicked.connect(self.handle_connect_button)
        self.ui.clear_terminal_pb.clicked.connect(self.handle_clear_terminal)
        self.ui.send_pb.clicked.connect(self.send_input)
        self.ui.send_te.returnPressed.connect(self.send_input)
        self.ui.soft_reset_tb.clicked.connect(self.handle_soft_reset)
        self.ui.unlock_tb.clicked.connect(self.handle_unlock)
        self.ui.homing_tb.clicked.connect(self.handle_homing)
        self.ui.zero_xy_pb.clicked.connect(self.handle_xy_0)
        self.ui.zero_x_pb.clicked.connect(self.handle_x_0)
        self.ui.zero_y_pb.clicked.connect(self.handle_y_0)
        self.ui.zero_z_pb.clicked.connect(self.handle_z_0)
        self.ui.center_tb.clicked.connect(self.handle_center_jog)
        self.ui.xMinusButton.clicked.connect(self.handle_x_minus)
        self.ui.xPlusButton.clicked.connect(self.handle_x_plus)
        self.ui.yMinusButton.clicked.connect(self.handle_y_minus)
        self.ui.yPlusButton.clicked.connect(self.handle_y_plus)
        self.ui.xYPlusButton.clicked.connect(self.handle_xy_plus)
        self.ui.xYPlusMinuButton.clicked.connect(self.handle_x_plus_y_minus)
        self.ui.xYMinusButton.clicked.connect(self.handle_xy_minus)
        self.ui.xYMinusPlusButton.clicked.connect(self.handle_x_minus_y_plus)
        self.ui.z_minus_pb.clicked.connect(self.handle_z_minus)
        self.ui.z_plus_pb.clicked.connect(self.handle_z_plus)

        self.ui.xy_plus_1_pb.clicked.connect(self.handle_xy_plus_1)
        self.ui.xy_minus_1_pb.clicked.connect(self.handle_xy_minus_1)
        self.ui.xy_div_10_pb.clicked.connect(self.handle_xy_div_10)
        self.ui.xy_mul_10_pb.clicked.connect(self.handle_xy_mul_10)
        self.ui.z_plus_1_pb.clicked.connect(self.handle_z_plus_1)
        self.ui.z_minus_1_pb.clicked.connect(self.handle_z_minus_1)
        self.ui.z_div_10_pb.clicked.connect(self.handle_z_div_10)
        self.ui.z_mul_10_pb.clicked.connect(self.handle_z_mul_10)

        self.ui.probe_pb.clicked.connect(self.handle_probe_cmd)
        self.ui.ABL_pb.clicked.connect(self.handle_auto_bed_levelling)
        self.ui.abl_active_chb.stateChanged.connect(
            lambda: self.controlWo.set_abl_active(self.ui.abl_active_chb.isChecked()))
        self.ui.get_bbox_pb.clicked.connect(self.controlWo.get_boundary_box)
        self.ui.x_num_step_sb.valueChanged.connect(self.update_bbox_x_steps)
        self.ui.y_num_step_sb.valueChanged.connect(self.update_bbox_y_steps)

        self.ui.soft_reset_tb.setEnabled(False)
        self.ui.unlock_tb.setEnabled(False)
        self.ui.homing_tb.setEnabled(False)
        self.ui.play_tb.setEnabled(False)
        self.ui.pause_resume_tb.setEnabled(False)
        self.ui.stop_tb.setEnabled(False)
        self.ui.tool_change_tb.setEnabled(False)

        self.ui.ABL_pb.setEnabled(False)
        self.ui.abl_active_chb.setEnabled(False)
        self.ui.get_bbox_pb.setEnabled(False)

        # todo: place the column behavior settings somewhere else
        self.ui.gcode_tw.setColumnWidth(0, 200)
        self.ui.gcode_tw.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.gcode_tw.setColumnWidth(1, 100)
        self.ui.gcode_tw.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.gcode_rb_group = QButtonGroup()
        self.gcode_rb_group.setExclusive(True)

        self.controller_connected_s.connect(lambda connected: self.controlWo.on_controller_connection(connected))
        self.ui.play_tb.clicked.connect(self.play_send_file)
        self.ui.stop_tb.clicked.connect(self.stop_send_file)
        self.ui.pause_resume_tb.clicked.connect(self.pause_resume)
        self.controlWo.stop_send_s.connect(self.stop_send_file)

        self.precalc_gcode_s.connect(self.controlWo.vectorize_new_gcode_file)
        self.select_gcode_s.connect(self.controlWo.select_active_gcode)
        self.controlWo.update_gcode_s.connect(self.visualize_gcode)

        self.init_serial_port_cb()

        self.ui.xy_step_cb.currentTextChanged.connect(self.xy_update_step)
        self.ui.z_step_cb.currentTextChanged.connect(self.z_update_step)
        self.ui.xy_step_val_dsb.setSingleStep(float(self.ui.xy_step_cb.currentText()))
        self.ui.z_step_val_dsb.setSingleStep(float(self.ui.z_step_cb.currentText()))

    def init_serial_port_cb(self):
        """
        Initialize the serial ports list combo-box.

        Returns
        -------

        """
        self.handle_refresh_button()
        lsp = self.app_settings.last_serial_port
        idx_last_serial = self.ui.serial_ports_cb.findText(lsp)
        if idx_last_serial != -1:
            self.ui.serial_ports_cb.setCurrentIndex(idx_last_serial)

    @Slot(list)
    def update_status(self, status_l):
        self.ui.status_l.setText(status_l[0])
        self.update_status_colors(status_l[0])
        self.update_status_buttons(status_l[0])
        self.ui.mpos_x_l.setText('{:.3f}'.format(status_l[1][0]))
        self.ui.mpos_y_l.setText('{:.3f}'.format(status_l[1][1]))
        self.ui.mpos_z_l.setText('{:.3f}'.format(status_l[1][2]))
        self.ui.wpos_x_l.setText('{:.3f}'.format(status_l[2][0]))
        self.ui.wpos_y_l.setText('{:.3f}'.format(status_l[2][1]))
        self.ui.wpos_z_l.setText('{:.3f}'.format(status_l[2][2]))
        self.ctrl_layer.update_pointer(coords=status_l[2])

    def update_status_buttons(self, status):
        sta = status.lower()
        enabled = False
        if "alarm" in sta:
            pass
        elif "run" in sta:
            enabled = True
        elif "jog" in sta:
            enabled = True
        elif "idle" in sta:
            enabled = True
        elif "hold" in sta:
            enabled = True
        elif "not connected" in sta:
            pass

        self.ui.pause_resume_tb.setEnabled(enabled)

    def update_status_colors(self, status):
        sta = status.lower()
        bkg_c = "gray"
        txt_c = "white"
        if "alarm" in sta:
            bkg_c = "red"
            txt_c = "white"
        elif "run" in sta:
            bkg_c = "green"
            txt_c = "black"
        elif "jog" in sta:
            bkg_c = "blue"
            txt_c = "white"
        elif "idle" in sta:
            bkg_c = "yellow"
            txt_c = "black"
        elif "not connected" in sta:
            bkg_c = "dark gray"
            txt_c = "black"

        self.ui.status_l.setStyleSheet("QLabel { background-color : " + bkg_c + "; color : " + txt_c + "; }")

    def element_not_in_table(self, element):
        """
        Search if there is an element in the gcode table.

        Parameters
        ----------
        element: str
            gcode path string.

        Returns
        -------
        bool
                True if element is not in table, False if element is in table.
        """
        num_rows = self.ui.gcode_tw.rowCount()
        for row in range(0, num_rows):
            if element == self.ui.gcode_tw.cellWidget(row, 0).toolTip():
                return False
        return True

    def open_gcode_files(self):
        load_gcode = QFileDialog.getOpenFileNames(None,
                                                  "Load G-Code File(s)",
                                                  self.app_settings.gcode_last_dir,
                                                  "G-Code Files (*.gcode)" + ";;All files (*.*)")  # todo: add other file extensions
        logging.debug(load_gcode)
        load_gcode_paths = load_gcode[0]
        if load_gcode_paths:
            self.app_settings.gcode_last_dir = os.path.dirname(load_gcode_paths[0])  # update setting
            for elem in load_gcode_paths:
                if self.element_not_in_table(elem):
                    self.precalc_gcode_s.emit(elem)
                    num_rows = self.ui.gcode_tw.rowCount()
                    self.ui.gcode_tw.insertRow(num_rows)
                    # The total path is just in the ToolTip while the name shown is only the name
                    new_le = QLineEdit(os.path.basename(elem))
                    new_le.setReadOnly(True)
                    new_le.setToolTip(elem)
                    self.ui.gcode_tw.setCellWidget(num_rows, 0, new_le)
                    column = 1
                    row = num_rows
                    new_rb = QRadioButton()
                    new_rb.setStyleSheet(StyleManager.set_radio_btn_style_sheet())
                    self.gcode_rb_group.addButton(new_rb)
                    self.ui.gcode_tw.setCellWidget(row, column, new_rb)
                    index = QPersistentModelIndex(
                        self.ui.gcode_tw.model().index(row, column))
                    new_rb.toggled.connect(
                        lambda *args, index=index: self.print_button_item_clicked(index))

    @Slot(QTableWidgetItem)
    def print_button_item_clicked(self, index):
        if index.isValid():
            row = index.row()
            gcode_path = self.ui.gcode_tw.cellWidget(row, 0).toolTip()
            if self.ui.gcode_tw.cellWidget(row, 1).isChecked():
                # read the tooltip
                logging.debug(gcode_path)
                self.select_gcode_s.emit(gcode_path)
                self.ui.ABL_pb.setEnabled(True)
                self.ui.abl_active_chb.setEnabled(True)
                self.ui.get_bbox_pb.setEnabled(True)
                if self.serial_connection_status:
                    self.ui.play_tb.setEnabled(True)
            else:
                tag, ov = self.controlWo.get_gcode_data(gcode_path)
                self.visualize_gcode(tag, ov, visible=False)

    def visualize_gcode(self, tag, ov, visible=True, redraw=False):
        if tag not in list(self.ctrl_layer.get_paths_tag()):
            self.ctrl_layer.add_gcode(tag, ov)
        elif redraw:
            self.ctrl_layer.remove_gcode(tag)
            self.ctrl_layer.add_gcode(tag, ov)

        self.ctrl_layer.set_gcode_visible(tag, visible)

    def gcode_cb_update(self):
        pass  # todo: to be implemented.

    def play_send_file(self):
        if self.serial_connection_status:
            num_rows = self.ui.gcode_tw.rowCount()
            for row in range(0, num_rows):
                if self.ui.gcode_tw.cellWidget(row, 1).isChecked():
                    self.send_gcode_s.emit(self.ui.gcode_tw.cellWidget(row, 0).toolTip())
                    self.ui.play_tb.setEnabled(False)
                    self.ui.stop_tb.setEnabled(True)
                    self.ui.unlock_tb.setEnabled(False)
                    self.ui.homing_tb.setEnabled(False)
                    self.enable_gcode_rb(False)

    def stop_send_file(self):
        self.stop_gcode_s.emit()
        self.enable_gcode_rb(True)
        self.ui.stop_tb.setEnabled(False)
        self.ui.unlock_tb.setEnabled(True)
        self.ui.homing_tb.setEnabled(True)
        if self.serial_connection_status:
            self.ui.play_tb.setEnabled(True)

    def pause_resume(self):
        self.pause_resume_gcode_s.emit()

    def enable_gcode_rb(self, enabling):
        num_rows = self.ui.gcode_tw.rowCount()
        for row in range(0, num_rows):
            self.ui.gcode_tw.cellWidget(row, 1).setEnabled(enabling)

    def is_gcode_rb_selected(self):
        num_rows = self.ui.gcode_tw.rowCount()
        for row in range(0, num_rows):
            if self.ui.gcode_tw.cellWidget(row, 1).isChecked():
                return True
        return False

    @Slot(list)
    def update_probe(self, probe_l):
        pass

    @Slot(str)
    def update_console_text(self, new_text):
        self.ui.serial_te.append(new_text)

    def send_input(self):
        """Send input to the serial port."""
        # self.serialTxQu.put(self.ui.send_te.text() + "\n")
        self.ui_serial_send_s.emit(self.ui.send_te.text() + "\n")
        self.ui.send_te.clear()

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        current_port = self.ui.serial_ports_cb.currentText()
        ls = self.serialWo.get_port_list()
        if ls:
            logger.debug("Available ports: " + str(ls))
            self.ui.serial_ports_cb.clear()
            self.ui.serial_ports_cb.addItems(ls)
        else:
            logger.info('No serial ports available.')
            self.ui.serial_te.append('No serial ports available.')
            self.ui.serial_ports_cb.clear()
        idx_last_serial = self.ui.serial_ports_cb.findText(current_port)
        if idx_last_serial != -1:
            self.ui.serial_ports_cb.setCurrentIndex(idx_last_serial)

    def handle_connect_button(self):
        """Connect/Disconnect button opens/closes the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        if not self.serial_connection_status:
            self.ui_serial_open_s.emit(self.ui.serial_ports_cb.currentText())
        else:
            self.ui_serial_close_s.emit()
            self.act_on_disconnection()

    @Slot(bool)
    def act_on_connection(self, connection_status):
        if connection_status:
            self.serial_connection_status = True
            self.controlWo.reset_controller_status_s.emit()
            self.ui.connect_pb.setText("Disconnect")
            self.ui.serial_ports_cb.hide()
            self.ui.serial_baud_cb.hide()
            self.ui.refresh_pb.hide()
            self.ui.send_te.show()
            self.ui.send_pb.show()
            self.ui.soft_reset_tb.setEnabled(True)
            self.ui.unlock_tb.setEnabled(True)
            self.ui.homing_tb.setEnabled(True)
            if self.is_gcode_rb_selected():
                self.ui.play_tb.setEnabled(True)
            self.controller_connected_s.emit(True)
            self.ctrl_layer.create_pointer(coords=(0, 0, 0))

    def act_on_disconnection(self):
        self.controlWo.reset_controller_status_s.emit()
        self.serial_connection_status = False
        self.ui.connect_pb.setText("Connect")
        self.ui.serial_ports_cb.show()
        self.ui.serial_baud_cb.show()
        self.ui.refresh_pb.show()
        self.ui.send_te.hide()
        self.ui.send_pb.hide()
        self.ui.status_l.setText("Not Connected")
        self.update_status_colors("Not Connected")
        self.ui.soft_reset_tb.setEnabled(False)
        self.ui.unlock_tb.setEnabled(False)
        self.ui.homing_tb.setEnabled(False)
        self.ui.play_tb.setEnabled(False)
        self.ui.stop_tb.setEnabled(False)
        self.ui.pause_resume_tb.setEnabled(False)
        self.controller_connected_s.emit(False)
        self.ctrl_layer.remove_pointer()

    def handle_clear_terminal(self):
        self.ui.serial_te.clear()

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()

    def handle_soft_reset(self):
        logging.info("Soft Reset Command")
        self.ui_serial_send_bytes_s.emit(b'\x18')

    def handle_unlock(self):
        logging.debug("Unlock Command")
        self.ui_serial_send_s.emit("$X\n")

    def handle_homing(self):
        logging.debug("Homing Command")
        self.ui_serial_send_s.emit("$H\n")

    def handle_xy_0(self):
        logging.debug("XY = 0")
        self.ui_serial_send_s.emit("G10 P1 L20 X0 Y0\n")

    def handle_x_0(self):
        logging.debug("X = 0")
        self.ui_serial_send_s.emit("G10 P1 L20 X0\n")

    def handle_y_0(self):
        logging.debug("Y = 0")
        self.ui_serial_send_s.emit("G10 P1 L20 Y0\n")

    def handle_z_0(self):
        logging.debug("Z = 0")
        self.ui_serial_send_s.emit("G10 P1 L20 Z0\n")

    def handle_center_jog(self):
        logging.debug("Go to XY working 0")
        self.ui_serial_send_s.emit("G90 G0 X0 Y0\n")

    def z_update_step(self):
        new_step_str = self.ui.z_step_cb.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.
        self.ui.z_step_val_dsb.setSingleStep(new_step_fl)
        self.ui.z_plus_1_pb.setText("+" + new_step_str)
        self.ui.z_minus_1_pb.setText("-" + new_step_str)

    def handle_x_minus(self):
        logging.debug("X_minus Command")
        x_min_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 X-" + str(x_min_val) + " F100000\n")

    def handle_x_plus(self):
        logging.debug("X_plus Command")
        x_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 X" + str(x_plus_val) + " F100000\n")

    def handle_y_minus(self):
        logging.debug("Y_minus Command")
        y_min_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 Y-" + str(y_min_val) + " F100000\n")

    def handle_y_plus(self):
        logging.debug("Y_plus Command")
        y_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 Y" + str(y_plus_val) + " F100000\n")

    def handle_xy_plus(self):
        logging.debug("XY_plus Command")
        xy_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 X" + str(xy_plus_val) + "Y" + str(xy_plus_val) + " F100000\n")

    def handle_x_plus_y_minus(self):
        logging.debug("X_plus_Y_minus Command")
        x_p_y_m_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 X" + str(x_p_y_m_val) + "Y-" + str(x_p_y_m_val) + " F100000\n")

    def handle_xy_minus(self):
        logging.debug("XY_minus Command")
        xy_minus_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 X-" + str(xy_minus_val) + "Y-" + str(xy_minus_val) + " F100000\n")

    def handle_x_minus_y_plus(self):
        logging.debug("X_minus_y_plus Command")
        x_m_y_p_val = self.ui.xy_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 X-" + str(x_m_y_p_val) + "Y" + str(x_m_y_p_val) + " F100000\n")

    def handle_z_minus(self):
        logging.debug("Z_minus Command")
        z_minus_val = self.ui.z_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 Z-" + str(z_minus_val) + " F100000\n")

    def handle_z_plus(self):
        logging.debug("Z_plus Command")
        z_plus_val = self.ui.z_step_val_dsb.value()
        self.ui_serial_send_s.emit("$J=G91 Z" + str(z_plus_val) + " F100000\n")

    def xy_update_step(self):
        new_step_str = self.ui.xy_step_cb.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.
        self.ui.xy_step_val_dsb.setSingleStep(new_step_fl)
        self.ui.xy_plus_1_pb.setText("+" + new_step_str)
        self.ui.xy_minus_1_pb.setText("-" + new_step_str)

    def handle_xy_plus_1(self):
        xy_val = self.ui.xy_step_val_dsb.value() + self.ui.xy_step_val_dsb.singleStep()
        self.ui.xy_step_val_dsb.setValue(xy_val)

    def handle_xy_minus_1(self):
        xy_val = self.ui.xy_step_val_dsb.value() - self.ui.xy_step_val_dsb.singleStep()
        self.ui.xy_step_val_dsb.setValue(xy_val)

    def handle_xy_div_10(self):
        xy_value = self.ui.xy_step_val_dsb.value()
        xy_value /= 10.0  # self.xy_value / 10.0
        # if not xy_value < 0.01:  # Minimum step is 0.01
        self.ui.xy_step_val_dsb.setValue(xy_value)

    def handle_xy_mul_10(self):
        xy_value = self.ui.xy_step_val_dsb.value()
        self.ui.xy_step_val_dsb.setValue(xy_value*10.0)

    def handle_z_plus_1(self):
        z_val = self.ui.z_step_val_dsb.value() + self.ui.z_step_val_dsb.singleStep()
        self.ui.z_step_val_dsb.setValue(z_val)

    def handle_z_minus_1(self):
        z_val = self.ui.z_step_val_dsb.value() - self.ui.z_step_val_dsb.singleStep()
        self.ui.z_step_val_dsb.setValue(z_val)

    def handle_z_div_10(self):
        z_value = self.ui.z_step_val_dsb.value()
        self.ui.z_step_val_dsb.setValue(z_value/10.0)

    def handle_z_mul_10(self):
        z_value = self.ui.z_step_val_dsb.value()
        self.ui.z_step_val_dsb.setValue(z_value*10.0)

    def handle_probe_cmd(self):
        logging.debug("Probe Command")
        # todo: fake parameters just to test probe
        probe_z_max = -11.0
        probe_feed_rate = 10.0
        self.controlWo.cmd_probe(probe_z_max, probe_feed_rate)

    def handle_auto_bed_levelling(self):
        logging.debug("Auto Bed Levelling Command")
        # todo: fake parameters just for testing ABL
        xy_coord_list = [(0.0, 0.0), (0.0, 10.0), (0.0, 20.0),
                         (10.0, 0.0), (10.0, 10.0), (10.0, 20.0),
                         (20.0, 0.0), (20.0, 10.0), (20.0, 20.0)]
        travel_z = 1.0
        probe_z_max = -11.0
        probe_feed_rate = 10.0
        bbox_t, steps_t = self.get_abl_inputs()
        self.controlWo.send_abl_s.emit(bbox_t, steps_t)
        # self.controlWo.cmd_auto_bed_levelling(xy_coord_list, travel_z, probe_z_max, probe_feed_rate)

    @Slot(float)
    def update_progress_bar(self, prog_percentage):
        logger.debug(prog_percentage)
        self.ui.progressBar.setValue(prog_percentage)

    @Slot()
    def update_bbox_x_steps(self):
        x_steps = abs(self.ui.x_max_dsb.value() - self.ui.x_min_dsb.value()) / self.ui.x_num_step_sb.value()
        self.ui.x_step_dsb.setValue(x_steps)

    @Slot()
    def update_bbox_y_steps(self):
        y_steps = abs(self.ui.y_max_dsb.value() - self.ui.y_min_dsb.value()) / self.ui.y_num_step_sb.value()
        self.ui.y_step_dsb.setValue(y_steps)

    def update_bbox_steps(self):
        self.update_bbox_x_steps()
        self.update_bbox_y_steps()

    @Slot(tuple)
    def update_bbox(self, bbox_t):
        logger.debug(bbox_t)
        self.ui.x_min_dsb.setValue(bbox_t[0])
        self.ui.y_min_dsb.setValue(bbox_t[1])
        self.ui.z_min_dsb.setValue(-11.0)
        self.ui.x_max_dsb.setValue(bbox_t[3])
        self.ui.y_max_dsb.setValue(bbox_t[4])
        self.ui.z_max_dsb.setValue(bbox_t[5])
        self.update_bbox_steps()

    def get_abl_inputs(self):
        bbox_t = (
            self.ui.x_min_dsb.value(),
            self.ui.y_min_dsb.value(),
            self.ui.z_min_dsb.value(),
            self.ui.x_max_dsb.value(),
            self.ui.y_max_dsb.value(),
            self.ui.z_max_dsb.value()
        )
        steps_t = (
            self.ui.x_num_step_sb.value(),
            self.ui.y_num_step_sb.value()
        )
        return bbox_t, steps_t


