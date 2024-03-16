import os.path

from PySide2.QtCore import QObject
from PySide2 import QtMultimedia
import qimage2ndarray
from shape_core.pcb_manager import PcbObj
from shape_core.gcode_drill_converter import DrillGcodeConverter
from double_side_manager import DoubleSideManager
import logging
import traceback

logger = logging.getLogger(__name__)


class AlignController(QObject):

    EXCELLON_EXTENSIONS = (".xln", ".drl")

    def __init__(self, settings):
        super(AlignController, self).__init__()
        self.settings = settings

        self.pcb = PcbObj()
        # TODO: parametrize drill diameter for gcode conversion
        dgc_cfg = {
            "default_gcode_drill_size": 0.7
        }
        self.dgc = DrillGcodeConverter(cfg=dgc_cfg)

        self.double_side_manager = DoubleSideManager()
        self.threshold_value = 0
        self.fipping_view = [False, False, False]

    def load_new_align_layer(self, layer, layer_path):
        try:
            exc_tags = self.pcb.EXN_KEYS
            if layer in exc_tags:
                ext = os.path.splitext(layer_path)[1]
                if ext.lower() in self.EXCELLON_EXTENSIONS:
                    self.pcb.load_excellon(layer_path, layer)
                    loaded_layer = self.pcb.get_excellon_layer(layer)
                    if not loaded_layer[0]:
                        loaded_layer = None
                else:
                    self.dgc.load_gcode(layer_path)
                    self.dgc.convert()
                    loaded_layer = self.dgc.get_drill_layer()
                    if not loaded_layer[0]:
                        loaded_layer = None
                return [loaded_layer, True]

        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logging.error(e, exc_info=True)
        except Exception:
            logger.error("Uncaught exception: %s", traceback.format_exc())

        return [None, None]

    def flip_align_layer_horizontally(self, flipped):
        self.fipping_view[0] = flipped

    def flip_align_layer_vertically(self, flipped):
        self.fipping_view[1] = flipped

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
