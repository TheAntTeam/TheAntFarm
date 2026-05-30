import logging

from app.services.machine_service import MachineService

logger = logging.getLogger(__name__)

_DELEGATED = {
    "status", "mpos_a", "wco_a", "wpos_a",
    "status_report_od", "workspace_params_od",
    "align_data", "abl_val", "gcodes_od",
    "prb_activated", "abl_activated", "prb_updated", "abl_updated",
    "abl_steps", "abl_cmd_ls",
    "prb_num_todo", "prb_num_done", "prb_reps_todo",
    "prb_val",
}


class ControlController:
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._service = MachineService()

    def __getattr__(self, name):
        if name in _DELEGATED:
            return getattr(self._service, name)
        msg = f"'{type(self).__name__}' has no attribute '{name}'"
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        if name in _DELEGATED:
            setattr(self._service, name, value)
        else:
            super().__setattr__(name, value)

    def get_probe_value(self):
        return self._service.get_probe_value()

    def set_align_data(self, align_data):
        if isinstance(align_data, (list, tuple)):
            self._service.set_align_data(align_data)

    def get_align_data(self):
        return self._service.get_align_data()

    def get_abl_value(self):
        return self._service.get_abl_value()

    def get_next_abl_cmd(self):
        return self._service.get_next_abl_command()

    def process_probe_and_abl(self):
        return list(self._service.process_probe_and_abl())

    def parse_bracket_angle(self, line):
        return self._service.parse_status_report(line)

    def parse_bracket_square(self, line):
        self._service.parse_bracket_square(line)
        return self.prb_val[0]

    def cmd_probe(self):
        self._service.arm_probe()

    def cmd_auto_bed_levelling(self, bbox_t, steps_t, feedrate_probe):
        xy_coord_list = self._service.get_grid_coords(bbox_t, steps_t)
        travel_z = bbox_t[5]
        probe_z_min = bbox_t[2]
        logger.debug(xy_coord_list)

        [abl_cmd_ls, prb_num_todo] = self._service.make_cmd_auto_bed_levelling(
            xy_coord_list, travel_z, probe_z_min, feedrate_probe
        )
        self._service.arm_auto_bed_levelling(abl_cmd_ls, prb_num_todo, (steps_t[0], steps_t[1]))

        return [self.abl_cmd_ls, self.prb_num_todo]

    def load_gcode_file(self, cfg, gcode_path):
        self._service.load_gcode_file(cfg, gcode_path)

    def remove_gcode_file(self, gcode_path):
        self._service.deregister_gcode(gcode_path)

    def get_gcode_tag_and_v(self, gcode_path):
        entry = self._service.get_gcode_entry(gcode_path)
        v = entry["gcode"].get_gcode_vectors()
        tag = entry["tag"]
        return tag, v

    def apply_alignment(self, gcode_path):
        self._service.apply_alignment(gcode_path)

    def remove_alignment(self, gcode_path):
        return self._service.remove_alignment(gcode_path)

    def apply_abl(self, gcode_path):
        self._service.apply_abl(gcode_path)

    def remove_abl(self, gcode_path):
        return self._service.remove_abl(gcode_path)

    def get_gcode_gcp(self, gcode_path):
        return self._service.get_gcode_gcp(gcode_path)

    def get_gcode_lines(self, gcode_path):
        return self._service.get_gcode_lines(gcode_path)

    def get_change_tool_lines(self):
        return self._service.get_change_tool_lines()

    def get_boundary_box(self, gcode_path):
        return self._service.get_boundary_box(gcode_path)
