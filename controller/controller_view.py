from PySide2.QtCore import QObject
from shape_core.pcb_manager import PcbObj
from shape_core.path_manager import MachinePath
from shape_core.gcode_manager import GCoder
import os
import logging
import traceback

logger = logging.getLogger(__name__)


class ViewController(QObject):
    def __init__(self, settings):
        super(ViewController, self).__init__()
        self.pcb = PcbObj()
        self.settings = settings

    def load_new_layer(self, layer, layer_path):
        try:
            grb_tags = self.pcb.GBR_KEYS
            exc_tags = self.pcb.EXN_KEYS
            if layer in grb_tags:
                self.pcb.load_gerber(layer_path, layer)
                loaded_layer = self.pcb.get_gerber_layer(layer)
                return [loaded_layer, False]
            if layer in exc_tags:
                self.pcb.load_excellon(layer_path, layer)
                loaded_layer = self.pcb.get_excellon_layer(layer)
                return [loaded_layer, True]
        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logging.error(e, exc_info=True)
        except Exception:
            logger.error("Uncaught exception: %s", traceback.format_exc())
        return [None, None]

    def generate_new_path(self, tag, cfg, machining_type):
        if machining_type == "gerber" or machining_type == "profile":
            machining_layer = self.pcb.get_gerber_layer(tag)
        elif machining_type == "drill":
            machining_layer = self.pcb.get_excellon_layer(tag)
        else:
            logger.error("Wrong machining type")
        path = MachinePath(tag, machining_type)
        path.load_geom(machining_layer[0])
        path.load_cfg(cfg)
        path.execute()
        new_paths = path.get_path()
        return new_paths

    def generate_new_gcode_file(self, tag, cfg, machining_type, path):
        if 'mirroring_axis' in self.settings.jobs_settings.jobs_settings_od["common"].keys():
            mt = self.settings.jobs_settings.jobs_settings_od["common"]['mirroring_axis']
            logger.debug("Mirror Axis: " + str(mt))
            gcoder = GCoder(tag, machining_type, mirror_type=mt)
        else:
            gcoder = GCoder(tag, machining_type)
        gcoder.load_cfg(cfg)
        gcoder.load_path(path)
        if gcoder.compute():
            gcode_filename = gcoder.get_file_name()
            gcode_path = os.path.join(self.settings.gcf_settings.gcode_folder, gcode_filename)
            gcoder.write(gcode_path)
        else:
            logging.error("Gcode generation failed.")
