from PySide6.QtCore import Signal, Slot, QObject, QSize, Qt, QPersistentModelIndex
from PySide6.QtWidgets import QFileDialog, QLabel, QRadioButton, QHeaderView, QButtonGroup, QAbstractItemView
from PySide6.QtGui import QIcon
from style_manager import StyleManager
from collections import OrderedDict as Od
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
    remove_gcode_s = Signal(str)

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
        self.controlWo.touched_probe_s.connect(self.touched_probe)
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

        combobox_ss = "QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}"
        self.ui.send_cb.setStyleSheet(combobox_ss)
        self.ui.send_cb.hide()
        self.ui.send_pb.hide()

        # Set x and y bbox step initial values.
        self.ui.x_num_step_sb.setValue(self.machine_settings.x_bbox_step)
        self.ui.y_num_step_sb.setValue(self.machine_settings.y_bbox_step)

        self.ui.refresh_pb.clicked.connect(self.handle_refresh_button)
        self.ui.connect_pb.clicked.connect(self.handle_connect_button)
        self.ui.clear_terminal_pb.clicked.connect(self.handle_clear_terminal)
        self.ui.send_pb.clicked.connect(self.send_input)
        self.ui.send_cb.key_event_cb.connect(self.send_input)
        self.ui.soft_reset_tb.clicked.connect(self.handle_soft_reset)
        self.ui.unlock_tb.clicked.connect(self.handle_unlock)
        self.ui.homing_tb.clicked.connect(self.handle_homing)
        self.ui.tool_change_tb.clicked.connect(self.handle_tool_change_start)
        self.ui.zero_xy_pb.clicked.connect(self.handle_xy_0)
        self.ui.zero_x_pb.clicked.connect(self.handle_x_0)
        self.ui.zero_y_pb.clicked.connect(self.handle_y_0)
        self.ui.zero_z_pb.clicked.connect(self.handle_z_0)
        self.ui.center_tb.clicked.connect(self.handle_center_jog)
        self.ui.x_minus_pb.clicked.connect(self.handle_x_minus)
        self.ui.x_plus_pb.clicked.connect(self.handle_x_plus)
        self.ui.y_minus_pb.clicked.connect(self.handle_y_minus)
        self.ui.y_plus_pb.clicked.connect(self.handle_y_plus)
        self.ui.x_plus_y_plus_pb.clicked.connect(self.handle_xy_plus)
        self.ui.x_plus_y_minus_pb.clicked.connect(self.handle_x_plus_y_minus)
        self.ui.x_minus_y_minus_pb.clicked.connect(self.handle_xy_minus)
        self.ui.x_minus_y_plus_pb.clicked.connect(self.handle_x_minus_y_plus)
        self.ui.z_minus_pb.clicked.connect(self.handle_z_minus)
        self.ui.z_plus_pb.clicked.connect(self.handle_z_plus)

        self.ui.center_tb_2.clicked.connect(self.handle_center_jog)
        self.ui.x_minus_pb_2.clicked.connect(self.handle_x_minus)
        self.ui.x_plus_pb_2.clicked.connect(self.handle_x_plus)
        self.ui.y_minus_pb_2.clicked.connect(self.handle_y_minus)
        self.ui.y_plus_pb_2.clicked.connect(self.handle_y_plus)
        self.ui.x_plus_y_plus_pb_2.clicked.connect(self.handle_xy_plus)
        self.ui.x_plus_y_minus_pb_2.clicked.connect(self.handle_x_plus_y_minus)
        self.ui.x_minus_y_minus_pb_2.clicked.connect(self.handle_xy_minus)
        self.ui.x_minus_y_plus_pb_2.clicked.connect(self.handle_x_minus_y_plus)
        self.ui.z_minus_pb_2.clicked.connect(self.handle_z_minus)
        self.ui.z_plus_pb_2.clicked.connect(self.handle_z_plus)

        self.ui.xy_plus_1_pb.clicked.connect(lambda: self.handle_xy_plus_1(self.ui.xy_step_val_dsb))
        self.ui.xy_minus_1_pb.clicked.connect(lambda: self.handle_xy_minus_1(self.ui.xy_step_val_dsb))
        self.ui.xy_div_10_pb.clicked.connect(lambda: self.handle_xy_div_10(self.ui.xy_step_val_dsb))
        self.ui.xy_mul_10_pb.clicked.connect(lambda: self.handle_xy_mul_10(self.ui.xy_step_val_dsb))
        self.ui.z_plus_1_pb.clicked.connect(lambda: self.handle_z_plus_1(self.ui.z_step_val_dsb))
        self.ui.z_minus_1_pb.clicked.connect(lambda: self.handle_z_minus_1(self.ui.z_step_val_dsb))
        self.ui.z_div_10_pb.clicked.connect(lambda: self.handle_z_div_10(self.ui.z_step_val_dsb))
        self.ui.z_mul_10_pb.clicked.connect(lambda: self.handle_z_mul_10(self.ui.z_step_val_dsb))

        self.ui.xy_plus_1_pb_2.clicked.connect(lambda: self.handle_xy_plus_1(self.ui.xy_step_val_dsb_2))
        self.ui.xy_minus_1_pb_2.clicked.connect(lambda: self.handle_xy_minus_1(self.ui.xy_step_val_dsb_2))
        self.ui.xy_div_10_pb_2.clicked.connect(lambda: self.handle_xy_div_10(self.ui.xy_step_val_dsb_2))
        self.ui.xy_mul_10_pb_2.clicked.connect(lambda: self.handle_xy_mul_10(self.ui.xy_step_val_dsb_2))
        self.ui.z_plus_1_pb_2.clicked.connect(lambda: self.handle_z_plus_1(self.ui.z_step_val_dsb_2))
        self.ui.z_minus_1_pb_2.clicked.connect(lambda: self.handle_z_minus_1(self.ui.z_step_val_dsb_2))
        self.ui.z_div_10_pb_2.clicked.connect(lambda: self.handle_z_div_10(self.ui.z_step_val_dsb_2))
        self.ui.z_mul_10_pb_2.clicked.connect(lambda: self.handle_z_mul_10(self.ui.z_step_val_dsb_2))

        self.ui.probe_pb.clicked.connect(self.handle_probe_cmd)
        self.ui.ABL_pb.clicked.connect(self.handle_auto_bed_levelling)
        self.ui.abl_active_chb.stateChanged.connect(
            lambda: self.controlWo.set_abl_active(self.ui.abl_active_chb.isChecked()))
        self.ui.get_bbox_pb.clicked.connect(self.controlWo.get_boundary_box)
        self.ui.x_min_dsb.valueChanged.connect(self.update_bbox_x_steps)
        self.ui.x_max_dsb.valueChanged.connect(self.update_bbox_x_steps)
        self.ui.x_num_step_sb.valueChanged.connect(self.update_bbox_x_num_steps)
        self.ui.y_min_dsb.valueChanged.connect(self.update_bbox_y_steps)
        self.ui.y_max_dsb.valueChanged.connect(self.update_bbox_y_steps)
        self.ui.y_num_step_sb.valueChanged.connect(self.update_bbox_y_num_steps)

        self.enable_control_jog_elements(False)
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
        # To Select Rows by Vertical Header
        self.ui.gcode_tw.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.gcode_tw.horizontalHeader().sectionPressed.disconnect()
        self.ui.gcode_tw.verticalHeader().sectionClicked.connect(self.select_gcode_row)
        self.ui.gcode_tw.verticalHeader().sectionDoubleClicked.connect(self.deselect_all_gcode_row)

        self.ui.upload_temp_tb.clicked.connect(self.update_temporary_gcode_files)
        self.ui.remove_gcode_tb.clicked.connect(self.remove_gcode_files)
        self.remove_gcode_s.connect(self.controlWo.remove_gcode)

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

    def enable_control_jog_elements(self, enable_flag=True):
        """
        Enable or disable ui elements of the control jog and related.

        Parameters
        ----------
        enable_flag enable ui elements if true
        """
        self.ui.x_minus_y_plus_pb.setEnabled(enable_flag)
        self.ui.x_plus_y_minus_pb.setEnabled(enable_flag)
        self.ui.x_minus_y_minus_pb.setEnabled(enable_flag)
        self.ui.x_plus_y_plus_pb.setEnabled(enable_flag)
        self.ui.x_minus_pb.setEnabled(enable_flag)
        self.ui.x_plus_pb.setEnabled(enable_flag)
        self.ui.y_minus_pb.setEnabled(enable_flag)
        self.ui.y_plus_pb.setEnabled(enable_flag)
        self.ui.center_tb.setEnabled(enable_flag)
        self.ui.z_plus_pb.setEnabled(enable_flag)
        self.ui.z_minus_pb.setEnabled(enable_flag)
        self.ui.probe_pb.setEnabled(enable_flag)
        self.ui.zero_x_pb.setEnabled(enable_flag)
        self.ui.zero_y_pb.setEnabled(enable_flag)
        self.ui.zero_z_pb.setEnabled(enable_flag)
        self.ui.zero_xy_pb.setEnabled(enable_flag)

    def deselect_all_gcode_row(self):
        self.ui.gcode_tw.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ui.gcode_tw.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.gcode_tw.clearSelection()
        self.ui.gcode_tw.setSelectionMode(QAbstractItemView.NoSelection)

    def select_gcode_row(self, index):
        self.ui.gcode_tw.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ui.gcode_tw.setSelectionBehavior(QAbstractItemView.SelectRows)
        qindexes = self.ui.gcode_tw.selectionModel().selectedRows()
        indexes = [x.row() for x in qindexes]
        if index in indexes:
            selectionModel = self.ui.gcode_tw.selectionModel()
            selectionModel.select(self.ui.gcode_tw.model().index(index, 0),
                                  selectionModel.Deselect | selectionModel.Rows)
        else:
            self.ui.gcode_tw.selectRow(index)
        self.ui.gcode_tw.setSelectionMode(QAbstractItemView.NoSelection)

    def init_xy_jog_step_value(self):
        """ Initialize XY step and value ui fields. """
        self.ui.xy_step_cb.setCurrentIndex(self.machine_settings.xy_step_idx)
        self.ui.xy_step_cb_2.setCurrentIndex(self.machine_settings.xy_step_idx)
        self.xy_update_step()
        self.xy_update_step_2()
        self.ui.xy_step_val_dsb.setValue(self.machine_settings.xy_step_value)
        self.ui.xy_step_cb.currentTextChanged.connect(self.xy_update_step)
        self.ui.xy_step_val_dsb.valueChanged.connect(lambda: self.xy_update_value(self.ui.xy_step_val_dsb))

        self.ui.xy_step_val_dsb_2.setValue(self.machine_settings.xy_step_value)
        self.ui.xy_step_cb_2.currentTextChanged.connect(self.xy_update_step_2)
        self.ui.xy_step_val_dsb_2.valueChanged.connect(lambda: self.xy_update_value(self.ui.xy_step_val_dsb_2))

    def init_z_jog_step_value(self):
        """ Initialize Z step and value ui fields. """
        self.ui.z_step_cb.setCurrentIndex(self.machine_settings.z_step_idx)
        self.ui.z_step_cb_2.setCurrentIndex(self.machine_settings.z_step_idx)
        self.z_update_step()
        self.z_update_step_2()
        self.ui.z_step_val_dsb.setValue(self.machine_settings.z_step_value)
        self.ui.z_step_val_dsb_2.setValue(self.machine_settings.z_step_value)
        self.ui.z_step_cb.currentTextChanged.connect(self.z_update_step)
        self.ui.z_step_cb_2.currentTextChanged.connect(self.z_update_step_2)
        self.ui.z_step_val_dsb.valueChanged.connect(lambda: self.z_update_value(self.ui.z_step_val_dsb))
        self.ui.z_step_val_dsb_2.valueChanged.connect(lambda: self.z_update_value(self.ui.z_step_val_dsb_2))

    def init_serial_port_cb(self):
        """ Initialize the serial ports' ui elements. """
        self.handle_refresh_button()

    @Slot(Od)
    def update_status(self, status_od):
        status_text = status_od["state"]
        if "pins" in status_od.keys():
            status_text += "\n" + status_od["pins"]
        self.ui.status_l.setText(status_text)
        self.update_status_colors(status_od["state"])
        self.update_status_buttons(status_od["state"])
        self.ui.mpos_x_l.setText('{:.3f}'.format(status_od["mpos"][0]))
        self.ui.mpos_y_l.setText('{:.3f}'.format(status_od["mpos"][1]))
        self.ui.mpos_z_l.setText('{:.3f}'.format(status_od["mpos"][2]))
        self.ui.wpos_x_l.setText('{:.3f}'.format(status_od["wpos"][0]))
        self.ui.wpos_y_l.setText('{:.3f}'.format(status_od["wpos"][1]))
        self.ui.wpos_z_l.setText('{:.3f}'.format(status_od["wpos"][2]))

        self.ui.mpos_x_l_2.setText('{:.3f}'.format(status_od["mpos"][0]))
        self.ui.mpos_y_l_2.setText('{:.3f}'.format(status_od["mpos"][1]))
        self.ui.mpos_z_l_2.setText('{:.3f}'.format(status_od["mpos"][2]))
        self.ui.wpos_x_l_2.setText('{:.3f}'.format(status_od["wpos"][0]))
        self.ui.wpos_y_l_2.setText('{:.3f}'.format(status_od["wpos"][1]))
        self.ui.wpos_z_l_2.setText('{:.3f}'.format(status_od["wpos"][2]))

        self.ctrl_layer.update_pointer(coords=status_od["wpos"])

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
        load_gcode = QFileDialog.getOpenFileNames(None, "Load G-Code File(s)",  # todo: add other file extensions?
                                                  self.app_settings.gcode_last_dir,
                                                  "G-Code Files (*.gcode *.nc)" + ";;All files (*.*)")
        logger.debug(load_gcode)
        gcode_actual_l = []
        load_gcode_paths = []

        # Actual gcode list paths are re-calculated here.
        num_rows = self.ui.gcode_tw.rowCount()
        for row in range(0, num_rows):
            gcode_actual_l.append(self.ui.gcode_tw.cellWidget(row, 0).toolTip())

        for elem in load_gcode[0]:
            norm_elem = os.path.normpath(elem)
            if norm_elem not in gcode_actual_l:  # Avoid re-loading the same gcode.
                load_gcode_paths.append(norm_elem)

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
                    new_la = QLabel(os.path.basename(elem))
                    new_la.setToolTip(elem)
                    self.ui.gcode_tw.setCellWidget(num_rows, 0, new_la)
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
        gcode_actual_l = []

        num_rows = self.ui.gcode_tw.rowCount()
        for row in range(0, num_rows):
            gcode_actual_l.append(self.ui.gcode_tw.cellWidget(row, 0).toolTip())

        for file in os.listdir(temp_dir):
            if file.endswith(".gcode") or file.endswith(".nc"):
                new_elem = os.path.join(temp_dir, file)
                if new_elem not in gcode_actual_l:
                    gcode_l.append(new_elem)

        if gcode_l:
            self._open_gcode_file(gcode_l)

    def remove_gcode_files(self):
        rows = set([x.row() for x in self.ui.gcode_tw.selectedIndexes()])
        for row in sorted(rows, reverse=True):
            gcode_path = self.ui.gcode_tw.cellWidget(row, 0).toolTip()
            tag, _ = self.controlWo.get_gcode_data(gcode_path)
            self.remove_gcode_s.emit(gcode_path)
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

    @Slot()
    def touched_probe(self):
        self.ui.probe_led_la.set_led_color("green")

    @Slot(list)
    def update_probe(self, probe_l):
        self.ui.probe_led_la.set_led_color("grey")

    @Slot(str)
    def update_console_text(self, new_text):
        pruned_text = new_text.strip()
        self.ui.serial_te.append(pruned_text)

    def send_input(self):
        """Send input to the serial port."""
        ct_cb = self.ui.send_cb.currentText()

        if not ct_cb == "":
            if self.ui.send_cb.count() == 0:
                self.ui.send_cb.addItem(ct_cb)
            else:
                self.ui.send_cb.setItemText(self.ui.send_cb.count()-1, ct_cb)

            self.ui.send_cb.addItem("")
            self.ui.send_cb.setCurrentIndex(self.ui.send_cb.count()-1)

            self.ui_serial_send_s.emit(ct_cb + "\n")

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
            self.ui.send_cb.show()
            self.ui.send_pb.show()
            self.ui.soft_reset_tb.setEnabled(True)
            self.ui.unlock_tb.setEnabled(True)
            self.ui.homing_tb.setEnabled(True)
            self.ui.tool_change_tb.setEnabled(True)
            if self.is_gcode_rb_selected():
                self.ui.play_tb.setEnabled(True)
            self.enable_control_jog_elements(True)
            self.controller_connected_s.emit(True)
            self.ctrl_layer.create_pointer(coords=(0, 0, 0))
            self.ui.get_tool_probe_pb.setEnabled(True)
            self.ui.probe_led_la.set_led_color("grey")
            self.ui.get_tool_change_pb.setEnabled(True)

    def act_on_disconnection(self):
        self.controlWo.reset_controller_status_s.emit()
        self.serial_connection_status = False
        self.ui.connect_pb.setText("Connect")
        self.ui.serial_ports_cb.show()
        self.ui.serial_baud_cb.show()
        self.ui.refresh_pb.show()
        self.ui.send_cb.hide()
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
        self.enable_control_jog_elements(False)
        self.controller_connected_s.emit(False)
        self.ctrl_layer.remove_pointer()
        self.ui.get_tool_probe_pb.setEnabled(False)
        self.ui.probe_led_la.set_led_color("grey")
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
        self.ui_send_cmd_s.emit("soft_reset", (None, None, None))

    def handle_unlock(self):
        logger.debug("Unlock Command")
        self.ui_send_cmd_s.emit("unlock", (None, None, None))

    def handle_homing(self):
        logger.debug("Homing Command")
        self.ui_send_cmd_s.emit("homing", (None, None, None))

    def handle_xy_0(self):
        logger.debug("XY = 0")
        self.ui_send_cmd_s.emit("set_wps", (0.0, 0.0, None))

    def handle_x_0(self):
        logger.debug("X = 0")
        self.ui_send_cmd_s.emit("set_wps", (0.0, None, None))

    def handle_y_0(self):
        logger.debug("Y = 0")
        self.ui_send_cmd_s.emit("set_wps", (None, 0.0, None))

    def handle_z_0(self):
        logger.debug("Z = 0")
        self.ui_send_cmd_s.emit("set_wps", (None, None, 0.0))

    def handle_center_jog(self):
        logger.debug("Go to XY working 0")
        self.ui_send_cmd_s.emit("goto", (0.0, 0.0, None))

    def z_update_step(self):
        current_index = self.ui.z_step_cb.currentIndex()
        self.machine_settings.z_step_idx = current_index
        new_step_str = self.ui.z_step_cb.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.
        self.ui.z_step_val_dsb.setSingleStep(new_step_fl)
        self.ui.z_plus_1_pb.setText("+" + new_step_str)
        self.ui.z_minus_1_pb.setText("-" + new_step_str)

        self.ui.z_step_cb_2.setCurrentIndex(current_index)  # This shall trigger the update of the other dro control

    def z_update_step_2(self):
        current_index = self.ui.z_step_cb_2.currentIndex()
        self.machine_settings.z_step_idx = current_index
        new_step_str = self.ui.z_step_cb_2.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.

        self.ui.z_step_val_dsb_2.setSingleStep(new_step_fl)
        self.ui.z_plus_1_pb_2.setText("+" + new_step_str)
        self.ui.z_minus_1_pb_2.setText("-" + new_step_str)

        self.ui.z_step_cb.setCurrentIndex(current_index)  # This shall trigger the update of the other dro control

    @Slot(float)
    def z_update_value(self, dsb):
        """ Update current value of Z STEP in the machine settings. """
        self.machine_settings.z_step_value = dsb.value()
        self.update_all_z_dsb_value(dsb.value())

    def handle_x_minus(self):
        logger.debug("X_minus Command")
        x_min_val = -self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (x_min_val, None, None))

    def handle_x_plus(self):
        logger.debug("X_plus Command")
        x_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (x_plus_val, None, None))

    def handle_y_minus(self):
        logger.debug("Y_minus Command")
        y_min_val = -self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (None, y_min_val, None))

    def handle_y_plus(self):
        logger.debug("Y_plus Command")
        y_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (None, y_plus_val, None))

    def handle_xy_plus(self):
        logger.debug("XY_plus Command")
        xy_plus_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (xy_plus_val, xy_plus_val, None))

    def handle_x_plus_y_minus(self):
        logger.debug("X_plus_Y_minus Command")
        x_p_y_m_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (x_p_y_m_val, -x_p_y_m_val, None))

    def handle_xy_minus(self):
        logger.debug("XY_minus Command")
        xy_minus_val = -self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (xy_minus_val, xy_minus_val, None))

    def handle_x_minus_y_plus(self):
        logger.debug("X_minus_y_plus Command")
        x_m_y_p_val = self.ui.xy_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (-x_m_y_p_val, x_m_y_p_val, None))

    def handle_z_minus(self):
        logger.debug("Z_minus Command")
        z_minus_val = self.ui.z_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (None, None, -z_minus_val))

    def handle_z_plus(self):
        logger.debug("Z_plus Command")
        z_plus_val = self.ui.z_step_val_dsb.value()
        self.ui_send_cmd_s.emit("jog", (None, None, z_plus_val))

    def xy_update_step(self):
        current_index = self.ui.xy_step_cb.currentIndex()
        self.machine_settings.xy_step_idx = current_index
        new_step_str = self.ui.xy_step_cb.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.
        self.ui.xy_step_val_dsb.setSingleStep(new_step_fl)
        self.ui.xy_plus_1_pb.setText("+" + new_step_str)
        self.ui.xy_minus_1_pb.setText("-" + new_step_str)

        self.ui.xy_step_cb_2.setCurrentIndex(current_index)  # This shall trigger the update of the other dro control

    def xy_update_step_2(self):
        current_index = self.ui.xy_step_cb_2.currentIndex()
        self.machine_settings.xy_step_idx = current_index
        new_step_str = self.ui.xy_step_cb_2.currentText()
        new_step_fl = float(new_step_str)  # try-except for the cast? No, because cb is not editable, up to now.

        self.ui.xy_step_val_dsb_2.setSingleStep(new_step_fl)
        self.ui.xy_plus_1_pb_2.setText("+" + new_step_str)
        self.ui.xy_minus_1_pb_2.setText("-" + new_step_str)

        self.ui.xy_step_cb.setCurrentIndex(current_index)  # This shall trigger the update of the other dro control

    def xy_update_value(self, dsb):
        """ Update current value of XY STEP in the machine settings. """
        self.machine_settings.xy_step_value = dsb.value()
        self.update_all_xy_dsb_value(dsb.value())

    def update_all_xy_dsb_value(self, new_xy_value):
        self.ui.xy_step_val_dsb.setValue(new_xy_value)
        self.ui.xy_step_val_dsb_2.setValue(new_xy_value)

    def handle_xy_plus_1(self, dsb):
        new_xy_value = round(dsb.value() + dsb.singleStep(), 2)
        if new_xy_value <= dsb.maximum():
            self.update_all_xy_dsb_value(new_xy_value)
        else:
            logger.warning(f"Cannot set value higher than maximum: {dsb.maximum()}")

    def handle_xy_minus_1(self, dsb):
        new_xy_value = round(dsb.value() - dsb.singleStep(), 2)
        if new_xy_value >= dsb.minimum():
            self.update_all_xy_dsb_value(new_xy_value)
        else:
            logger.warning(f"Cannot set value less than minimum: {dsb.minimum()}")

    def handle_xy_div_10(self, dsb):
        xy_value = dsb.value()
        new_xy_value = round(xy_value / 10.0, 2)
        if new_xy_value >= dsb.minimum():
            self.update_all_xy_dsb_value(new_xy_value)
        else:
            logger.warning(f"Cannot set value less than minimum: {dsb.minimum()}")

    def handle_xy_mul_10(self, dsb):
        xy_value = dsb.value()
        new_xy_value = round(xy_value * 10.0, 2)
        if new_xy_value <= dsb.maximum():
            self.update_all_xy_dsb_value(new_xy_value)
        else:
            logger.warning(f"Cannot set value higher than maximum: {dsb.maximum()}")

    def update_all_z_dsb_value(self, new_z_value):
        self.ui.z_step_val_dsb.setValue(new_z_value)
        self.ui.z_step_val_dsb_2.setValue(new_z_value)

    def handle_z_plus_1(self, dsb):
        new_z_value = round(dsb.value() + dsb.singleStep(), 2)
        if new_z_value <= dsb.maximum():
            self.update_all_z_dsb_value(new_z_value)
        else:
            logger.warning(f"Cannot set value higher than maximum: {dsb.maximum()}")

    def handle_z_minus_1(self, dsb):
        new_z_value = round(dsb.value() - dsb.singleStep(), 2)
        if new_z_value >= dsb.minimum():
            self.update_all_z_dsb_value(new_z_value)
        else:
            logger.warning(f"Cannot set value less than minimum: {dsb.minimum()}")

    def handle_z_div_10(self, dsb):
        new_z_value = round(dsb.value() / 10.0, 2)
        if new_z_value >= dsb.minimum():
            self.update_all_z_dsb_value(new_z_value)
        else:
            logger.warning(f"Cannot set value less than minimum: {dsb.minimum()}")

    def handle_z_mul_10(self, dsb):
        new_z_value = round(dsb.value() * 10.0, 2)
        if new_z_value <= dsb.maximum():
            self.update_all_z_dsb_value(new_z_value)
        else:
            logger.warning(f"Cannot set value higher than maximum: {dsb.maximum()}")

    def handle_z_min_changed(self):
        self.machine_settings.probe_z_min = self.ui.z_min_dsb.value()

    def handle_z_max_changed(self):
        self.machine_settings.probe_z_max = self.ui.z_max_dsb.value()

    def handle_probe_cmd(self):
        logger.debug("Probe Command")
        self.ui.probe_led_la.set_led_color("yellow")
        probe_z_min = self.ui.z_min_dsb.value()
        self.controlWo.cmd_probe(probe_z_min)

    def handle_auto_bed_levelling(self):
        logger.debug("Auto Bed Levelling Command")
        bbox_t, steps_t = self.get_abl_inputs()
        self.controlWo.send_abl_s.emit(bbox_t, steps_t)

    @Slot(float)
    def update_progress_bar(self, prog_percentage):
        logger.debug(prog_percentage)
        self.ui.progress_bar.setValue(prog_percentage)

    @Slot()
    def update_bbox_x_num_steps(self):
        self.machine_settings.x_bbox_step = self.ui.x_num_step_sb.value()
        self.update_bbox_x_steps()

    @Slot()
    def update_bbox_x_steps(self):
        x_steps = abs(self.ui.x_max_dsb.value() - self.ui.x_min_dsb.value()) / self.ui.x_num_step_sb.value()
        self.ui.x_step_dsb.setValue(x_steps)

    @Slot()
    def update_bbox_y_num_steps(self):
        self.machine_settings.y_bbox_step = self.ui.y_num_step_sb.value()
        self.update_bbox_y_steps()

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
