import pytest
import numpy as np
from unittest.mock import MagicMock, patch

from TheAntFarm.app.events import CameraFrame, LayerResult


@pytest.fixture(scope="module")
def mock_settings():
    settings = MagicMock()
    settings.app_settings.camera_rotation_angle = 0
    settings.app_settings.camera_flip_h = False
    settings.app_settings.camera_flip_v = False
    return settings


@pytest.fixture(scope="module")
def align_controller(mock_settings):
    with patch("controller.controller_align.AlignService") as MockService:
        mock_service = MagicMock()
        mock_service.flipping_view = [False, False, False]
        mock_service.align_data = []
        mock_service.threshold_value = 0
        MockService.return_value = mock_service
        from controller.controller_align import AlignController
        return AlignController(mock_settings)


def test_init_attributes(align_controller, mock_settings):
    assert align_controller.settings == mock_settings
    assert align_controller.threshold_value == 0
    assert align_controller.flipping_view == [False, False, False]
    assert align_controller.align_data == []


def test_load_new_align_layer_excellon_valid(align_controller):
    loaded_layer = [MagicMock(), True]
    align_controller._service.load_align_layer = MagicMock(
        return_value=LayerResult(loaded_layer, "drill", "/test/drills.drl", True, True)
    )
    result = align_controller.load_new_align_layer("drill", "/test/drills.drl")
    assert result[0] == loaded_layer
    assert result[1] is True


def test_load_new_align_layer_gcode_valid(align_controller):
    loaded_layer = [MagicMock(), True]
    align_controller._service.load_align_layer = MagicMock(
        return_value=LayerResult(loaded_layer, "drill", "/test/drills.nc", True, True)
    )
    result = align_controller.load_new_align_layer("drill", "/test/drills.nc")
    assert result[0] == loaded_layer
    assert result[1] is True


def test_load_new_align_layer_not_loaded(align_controller):
    align_controller._service.load_align_layer = MagicMock(
        return_value=LayerResult(None, "drill", "/test/drills.drl", True, False)
    )
    result = align_controller.load_new_align_layer("drill", "/test/drills.drl")
    assert result[0] is None
    assert result[1] is True


def test_load_new_align_layer_invalid(align_controller):
    align_controller._service.load_align_layer = MagicMock(
        return_value=LayerResult(None, "invalid", "/test/invalid.drl", False, False)
    )
    result = align_controller.load_new_align_layer("invalid", "/test/invalid.drl")
    assert result[0] is None
    assert result[1] is None


def test_remove_align_points(align_controller):
    align_controller.align_data = [(1, 2), (3, 4), (5, 6)]
    align_controller._service.remove_align_points = MagicMock(return_value=[(1, 2), (5, 6)])
    result = align_controller.remove_align_points([1])
    assert len(result) == 2
    assert (3, 4) not in result


def test_remove_align_points_multiple(align_controller):
    align_controller.align_data = [(1, 2), (3, 4), (5, 6)]
    align_controller._service.remove_align_points = MagicMock(return_value=[(3, 4)])
    result = align_controller.remove_align_points([0, 2])
    assert len(result) == 1
    assert (3, 4) in result


def test_flip_align_layer_horizontally(align_controller):
    align_controller._service.flip_horizontally = MagicMock(
        side_effect=lambda v: align_controller._service.flipping_view.__setitem__(0, v)
    )
    align_controller.flip_align_layer_horizontally(True)
    align_controller._service.flip_horizontally.assert_called_with(True)
    assert align_controller.flipping_view[0] is True


def test_flip_align_layer_vertically(align_controller):
    align_controller._service.flip_vertically = MagicMock(
        side_effect=lambda v: align_controller._service.flipping_view.__setitem__(1, v)
    )
    align_controller.flip_align_layer_vertically(True)
    align_controller._service.flip_vertically.assert_called_with(True)
    assert align_controller.flipping_view[1] is True


def test_update_threshold_value(align_controller):
    align_controller._service.set_threshold = MagicMock(side_effect=lambda v: setattr(align_controller._service, "threshold_value", v))
    align_controller.update_threshold_value(128)
    assert align_controller.threshold_value == 128


def test_set_camera_rotation(align_controller):
    align_controller._service.set_camera_rotation = MagicMock()
    align_controller.set_camera_rotation(90.0)
    align_controller._service.set_camera_rotation.assert_called_with(90.0)


def test_set_camera_flip_h(align_controller):
    align_controller._service.set_camera_flip_h = MagicMock()
    align_controller.set_camera_flip_h(True)
    align_controller._service.set_camera_flip_h.assert_called_with(True)


def test_set_camera_flip_v(align_controller):
    align_controller._service.set_camera_flip_v = MagicMock()
    align_controller.set_camera_flip_v(True)
    align_controller._service.set_camera_flip_v.assert_called_with(True)


def test_get_camera_list(align_controller):
    align_controller._service.get_camera_list = MagicMock(return_value=[0, 1])
    result = align_controller.get_camera_list()
    assert result == [0, 1]


def test_update_camera_selected(align_controller):
    align_controller._service.update_camera = MagicMock(return_value=True)
    result = align_controller.update_camera_selected(0)
    assert result is True


def test_camera_new_frame_with_frame(align_controller):
    frame = CameraFrame(data=np.zeros((10, 10, 3), dtype=np.uint8), width=10, height=10)
    align_controller._service.get_camera_frame = MagicMock(return_value=frame)
    result = align_controller.camera_new_frame()
    assert result is not None


def test_camera_new_frame_no_frame(align_controller):
    align_controller._service.get_camera_frame = MagicMock(return_value=None)
    result = align_controller.camera_new_frame()
    assert result is None


def test_add_new_align_point(align_controller):
    align_controller.align_data = []
    align_controller._service.add_align_point = MagicMock(return_value=[((100, 200), (50, 50))])
    result = align_controller.add_new_align_point((100, 200), (50, 50))
    assert len(result) == 1
    assert result[0] == ((100, 200), (50, 50))


def test_add_new_align_point_none_geom(align_controller):
    align_controller.align_data = []
    align_controller._service.add_align_point = MagicMock(return_value=[])
    result = align_controller.add_new_align_point(None, (50, 50))
    assert len(result) == 0


def test_add_new_align_point_none_working(align_controller):
    align_controller.align_data = []
    align_controller._service.add_align_point = MagicMock(return_value=[])
    result = align_controller.add_new_align_point((100, 200), None)
    assert len(result) == 0