from PySide2.QtCore import QObject
from PySide2 import QtMultimedia
import qimage2ndarray
from shape_core.pcb_manager import PcbObj
from double_side_manager import DoubleSideManager
import logging
import traceback

logger = logging.getLogger(__name__)


class AlignController(QObject):
    def __init__(self, settings):
        super(AlignController, self).__init__()
        self.settings = settings

        self.pcb = PcbObj()

        self.double_side_manager = DoubleSideManager()
        self.threshold_value = 0

    def load_new_align_layer(self, layer, layer_path):
        try:
            # grb_tags = self.pcb.GBR_KEYS
            exc_tags = self.pcb.EXN_KEYS
            # This commented part should change to be used for
            # GCODE conversion to drill file
            # if layer in grb_tags:
            #     self.pcb.load_gerber(layer_path, layer)
            #     loaded_layer = self.pcb.get_gerber_layer(layer)
            #     if not loaded_layer[0]:
            #         loaded_layer = None
            #     return [loaded_layer, False]
            if layer in exc_tags:
                self.pcb.load_excellon(layer_path, layer)
                loaded_layer = self.pcb.get_excellon_layer(layer)
                if not loaded_layer[0]:
                    loaded_layer = None
                return [loaded_layer, True]
        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logging.error(e, exc_info=True)
        except Exception:
            logger.error("Uncaught exception: %s", traceback.format_exc())
        return [None, None]

    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    def get_camera_list(self):
        return self.double_side_manager.list_cameras_indexes()

    def update_camera_selected(self, index):
        return self.double_side_manager.update_camera(index)

    def camera_new_frame(self):
        frame = self.double_side_manager.get_webcam_frame()
        image = None
        if frame is not None:
            frame = self.double_side_manager.detect_holes(frame, self.threshold_value)
            image = qimage2ndarray.array2qimage(frame)
        return image
