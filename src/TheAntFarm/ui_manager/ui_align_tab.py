from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap
import logging

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
        self.align_applied = False

        # Align TAB related controls.
        self.ui.main_tab_widget.currentChanged.connect(self.check_align_is_active)
        self.align_active_s.connect(self.controlWo.set_align_is_active)
        self.align_apply_s.connect(lambda align_active_bool: self.controlWo.set_align_active(align_active_bool))
        self.ui.apply_alignment_tb.clicked.connect(self.apply_align)
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
        align_activated = not self.ui.apply_alignment_tb.isChecked()
        self.align_apply_s.emit(align_activated)


if __name__ == "__main__":
    pass
