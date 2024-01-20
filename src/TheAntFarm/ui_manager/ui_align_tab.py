from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel
import logging
import math

logger = logging.getLogger(__name__)


class UiAlignTab(QObject):
    """Class dedicated to UI <--> Control interactions on Align Tab. """
    align_active_s = Signal(bool)
    align_apply_s = Signal(bool)
    update_threshold_s = Signal(int)

    def __init__(self, ui, control_worker):
        super(UiAlignTab, self).__init__()
        self.ui = ui
        self.controlWo = control_worker

        # Align TAB related controls.
        self.ui.main_tab_widget.currentChanged.connect(self.check_align_is_active)
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.align_apply_s.connect(self.controlWo.set_align_active)
        self.ui.apply_alignment_tb.clicked.connect(self.apply_align)
        self.ui.add_point_tb.clicked.connect(self.add_new_point)
        self.ui.remove_point_tb.clicked.connect(self.remove_point)
        self.ui.contrast_slider.valueChanged.connect(self.update_threshold)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)

        self.controlWo.update_camera_image_s.connect(self.update_camera_image)
        self.controlWo.update_camera_list_s.connect(self.update_camera_list)
        self.ui.camera_list_cb.currentIndexChanged.connect(lambda: self.controlWo.update_camera_selected(
            self.ui.camera_list_cb.currentIndex()))
        self.controlWo.refresh_camera_list()

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        self.ui.camera_la.setPixmap(pixmap)

    def check_align_is_active(self):
        self.align_active_s.emit(self.ui.main_tab_widget.currentWidget().objectName() == "align_tab")

    def update_threshold(self):
        self.update_threshold_s.emit(self.ui.contrast_slider.value())

    @Slot(list)
    def update_camera_list(self, camera_list):
        for cam in camera_list:
            self.ui.camera_list_cb.addItem(str(cam))

    def apply_align(self):
        self.align_apply_s.emit(self.ui.apply_alignment_tb.isChecked())

    def add_new_point(self):
        x_val = self.ui.x_point_layer_dsb.value()
        y_val = self.ui.y_point_layer_dsb.value()
        offset_val = self.ui.distance_offset_dsb.value()
        angle_val = self.ui.angle_dsb.value()

        new_x_val = x_val + (offset_val * math.cos(math.radians(angle_val)))
        new_y_val = y_val + (offset_val * math.sin(math.radians(angle_val)))

        num_rows = self.ui.align_points_tw.rowCount()
        self.ui.align_points_tw.insertRow(num_rows)
        self.ui.align_points_tw.setCellWidget(num_rows, 0, QLabel("{:.3f}".format(x_val)))
        self.ui.align_points_tw.setCellWidget(num_rows, 1, QLabel("{:.3f}".format(y_val)))
        self.ui.align_points_tw.setCellWidget(num_rows, 2, QLabel("{:.3f}".format(new_x_val)))
        self.ui.align_points_tw.setCellWidget(num_rows, 3, QLabel("{:.3f}".format(new_y_val)))

    def remove_point(self):
        selection_model = self.ui.align_points_tw.selectionModel()
        selected_rows = selection_model.selectedRows()
        selected_rows.sort()
        for r in selected_rows[::-1]:
            self.ui.align_points_tw.removeRow(r.row())
        self.ui.align_points_tw.clearSelection()




if __name__ == "__main__":
    pass
