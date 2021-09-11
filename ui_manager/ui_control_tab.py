from PySide2.QtCore import Signal, Slot, QObject, QSize, Qt, QPersistentModelIndex
from PySide2.QtWidgets import QFileDialog, QLineEdit, QRadioButton, QTableWidgetItem, \
                              QHeaderView, QCheckBox, QButtonGroup
from style_manager import StyleManager
import os
import logging

logger = logging.getLogger(__name__)


class UiControlTab(QObject):
    """Class dedicated to UI <--> Control interactions on Control Tab. """
    ui_serial_send_s = Signal(str)

    send_gcode_s = Signal(str)                   # Signal to start sending a gcode file
    stop_gcode_s = Signal()                      # Signal to stop sending a gcode file
    pause_resume_gcode_s = Signal()              # Signal to pause/resume sending a gcode file

    precalc_gcode_s = Signal(str)
    select_gcode_s = Signal(str)

    def __init__(self, ui, control_worker, serial_worker, ctrl_layer, app_settings):
        super(UiControlTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.ctrl_layer = ctrl_layer
        self.app_settings = app_settings

        self.ui.xy_jog_l.setText("XY [" + str(self.ui.xy_step_val_dsb.value()) + " mm]")
        self.ui.z_jog_l.setText("Z [" + str(self.ui.z_step_val_dsb.value()) + " mm]")

        self.serial_connection_status = False
        self.ui_serial_send_s.connect(self.serialWo.send)
        self.controlWo.update_status_s.connect(self.update_status)
        self.controlWo.update_probe_s.connect(self.update_probe)
        self.controlWo.update_console_text_s.connect(self.update_console_text)
        self.controlWo.update_file_progress_s.connect(self.update_progress_bar)

        self.send_gcode_s.connect(self.controlWo.send_gcode_file)

        # From Controller Manager to Serial Manager
        self.controlWo.serial_send_s.connect(self.serialWo.send)
        self.controlWo.serial_tx_available_s.connect(self.serialWo.send_from_queue)

        # From Serial Manager to UI Manager
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
        self.ui.unlock_tb.clicked.connect(self.handle_unlock)
        self.ui.homing_tb.clicked.connect(self.handle_homing)
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

        self.ui.unlock_tb.setEnabled(False)
        self.ui.homing_tb.setEnabled(False)
        self.ui.play_tb.setEnabled(False)
        self.ui.pause_resume_tb.setEnabled(False)
        self.ui.stop_tb.setEnabled(False)
        self.ui.tool_change_tb.setEnabled(False)

        # todo: place the column behavior settings somewhere else
        self.ui.gcode_tw.setColumnWidth(0, 200)
        self.ui.gcode_tw.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.gcode_tw.setColumnWidth(1, 100)
        self.ui.gcode_tw.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.gcode_rb_group = QButtonGroup()
        self.gcode_rb_group.setExclusive(True)
        self.ui.play_tb.clicked.connect(self.play_send_file)

        self.precalc_gcode_s.connect(self.controlWo.vectorize_new_gcode_file)
        self.select_gcode_s.connect(self.controlWo.get_gcode)
        self.controlWo.update_gcode_s.connect(self.visualize_gcode)

    @Slot(list)
    def update_status(self, status_l):
        self.ui.status_l.setText(status_l[0])
        self.update_status_colors(status_l[0])
        self.ui.mpos_x_label.setText(status_l[1][0])
        self.ui.mpos_y_label.setText(status_l[1][1])
        self.ui.mpos_z_label.setText(status_l[1][2])

    def update_status_colors(self, status):
        sta = status.lower()
        bkg_c = "gray"
        txt_c = "white"
        if "alarm" in sta:
            bkg_c = "red"
            txt_c = "white"
        elif "running" in sta:
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
        """ Search if there is an element in the gcode table.
            The element shall be the gcode path, a string.
            :returns True if element is not in table
            :returns False if element is in table. """
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
            else:
                print(gcode_path)
                tag, ov = self.controlWo.get_gcode_data(gcode_path)
                print(tag)
                self.visualize_gcode(tag, ov, False)

    def visualize_gcode(self, tag, ov, visible=True):
        print(list(self.ctrl_layer.get_paths_tag()))
        if tag not in list(self.ctrl_layer.get_paths_tag()):
            self.ctrl_layer.add_gcode(tag, ov)

        self.ctrl_layer.set_gcode_visible(tag, visible)

    def gcode_cb_update(self):
        pass  # todo: to be implemented.

    def play_send_file(self):
        print(self.ui.gcode_tw.selectedItems())
        print(self.ui.gcode_tw.currentItem())
        # gcode_path = self.ui.gcode_tw.selectedItems.cellWidget(row, 0).toolTip()
        self.ui.play_tb.setEnabled(True)

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
                self.ui.connect_pb.setText("Disconnect")
                self.ui.serial_ports_cb.hide()
                self.ui.serial_baud_cb.hide()
                self.ui.refresh_pb.hide()
                self.ui.send_te.show()
                self.ui.send_pb.show()
                self.ui.unlock_tb.setEnabled(True)
                self.ui.homing_tb.setEnabled(True)
        else:
            self.serialWo.close_port()
            self.serial_connection_status = False
            self.ui.connect_pb.setText("Connect")
            self.ui.serial_ports_cb.show()
            self.ui.serial_baud_cb.show()
            self.ui.refresh_pb.show()
            self.ui.send_te.hide()
            self.ui.send_pb.hide()
            self.ui.status_l.setText("Not Connected")
            self.update_status_colors("Not Connected")
            self.ui.unlock_tb.setEnabled(False)
            self.ui.homing_tb.setEnabled(False)

    def handle_clear_terminal(self):
        self.ui.serial_te.clear()

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()

    def handle_unlock(self):
        logging.debug("Unlock Command")
        self.ui_serial_send_s.emit("$X\n")

    def handle_homing(self):
        logging.debug("Homing Command")
        self.ui_serial_send_s.emit("$H\n")

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

    def handle_xy_plus_1(self):
        xy_val = self.ui.xy_step_val_dsb.value() + self.ui.xy_step_val_dsb.singleStep()
        self.ui.xy_step_val_dsb.setValue(xy_val)

    def handle_xy_minus_1(self):
        xy_val = self.ui.xy_step_val_dsb.value() - self.ui.xy_step_val_dsb.singleStep()
        self.ui.xy_step_val_dsb.setValue(xy_val)

    def handle_xy_div_10(self):
        xy_step_val = self.ui.xy_step_val_dsb.singleStep()
        if not xy_step_val == 0.01:  # Minimum step is 0.01
            xy_step_val /= 10.0  # self.xy_step_val / 10.0
            self.ui.xy_step_val_dsb.setSingleStep(xy_step_val)
            self.ui.xy_jog_l.setText("XY [" + str(xy_step_val) + " mm]")

    def handle_xy_mul_10(self):
        xy_step_val = self.ui.xy_step_val_dsb.singleStep()
        if not xy_step_val == 100.0:  # Maximum step is 100.0
            xy_step_val = self.ui.xy_step_val_dsb.singleStep() * 10.0  # xy_step_val * 10.0
            self.ui.xy_step_val_dsb.setSingleStep(xy_step_val)
            self.ui.xy_jog_l.setText("XY [" + str(xy_step_val) + " mm]")

    def handle_z_plus_1(self):
        z_val = self.ui.z_step_val_dsb.value() + self.ui.z_step_val_dsb.singleStep()
        self.ui.z_step_val_dsb.setValue(z_val)

    def handle_z_minus_1(self):
        z_val = self.ui.z_step_val_dsb.value() - self.ui.z_step_val_dsb.singleStep()
        self.ui.z_step_val_dsb.setValue(z_val)

    def handle_z_div_10(self):
        z_step_val = self.ui.z_step_val_dsb.singleStep()
        if not z_step_val == 0.01:  # Minimum step is 0.01
            z_step_val /= 10.0
            self.ui.z_step_val_dsb.setSingleStep(z_step_val)
            self.ui.z_jog_l.setText("Z [" + str(z_step_val) + " mm]")

    def handle_z_mul_10(self):
        z_step_val = self.ui.z_step_val_dsb.singleStep()
        if not z_step_val == 100.0:  # Maximum step is 100.0
            z_step_val *= 10.0
            self.ui.z_step_val_dsb.setSingleStep(z_step_val)
            self.ui.z_jog_l.setText("Z [" + str(z_step_val) + " mm]")

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
        self.controlWo.cmd_auto_bed_levelling(xy_coord_list, travel_z, probe_z_max, probe_feed_rate)

    @Slot(float)
    def update_progress_bar(self, prog_percentage):
        logger.info(prog_percentage)
        self.ui.progressBar.setValue(prog_percentage)


