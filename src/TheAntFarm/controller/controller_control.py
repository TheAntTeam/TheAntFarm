import logging
from collections import OrderedDict, deque

import numpy as np
from app.services.machine_service import MachineService
from PySide6.QtCore import QObject

logger = logging.getLogger(__name__)


class ControlController(QObject):
    def __init__(self, settings):
        super(ControlController, self).__init__()
        self.settings = settings
        self._service = MachineService()

        self.status = []
        self.mpos_a = np.array([0, 0, 0])
        self.wco_a = np.array([0, 0, 0])
        self.wpos_a = np.array([0, 0, 0])
        self.dro_status_updated = False
        self.prb_activated = False
        self.abl_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.prb_val = deque([[-1.0, -1.0, -1.0], [-1.0, -1.0, -1.0]], maxlen=2)
        self.abl_steps = ()
        self.abl_cmd_ls = []
        self.prb_num_todo = 0
        self.prb_num_done = 0
        self.prb_reps_todo = 1
        self.prb_reps_done = 0

    @property
    def status(self):
        return self._service.status

    @status.setter
    def status(self, value):
        self._service.status = value

    @property
    def mpos_a(self):
        return self._service.mpos_a

    @mpos_a.setter
    def mpos_a(self, value):
        self._service.mpos_a = np.array(value)

    @property
    def wco_a(self):
        return self._service.wco_a

    @wco_a.setter
    def wco_a(self, value):
        self._service.wco_a = np.array(value)

    @property
    def wpos_a(self):
        return self._service.wpos_a

    @wpos_a.setter
    def wpos_a(self, value):
        self._service.wpos_a = np.array(value)

    @property
    def status_report_od(self):
        return self._service.status_report_od

    @status_report_od.setter
    def status_report_od(self, value):
        self._service.status_report_od = OrderedDict(value)

    @property
    def workspace_params_od(self):
        return self._service.workspace_params_od

    @workspace_params_od.setter
    def workspace_params_od(self, value):
        self._service.workspace_params_od = OrderedDict(value)

    @property
    def align_data(self):
        return self._service.align_data

    @align_data.setter
    def align_data(self, value):
        self._service.align_data = value

    @property
    def abl_val(self):
        return self._service.abl_val

    @abl_val.setter
    def abl_val(self, value):
        self._service.abl_val = value

    @property
    def gcodes_od(self):
        return self._service.gcodes_od

    @gcodes_od.setter
    def gcodes_od(self, value):
        self._service.gcodes_od = value

    @property
    def prb_activated(self):
        return self._service.prb_activated

    @prb_activated.setter
    def prb_activated(self, value):
        self._service.prb_activated = value

    @property
    def abl_activated(self):
        return self._service.abl_activated

    @abl_activated.setter
    def abl_activated(self, value):
        self._service.abl_activated = value

    @property
    def prb_updated(self):
        return self._service.prb_updated

    @prb_updated.setter
    def prb_updated(self, value):
        self._service.prb_updated = value

    @property
    def abl_updated(self):
        return self._service.abl_updated

    @abl_updated.setter
    def abl_updated(self, value):
        self._service.abl_updated = value

    @property
    def abl_steps(self):
        return self._service.abl_steps

    @abl_steps.setter
    def abl_steps(self, value):
        self._service.abl_steps = value

    @property
    def abl_cmd_ls(self):
        return self._service.abl_cmd_ls

    @abl_cmd_ls.setter
    def abl_cmd_ls(self, value):
        self._service.abl_cmd_ls = value

    @property
    def prb_num_todo(self):
        return self._service.prb_num_todo

    @prb_num_todo.setter
    def prb_num_todo(self, value):
        self._service.prb_num_todo = value

    @property
    def prb_num_done(self):
        return self._service.prb_num_done

    @prb_num_done.setter
    def prb_num_done(self, value):
        self._service.prb_num_done = value

    @property
    def prb_reps_todo(self):
        return self._service.prb_reps_todo

    @prb_reps_todo.setter
    def prb_reps_todo(self, value):
        self._service.prb_reps_todo = value

    @property
    def prb_val(self):
        return self._service.prb_val

    @prb_val.setter
    def prb_val(self, value):
        self._service.prb_val = deque(list(value), maxlen=2)

    def get_probe_value(self):
        return self._service.get_probe_value()

    def set_align_data(self, align_data):
        if isinstance(align_data, (list, tuple)):
            self._service.set_align_data(align_data)
            logger.debug("Applied Alignment DATA")

    def get_align_data(self):
        logger.debug("GET ALIGN DATA")
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
        logger.debug("Apply Alignment")
        self._service.apply_alignment(gcode_path)

    def remove_alignment(self, gcode_path):
        return self._service.remove_alignment(gcode_path)

    def apply_abl(self, gcode_path):
        logger.debug("Apply ABL")
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
        logger.debug(gcode_path)
        return self._service.get_boundary_box(gcode_path)
