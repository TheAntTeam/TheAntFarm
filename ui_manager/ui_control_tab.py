from PySide2.QtCore import Signal, Slot, QObject, QSize, Qt, QPersistentModelIndex
from PySide2.QtWidgets import QFileDialog, QLineEdit, QRadioButton, QHeaderView, QButtonGroup
from PySide2.QtGui import QIcon
from style_manager import StyleManager
import os
import logging

logger = logging.getLogger(__name__)


class UiControlTab(QObject):
    """Class dedicated to UI <--> Control interactions on Control Tab. """
    controller_connected_s = Signal(bool)
    ui_serial_send_s = Signal(str)
    ui_serial_open_s = Signal(str, int)
    ui_serial_close_s = Signal()

    send_gcode_s = Signal(str)                   # Signal to start sending a gcode file
    stop_gcode_s = Signal()                      # Signal to stop sending a gcode file
    pause_resume_gcode_s = Signal()              # Signal to pause/resume sending a gcode file

    precalc_gcode_s = Signal(str)
    select_gcode_s = Signal(str)

    ui_send_cmd_s = Signal(str, tuple)

    def __init__(self, ui, control_worker, serial_worker, ctrl_layer, settings):
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
        settings: SettingsHandler
            Handler object that allows the access to all the settings.
        """
        super(UiControlTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker
        self.ctrl_layer = ctrl_layer
        self.app_settings = settings.app_settings
        self.gcf_settings = settings.gcf_settings
        self.machine_settings = settings.machine_settings

        self.holding_status = False
        self.serial_connection_status = False
        self.serial_ports_name_ls = []
        self.serial_ports_baudrate_ls = []
        self.ui_serial_send_s.connect(self.controlWo.execute_gcode_cmd)
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
        self.controlWo.gcode_vectorized_s.connect(self.enable_gcode_cb)
        self.controlWo.serial_send_s.connect(self.serialWo.send)
        self.controlWo.serial_tx_available_s.connect(self.serialWo.send_from_queue)

        # From Serial Manager to UI Manager
        self.serialWo.get_port_list_s.connect(self.get_ports_and_bauds)
        self.serialWo.open_port_s.connect(self.act_on_connection)
        self.serialWo.close_for_error_s.connect(self.handle_connect_button)
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
        self.ui.tool_change_tb.clicked.connect(self.handle_tool_change_start)
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
        self.ui.x_min_dsb.valueChanged.connect(self.update_bbox_x_steps)
        self.ui.x_max_dsb.valueChanged.connect(self.update_bbox_x_steps)
        self.ui.x_num_step_sb.valueChanged.connect(self.update_bbox_x_steps)
        self.ui.y_min_dsb.valueChanged.connect(self.update_bbox_y_steps)
        self.ui.y_max_dsb.valueChanged.connect(self.update_bbox_y_steps)
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

        self.ui.upload_temp_tb.clicked.connect(self.update_temporary_gcode_files)
        self.ui.remove_gcode_tb.clicked.connect(self.remove_gcode_files)

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

        self.ui_send_cmd_s.connect(self.controlWo.execute_user_interface_cmd)

        self.init_xy_jog_step_value()
        self.init_z_jog_step_value()

        self.init_serial_port_cb()

        self.ui.z_min_dsb.setValue(self.machine_settings.probe_z_min)
        self.ui.z_max_dsb.setValue(self.machine_settings.probe_z_max)
        self.ui.z_min_dsb.valueChanged.connect(self.handle_z_min_changed)
        self.ui.z_max_dsb.valueChanged.connect(self.handle_z_max_changed)

    def init_xy_jog_step_value(self):
        """ Initialize XY step and value ui fields. """
        self.ui.xy_step_cb.setCurrentIndex(self.machine_settings.xy_step_idx)
        self.xy_update_step()
        self.ui.xy_step_val_dsb.setValue(self.machine_settings.xy_step_value)
        self.ui.xy_step_cb.currentTextChanged.connect(self.xy_update_step)
        self.ui.xy_step_val_dsb.valueChanged.connect(self.xy_update_value)

    def init_z_jog_step_value(self):
        """ Initialize Z step and value ui fields. """
        self.ui.z_step_cb.setCurrentIndex(self.machine_settings.z_step_idx)
        self.z_update_step()
        self.ui.z_step_val_dsb.setValue(self.machine_settings.z_step_value)
        self.ui.z_step_cb.currentTextChanged.connect(self.z_update_step)
        self.ui.z_step_val_dsb.valueChanged.connect(self.z_update_value)

    def init_serial_port_cb(self):
        """ Initialize the serial ports' ui elements. """
        self.handle_refresh_button()

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
        holding = False
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
            holding = True
        elif "not connected" in sta:
            pass

        if holding:
            if not self.holding_status:
                self.holding_status = True
                icon = QIcon()
                icon.addFile(u":/resources/resources/icons/white-play-and-pause-button.svg", QSize(), QIcon.Normal,
                             QIcon.Off)
                icon.addFile(u":/resources/resources/icons/gray-play-and-pause-button.svg", QSize(), QIcon.Disabled,
                             QIcon.Off)
                icon.addFile(u":/resources/resources/icons/gray-play-and-pause-button.svg", QSize(), QIcon.Disabled,
                             QIcon.On)
                self.ui.pause_resume_tb.setIcon(icon)
                self.ui.pause_resume_tb.setIconSize(QSize(64, 64))
                self.ui.pause_resume_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)
        else:
            if self.holding_status:
                self.holding_status = False
                icon = QIcon()
                icon.addFile(u":/resources/resources/icons/white-pause-multimedia-big-gross-symbol-lines.svg", QSize(),
                             QIcon.Normal, QIcon.Off)
                icon.addFile(u":/resources/resources/icons/gray-pause-multimedia-big-gross-symbol-lines.svg", QSize(),
                             QIcon.Disabled, QIcon.Off)
                icon.addFile(u":/resources/resources/icons/gray-pause-multimedia-big-gross-symbol-lines.svg", QSize(),
                             QIcon.Disabled, QIcon.On)
                self.ui.pause_resume_tb.setIcon(icon)
                self.ui.pause_resume_tb.setIconSize(QSize(64, 64))
                self.ui.pause_resume_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

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

    def element_in_table(self, element):
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
            tool_t = self.ui.gcode_tw.cellWidget(row, 0).toolTip()
            if element == tool_t:
                return row
        return -1

    def open_gcode_files(self):
        load_gcode = QFileDialog.getOpenFileNames(None,
                                                  "Load G-Code File(s)",
                                                  self.app_settings.gcode_last_dir,
                                                  "G-Code Files (*.gcode)" + ";;All files (*.*)")  # todo: add other file extensions
        logger.debug(load_gcode)
        load_gcode_paths = load_gcode[0]
        if load_gcode_paths:
            self.app_settings.gcode_last_dir = os.path.dirname(load_gcode_paths[0])  # update setting
            self._open_gcode_file(load_gcode_paths)

    def _open_gcode_file(self, load_gcode_paths):
        if load_gcode_paths:
            for elem_not_norm in load_gcode_paths:
                elem = os.path.normpath(elem_not_norm)
                elem_row = self.element_in_table(elem)
                if elem_row < 0:
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
                    new_rb.setEnabled(False)
                    self.gcode_rb_group.addButton(new_rb)
                    self.ui.gcode_tw.setCellWidget(row, column, new_rb)
                    index = QPersistentModelIndex(
                        self.ui.gcode_tw.model().index(row, column))
                    new_rb.toggled.connect(
                        lambda *args, index=index: self.gcode_item_selected(index))
                else:
                    if self.ui.gcode_tw.cellWidget(elem_row, 1).isChecked():
                        tag, ov = self.controlWo.get_gcode_data(elem)
                        self.visualize_gcode(tag, ov, visible=True, redraw=True)

                self.precalc_gcode_s.emit(elem)

    @Slot(str)
    def enable_gcode_cb(self, gcode_path):
        row = self.element_in_table(gcode_path)
        if row >= 0:
            self.ui.gcode_tw.cellWidget(row, 1).setEnabled(True)

    @Slot(int)
    def gcode_item_selected(self, index):
        if index.isValid():
            row = index.row()
            gcode_path = self.ui.gcode_tw.cellWidget(row, 0).toolTip()
            if self.ui.gcode_tw.cellWidget(row, 1).isChecked():
                # read the tooltip
                logger.debug(gcode_path)
                self.select_gcode_s.emit(gcode_path)
                self.ui.ABL_pb.setEnabled(True)
                self.ui.abl_active_chb.setEnabled(True)
                self.ui.get_bbox_pb.setEnabled(True)
                if self.serial_connection_status:
                    self.ui.play_tb.setEnabled(True)
            else:
                tag, ov = self.controlWo.get_gcode_data(gcode_path)
                self.visualize_gcode(tag, ov, visible=False)

    def update_temporary_gcode_files(self):
        temp_dir = self.gcf_settings.gcode_folder
        gcode_l = []
        for file in os.listdir(temp_dir):
            if file.endswith(".gcode"):
                gcode_l.append(os.path.join(temp_dir, file))

        if gcode_l:
            self._open_gcode_file(gcode_l)

    def remove_gcode_files(self):
        rows = set([x.row() for x in self.ui.gcode_tw.selectedIndexes()])
        for row in sorted(rows, reverse=True):
            gcode_path = self.ui.gcode_tw.cellWidget(row, 0).toolTip()
            tag, _ = self.controlWo.get_gcode_data(gcode_path)
            self.ctrl_layer.remove_gcode(tag)
            self.ui.gcode_tw.removeRow(row)

    def visualize_gcode(self, tag, ov, visible=True, redraw=False):
        if tag not in list(self.ctrl_layer.get_paths_tag()):
            self.ctrl_layer.add_gcode(tag, ov)
        elif redraw:
            self.ctrl_layer.remove_gcode(tag)
            self.ctrl_layer.add_gcode(tag, ov)

        self.ctrl_layer.set_gcode_visible(tag, visible)

    def get_selected_file(self):
        num_rows = self.ui.gcode_tw.rowCount()
        checked_row = -1
        for row in range(0, num_rows):
            if self.ui.gcode_tw.cellWidget(row, 1).isChecked() and checked_row < 0:
                checked_row = row
        return checked_row

    def disable_during_send(self):
        self.ui.play_tb.setEnabled(False)
        self.ui.stop_tb.setEnabled(True)
        self.ui.unlock_tb.setEnabled(False)
        self.ui.homing_tb.setEnabled(False)
        self.ui.tool_change_tb.setEnabled(False)
        self.enable_gcode_rb(False)

    def enable_after_send(self):
        self.ui.stop_tb.setEnabled(False)
        self.ui.unlock_tb.setEnabled(True)
        self.ui.homing_tb.setEnabled(True)
        self.ui.tool_change_tb.setEnabled(True)
        checked_row = self.get_selected_file()
        if self.serial_connection_status and checked_row >= 0:
            self.ui.play_tb.setEnabled(True)

    def play_send_file(self):
        if self.serial_connection_status:
            checked_row = self.get_selected_file()
            if checked_row >= 0:
                self.send_gcode_s.emit(self.ui.gcode_tw.cellWidget(checked_row, 0).toolTip())
                self.disable_during_send()

    def stop_send_file(self):
        self.stop_gcode_s.emit()
        self.enable_gcode_rb(True)
        self.enable_after_send()

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
        pruned_text = new_text.strip()
        self.ui.serial_te.append(pruned_text)

    def send_input(self):
        """Send input to the serial port."""
        # self.serialTxQu.put(self.ui.send_te.text() + "\n")
        self.ui_serial_send_s.emit(self.ui.send_te.text() + "\n")
        self.ui.send_te.clear()

    @Slot(list, list)
    def get_ports_and_bauds(self, port_names, baudrates):
        self.serial_ports_name_ls = port_names
        self.serial_ports_baudrate_ls = baudrates
        current_port = self.ui.serial_ports_cb.currentText()
        current_baud = self.ui.serial_baud_cb.currentText()
        idx_last_serial = self.ui.serial_ports_cb.findText(current_port)
        idx_last_baud = self.ui.serial_baud_cb.findText(current_baud)
        if self.serial_ports_name_ls:
            logger.debug("Available ports: " + str(self.serial_ports_name_ls))
            self.ui.serial_ports_cb.clear()
            self.ui.serial_ports_cb.addItems(self.serial_ports_name_ls)
            self.ui.serial_baud_cb.clear()
            self.ui.serial_baud_cb.addItems([str(baud) for baud in baudrates])
        else:
            logger.info('No serial ports available.')
            self.ui.serial_te.append('No serial ports available.')
            self.ui.serial_ports_cb.clear()
            self.ui.serial_baud_cb.clear()

        if idx_last_serial != -1:
            self.ui.serial_ports_cb.setCurrentIndex(idx_last_serial)
        else:
            lsp = self.app_settings.last_serial_port
            idx_last_serial = self.ui.serial_ports_cb.findText(lsp)
            if idx_last_serial != -1:
                self.ui.serial_ports_cb.setCurrentIndex(idx_last_serial)

        if idx_last_baud != -1:
            self.ui.serial_baud_cb.setCurrentIndex(idx_last_baud)
        else:
            idx_default_baud = self.ui.serial_baud_cb.findText(str(self.app_settings.last_serial_baud))
            if idx_default_baud != -1:
                self.ui.serial_baud_cb.setCurrentIndex(idx_default_baud)

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        self.serialWo.refresh_port_list_s.emit()

    def handle_connect_button(self):
        """Connect/Disconnect button opens/closes the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        if not self.serial_connection_status:
            self.ui_serial_open_s.emit(self.ui.serial_ports_cb.currentText(),
                                       int(self.ui.serial_baud_cb.currentText()))
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
            self.ui.tool_change_tb.setEnabled(True)
            if self.is_gcode_rb_selected():
                self.ui.play_tb.setEnabled(True)
            self.controller_connected_s.emit(True)
            self.ctrl_layer.create_pointer(coords=(0, 0, 0))

            self.ui.get_tool_probe_pb.setEnabled(True)
            self.ui.get_tool_change_pb.setEnabled(True)

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
        self.ui.tool_change_tb.setEnabled(False)
        self.controller_connected_s.emit(False)
        self.ctrl_layer.remove_pointer()

        self.ui.get_tool_probe_pb.setEnabled(False)
        self.ui.get_tool_change_pb.setEnabled(False)

    def handle_clear_terminal(self):
        self.ui.serial_te.clear()

    def hide_show_console(self):
        if self.ui.actionHide_Show_Console.isChecked():
            self.ui.logging_plain_te.show()
        else:
            self.ui.logging_plain_te.hide()

    def handle_tool_change_start(self):
        logger.debug("Tool change")
        self.controlWo.send_tool_change_s.emit()
        self.disable_during_send()

    def handle_soft_reset(self):
        logger.info("Soft Reset Command")
        self.ui_send_cmd_s.emit("soft_reset", ())

    def handle_unlock(self):
        logger.debug("Unlock Command")
        self.ui_send_cmd_s.emit("unlock", ())

    def handle_homing(self):
        logger.debug("Homing Command")
        self.ui_send_cmd_s.emit("homing", ())

    def handle_xy_0(self):
        logger.debug("XY = 0")
        self.ui_send_cmd_s.emit("xy=0", ())

    def handle_x_0(self):
        logger.debug("X = 0")
        self.ui_send_cmd_s.emit("x=0", ())

    def handle_y_0(self):
        logger.debug("Y = 0")
        self.ui_send_cmd_s.emit("y=0", ())

    def handle_z_0(self):
        logger.debug("Z = 0")
        self.ui_send_cmd_s.emit("z=0", ())

    def handle_center_jog(self):
        logger.debug("Go to XY working 0")
        self.ui_send_cmd_s.emit("goto_wps_0", ())

    def z_update_step(self):
        self.machine_settings.z_step_idx = self.ui.z_step_cb.currentIndex()
        new_step_str = self.ui.z_step_cb.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.
        self.ui.z_step_val_dsb.setSingleStep(new_step_fl)
        self.ui.z_plus_1_pb.setText("+" + new_step_str)
        self.ui.z_minus_1_pb.setText("-" + new_step_str)

    @Slot()
    def z_update_value(self):
        """ Update current value of Z STEP in the machine settings. """
        self.machine_settings.z_step_value = self.ui.z_step_val_dsb.value()

    def handle_x_minus(self):
        logger.debug("X_minus Command")
        x_min_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("x_minus", (str(x_min_val),))

    def handle_x_plus(self):
        logger.debug("X_plus Command")
        x_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("x_plus", (str(x_plus_val),))

    def handle_y_minus(self):
        logger.debug("Y_minus Command")
        y_min_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("y_minus", (str(y_min_val),))

    def handle_y_plus(self):
        logger.debug("Y_plus Command")
        y_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("y_plus", (str(y_plus_val),))

    def handle_xy_plus(self):
        logger.debug("XY_plus Command")
        xy_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("xy_plus", (str(xy_plus_val), str(xy_plus_val)))

    def handle_x_plus_y_minus(self):
        logger.debug("X_plus_Y_minus Command")
        x_p_y_m_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("x_plus_y_minus", (str(x_p_y_m_val), str(x_p_y_m_val)))

    def handle_xy_minus(self):
        logger.debug("XY_minus Command")
        xy_minus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("xy_minus", (str(xy_minus_val), str(xy_minus_val)))

    def handle_x_minus_y_plus(self):
        logger.debug("X_minus_y_plus Command")
        x_m_y_p_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("x_minus_y_plus", (str(x_m_y_p_val), str(x_m_y_p_val)))

    def handle_z_minus(self):
        logger.debug("Z_minus Command")
        z_minus_val = self.ui.z_step_val_dsb.value()
        self.ui_send_cmd_s.emit("z_minus", (str(z_minus_val),))

    def handle_z_plus(self):
        logger.debug("Z_plus Command")
        z_plus_val = self.ui.z_step_val_dsb.value()
        self.ui_send_cmd_s.emit("z_plus", (str(z_plus_val),))

    def xy_update_step(self):
        self.machine_settings.xy_step_idx = self.ui.xy_step_cb.currentIndex()
        new_step_str = self.ui.xy_step_cb.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.
        self.ui.xy_step_val_dsb.setSingleStep(new_step_fl)
        self.ui.xy_plus_1_pb.setText("+" + new_step_str)
        self.ui.xy_minus_1_pb.setText("-" + new_step_str)

    @Slot()
    def xy_update_value(self):
        """ Update current value of XY STEP in the machine settings. """
        self.machine_settings.xy_step_value = self.ui.xy_step_val_dsb.value()

    def handle_xy_plus_1(self):
        xy_val = self.ui.xy_step_val_dsb.value() + self.ui.xy_step_val_dsb.singleStep()
        self.ui.xy_step_val_dsb.setValue(xy_val)

    def handle_xy_minus_1(self):
        xy_val = self.ui.xy_step_val_dsb.value() - self.ui.xy_step_val_dsb.singleStep()
        self.ui.xy_step_val_dsb.setValue(xy_val)

    def handle_xy_div_10(self):
        xy_value = self.ui.xy_step_val_dsb.value()
        self.ui.xy_step_val_dsb.setValue(round(xy_value/10.0, 2))

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
        self.ui.z_step_val_dsb.setValue(round(z_value/10.0, 2))

    def handle_z_mul_10(self):
        z_value = self.ui.z_step_val_dsb.value()
        self.ui.z_step_val_dsb.setValue(z_value*10.0)

    def handle_z_min_changed(self):
        self.machine_settings.probe_z_min = self.ui.z_min_dsb.value()

    def handle_z_max_changed(self):
        self.machine_settings.probe_z_max = self.ui.z_max_dsb.value()

    def handle_probe_cmd(self):
        logger.debug("Probe Command")
        # todo: fake parameters just to test probe
        probe_z_min = self.ui.z_min_dsb.value()
        self.controlWo.cmd_probe(probe_z_min)

    def handle_auto_bed_levelling(self):
        logger.debug("Auto Bed Levelling Command")
        bbox_t, steps_t = self.get_abl_inputs()
        self.controlWo.send_abl_s.emit(bbox_t, steps_t)

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
        self.ui.x_max_dsb.setValue(bbox_t[3])
        self.ui.y_max_dsb.setValue(bbox_t[4])
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


