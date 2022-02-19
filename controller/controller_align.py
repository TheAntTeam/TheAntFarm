from PySide6.QtCore import QObject
from PySide6.QtGui import QImage
from double_side_manager import DoubleSideManager
import logging
import traceback

logger = logging.getLogger(__name__)


class AlignController(QObject):
    def __init__(self, settings):
        super(AlignController, self).__init__()
        self.settings = settings

        self.double_side_manager = DoubleSideManager()
        self.threshold_value = 0

    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    def camera_new_frame(self):
        frame = self.double_side_manager.get_webcam_frame()
        logger.debug(str(self.threshold_value))
        frame = self.double_side_manager.detect_holes(frame, self.threshold_value)

        # frame is a numpy array expected to be 640x480, RGB - (see double_side_manager.py)
        height, width, channel = frame.shape
        image = QImage(frame.data, width, height, width * 3, QImage.Format_RGB888)
        return image
