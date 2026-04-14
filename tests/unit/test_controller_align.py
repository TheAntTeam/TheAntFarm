import pytest
import numpy as np
from unittest.mock import MagicMock, patch, PropertyMock


@pytest.fixture(scope="module")
def mock_settings():
    settings = MagicMock()
    settings.app_settings.camera_rotation_angle = 0
    settings.app_settings.camera_flip_h = False
    settings.app_settings.camera_flip_v = False
    return settings


@pytest.fixture(scope="module")
def align_controller(mock_settings):
    with patch("PySide6.QtMultimedia"), \
         patch("double_side_manager.DoubleSideManager"), \
         patch("controller.controller_align.PcbObj"), \
         patch("controller.controller_align.DrillGcodeConverter"):
        from controller.controller_align import AlignController
        return AlignController(mock_settings)


def test_init_attributes(align_controller, mock_settings):
    assert align_controller.settings == mock_settings
    assert align_controller.pcb is not None
    assert align_controller.dgc is not None
    assert align_controller.double_side_manager is not None
    assert align_controller.threshold_value == 0
    assert align_controller.flipping_view == [False, False, False]
    assert align_controller.align_data == []


def test_load_new_align_layer_excellon_valid(align_controller):
    align_controller.pcb.EXN_KEYS = ["drills"]
    align_controller.pcb.get_excellon_layer = MagicMock(return_value=[MagicMock(), True])
    result = align_controller.load_new_align_layer("drills", "/test/drills.drl")
    assert result[1] is True


def test_load_new_align_layer_gcode_valid(align_controller):
    align_controller.pcb.EXN_KEYS = ["drills"]
    align_controller.dgc.get_drill_layer = MagicMock(return_value=[MagicMock(), True])
    result = align_controller.load_new_align_layer("drills", "/test/drills.nc")
    assert result[1] is True


def test_load_new_align_layer_not_loaded(align_controller):
    align_controller.pcb.EXN_KEYS = ["drills"]
    align_controller.pcb.get_excellon_layer = MagicMock(return_value=[None, True])
    result = align_controller.load_new_align_layer("drills", "/test/drills.drl")
    assert result[0] is None


def test_load_new_align_layer_invalid(align_controller):
    align_controller.pcb.EXN_KEYS = ["drills"]
    result = align_controller.load_new_align_layer("invalid", "/test/invalid.drl")
    assert result[0] is None


def test_load_new_align_layer_attribute_error(align_controller):
    align_controller.pcb.EXN_KEYS = ["drills"]
    align_controller.pcb.load_excellon = MagicMock(side_effect=AttributeError("test"))
    result = align_controller.load_new_align_layer("drills", "/test/drills.drl")
    assert result[0] is None


def test_remove_align_points(align_controller):
    align_controller.align_data = [(1, 2), (3, 4), (5, 6)]
    result = align_controller.remove_align_points([1])
    assert len(result) == 2
    assert (3, 4) not in result


def test_remove_align_points_multiple(align_controller):
    align_controller.align_data = [(1, 2), (3, 4), (5, 6)]
    result = align_controller.remove_align_points([0, 2])
    assert len(result) == 1
    assert (3, 4) in result


def test_flip_align_layer_horizontally(align_controller):
    align_controller.flip_align_layer_horizontally(True)
    assert align_controller.flipping_view[0] is True


def test_flip_align_layer_vertically(align_controller):
    align_controller.flip_align_layer_vertically(True)
    assert align_controller.flipping_view[1] is True


def test_update_threshold_value(align_controller):
    align_controller.update_threshold_value(128)
    assert align_controller.threshold_value == 128


def test_set_camera_rotation(align_controller):
    align_controller.double_side_manager.set_camera_rotation.reset_mock()
    align_controller.set_camera_rotation(90.0)
    align_controller.double_side_manager.set_camera_rotation.assert_called_with(90.0)


def test_set_camera_flip_h(align_controller):
    align_controller.set_camera_flip_h(True)
    align_controller.double_side_manager.flip_h = True


def test_set_camera_flip_v(align_controller):
    align_controller.set_camera_flip_v(True)
    align_controller.double_side_manager.flip_v = True


def test_get_camera_list(align_controller):
    align_controller.double_side_manager.list_cameras_indexes = MagicMock(return_value=[0, 1])
    result = align_controller.get_camera_list()
    assert result == [0, 1]


def test_update_camera_selected(align_controller):
    align_controller.double_side_manager.update_camera = MagicMock(return_value=True)
    result = align_controller.update_camera_selected(0)
    assert result is True


def test_camera_new_frame_with_frame(align_controller):
    align_controller.double_side_manager.get_webcam_frame = MagicMock(return_value=MagicMock())
    align_controller.double_side_manager.detect_holes = MagicMock(return_value=np.array([[1, 2, 3]]))
    result = align_controller.camera_new_frame()
    assert result is not None


def test_camera_new_frame_no_frame(align_controller):
    align_controller.double_side_manager.get_webcam_frame = MagicMock(return_value=None)
    result = align_controller.camera_new_frame()
    assert result is None


def test_add_new_align_point(align_controller):
    align_controller.align_data = []
    result = align_controller.add_new_align_point((100, 200), (50, 50))
    assert len(result) == 1
    assert result[0] == ((100, 200), (50, 50))


def test_add_new_align_point_none_geom(align_controller):
    align_controller.align_data = []
    result = align_controller.add_new_align_point(None, (50, 50))
    assert len(result) == 0


def test_add_new_align_point_none_working(align_controller):
    align_controller.align_data = []
    result = align_controller.add_new_align_point((100, 200), None)
    assert len(result) == 0