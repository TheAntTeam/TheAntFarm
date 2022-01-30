import os
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import Signal, Slot, QObject
from collections import OrderedDict as Od
import logging

logger = logging.getLogger(__name__)


class UiViewLoadLayerTab(QObject):
    """Class dedicated to UI <--> Control interactions on Load Layer Tab. """

    load_layer_s = Signal(str, str)

    def __init__(self, main_win, control_worker, vis_layer, lay_tags, lay_names, app_settings):
        super(UiViewLoadLayerTab, self).__init__()
        self.main_win = main_win
        self.ui = main_win.ui
        self.controlWo = control_worker
        self.vis_layer = vis_layer
        self.lay_tags = lay_tags
        self.lay_names = lay_names
        self.app_settings = app_settings

        lay_colors = [app_settings.top_layer_color, app_settings.bottom_layer_color,
                      app_settings.profile_layer_color, app_settings.drill_layer_color,
                      app_settings.nc_top_layer_color, app_settings.nc_bottom_layer_color]

        self.layer_colors = Od([(k, v) for k, v in zip(self.lay_tags, lay_colors)])
        self.L_TEXT = [self.ui.top_file_le, self.ui.bottom_file_le, self.ui.profile_file_le,
                       self.ui.drill_file_le, self.ui.no_copper_1_le, self.ui.no_copper_2_le]
        self.layers_te = Od([(k, t) for k, t in zip(self.lay_tags, self.L_TEXT)])
        self.L_CHECKBOX = [self.ui.top_view_chb, self.ui.bottom_view_chb, self.ui.profile_view_chb,
                           self.ui.drill_view_chb, self.ui.no_copper_1_chb, self.ui.no_copper_2_chb]
        self.layers_chb = Od([(k, t) for k, t in zip(self.lay_tags, self.L_CHECKBOX)])

        self.ui.pushButton_3.clicked.connect(self.vis_layer.top_view)
        self.ui.pushButton_4.clicked.connect(self.vis_layer.bottom_view)

        # Load Layer TAB related controls.
        self.load_layer_s.connect(self.controlWo.load_new_layer)
        self.controlWo.update_layer_s.connect(self.visualize_new_layer)
        gerber_extensions = "Gerber (*.gbr *.GBR *.gbl *.GBL *.gtl *.GTL)"
        excellon_extensions = "Excellon (*.xln *.XLN *.drl *.DRL)"
        self.ui.top_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[0], "Load Top Gerber File", gerber_extensions))
        self.ui.bottom_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[1], "Load Bottom Gerber File", gerber_extensions))
        self.ui.profile_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[2], "Load Profile Gerber File", gerber_extensions))
        self.ui.drill_load_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[3], "Load Drill Excellon File", excellon_extensions))
        self.ui.no_copper_1_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[4], "Load No Copper TOP Gerber File", gerber_extensions))
        self.ui.no_copper_2_pb.clicked.connect(
            lambda: self.load_gerber_file(self.lay_tags[5], "Load No Copper BOTTOM Gerber File", gerber_extensions))
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

        # Temporarily hide the not implemented parts # Todo: remove the following hide code when the NC are implemented.
        self.ui.no_copper_1_chb.hide()
        self.ui.no_copper_1_le.hide()
        self.ui.no_copper_1_pb.hide()
        self.ui.no_copper_2_chb.hide()
        self.ui.no_copper_2_le.hide()
        self.ui.no_copper_2_pb.hide()

    def load_gerber_file(self, layer="top", load_text="Load File", extensions=""):
        filters = extensions + ";;All files (*.*)"
        load_file_path = QFileDialog.getOpenFileName(self.main_win, load_text, self.app_settings.layer_last_dir, filters)
        if load_file_path[0]:
            self.vis_layer.remove_layer(layer)
            self.vis_layer.remove_path(layer)
            self.app_settings.layer_last_dir = os.path.dirname(load_file_path[0])
            logger.info("Loading " + load_file_path[0])
            self.load_layer_s.emit(layer, load_file_path[0])

    @Slot(Od, str, str, bool)
    def visualize_new_layer(self, loaded_layer, layer_tag, layer_path, holes):
        self.vis_layer.add_layer(layer_tag, loaded_layer[0], self.layer_colors[layer_tag], holes)
        self.layers_te[layer_tag].setText(layer_path)

    def visualize_all_active_layers(self):
        [self.vis_layer.set_layer_visible(x, False) for x in self.lay_tags]
        loaded_views = list(self.vis_layer.get_layers_tag())
        for view in loaded_views:
            self.vis_layer.set_path_visible(view, False)
            if self.layers_chb[view].isChecked():
                self.vis_layer.set_layer_visible(view, True)

    def remove_all_vis_layers(self):
        loaded_views = list(self.vis_layer.get_layers_tag())
        for view in loaded_views:
            self.vis_layer.remove_layer(view)
            self.vis_layer.remove_path(view)
        for layer_tag in self.layers_te:
            self.layers_te[layer_tag].setText("")
        self.ui.jobs_sw.setCurrentIndex(0)

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
