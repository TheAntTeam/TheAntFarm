from PySide2.QtCore import Signal, Slot, QObject, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QFileDialog, QHeaderView
from collections import OrderedDict as Od
from style_manager import StyleManager
from qcamera_label import QCameraLabel
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
    request_new_alignment_point_coords_s = Signal(list, bool)
    remove_point_rows = Signal(list)
    update_zoom_value_s = Signal(int)

    MIN_ALIGNMENT_POINTS_NUMBER = 4

    def __init__(self, main_win, control_worker, vis_align_layer, app_settings):
        super(UiAlignTab, self).__init__()
        self.main_win = main_win
        self.ui = self.main_win.ui
        self.controlWo = control_worker
        self.vis_align_layer = vis_align_layer
        self.app_settings = app_settings

        self.layer_colors = self.app_settings.layer_color

        align_extensions = "Excellon (*.xln *.XLN *.drl *.DRL)"

        align_points_tw_horizontal_headers = self.ui.align_points_tw.horizontalHeader()
        align_points_tw_horizontal_headers.setSectionResizeMode(0, QHeaderView.Stretch)
        align_points_tw_horizontal_headers.setSectionResizeMode(1, QHeaderView.Stretch)
        align_points_tw_horizontal_headers.setSectionResizeMode(2, QHeaderView.Stretch)
        align_points_tw_horizontal_headers.setSectionResizeMode(3, QHeaderView.Stretch)

        # Align TAB related controls.
        self.load_align_layer_s.connect(self.controlWo.load_new_align_layer)
        self.controlWo.update_align_layer_s.connect(self.visualize_new_align_layer)
        self.controlWo.update_align_layer_view_s.connect(self.flip_align_layer)
        self.ui.main_tab_widget.currentChanged.connect(self.check_align_is_active)
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.align_apply_s.connect(self.controlWo.set_align_active)
        # self.ui.apply_alignment_tb.clicked.connect(self.apply_align)
        self.ui.apply_alignment_tb.clicked.connect(
            lambda: self.set_alignment_tb_check(self.ui.apply_alignment_tb.isChecked()))
        self.ui.apply_alignment_tb_2.clicked.connect(
            lambda: self.set_alignment_tb_check(self.ui.apply_alignment_tb_2.isChecked()))
        self.ui.add_point_tb.clicked.connect(self.request_new_point)
        self.ui.remove_point_tb.clicked.connect(self.remove_point)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)
        self.ui.load_align_layer_tb.clicked.connect(
            lambda: self.load_align_file("Load Align File", align_extensions))

        self.ui.flip_horizontally_tb.setChecked(self.app_settings.flip_horizontal_selected)
        self.ui.flip_horizontally_tb.clicked.connect(
            lambda: self.controlWo.flip_align_layer_horizontally(self.ui.flip_horizontally_tb.isChecked()))
        self.ui.flip_vertically_tb.setChecked(self.app_settings.flip_vertical_selected)
        self.ui.flip_vertically_tb.clicked.connect(
            lambda: self.controlWo.flip_align_layer_vertically(self.ui.flip_vertically_tb.isChecked()))
        self.request_new_alignment_point_coords_s.connect(self.controlWo.add_new_align_point)
        self.remove_point_rows.connect(self.controlWo.remove_align_points)

        self.ui.tool_or_camera_tb.setChecked(self.app_settings.camera_selected_or_tool)
        self.update_tool_or_camera()
        self.ui.tool_or_camera_tb.clicked.connect(self.update_tool_or_camera)

        self.controlWo.update_camera_image_s.connect(self.update_camera_image)
        self.controlWo.update_camera_list_s.connect(self.update_camera_list)
        self.ui.camera_list_cb.currentIndexChanged.connect(lambda: self.controlWo.update_camera_selected(
            self.ui.camera_list_cb.currentIndex()))
        self.controlWo.refresh_camera_list()

        self.controlWo.update_align_points_s.connect(self.update_alignment_points_list)
        self.camera_zoom_cb_init()
        self.ui.camera_zoom_cb.currentIndexChanged.connect(lambda: self.update_zoom_value(
            int(self.ui.camera_zoom_cb.currentText()[:-1])))

        self.ui.camera_la.mouse_wheel_up_or_down_s.connect(self.update_camera_zoom)
        self.update_zoom_value_s.connect(self.controlWo.update_camera_zoom_value)

    def camera_zoom_cb_init(self):
        self.ui.camera_zoom_cb.clear()
        self.ui.camera_zoom_cb.addItems(["1x", "2x", "3x", "4x", "5x"])
        self.ui.camera_zoom_cb.setCurrentIndex(0)

    @Slot(int)
    def update_camera_zoom(self, increment):
        zoom_cb_index = self.ui.camera_zoom_cb.currentIndex()
        zoom_cb_max = self.ui.camera_zoom_cb.count()
        new_cb_index = zoom_cb_index + increment
        if 0 <= new_cb_index < zoom_cb_max:
            self.ui.camera_zoom_cb.setCurrentIndex(new_cb_index)
            current_zoom = int(self.ui.camera_zoom_cb.currentText()[:-1])
            self.update_zoom_value(current_zoom)

    def update_zoom_value(self, current_zoom_value):
        self.update_zoom_value_s.emit(current_zoom_value)

    def remove_point(self):
        sel_model = self.ui.align_points_tw.selectionModel()
        sel_rows = sel_model.selectedRows()
        row_indexes = [x.row() for x in sel_rows]
        self.remove_point_rows.emit(row_indexes)

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        if not pixmap.isNull():
            scaled_frame = pixmap.scaled(self.ui.camera_la.width(), 1000, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.camera_la.setPixmap(scaled_frame)
            # self.ui.camera_la.setPixmap(pixmap)

    def update_tool_or_camera(self):
        if self.ui.tool_or_camera_tb.isChecked():
            self.ui.tool_or_camera_tb.setText("CAMERA_POSITION")
            self.app_settings.camera_selected_or_tool = True
        else:
            self.ui.tool_or_camera_tb.setText("TOOL_POSITION")
            self.app_settings.camera_selected_or_tool = False

    def check_align_is_active(self):
        self.align_active_s.emit(self.ui.main_tab_widget.currentWidget().objectName() == "align_tab")

    @Slot(list)
    def update_camera_list(self, camera_list):
        self.ui.camera_list_cb.addItem("No CAMERA")
        for cam in camera_list:
            self.ui.camera_list_cb.addItem(str(cam))

    def update_ui_alignment_applied(self, alignment_applied_flag, num_points):
        if alignment_applied_flag:
            self.ui.apply_alignment_tb.setStyleSheet(StyleManager.set_tool_button_color(bg_color="blue",
                                                                                        color="black"))
            self.ui.apply_alignment_tb_2.setStyleSheet(StyleManager.set_tool_button_color(bg_color="blue",
                                                                                          color="black"))
        elif num_points >= self.MIN_ALIGNMENT_POINTS_NUMBER:
            self.ui.apply_alignment_tb.setStyleSheet(StyleManager.set_tool_button_color(bg_color="yellow",
                                                                                        color="black"))
            self.ui.apply_alignment_tb_2.setStyleSheet(StyleManager.set_tool_button_color(bg_color="yellow",
                                                                                          color="black"))
        else:
            self.ui.apply_alignment_tb.setStyleSheet(StyleManager.set_tool_button_color(bg_color="QColor(53, 53, 53)",
                                                                                        color="white"))
            self.ui.apply_alignment_tb_2.setStyleSheet(StyleManager.set_tool_button_color(bg_color="QColor(53, 53, 53)",
                                                                                          color="white"))

    def set_alignment_tb_check(self, alignment_check_status):
        self.ui.apply_alignment_tb.clicked.disconnect()
        self.ui.apply_alignment_tb_2.clicked.disconnect()

        self.ui.apply_alignment_tb.setChecked(alignment_check_status)  # sync check status of the aliment tb
        self.ui.apply_alignment_tb_2.setChecked(alignment_check_status)  # sync check status of the aliment tb

        self.ui.apply_alignment_tb.clicked.connect(
            lambda: self.set_alignment_tb_check(self.ui.apply_alignment_tb.isChecked()))
        self.ui.apply_alignment_tb_2.clicked.connect(
            lambda: self.set_alignment_tb_check(self.ui.apply_alignment_tb_2.isChecked()))

        self.apply_align()

    def apply_align(self):
        alignment_points = list()
        num_rows = self.ui.align_points_tw.rowCount()
        alignment_tb_check_status = self.ui.apply_alignment_tb.isChecked()
        align_to_be_applied_flag = alignment_tb_check_status and (num_rows >= self.MIN_ALIGNMENT_POINTS_NUMBER)
        # Grab alignment points only if apply alignment button is checked
        if align_to_be_applied_flag:
            self.update_ui_alignment_applied(True, num_rows)
            for r in range(0, num_rows):
                x_base = float(self.ui.align_points_tw.cellWidget(r, 0).text())
                y_base = float(self.ui.align_points_tw.cellWidget(r, 1).text())
                x_offs = float(self.ui.align_points_tw.cellWidget(r, 2).text())
                y_offs = float(self.ui.align_points_tw.cellWidget(r, 3).text())
                points_l = [(x_base, y_base), (x_offs, y_offs)]
                alignment_points.append(points_l)
        else:
            self.update_ui_alignment_applied(False, num_rows)
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

        self.request_new_alignment_point_coords_s.emit(selection_centroid, self.app_settings.camera_selected_or_tool)

    @Slot(list)
    def update_alignment_points_list(self, alignment_coords_l):

        self.ui.align_points_tw.setRowCount(0)  # Remove all elements
        num_rows = 0

        for r in alignment_coords_l:
            self.ui.align_points_tw.insertRow(num_rows)
            self.ui.align_points_tw.setCellWidget(num_rows, 0, QLabel("{:.3f}".format(r[0][0])))
            self.ui.align_points_tw.setCellWidget(num_rows, 1, QLabel("{:.3f}".format(r[0][1])))
            self.ui.align_points_tw.setCellWidget(num_rows, 2, QLabel("{:.3f}".format(r[1][0])))
            self.ui.align_points_tw.setCellWidget(num_rows, 3, QLabel("{:.3f}".format(r[1][1])))
            num_rows += 1

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
