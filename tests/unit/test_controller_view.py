import pytest
from unittest.mock import MagicMock, patch

from TheAntFarm.app.events import GCodeResult, LayerResult, PathResult


class TestViewController:
    @pytest.fixture
    def mock_settings(self):
        settings = MagicMock()
        settings.jobs_settings.jobs_settings_od = {"common": {}}
        settings.gcf_settings = MagicMock()
        settings.gcf_settings.gcode_folder = "/test/gcode"
        return settings

    @pytest.fixture
    def view_controller(self, mock_settings):
        with patch("controller.controller_view.PcbService"):
            from controller.controller_view import ViewController
            return ViewController(mock_settings)

    def test_init(self, mock_settings):
        with patch("controller.controller_view.PcbService"):
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            assert vc.settings == mock_settings
            assert vc._service is not None

    def test_load_new_layer_gerber_valid(self, view_controller):
        loaded_layer = [MagicMock(), False]
        view_controller._service.load_layer = MagicMock(
            return_value=LayerResult(loaded_layer, "top", "/test/path.gbr", False, True)
        )
        result = view_controller.load_new_layer("top", "/test/path.gbr")
        assert result[1] is False
        assert result[0] == loaded_layer

    def test_load_new_layer_excellon_valid(self, view_controller):
        loaded_layer = [MagicMock(), True]
        view_controller._service.load_layer = MagicMock(
            return_value=LayerResult(loaded_layer, "drill", "/test/drills.drl", True, True)
        )
        result = view_controller.load_new_layer("drill", "/test/drills.drl")
        assert result[1] is True
        assert result[0] == loaded_layer

    def test_load_new_layer_gerber_not_loaded(self, view_controller):
        view_controller._service.load_layer = MagicMock(
            return_value=LayerResult(None, "top", "/test/path.gbr", False, False)
        )
        result = view_controller.load_new_layer("top", "/test/path.gbr")
        assert result[0] is None
        assert result[1] is False

    def test_load_new_layer_excellon_not_loaded(self, view_controller):
        view_controller._service.load_layer = MagicMock(
            return_value=LayerResult(None, "drill", "/test/drills.drl", True, False)
        )
        result = view_controller.load_new_layer("drill", "/test/drills.drl")
        assert result[0] is None
        assert result[1] is True

    def test_load_new_layer_invalid(self, view_controller):
        view_controller._service.load_layer = MagicMock(
            return_value=LayerResult(None, "invalid_layer", "/test/path.gbr", False, False)
        )
        result = view_controller.load_new_layer("invalid_layer", "/test/path.gbr")
        assert result[0] is None
        assert result[1] is None

    def test_generate_new_path_gerber(self, view_controller):
        view_controller._service.generate_path = MagicMock(return_value=PathResult("top", ["path1", "path2"]))
        result = view_controller.generate_new_path("top", {}, "gerber")
        assert result == ["path1", "path2"]

    def test_generate_new_path_drill(self, view_controller):
        view_controller._service.generate_path = MagicMock(return_value=PathResult("drill", ["path1"]))
        result = view_controller.generate_new_path("drill", {}, "drill")
        assert result == ["path1"]

    def test_generate_new_path_profile(self, view_controller):
        view_controller._service.generate_path = MagicMock(return_value=PathResult("outline", []))
        result = view_controller.generate_new_path("outline", {}, "profile")
        assert result == []

    def test_generate_new_gcode_file_with_mirror(self, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od = {"common": {"mirroring_axis": "X"}}
        mock_settings.gcf_settings.gcode_folder = "/test/gcode"
        with patch("controller.controller_view.PcbService") as MockService:
            mock_service = MagicMock()
            mock_service.generate_gcode.return_value = GCodeResult("top", "/test/gcode/test.nc")
            MockService.return_value = mock_service
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            vc.generate_new_gcode_file("top", {}, "gerber", [])
            mock_service.generate_gcode.assert_called_once()

    def test_generate_new_gcode_file_without_mirror(self, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od = {"common": {}}
        mock_settings.gcf_settings.gcode_folder = "/test/gcode"
        with patch("controller.controller_view.PcbService") as MockService:
            mock_service = MagicMock()
            mock_service.generate_gcode.return_value = GCodeResult("top", "/test/gcode/test.nc")
            MockService.return_value = mock_service
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            vc.generate_new_gcode_file("top", {}, "gerber", [])
            mock_service.generate_gcode.assert_called_once()

    def test_generate_new_gcode_file_compute_fails(self, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od = {"common": {}}
        mock_settings.gcf_settings.gcode_folder = "/test/gcode"
        with patch("controller.controller_view.PcbService") as MockService:
            mock_service = MagicMock()
            mock_service.generate_gcode.return_value = GCodeResult("top", "")
            MockService.return_value = mock_service
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            vc.generate_new_gcode_file("top", {}, "gerber", [])
            mock_service.generate_gcode.assert_called_once()