import os
from PySide2.QtWidgets import QFileDialog, QLabel, QDoubleSpinBox, QHeaderView
from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap, Qt
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

    def __init__(self, main_win, ui, control_worker, serial_worker):
        super(UiManager, self).__init__()
        self.main_win = main_win
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker

        self.vis_layer = VisualLayer(self.ui.viewCanvasWidget)

        # UI Sub-Managers
        self.ui_load_layer_m = UiViewLoadLayerTab(main_win, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES,
                                                  self.L_COLORS)
        self.ui_create_job_m = UiCreateJobLayerTab(ui, control_worker, self.vis_layer, self.L_TAGS, self.L_NAMES)
        self.ui_control_tab_m = UiControlTab(ui, control_worker, serial_worker)
        self.ui_align_tab_m = UiAlignTab(ui, control_worker)

        self.ui.prepare_widget.currentChanged.connect(self.from_load_to_create)
        self.ui.actionHide_Show_Console.triggered.connect(self.hide_show_console)

    def from_load_to_create(self):
        if self.ui.prepare_widget.currentWidget().objectName() == "create_job_tab":
            self.ui_create_job_m.load_active_layers(self.ui_load_layer_m.get_loaded_layers())
        elif self.ui.prepare_widget.currentWidget().objectName() == "load_layers_tab":
            self.ui_load_layer_m.visualize_all_active_layers()

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
    """Class dedicated to UI <--> Control interactions on Load Layer Tab. """

    load_layer_s = Signal(str, str)

    def __init__(self, main_win, control_worker, vis_layer, lay_tags, lay_names, lay_colors):
        super(UiViewLoadLayerTab, self).__init__()
        self.main_win = main_win
        self.ui = main_win.ui
        self.controlWo = control_worker
        self.vis_layer = vis_layer
        self.lay_tags = lay_tags
        self.lay_names = lay_names
        self.layer_last_dir = ""

        self.layer_colors = Od([(k, v) for k, v in zip(self.lay_tags, lay_colors)])
        self.L_TEXT = [self.ui.top_file_le, self.ui.bottom_file_le, self.ui.profile_file_le,
                       self.ui.drill_file_le, self.ui.no_copper_1_le, self.ui.no_copper_2_le]
        self.layers_te = Od([(k, t) for k, t in zip(self.lay_tags, self.L_TEXT)])
        self.L_CHECKBOX = [self.ui.top_view_chb, self.ui.bottom_view_chb, self.ui.profile_view_chb,
                           self.ui.drill_view_chb, self.ui.no_copper_1_chb, self.ui.no_copper_2_chb]
        self.layers_chb = Od([(k, t) for k, t in zip(self.lay_tags, self.L_CHECKBOX)])

        # Load Layer TAB related controls.
        self.load_layer_s.connect(self.controlWo.load_new_layer)
        self.controlWo.update_layer_s.connect(self.visualize_new_layer)
        self.ui.top_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[0], "Load Top Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.bottom_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[1], "Load Bottom Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.profile_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[2], "Load Profile Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.drill_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[3], "Load Drill Excellon File", "Excellon (*.xln *.XLN)"))
        self.ui.no_copper_1_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[4], "Load No Copper TOP Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.no_copper_2_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[5], "Load No Copper BOTTOM Gerber File", "Gerber (*.gbr *.GBR)"))
        self.ui.top_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.lay_tags[0], self.ui.top_view_chb.isChecked()))
        self.ui.bottom_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.lay_tags[1], self.ui.bottom_view_chb.isChecked()))
        self.ui.profile_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.lay_tags[2], self.ui.profile_view_chb.isChecked()))
        self.ui.drill_view_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.lay_tags[3], self.ui.drill_view_chb.isChecked()))
        self.ui.no_copper_1_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.lay_tags[4], self.ui.no_copper_1_chb.isChecked()))
        self.ui.no_copper_2_chb.stateChanged.connect(
            lambda: self.set_layer_visible(self.lay_tags[5], self.ui.no_copper_2_chb.isChecked()))
        self.ui.all_view_chb.stateChanged.connect(lambda: self.hide_show_layers(self.ui.all_view_chb.isChecked()))
        self.ui.clear_views_pb.clicked.connect(self.remove_all_vis_layers)

    def load_gerber_file(self, layer="top", load_text="Load File", extensions=""):
        filters = extensions + ";;All files (*.*)"
        load_file_path = QFileDialog.getOpenFileName(self.main_win, load_text, self.layer_last_dir, filters)
        if load_file_path[0]:
            self.vis_layer.remove_layer(layer)
            self.layer_last_dir = os.path.dirname(load_file_path[0])
            logging.info("Loading " + load_file_path[0])
            self.load_layer_s.emit(layer, load_file_path[0])

    @Slot(Od, str, str, bool)
    def visualize_new_layer(self, loaded_layer, layer_tag, layer_path, holes):
        self.vis_layer.add_layer(layer_tag, loaded_layer[0], self.layer_colors[layer_tag], holes)
        self.layers_te[layer_tag].setText(layer_path)

    def visualize_all_active_layers(self):
        [self.vis_layer.set_layer_visible(x, False) for x in self.lay_tags]
        loaded_views = list(self.vis_layer.get_layers_tag())
        for view in loaded_views:
            if self.layers_chb[view].isChecked():
                self.vis_layer.set_layer_visible(view, True)

    def remove_all_vis_layers(self):
        loaded_views = list(self.vis_layer.get_layers_tag())
        for view in loaded_views:
            self.vis_layer.remove_layer(view)
        for layer_tag in self.layers_te:
            self.layers_te[layer_tag].setText("")

    def hide_show_layers(self, checked):
        for chb in self.layers_chb:
            self.layers_chb[chb].setChecked(checked)

    @Slot(str, bool)
    def set_layer_visible(self, tag, visible):
        self.vis_layer.set_layer_visible(tag, visible)

    def get_loaded_layers(self):
        loaded_layers = Od({})
        for tag in self.lay_tags:
            if self.layers_te[tag] != "":
                loaded_layers[tag] = self.layers_te[tag].text()
        return loaded_layers


class UiCreateJobLayerTab(QObject):
    """Class dedicated to UI <--> Control interactions on Create Job Layer Tab. """

    generate_path_s = Signal(str, Od)

    TAPS_TYPE_TEXT = ["None", "1 Left + 1 Right", "1 Top + 1 Bottom", "4 - 1 per side",
                              "2 Left + 2 Right", "2 Top + 2 Bottom", "8 - 2 per side"]

    def __init__(self, ui, control_wo, vis_layer, lay_tags, lay_names):
        super(UiCreateJobLayerTab, self).__init__()
        self.ui = ui
        self.control_wo = control_wo
        self.vis_layer = vis_layer
        self.lay_tags = lay_tags
        self.lay_names = lay_names

        self.current_drill_tool_idx = 0

        header = self.ui.drill_tw.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        [self.ui.profile_taps_layout_cb.addItem(x) for x in self.TAPS_TYPE_TEXT]

        self.ui.layer_choice_cb.currentIndexChanged.connect(self.change_job_page)
        self.ui.add_drill_tool_tb.clicked.connect(self.add_default_drill_tool)
        self.ui.remove_drill_tool_tb.clicked.connect(self.remove_drill_tool)

        self.ui.top_generate_job_pb.clicked.connect(self.generate_top_path)
        self.ui.bottom_generate_job_pb.clicked.connect(self.generate_bottom_path)
        self.generate_path_s.connect(self.control_wo.generate_new_path)
        self.control_wo.update_path_s.connect(self.add_new_path)

    def load_active_layers(self, active_layers):
        self.ui.layer_choice_cb.clear()

        for layer_tag in active_layers:
            if active_layers[layer_tag] != "":
                self.ui.layer_choice_cb.addItem(self.lay_names[self.lay_tags.index(layer_tag)])

    def visualize_active_layer(self):
        current_text_cb = self.ui.layer_choice_cb.currentText()

        [self.vis_layer.set_layer_visible(x, False) for x in self.lay_tags]

        if current_text_cb in self.lay_names:
            self.vis_layer.set_layer_visible(self.lay_tags[self.lay_names.index(current_text_cb)], True)

    def change_job_page(self):
        current_text_cb = self.ui.layer_choice_cb.currentText()
        idx = 0
        if current_text_cb in self.lay_names:
            idx = self.lay_names.index(current_text_cb) + 1  # The offset is needed for the empty page, the first one

        self.ui.jobs_sw.setCurrentIndex(idx)
        self.visualize_active_layer()

    def add_drill_tool(self, label, value):
        count_row = self.ui.drill_tw.rowCount()
        self.ui.drill_tw.insertRow(count_row)
        new_tool_label = QLabel(label)
        self.current_drill_tool_idx = self.current_drill_tool_idx + 1
        new_tool_label.setAlignment(Qt.AlignCenter)
        self.ui.drill_tw.setCellWidget(count_row, 0, new_tool_label)
        new_tool_diameter = QDoubleSpinBox()
        new_tool_diameter.setAlignment(Qt.AlignCenter)
        new_tool_diameter.setValue(value)
        new_tool_diameter.setSingleStep(0.01)
        new_tool_diameter.setMinimum(0.01)
        new_tool_diameter.setMaximum(99.99)
        self.ui.drill_tw.setCellWidget(count_row, 1, new_tool_diameter)

    def add_default_drill_tool(self):
        count_row = self.ui.drill_tw.rowCount()
        self.ui.drill_tw.insertRow(count_row)
        new_tool_label = QLabel("Bit" + str(self.current_drill_tool_idx))
        self.current_drill_tool_idx = self.current_drill_tool_idx + 1
        new_tool_label.setAlignment(Qt.AlignCenter)
        self.ui.drill_tw.setCellWidget(count_row, 0, new_tool_label)
        new_tool_diameter = QDoubleSpinBox()
        new_tool_diameter.setAlignment(Qt.AlignCenter)
        new_tool_diameter.setValue(0.07)
        new_tool_diameter.setSingleStep(0.01)
        new_tool_diameter.setMinimum(0.01)
        new_tool_diameter.setMaximum(99.99)
        self.ui.drill_tw.setCellWidget(count_row, 1, new_tool_diameter)

    def remove_drill_tool(self):
        sel_range = self.ui.drill_tw.selectedIndexes()
        del_rows = []
        for s in sel_range:
            del_rows.append(s.row())
        del_rows = list(set(del_rows))
        del_rows.reverse()
        for x in del_rows:
            self.ui.drill_tw.removeRow(x)

    def set_settings_per_top(self, settings_top):
        self.ui.top_tool_diameter_dsb.setValue(settings_top["tool_diameter"])
        self.ui.top_n_passes_sb.setValue(settings_top["passages"])
        self.ui.top_overlap_dsb.setValue(settings_top["overlap"])
        self.ui.top_cut_z_dsb.setValue(settings_top["cut"])
        self.ui.top_travel_z_dsb.setValue(settings_top["travel"])
        self.ui.top_spindle_speed_dsb.setValue(settings_top["spindle"])
        self.ui.top_xy_feed_rate_dsb.setValue(settings_top["xy_feedrate"])
        self.ui.top_z_feed_rate_dsb.setValue(settings_top["z_feedrate"])

    def set_settings_per_bottom(self, settings_bottom):
        self.ui.bottom_tool_diameter_dsb.setValue(settings_bottom["tool_diameter"])
        self.ui.bottom_n_passes_sb.setValue(settings_bottom["passages"])
        self.ui.bottom_overlap_dsb.setValue(settings_bottom["overlap"])
        self.ui.bottom_cut_z_dsb.setValue(settings_bottom["cut"])
        self.ui.bottom_travel_z_dsb.setValue(settings_bottom["travel"])
        self.ui.bottom_spindle_speed_dsb.setValue(settings_bottom["spindle"])
        self.ui.bottom_xy_feed_rate_dsb.setValue(settings_bottom["xy_feedrate"])
        self.ui.bottom_z_feed_rate_dsb.setValue(settings_bottom["z_feedrate"])

    def set_settings_per_profile(self, settings_profile):
        self.ui.profile_tool_diameter_dsb.setValue(settings_profile["tool_diameter"])
        self.ui.profile_margin_dsb.setValue(settings_profile["margin"])
        if settings_profile["multi_depth"]:
            self.ui.profile_multi_depth_chb.setCheckState(Qt.Checked)
        else:
            self.ui.profile_multi_depth_chb.setCheckState(Qt.Unchecked)
        self.ui.profile_depth_pass_dsb.setValue(settings_profile["depth_per_pass"])
        self.ui.profile_cut_z_dsb.setValue(settings_profile["cut"])
        self.ui.profile_travel_z_dsb.setValue(settings_profile["travel"])
        self.ui.profile_spindle_speed_dsb.setValue(settings_profile["spindle"])
        self.ui.profile_xy_feed_rate_dsb.setValue(settings_profile["xy_feedrate"])
        self.ui.profile_z_feed_rate_dsb.setValue(settings_profile["z_feedrate"])
        self.ui.profile_taps_layout_cb.setCurrentIndex(settings_profile["taps_type"])
        self.ui.profile_tap_size_dsb.setValue(settings_profile["taps_length"])

    def set_settings_per_drill(self, settings_drill):
        drill_tools_list = settings_drill["bits_diameter"]
        for dt in drill_tools_list:
            self.add_drill_tool(dt[0], dt[1])

        self.ui.drill_milling_tool_chb.setCheckState(settings_drill["milling_tool"])
        self.ui.drill_milling_tool_diameter_dsb.setValue(settings_drill["milling_tool_diameter"])
        self.ui.drill_cut_z_dsb.setValue(settings_drill["cut"])
        self.ui.drill_travel_z_dsb.setValue(settings_drill["travel"])
        self.ui.drill_spindle_speed_dsb.setValue(settings_drill["spindle"])
        self.ui.drill_xy_feed_rate_dsb.setValue(settings_drill["xy_feedrate"])
        self.ui.drill_z_feed_rate_dsb.setValue(settings_drill["z_feedrate"])

    def get_settings_per_nc_top(self, settings_nc_top):
        self.ui.nc_top_tool_diameter_dsb.setValue(settings_nc_top["tool_diameter"])
        self.ui.nc_top_overlap_dsb.setValue(settings_nc_top["overlap"])
        self.ui.nc_top_cut_z_dsb.setValue(settings_nc_top["cut"])
        self.ui.nc_top_travel_z_dsb.setValue(settings_nc_top["travel"])
        self.ui.nc_top_spindle_speed_dsb.setValue(settings_nc_top["spindle"])
        self.ui.nc_top_xy_feed_rate_dsb.setValue(settings_nc_top["xy_feedrate"])
        self.ui.nc_top_z_feed_rate_dsb.setValue(settings_nc_top["z_feedrate"])

    def get_settings_per_nc_bottom(self, settings_nc_bottom):
        self.ui.nc_bottom_tool_diameter_dsb.setValue(settings_nc_bottom["tool_diameter"])
        self.ui.nc_bottom_overlap_dsb.setValue(settings_nc_bottom["overlap"])
        self.ui.nc_bottom_cut_z_dsb.setValue(settings_nc_bottom["cut"])
        self.ui.nc_bottom_travel_z_dsb.setValue(settings_nc_bottom["travel"])
        self.ui.nc_bottom_spindle_speed_dsb.setValue(settings_nc_bottom["spindle"])
        self.ui.nc_bottom_xy_feed_rate_dsb.setValue(settings_nc_bottom["xy_feedrate"])
        self.ui.nc_bottom_z_feed_rate_dsb.setValue(settings_nc_bottom["z_feedrate"])

    def set_settings_per_page(self, tag, settings):
        if tag == self.lay_tags[0]:
            return self.set_settings_per_top(settings)
        elif tag == self.lay_tags[1]:
            return self.set_settings_per_bottom(settings)
        elif tag == self.lay_tags[2]:
            return self.set_settings_per_profile(settings)
        elif tag == self.lay_tags[3]:
            return self.set_settings_per_drill(settings)
        elif tag == self.lay_tags[4]:
            return self.set_settings_per_nc_top(settings)
        elif tag == self.lay_tags[5]:
            return self.set_settings_per_nc_bottom(settings)

    def get_settings_per_top(self):
        settings_top = Od({})
        settings_top["tool_diameter"] = self.ui.top_tool_diameter_dsb.value()
        settings_top["passages"] = self.ui.top_n_passes_sb.value()
        settings_top["overlap"] = self.ui.top_overlap_dsb.value()
        settings_top["cut"] = self.ui.top_cut_z_dsb.value()
        settings_top["travel"] = self.ui.top_travel_z_dsb.value()
        settings_top["spindle"] = self.ui.top_spindle_speed_dsb.value()
        settings_top["xy_feedrate"] = self.ui.top_xy_feed_rate_dsb.value()
        settings_top["z_feedrate"] = self.ui.top_z_feed_rate_dsb.value()
        logging.debug(settings_top)
        return settings_top

    def get_settings_per_bottom(self):
        settings_bottom = Od({})
        settings_bottom["tool_diameter"] = self.ui.bottom_tool_diameter_dsb.value()
        settings_bottom["passages"] = self.ui.bottom_n_passes_sb.value()
        settings_bottom["overlap"] = self.ui.bottom_overlap_dsb.value()
        settings_bottom["cut"] = self.ui.bottom_cut_z_dsb.value()
        settings_bottom["travel"] = self.ui.bottom_travel_z_dsb.value()
        settings_bottom["spindle"] = self.ui.bottom_spindle_speed_dsb.value()
        settings_bottom["xy_feedrate"] = self.ui.bottom_xy_feed_rate_dsb.value()
        settings_bottom["z_feedrate"] = self.ui.bottom_z_feed_rate_dsb.value()
        logging.debug(settings_bottom)
        return settings_bottom

    def get_settings_per_profile(self):
        settings_profile = Od({})
        settings_profile["tool_diameter"] = self.ui.profile_tool_diameter_dsb.value()
        settings_profile["margin"] = self.ui.profile_margin_dsb.value()
        settings_profile["multi_depth"] = self.ui.profile_multi_depth_chb.isChecked()
        settings_profile["depth_per_pass"] = self.ui.profile_depth_pass_dsb.value()
        settings_profile["cut"] = self.ui.profile_cut_z_dsb.value()
        settings_profile["travel"] = self.ui.profile_travel_z_dsb.value()
        settings_profile["spindle"] = self.ui.profile_spindle_speed_dsb.value()
        settings_profile["xy_feedrate"] = self.ui.profile_xy_feed_rate_dsb.value()
        settings_profile["z_feedrate"] = self.ui.profile_z_feed_rate_dsb.value()
        settings_profile["taps_type"] = self.ui.profile_taps_layout_cb.currentIndex()
        settings_profile["taps_length"] = self.ui.profile_tap_size_dsb.value()
        logging.debug(settings_profile)
        return settings_profile

    def get_settings_per_drill(self):
        settings_drill = Od({})
        drill_tools_list = []
        count_row = self.ui.drill_tw.rowCount()
        for x in range(0, count_row):
            drill_tool_l = (self.ui.drill_tw.cellWidget(x, 0).text(), self.ui.drill_tw.cellWidget(x, 1).value())
            drill_tools_list.append(drill_tool_l)

        settings_drill["bits_diameter"] = drill_tools_list
        settings_drill["milling_tool"] = self.ui.drill_milling_tool_chb.isChecked()
        settings_drill["milling_tool_diameter"] = self.ui.drill_milling_tool_diameter_dsb.value()
        settings_drill["cut"] = self.ui.drill_cut_z_dsb.value()
        settings_drill["travel"] = self.ui.drill_travel_z_dsb.value()
        settings_drill["spindle"] = self.ui.drill_spindle_speed_dsb.value()
        settings_drill["xy_feedrate"] = self.ui.drill_xy_feed_rate_dsb.value()
        settings_drill["z_feedrate"] = self.ui.drill_z_feed_rate_dsb.value()
        logging.debug(settings_drill)
        return settings_drill

    def get_settings_per_nc_top(self):
        settings_nc_top = Od({})
        settings_nc_top["tool_diameter"] = self.ui.nc_top_tool_diameter_dsb.value()
        settings_nc_top["overlap"] = self.ui.nc_top_overlap_dsb.value()
        settings_nc_top["cut"] = self.ui.nc_top_cut_z_dsb.value()
        settings_nc_top["travel"] = self.ui.nc_top_travel_z_dsb.value()
        settings_nc_top["spindle"] = self.ui.nc_top_spindle_speed_dsb.value()
        settings_nc_top["xy_feedrate"] = self.ui.nc_top_xy_feed_rate_dsb.value()
        settings_nc_top["z_feedrate"] = self.ui.nc_top_z_feed_rate_dsb.value()
        logging.debug(settings_nc_top)
        return settings_nc_top

    def get_settings_per_nc_bottom(self):
        settings_nc_bottom = Od({})
        settings_nc_bottom["tool_diameter"] = self.ui.nc_bottom_tool_diameter_dsb.value()
        settings_nc_bottom["overlap"] = self.ui.nc_bottom_overlap_dsb.value()
        settings_nc_bottom["cut"] = self.ui.nc_bottom_cut_z_dsb.value()
        settings_nc_bottom["travel"] = self.ui.nc_bottom_travel_z_dsb.value()
        settings_nc_bottom["spindle"] = self.ui.nc_bottom_spindle_speed_dsb.value()
        settings_nc_bottom["xy_feedrate"] = self.ui.nc_bottom_xy_feed_rate_dsb.value()
        settings_nc_bottom["z_feedrate"] = self.ui.nc_bottom_z_feed_rate_dsb.value()
        logging.debug(settings_nc_bottom)
        return settings_nc_bottom

    def get_settings_per_page(self, tag):
        if tag == self.lay_tags[0]:
            return self.get_settings_per_top()
        elif tag == self.lay_tags[1]:
            return self.get_settings_per_bottom()
        elif tag == self.lay_tags[2]:
            return self.get_settings_per_profile()
        elif tag == self.lay_tags[3]:
            return self.get_settings_per_drill()
        elif tag == self.lay_tags[4]:
            return self.get_settings_per_nc_top()
        elif tag == self.lay_tags[5]:
            return self.get_settings_per_nc_bottom()

    def get_all_settings(self):
        settings = Od({})
        settings[self.lay_tags[0]] = self.get_settings_per_page(self.lay_tags[0])
        settings[self.lay_tags[1]] = self.get_settings_per_page(self.lay_tags[1])
        settings[self.lay_tags[2]] = self.get_settings_per_page(self.lay_tags[2])
        settings[self.lay_tags[3]] = self.get_settings_per_page(self.lay_tags[3])
        settings[self.lay_tags[4]] = self.get_settings_per_page(self.lay_tags[4])
        settings[self.lay_tags[5]] = self.get_settings_per_page(self.lay_tags[5])
        return settings

    def generate_top_path(self):
        cfg = self.get_settings_per_page("top")
        self.generate_path_s.emit("top", cfg)

    def generate_bottom_path(self):
        cfg = self.get_settings_per_page("bottom")
        self.generate_path_s.emit("bottom", cfg)

    @Slot(str, list)
    def add_new_path(self, tag, path):
        self.vis_layer.add_path(tag, path, color="white")


class UiControlTab(QObject):
    """Class dedicated to UI <--> Control interactions on Control Tab. """
    serial_send_s = Signal(str)

    def __init__(self, ui, control_worker, serial_worker):
        super(UiControlTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker
        self.serialWo = serial_worker

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

    def __init__(self, ui, control_worker):
        super(UiAlignTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker

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
