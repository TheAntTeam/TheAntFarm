from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QPixmap
import logging

logger = logging.getLogger(__name__)


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
        self.ui.contrast_slider.valueChanged.connect(self.update_threshold)
        self.update_threshold_s.connect(self.controlWo.update_threshold_value)

        self.controlWo.update_camera_image_s.connect(self.update_camera_image)

    @Slot(QPixmap)
    def update_camera_image(self, pixmap):
        self.ui.camera_la.setPixmap(pixmap)

    def check_align_is_active(self):
        self.align_active_s.emit(self.ui.main_tab_widget.currentWidget().objectName() == "align_tab")

    def update_threshold(self):
        self.update_threshold_s.emit(self.ui.contrast_slider.value())


if __name__ == "__main__":
    pass
