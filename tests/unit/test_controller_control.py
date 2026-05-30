import pytest
from collections import OrderedDict, deque
from unittest.mock import MagicMock, patch
import numpy as np


@pytest.fixture(scope="module")
def mock_settings():
    settings = MagicMock()
    return settings


@pytest.fixture(scope="module")
def control_controller(mock_settings):
    from controller.controller_control import ControlController
    return ControlController(mock_settings)


def test_init_attributes(control_controller, mock_settings):
    assert control_controller.settings == mock_settings
    assert control_controller.status == ""
    assert np.array_equal(control_controller.mpos_a, np.array([0, 0, 0]))
    assert np.array_equal(control_controller.wco_a, np.array([0, 0, 0]))
    assert np.array_equal(control_controller.wpos_a, np.array([0, 0, 0]))
    assert control_controller.prb_activated is False
    assert control_controller.abl_activated is False
    assert control_controller.prb_updated is False
    assert control_controller.abl_updated is False
    assert control_controller.align_data == []
    assert control_controller.abl_cmd_ls == []
    assert control_controller.prb_num_todo == 0
    assert control_controller.prb_num_done == 0
    assert control_controller.status_report_od == OrderedDict({})
    assert control_controller.workspace_params_od == OrderedDict({})
    assert control_controller.gcodes_od == OrderedDict({})


def test_get_probe_value(control_controller):
    control_controller.prb_val.appendleft([1.0, 2.0, 3.0])
    result = control_controller.get_probe_value()
    assert result == [1.0, 2.0, 3.0]


def test_set_align_data_list(control_controller):
    align_data = [((1, 2), (3, 4)), ((5, 6), (7, 8))]
    control_controller.set_align_data(align_data)
    assert control_controller.align_data == align_data


def test_set_align_data_tuple(control_controller):
    align_data = (((1, 2), (3, 4)), ((5, 6), (7, 8)))
    control_controller.set_align_data(align_data)
    assert control_controller.align_data == align_data


def test_get_align_data(control_controller):
    control_controller.align_data = [((1, 2), (3, 4))]
    result = control_controller.get_align_data()
    assert result == [((1, 2), (3, 4))]


def test_get_abl_value(control_controller):
    control_controller.abl_val = [[1.0, 2.0, 3.0]]
    result = control_controller.get_abl_value()
    assert result == [[1.0, 2.0, 3.0]]


def test_process_probe_and_abl_probe_activated(control_controller):
    control_controller.prb_activated = True
    control_controller.prb_updated = True
    result = control_controller.process_probe_and_abl()
    assert result[0] is True
    assert result[3] is False


def test_process_probe_and_abl_abl_activated(control_controller):
    control_controller.prb_activated = False
    control_controller.prb_updated = False
    control_controller.abl_activated = True
    with patch.object(control_controller._service, "process_probe_and_abl", return_value=(False, False, True, False)):
        result = control_controller.process_probe_and_abl()
        assert result[2] is True


def test_process_probe_and_abl_other(control_controller):
    control_controller.prb_activated = False
    control_controller.prb_updated = False
    control_controller.abl_activated = False
    result = control_controller.process_probe_and_abl()
    assert result[3] is True


def test_parse_bracket_angle_mpos(control_controller):
    line = "<Idle|MPos:1.000,2.000,3.000|WPos:0.000,0.000,0.000>"
    control_controller.parse_bracket_angle(line)
    assert control_controller.status_report_od["state"] == "Idle"


def test_parse_bracket_angle_with_pins(control_controller):
    line = "<Idle|MPos:1.000,2.000,3.000|WPos:0.000,0.000,0.000|Pn:XZ>"
    control_controller.parse_bracket_angle(line)
    assert control_controller.status_report_od["pins"] == "XZ"


def test_parse_bracket_angle_feed(control_controller):
    control_controller.parse_bracket_angle("<Idle,MPos:1.000,2.000,3.000,F:1500.0,WPos:0.000,0.000,0.000>")


def test_parse_bracket_angle_fs(control_controller):
    control_controller.parse_bracket_angle("<Idle,MPos:1.000,2.000,3.000,FS:1500.0,24000,WPos:0.000,0.000,0.000>")


def test_parse_bracket_angle_bf(control_controller):
    control_controller.parse_bracket_angle("<Idle,MPos:1.000,2.000,3.000,Bf:128,145,WPos:0.000,0.000,0.000>")


def test_parse_bracket_angle_ov(control_controller):
    control_controller.parse_bracket_angle("<Idle,MPos:1.000,2.000,3.000,Ov:100,100,100,WPos:0.000,0.000,0.000>")


def test_parse_bracket_angle_wco(control_controller):
    control_controller.parse_bracket_angle("<Idle,MPos:1.000,2.000,3.000,WCO:0.100,0.200,0.300,WPos:0.900,0.800,0.700>")


def test_parse_bracket_square_prb(control_controller):
    control_controller.prb_updated = False
    line = "[PRB:1.000,2.000,3.000:1]"
    result = control_controller.parse_bracket_square(line)
    assert control_controller.prb_updated is True


def test_parse_bracket_square_g54(control_controller):
    line = "[G54:1.000,2.000,3.000]"
    result = control_controller.parse_bracket_square(line)
    assert "G54" in control_controller.workspace_params_od


def test_parse_bracket_square_g55(control_controller):
    line = "[G55:1.000,2.000,3.000]"
    result = control_controller.parse_bracket_square(line)
    assert "G55" in control_controller.workspace_params_od


def test_parse_bracket_square_tlo(control_controller):
    line = "[TLO:1.234]"
    result = control_controller.parse_bracket_square(line)
    assert control_controller.workspace_params_od["TLO"] == 1.234


def test_cmd_probe(control_controller):
    control_controller.cmd_probe()
    assert control_controller.prb_activated is True
    assert control_controller.prb_updated is False
    assert control_controller.prb_num_todo == 1
    assert control_controller.prb_reps_todo == 1


def test_cmd_auto_bed_levelling_delegates_grid_and_cmd_builder(control_controller):
    bbox_t = (0, 0, -1, 10, 10, 5)
    steps_t = (3, 3)
    with patch.object(control_controller._service, "get_grid_coords", return_value=[(0.0, 0.0)]), patch.object(
        control_controller._service,
        "make_cmd_auto_bed_levelling",
        return_value=[["G38.2 Z-1 F100"], 1],
    ), patch.object(control_controller._service, "arm_auto_bed_levelling") as arm_mock:
        result = control_controller.cmd_auto_bed_levelling(bbox_t, steps_t, 100)

    assert result[1] == 1
    assert result[0] == control_controller.abl_cmd_ls
    arm_mock.assert_called_once_with(["G38.2 Z-1 F100"], 1, (3, 3))


def test_process_probe_and_abl_sends_next_abl_probe(control_controller):
    control_controller.prb_activated = False
    control_controller.abl_activated = True
    control_controller.prb_updated = True
    control_controller.prb_num_done = 0
    control_controller.prb_num_todo = 5
    control_controller.abl_val = []
    control_controller.prb_val = deque([[1.0, 2.0, 3.0], [-1.0, -1.0, -1.0]], maxlen=2)
    result = control_controller.process_probe_and_abl()
    assert result[1] is False
    assert result[2] is True
    assert len(control_controller.abl_val) == 1


def test_process_probe_and_abl_acknowledges_last_abl_probe(control_controller):
    control_controller.prb_activated = False
    control_controller.abl_activated = True
    control_controller.prb_updated = True
    control_controller.prb_num_done = 4
    control_controller.prb_num_todo = 5
    control_controller.abl_val = [[1, 1, 1]]
    control_controller.prb_val = deque([[1.0, 2.0, 3.0], [-1.0, -1.0, -1.0]], maxlen=2)
    result = control_controller.process_probe_and_abl()
    assert result[1] is True
    assert control_controller.abl_activated is False


def test_load_gcode_file(control_controller):
    with patch.object(control_controller._service, "load_gcode_file") as load_mock:
        control_controller.load_gcode_file({}, "/test.gcode")
    load_mock.assert_called_once_with({}, "/test.gcode")


def test_remove_gcode_file(control_controller):
    control_controller.gcodes_od = {"test.gcode": {"gcode": MagicMock(), "tag": "ABCD"}}
    control_controller.remove_gcode_file("test.gcode")
    assert "test.gcode" not in control_controller.gcodes_od


def test_get_gcode_tag_and_v(control_controller):
    mock_gcp = MagicMock()
    mock_gcp.get_gcode_vectors.return_value = []
    control_controller.gcodes_od = {"test.gcode": {"gcode": mock_gcp, "tag": "ABCD"}}
    tag, v = control_controller.get_gcode_tag_and_v("test.gcode")
    assert tag == "ABCD"
    assert v == []


def test_get_boundary_box(control_controller):
    mock_gcp = MagicMock()
    mock_gcp.get_bbox.return_value = (0, 0, 10, 10)
    control_controller.gcodes_od = {"test.gcode": {"gcode": mock_gcp, "tag": "ABCD"}}
    result = control_controller.get_boundary_box("test.gcode")
    assert result == (0, 0, 10, 10)