from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QFileDialog
from collections import OrderedDict as Od
import logging
import math
import os

logger = logging.getLogger(__name__)


class UiAlignTab(QObject):
    """Class dedicated to UI <--> Control interactions on Align Tab. """
    load_align_layer_s = Signal(str, str)
    align_active_s = Signal(bool)
    align_apply_s = Signal(bool, list)
    update_threshold_s = Signal(int)
    request_new_alignment_point_coords_s = Signal(list, tuple)

    def __init__(self, main_win, control_worker, vis_align_layer, app_settings):
        super(UiAlignTab, self).__init__()
        self.main_win = main_win
        self.ui = self.main_win.ui
        self.controlWo = control_worker
        self.vis_align_layer = vis_align_layer
        self.app_settings = app_settings

        self.layer_colors = self.app_settings.layer_color

        self.camera_pos_selected = False

        align_extensions = "Excellon (*.xln *.XLN *.drl *.DRL)"

        # Align TAB related controls.
        self.load_align_layer_s.connect(self.controlWo.load_new_align_layer)
        self.controlWo.update_align_layer_s.connect(self.visualize_new_align_layer)
        self.controlWo.update_align_layer_view_s.connect(self.flip_align_layer)
        self.ui.main_tab_widget.currentChanged.connect(self.check_align_is_active)
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.align_apply_s.connect(self.controlWo.set_align_active)
        self.ui.apply_alignment_tb.clicked.connect(self.apply_align)
        self.ui.add_point_tb.clicked.connect(self.request_new_point)
        self.ui.remove_point_tb.clicked.connect(self.remove_point)
        self.ui.contrast_slider.valueChanged.connect(self.update_threshold)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)
        self.ui.load_align_layer_tb.clicked.connect(
            lambda: self.load_align_file("Load Align File", align_extensions))
        self.ui.flip_horizontally_tb.clicked.connect(
            lambda: self.controlWo.flip_align_layer_horizontally(self.ui.flip_horizontally_tb.isChecked()))
        self.ui.flip_vertically_tb.clicked.connect(
            lambda: self.controlWo.flip_align_layer_vertically(self.ui.flip_vertically_tb.isChecked()))
        self.request_new_alignment_point_coords_s.connect(self.controlWo.add_new_align_point)

        self.ui.tool_or_camera_tb.clicked.connect(self.update_tool_or_camera)

        self.controlWo.update_camera_image_s.connect(self.update_camera_image)
        self.controlWo.update_camera_list_s.connect(self.update_camera_list)
        self.ui.camera_list_cb.currentIndexChanged.connect(lambda: self.controlWo.update_camera_selected(
            self.ui.camera_list_cb.currentIndex()))
        self.controlWo.refresh_camera_list()

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        self.ui.camera_la.setPixmap(pixmap)

    def update_tool_or_camera(self):
        if self.ui.tool_or_camera_tb.isChecked():
            self.ui.tool_or_camera_tb.setText("CAMERA_POSITION")
            self.camera_pos_selected = True
        else:
            self.ui.tool_or_camera_tb.setText("TOOL_POSITION")
            self.camera_pos_selected = False

    def check_align_is_active(self):
        self.align_active_s.emit(self.ui.main_tab_widget.currentWidget().objectName() == "align_tab")

    def update_threshold(self):
        self.update_threshold_s.emit(self.ui.contrast_slider.value())

    @Slot(list)
    def update_camera_list(self, camera_list):
        self.ui.camera_list_cb.addItem("No CAMERA")
        for cam in camera_list:
            self.ui.camera_list_cb.addItem(str(cam))

    def update_ui_alignment_applied(self, alignment_applied_flag=False):
        if alignment_applied_flag:
            self.ui.led_la.set_led_color("blue")
            self.ui.led_la.setToolTip("Alignment Applied!")
            self.ui.alignment_led_la.set_led_color("blue")
            self.ui.alignment_led_la.setToolTip("Alignment Applied!")
        else:
            self.ui.led_la.set_led_color("grey")
            self.ui.led_la.setToolTip("Alignment not applied")
            self.ui.alignment_led_la.set_led_color("grey")
            self.ui.alignment_led_la.setToolTip("Alignment not applied")

    def apply_align(self):
        alignment_points = list()
        num_rows = self.ui.align_points_tw.rowCount()
        align_to_be_applied_flag = self.ui.apply_alignment_tb.isChecked() and (num_rows >= 2)
        # Grab alignment points only if apply alignment button is checked
        if align_to_be_applied_flag:
            self.update_ui_alignment_applied(True)
            for r in range(0, num_rows):
                x_base = float(self.ui.align_points_tw.cellWidget(r, 0).text())
                y_base = float(self.ui.align_points_tw.cellWidget(r, 1).text())
                x_offs = float(self.ui.align_points_tw.cellWidget(r, 2).text())
                y_offs = float(self.ui.align_points_tw.cellWidget(r, 3).text())
                points_l = [(x_base, y_base), (x_offs, y_offs)]
                alignment_points.append(points_l)
        else:
            self.update_ui_alignment_applied(False)

        self.align_apply_s.emit(align_to_be_applied_flag, alignment_points)

    @staticmethod
    def compute_offset_point(x_in, y_in, offset_in, angle_in):
        x_out = offset_in + (x_in * math.cos(math.radians(angle_in)) -
                             (y_in * math.sin(math.radians(angle_in))))
        y_out = offset_in + ((x_in * math.sin(math.radians(angle_in))) +
                             (y_in * math.cos(math.radians(angle_in))))
        return x_out, y_out

    def request_new_point(self):
        selection_centroid = self.vis_align_layer.get_selected_centroid()
        offset_info = (0, 0)  # todo: get this from the alignment settings
        if self.camera_pos_selected:
            offset_info = (-1.0, -1.0)  # todo: check and apply correct offset

        self.request_new_alignment_point_coords_s.emit(selection_centroid, offset_info)

    def add_new_point(self):
        x_val = 0  # todo: get the real values
        y_val = 0  # todo: get the real values
        offset_val = 0  # todo: get the real values
        angle_val = 0  # todo: get the real values
        num_rows = self.ui.align_points_tw.rowCount()

        for r in range(0, num_rows):
            actual_x_base = float(self.ui.align_points_tw.cellWidget(r, 0).text())
            actual_y_base = float(self.ui.align_points_tw.cellWidget(r, 1).text())
            updated_x_offs, updated_y_offs = self.compute_offset_point(actual_x_base, actual_y_base,
                                                                       offset_val, angle_val)
            self.ui.align_points_tw.setCellWidget(r, 2, QLabel("{:.3f}".format(updated_x_offs)))
            self.ui.align_points_tw.setCellWidget(r, 3, QLabel("{:.3f}".format(updated_y_offs)))

        new_x_val, new_y_val = self.compute_offset_point(x_val, y_val, offset_val, angle_val)

        self.ui.align_points_tw.insertRow(num_rows)
        self.ui.align_points_tw.setCellWidget(num_rows, 0, QLabel("{:.3f}".format(x_val)))
        self.ui.align_points_tw.setCellWidget(num_rows, 1, QLabel("{:.3f}".format(y_val)))
        self.ui.align_points_tw.setCellWidget(num_rows, 2, QLabel("{:.3f}".format(new_x_val)))
        self.ui.align_points_tw.setCellWidget(num_rows, 3, QLabel("{:.3f}".format(new_y_val)))
        self.apply_align()

    def remove_point(self):
        selection_model = self.ui.align_points_tw.selectionModel()
        selected_rows = selection_model.selectedRows()
        selected_rows.sort()
        for r in selected_rows[::-1]:
            self.ui.align_points_tw.removeRow(r.row())
        self.ui.align_points_tw.clearSelection()
        self.apply_align()

    def load_align_file(self, load_text="Load Align File", extensions=""):
        layer = "drill"
        filters = extensions + ";;All files (*.*)"
        kwargs = {}
        if "PYCHARM_HOSTED" in os.environ:
            logger.debug("pycharm hosted")
            kwargs['options'] = QFileDialog.DontUseNativeDialog
        load_file_path = QFileDialog.getOpenFileName(self.main_win, load_text, self.app_settings.layer_last_dir,
                                                     filters, **kwargs)

        if load_file_path[0]:
            self.vis_align_layer.remove_layer(layer)
            self.vis_align_layer.remove_path(layer)
            self.app_settings.layer_last_dir = os.path.dirname(load_file_path[0])
            logger.info("Loading Align " + load_file_path[0])
            self.load_align_layer_s.emit(layer, load_file_path[0])

    @Slot(Od, str, str, bool)
    def visualize_new_align_layer(self, loaded_layer, layer_tag, layer_path, holes):
        if loaded_layer is None or layer_path == "":
            self.ui.status_bar.showMessage("WARNING: user tried to load an empty layer.", 3000)
        else:
            self.vis_align_layer.add_layer(layer_tag, loaded_layer[0], self.layer_colors[layer_tag], holes)

    @Slot(list)
    def flip_align_layer(self, flip_info):
        self.vis_align_layer.flip_camera(flip_info)


if __name__ == "__main__":
    pass
