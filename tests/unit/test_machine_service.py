from collections import OrderedDict, deque
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.services.machine_service import MachineService


@pytest.fixture
def service():
    return MachineService()


class TestInit:
    def test_default_state(self, service):
        assert np.array_equal(service.mpos_a, np.array([0.0, 0.0, 0.0]))
        assert np.array_equal(service.wco_a, np.array([0.0, 0.0, 0.0]))
        assert np.array_equal(service.wpos_a, np.array([0.0, 0.0, 0.0]))
        assert service.status == ""
        assert service.status_report_od == OrderedDict()
        assert service.workspace_params_od == OrderedDict()
        assert service.prb_activated is False
        assert service.abl_activated is False
        assert service.prb_updated is False
        assert service.abl_updated is False
        assert service.prb_num_todo == 0
        assert service.prb_num_done == 0
        assert service.prb_reps_todo == 1
        assert service.abl_cmd_ls == []
        assert service.abl_steps == (0, 0)
        assert service.align_data == []
        assert service.gcodes_od == OrderedDict()


class TestParseStatusReport:
    def test_basic_idle_state(self, service):
        line = "<Idle|MPos:1.000,2.000,3.000|WCO:0.000,0.000,0.000>"
        result = service.parse_status_report(line)
        assert result["state"] == "Idle"
        assert np.array_equal(service.mpos_a, np.array([1.0, 2.0, 3.0]))
        assert np.array_equal(service.wco_a, np.array([0.0, 0.0, 0.0]))
        assert np.array_equal(service.wpos_a, np.array([1.0, 2.0, 3.0]))

    def test_with_pins(self, service):
        line = "<Idle|MPos:1.000,2.000,3.000|WCO:0.000,0.000,0.000|Pn:XZ>"
        result = service.parse_status_report(line)
        assert result["pins"] == "XZ"

    def test_with_feed(self, service):
        service.parse_status_report("<Idle|MPos:1.000,2.000,3.000|WCO:0.000,0.000,0.000|F:1500.0>")
        assert service.status_report_od["curfeed"] == 1500.0

    def test_with_fs(self, service):
        service.parse_status_report("<Idle|MPos:1.000,2.000,3.000|WCO:0.000,0.000,0.000|FS:1500.0,24000>")
        assert service.status_report_od["curfeed"] == 1500.0
        assert service.status_report_od["curspindle"] == 24000.0

    def test_with_bf(self, service):
        service.parse_status_report("<Idle|MPos:1.000,2.000,3.000|WCO:0.000,0.000,0.000|Bf:128,145>")
        assert service.status_report_od["planner"] == 128
        assert service.status_report_od["rxbytes"] == 145

    def test_with_ov(self, service):
        service.parse_status_report("<Idle|MPos:1.000,2.000,3.000|WCO:0.000,0.000,0.000|Ov:100,100,100>")
        assert service.status_report_od["OvFeed"] == 100
        assert service.status_report_od["OvRapid"] == 100
        assert service.status_report_od["OvSpindle"] == 100

    def test_with_wco_offset(self, service):
        service.parse_status_report("<Idle|MPos:1.000,2.000,3.000|WCO:0.100,0.200,0.300>")
        assert np.array_equal(service.wco_a, np.array([0.1, 0.2, 0.3]))
        assert np.array_equal(service.wpos_a, np.array([0.9, 1.8, 2.7]))

    def test_malformed_field_does_not_raise(self, service):
        service.parse_status_report("<Idle|MPos:1.000,2.000|WCO:0.000,0.000,0.000>")
        assert service.status_report_od["state"] == "Idle"


class TestParseBracketSquare:
    def test_prb(self, service):
        service.prb_updated = False
        service.parse_bracket_square("[PRB:1.000,2.000,3.000:1]")
        assert service.prb_updated is True
        assert list(service.prb_val[0]) == [1.0, 2.0, 3.0]

    def test_g54(self, service):
        service.parse_bracket_square("[G54:1.000,2.000,3.000]")
        assert "G54" in service.workspace_params_od
        assert np.array_equal(service.workspace_params_od["G54"], np.array([1.0, 2.0, 3.0]))

    def test_g55(self, service):
        service.parse_bracket_square("[G55:1.000,2.000,3.000]")
        assert "G55" in service.workspace_params_od

    def test_tlo(self, service):
        service.parse_bracket_square("[TLO:1.234]")
        assert service.workspace_params_od["TLO"] == 1.234


class TestProbeAndAbl:
    def test_process_probe_activated(self, service):
        service.prb_activated = True
        service.prb_updated = True
        result = service.process_probe_and_abl()
        assert result == (True, False, False, False)

    def test_process_abl_activated(self, service):
        service.abl_activated = True
        service.prb_updated = True
        service.prb_num_done = 0
        service.prb_num_todo = 5
        service.prb_val = deque([[1.0, 2.0, 3.0], [-1.0, -1.0, -1.0]], maxlen=2)
        result = service.process_probe_and_abl()
        assert result == (False, False, True, False)
        assert len(service.abl_val) == 1

    def test_process_abl_acknowledges_last(self, service):
        service.abl_activated = True
        service.prb_updated = True
        service.prb_num_done = 4
        service.prb_num_todo = 5
        service.prb_val = deque([[1.0, 2.0, 3.0], [-1.0, -1.0, -1.0]], maxlen=2)
        result = service.process_probe_and_abl()
        assert result == (False, True, False, False)
        assert service.abl_activated is False

    def test_process_other(self, service):
        service.prb_activated = False
        service.prb_updated = False
        service.abl_activated = False
        result = service.process_probe_and_abl()
        assert result == (False, False, False, True)

    def test_arm_probe(self, service):
        service.arm_probe()
        assert service.prb_activated is True
        assert service.prb_updated is False
        assert service.prb_num_todo == 1
        assert service.prb_reps_todo == 1

    def test_get_probe_value(self, service):
        service.prb_val.appendleft([1.0, 2.0, 3.0])
        result = service.get_probe_value()
        assert result == [1.0, 2.0, 3.0]

    def test_get_next_abl_command(self, service):
        service.abl_cmd_ls = ["G0 X0", "G1 Z-1"]
        cmd = service.get_next_abl_command()
        assert cmd == "G0 X0"
        assert cmd == service.get_next_abl_command()  # idempotent, does not consume

    def test_get_next_abl_command_returns_none_when_done(self, service):
        service.abl_cmd_ls = []
        service.prb_num_done = 0
        assert service.get_next_abl_command() is None

    @patch.object(MachineService, "get_grid_coords", return_value=[(0.0, 0.0)])
    @patch.object(MachineService, "make_cmd_auto_bed_levelling", return_value=[["G38.2 Z-1 F100"], 1])
    def test_arm_auto_bed_levelling(self, mock_grid, mock_make, service):
        bbox_t = (0, 0, -1, 10, 10, 5)
        steps_t = (3, 3)
        xy_c_l = MachineService.get_grid_coords(bbox_t, steps_t)
        abl_cmd_ls, prb_num_todo = MachineService.make_cmd_auto_bed_levelling(xy_c_l, 5, -1, 100)
        service.arm_auto_bed_levelling(abl_cmd_ls, prb_num_todo, steps_t)
        assert service.abl_activated is True
        assert service.abl_cmd_ls == ["G38.2 Z-1 F100"]
        assert service.prb_num_todo == 1
        assert service.abl_steps == (3, 3)


class TestGetGridCoords:
    def test_returns_correct_points(self):
        bbox = (0, 0, -1, 10, 10, 5)
        steps = (3, 3)
        coords = MachineService.get_grid_coords(bbox, steps)
        assert len(coords) == 9
        assert coords[0] == (0.0, 0.0)
        assert coords[4] == (5.0, 5.0)
        assert coords[8] == (10.0, 10.0)


class TestAlignment:
    def test_set_align_data(self, service):
        data = [((1, 2), (3, 4))]
        service.set_align_data(data)
        assert service.align_data == data

    def test_set_align_data_rejects_non_list(self, service):
        service.set_align_data("invalid")
        assert service.align_data == []

    def test_get_align_data(self, service):
        data = [((1, 2), (3, 4))]
        service.align_data = data
        assert service.get_align_data() == data


class TestGcodeRegistry:
    def test_register_and_deregister(self, service):
        mock_gcp = MagicMock()
        tag = service.register_gcode("/test.gcode", mock_gcp)
        assert len(tag) == 4
        assert tag in {v["tag"] for v in service.gcodes_od.values()}
        assert service.gcodes_od["/test.gcode"]["gcode"] is mock_gcp

        service.deregister_gcode("/test.gcode")
        assert "/test.gcode" not in service.gcodes_od

    def test_get_gcode_entry_missing_returns_none(self, service):
        assert service.get_gcode_entry("/nonexistent.gcode") is None
