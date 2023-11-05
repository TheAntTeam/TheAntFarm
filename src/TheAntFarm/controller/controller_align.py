from PySide2.QtCore import QObject
import qimage2ndarray
from double_side_manager import DoubleSideManager
import logging

logger = logging.getLogger(__name__)


class AlignController(QObject):
    def __init__(self, settings):
        super(AlignController, self).__init__()
        self.settings = settings

        self.double_side_manager = DoubleSideManager()
        self.threshold_value = 0

    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    def get_camera_list(self):
        return self.double_side_manager.list_cameras_indexes()

    def update_camera_selected(self, index):
        return self.double_side_manager.update_camera(index)

    def camera_new_frame(self):
        frame = self.double_side_manager.get_webcam_frame()
        logger.debug(str(self.threshold_value))
        frame = self.double_side_manager.detect_holes(frame, self.threshold_value)
        image = qimage2ndarray.array2qimage(frame)
        return image
