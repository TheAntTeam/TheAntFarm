import logging

from app.services.pcb_service import PcbService

logger = logging.getLogger(__name__)


class ViewController:
    GERBER_LAYER_TAGS = ("top", "bottom", "profile", "noncopper_top", "noncopper_bottom")
    EXCELLON_LAYER_TAGS = ("drill",)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._service = PcbService()

    def load_new_layer(self, layer, layer_path):
        result = self._service.load_layer(layer, layer_path)

        # Keep legacy return contract expected by ControllerWorker/tests:
        # [loaded_layer, exc_flag] where exc_flag is None only for unknown layer tags.
        if result.ok and result.layer_data is not None:
            return [result.layer_data, result.has_drill_exceptions]

        if layer in self.GERBER_LAYER_TAGS or layer in self.EXCELLON_LAYER_TAGS:
            return [None, result.has_drill_exceptions]
        return [None, None]

    def generate_new_path(self, tag, cfg, machining_type):
        result = self._service.generate_path(tag, cfg, machining_type)
        return result.paths

    def generate_new_gcode_file(self, tag, cfg, machining_type, path):
        mt = "x"
        if "mirroring_axis" in self.settings.jobs_settings.jobs_settings_od["common"].keys():
            mt = self.settings.jobs_settings.jobs_settings_od["common"]["mirroring_axis"]
            logger.debug("Mirror Axis: " + str(mt))

        result = self._service.generate_gcode(
            tag=tag,
            cfg=cfg,
            machining_type=machining_type,
            paths=path,
            output_folder=self.settings.gcf_settings.gcode_folder,
            mirror_type=str(mt).lower(),
        )
        if not result.gcode_path:
            logging.error("Gcode generation failed.")
