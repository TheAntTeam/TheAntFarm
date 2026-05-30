from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch

import numpy as np
import pytest

from app.events import CameraFrame


@pytest.fixture
def align_service():
    with patch("app.services.align_service.DoubleSideManager") as mock_dsm:
        from app.services.align_service import AlignService

        service = AlignService(camera_rotation=0.0, flip_h=False, flip_v=False)
        yield service


@pytest.fixture
def gerber_path():
    return Path(__file__).parent.parent / "test_data" / "gerbers"


class TestInit:
    def test_default_state(self, align_service):
        assert align_service.threshold_value == 0
        assert align_service.flipping_view == [False, False, False]
        assert align_service.align_data == []

    def test_custom_camera_settings(self):
        with patch("app.services.align_service.DoubleSideManager"):
            from app.services.align_service import AlignService

            service = AlignService(camera_rotation=90.0, flip_h=True, flip_v=True)
            assert service is not None


class TestLoadAlignLayer:
    def test_load_excellon_layer_success(self, align_service, gerber_path):
        result = align_service.load_align_layer("drill", str(gerber_path / "simple_drill.drl"))
        assert result.ok is True
        assert result.layer_data is not None

    def test_load_resets_align_data_on_success(self, align_service, gerber_path):
        align_service.align_data = [((1, 2), (3, 4))]
        align_service.load_align_layer("drill", str(gerber_path / "simple_drill.drl"))
        assert align_service.align_data == []

    def test_load_invalid_file_returns_not_ok(self, align_service, gerber_path):
        result = align_service.load_align_layer("drill", str(gerber_path / "invalid.gbr"))
        assert result.ok is False


class TestAlignPoints:
    def test_add_align_point(self, align_service):
        result = align_service.add_align_point([1.0, 2.0], [3.0, 4.0])
        assert result == [([1.0, 2.0], [3.0, 4.0])]

    def test_add_multiple_points(self, align_service):
        align_service.add_align_point([1.0, 2.0], [3.0, 4.0])
        result = align_service.add_align_point([5.0, 6.0], [7.0, 8.0])
        assert len(result) == 2

    def test_add_align_point_none_geom(self, align_service):
        result = align_service.add_align_point(None, [3.0, 4.0])
        assert result == []

    def test_remove_align_points(self, align_service):
        align_service.add_align_point([1.0, 2.0], [3.0, 4.0])
        align_service.add_align_point([5.0, 6.0], [7.0, 8.0])
        result = align_service.remove_align_points([0])
        assert len(result) == 1
        assert result[0] == ([5.0, 6.0], [7.0, 8.0])

    def test_remove_align_points_invalid_row(self, align_service):
        align_service.add_align_point([1.0, 2.0], [3.0, 4.0])
        result = align_service.remove_align_points([5])
        assert len(result) == 1


class TestCameraSettings:
    def test_set_camera_rotation(self, align_service):
        align_service._dsm.set_camera_rotation.reset_mock()
        align_service.set_camera_rotation(90.0)
        align_service._dsm.set_camera_rotation.assert_called_once_with(90.0)

    def test_set_camera_flip_h(self, align_service):
        align_service.set_camera_flip_h(True)
        assert align_service._dsm.flip_h is True

    def test_set_camera_flip_v(self, align_service):
        align_service.set_camera_flip_v(True)
        assert align_service._dsm.flip_v is True

    def test_set_threshold(self, align_service):
        align_service.set_threshold(128)
        assert align_service.threshold_value == 128

    def test_get_camera_list(self, align_service):
        align_service._dsm.list_cameras_indexes.return_value = [0, 1]
        result = align_service.get_camera_list()
        assert result == [0, 1]

    def test_update_camera(self, align_service):
        align_service.update_camera(0)
        align_service._dsm.update_camera.assert_called_once_with(0)


class TestCameraFrame:
    def test_get_camera_frame_returns_frame(self, align_service):
        mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        align_service._dsm.get_webcam_frame.return_value = mock_frame
        align_service._dsm.detect_holes.return_value = mock_frame

        result = align_service.get_camera_frame(zoom=1.0)
        assert isinstance(result, CameraFrame)
        assert result.width == 640
        assert result.height == 480
        assert np.array_equal(result.data, mock_frame)

    def test_get_camera_frame_no_frame_returns_none(self, align_service):
        align_service._dsm.get_webcam_frame.return_value = None
        result = align_service.get_camera_frame(zoom=1.0)
        assert result is None

    def test_get_camera_frame_applies_zoom(self, align_service):
        mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        align_service._dsm.get_webcam_frame.return_value = mock_frame
        align_service._dsm.detect_holes.return_value = mock_frame

        align_service.get_camera_frame(zoom=2.0)
        align_service._dsm.detect_holes.assert_called_once()


class TestFlipView:
    def test_flip_horizontally(self, align_service):
        align_service.flip_horizontally(True)
        assert align_service.flipping_view[0] is True

    def test_flip_vertically(self, align_service):
        align_service.flip_vertically(True)
        assert align_service.flipping_view[1] is True

    def test_flip_multiple_times(self, align_service):
        align_service.flip_horizontally(True)
        align_service.flip_horizontally(False)
        assert align_service.flipping_view[0] is False
