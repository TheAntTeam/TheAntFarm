from PySide2.QtWidgets import QLabel, QDoubleSpinBox, QHeaderView
from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import Qt
from collections import OrderedDict as Od
import math
import logging

logger = logging.getLogger(__name__)


class UiCreateJobLayerTab(QObject):
    """Class dedicated to UI <--> Control interactions on Create Job Layer Tab. """

    generate_path_s = Signal(str, Od, str)

    TAPS_TYPE_TEXT = ["None", "1 Left + 1 Right", "1 Top + 1 Bottom", "4 - 1 per side",
                              "2 Left + 2 Right", "2 Top + 2 Bottom", "8 - 2 per side", "4 - 1 per corner"]

    def __init__(self, ui, control_wo, vis_layer, lay_tags, lay_names, jobs_settings):
        super(UiCreateJobLayerTab, self).__init__()
        self.ui = ui
        self.control_wo = control_wo
        self.vis_layer = vis_layer
        self.lay_tags = lay_tags
        self.lay_names = lay_names
        self.jobs_settings = jobs_settings

        self.current_drill_tool_idx = 0

        self.set_all_settings_per_page()

        header = self.ui.drill_tw.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        [self.ui.profile_taps_layout_cb.addItem(x) for x in self.TAPS_TYPE_TEXT]

        self.ui.layer_choice_cb.currentIndexChanged.connect(self.change_job_page)
        self.ui.add_drill_tool_tb.clicked.connect(self.add_default_drill_tool)
        self.ui.remove_drill_tool_tb.clicked.connect(self.remove_drill_tool)

        self.ui.top_generate_job_pb.clicked.connect(self.generate_top_path)
        self.ui.bottom_generate_job_pb.clicked.connect(self.generate_bottom_path)
        self.ui.profile_generate_job_pb.clicked.connect(self.generate_profile_path)
        self.ui.drill_generate_job_pb.clicked.connect(self.generate_drill_path)

        self.generate_path_s.connect(self.control_wo.generate_new_path)
        self.control_wo.update_path_s.connect(self.add_new_path)

    def load_active_layers(self, active_layers):
        self.ui.layer_choice_cb.clear()

        for layer_tag in active_layers:
            if active_layers[layer_tag] != "":
                self.ui.layer_choice_cb.addItem(self.lay_names[self.lay_tags.index(layer_tag)])

    def visualize_active_layer(self):
        current_text_cb = self.ui.layer_choice_cb.currentText()

        for x in self.lay_tags:
            self.vis_layer.set_layer_visible(x, False)
            self.vis_layer.set_path_visible(x, False)

        if current_text_cb in self.lay_names:
            current_layer_tag = self.lay_tags[self.lay_names.index(current_text_cb)]
            self.vis_layer.set_layer_visible(self.lay_tags[self.lay_names.index(current_text_cb)], True)
            self.vis_layer.set_path_visible(current_layer_tag, True)

    def change_job_page(self):
        current_text_cb = self.ui.layer_choice_cb.currentText()

        if current_text_cb in self.lay_names:
            idx = self.lay_names.index(current_text_cb)
            # self.set_settings_per_page(self.lay_tags[idx])

            self.ui.jobs_sw.setCurrentIndex(idx + 1)  # The offset is needed for the empty page, the first one
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

    def set_settings_per_top(self):
        settings_top = self.jobs_settings.jobs_settings_od["top"]
        self.ui.top_tool_diameter_dsb.setValue(settings_top["tool_diameter"])
        self.ui.top_n_passes_sb.setValue(settings_top["passages"])
        self.ui.top_overlap_dsb.setValue(settings_top["overlap"])
        self.ui.top_cut_z_dsb.setValue(settings_top["cut"])
        self.ui.top_travel_z_dsb.setValue(settings_top["travel"])
        self.ui.top_spindle_speed_dsb.setValue(settings_top["spindle"])
        self.ui.top_xy_feed_rate_dsb.setValue(settings_top["xy_feedrate"])
        self.ui.top_z_feed_rate_dsb.setValue(settings_top["z_feedrate"])

    def set_settings_per_bottom(self):
        settings_bottom = self.jobs_settings.jobs_settings_od["bottom"]
        self.ui.bottom_tool_diameter_dsb.setValue(settings_bottom["tool_diameter"])
        self.ui.bottom_n_passes_sb.setValue(settings_bottom["passages"])
        self.ui.bottom_overlap_dsb.setValue(settings_bottom["overlap"])
        self.ui.bottom_cut_z_dsb.setValue(settings_bottom["cut"])
        self.ui.bottom_travel_z_dsb.setValue(settings_bottom["travel"])
        self.ui.bottom_spindle_speed_dsb.setValue(settings_bottom["spindle"])
        self.ui.bottom_xy_feed_rate_dsb.setValue(settings_bottom["xy_feedrate"])
        self.ui.bottom_z_feed_rate_dsb.setValue(settings_bottom["z_feedrate"])

    def set_settings_per_profile(self):
        settings_profile = self.jobs_settings.jobs_settings_od["profile"]
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

    def set_settings_per_drill(self):
        settings_drill = self.jobs_settings.jobs_settings_od["drill"]
        drill_tools_names_list = settings_drill["bits_names"]
        drill_tools_diameter_list = settings_drill["bits_diameter"]
        if drill_tools_diameter_list and drill_tools_names_list:
            for index, elem in enumerate(drill_tools_names_list):
                self.add_drill_tool(elem, drill_tools_diameter_list[index])

        if settings_drill["milling_tool"]:
            self.ui.drill_milling_tool_chb.setCheckState(Qt.Checked)
        else:
            self.ui.drill_milling_tool_chb.setCheckState(Qt.Unchecked)

        self.ui.drill_milling_tool_diameter_dsb.setValue(settings_drill["tool_diameter"])
        self.ui.drill_cut_z_dsb.setValue(settings_drill["cut"])
        self.ui.drill_travel_z_dsb.setValue(settings_drill["travel"])
        self.ui.drill_spindle_speed_dsb.setValue(settings_drill["spindle"])
        self.ui.drill_xy_feed_rate_dsb.setValue(settings_drill["xy_feedrate"])
        self.ui.drill_z_feed_rate_dsb.setValue(settings_drill["z_feedrate"])

        if settings_drill["optimize"]:
            self.ui.drill_optimization_chb.setCheckState(Qt.Checked)
        else:
            self.ui.drill_optimization_chb.setCheckState(Qt.Unchecked)

    def set_settings_per_nc_top(self):
        settings_nc_top = self.jobs_settings.jobs_settings_od["no_copper_top"]
        self.ui.nc_top_tool_diameter_dsb.setValue(settings_nc_top["tool_diameter"])
        self.ui.nc_top_overlap_dsb.setValue(settings_nc_top["overlap"])
        self.ui.nc_top_cut_z_dsb.setValue(settings_nc_top["cut"])
        self.ui.nc_top_travel_z_dsb.setValue(settings_nc_top["travel"])
        self.ui.nc_top_spindle_speed_dsb.setValue(settings_nc_top["spindle"])
        self.ui.nc_top_xy_feed_rate_dsb.setValue(settings_nc_top["xy_feedrate"])
        self.ui.nc_top_z_feed_rate_dsb.setValue(settings_nc_top["z_feedrate"])

    def set_settings_per_nc_bottom(self):
        settings_nc_bottom = self.jobs_settings.jobs_settings_od["no_copper_bottom"]
        self.ui.nc_bottom_tool_diameter_dsb.setValue(settings_nc_bottom["tool_diameter"])
        self.ui.nc_bottom_overlap_dsb.setValue(settings_nc_bottom["overlap"])
        self.ui.nc_bottom_cut_z_dsb.setValue(settings_nc_bottom["cut"])
        self.ui.nc_bottom_travel_z_dsb.setValue(settings_nc_bottom["travel"])
        self.ui.nc_bottom_spindle_speed_dsb.setValue(settings_nc_bottom["spindle"])
        self.ui.nc_bottom_xy_feed_rate_dsb.setValue(settings_nc_bottom["xy_feedrate"])
        self.ui.nc_bottom_z_feed_rate_dsb.setValue(settings_nc_bottom["z_feedrate"])

    def set_settings_per_page(self, tag):
        if tag == self.lay_tags[0]:
            return self.set_settings_per_top()
        elif tag == self.lay_tags[1]:
            return self.set_settings_per_bottom()
        elif tag == self.lay_tags[2]:
            return self.set_settings_per_profile()
        elif tag == self.lay_tags[3]:
            return self.set_settings_per_drill()
        elif tag == self.lay_tags[4]:
            return self.set_settings_per_nc_top()
        elif tag == self.lay_tags[5]:
            return self.set_settings_per_nc_bottom()

    def set_all_settings_per_page(self):
        [self.set_settings_per_page(tag) for tag in self.lay_tags]

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
        settings_profile["passages"] = 1
        if settings_profile["multi_depth"]:
            settings_profile["passages"] = math.ceil(abs(settings_profile["cut"]/settings_profile["depth_per_pass"]))
        settings_profile["overlap"] = 1.0
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
        drill_tools_names = []
        drill_tools_diameters = []
        count_row = self.ui.drill_tw.rowCount()
        for x in range(0, count_row):
            drill_tools_diameters.append(self.ui.drill_tw.cellWidget(x, 1).value())
            drill_tools_names.append(self.ui.drill_tw.cellWidget(x, 0).text())

        settings_drill["bits_names"] = drill_tools_names
        settings_drill["bits_diameter"] = drill_tools_diameters
        settings_drill["milling_tool"] = self.ui.drill_milling_tool_chb.isChecked()
        settings_drill["tool_diameter"] = self.ui.drill_milling_tool_diameter_dsb.value()
        settings_drill["cut"] = self.ui.drill_cut_z_dsb.value()
        settings_drill["travel"] = self.ui.drill_travel_z_dsb.value()
        settings_drill["spindle"] = self.ui.drill_spindle_speed_dsb.value()
        settings_drill["xy_feedrate"] = self.ui.drill_xy_feed_rate_dsb.value()
        settings_drill["z_feedrate"] = self.ui.drill_z_feed_rate_dsb.value()
        settings_drill["optimize"] = self.ui.drill_optimization_chb.isChecked()
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
        self.generate_path_s.emit("top", cfg, "gerber")

    def generate_bottom_path(self):
        cfg = self.get_settings_per_page("bottom")
        self.generate_path_s.emit("bottom", cfg, "gerber")

    def generate_profile_path(self):
        cfg = self.get_settings_per_page("profile")
        self.generate_path_s.emit("profile", cfg, "profile")

    def generate_drill_path(self):
        cfg = self.get_settings_per_page("drill")
        self.generate_path_s.emit("drill", cfg, "drill")

    @Slot(str, list)
    def add_new_path(self, tag, path):
        self.vis_layer.remove_path(tag)
        self.vis_layer.add_path(tag, path, color="white")
        index_tag_cb = self.lay_names.index(self.ui.layer_choice_cb.currentText())
        if self.lay_tags[index_tag_cb] != tag:
            self.vis_layer.set_path_visible(tag, False)
