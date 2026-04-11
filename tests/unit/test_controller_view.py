import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock, patch, PropertyMock


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
        with patch("controller.controller_view.PcbObj"):
            from controller.controller_view import ViewController
            return ViewController(mock_settings)

    def test_init(self, mock_settings):
        with patch("controller.controller_view.PcbObj"):
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            assert vc.settings == mock_settings

    def test_load_new_layer_gerber_valid(self, view_controller):
        view_controller.pcb.GBR_KEYS = ["top_copper"]
        view_controller.pcb.get_gerber_layer = MagicMock(return_value=[MagicMock(), False])
        result = view_controller.load_new_layer("top_copper", "/test/path.gbr")
        assert result[1] is False

    def test_load_new_layer_excellon_valid(self, view_controller):
        view_controller.pcb.EXN_KEYS = ["drills"]
        view_controller.pcb.get_excellon_layer = MagicMock(return_value=[MagicMock(), True])
        result = view_controller.load_new_layer("drills", "/test/drills.drl")
        assert result[1] is True

    def test_load_new_layer_gerber_not_loaded(self, view_controller):
        view_controller.pcb.GBR_KEYS = ["top_copper"]
        view_controller.pcb.get_gerber_layer = MagicMock(return_value=[None, False])
        result = view_controller.load_new_layer("top_copper", "/test/path.gbr")
        assert result[0] is None

    def test_load_new_layer_excellon_not_loaded(self, view_controller):
        view_controller.pcb.EXN_KEYS = ["drills"]
        view_controller.pcb.get_excellon_layer = MagicMock(return_value=[None, True])
        result = view_controller.load_new_layer("drills", "/test/drills.drl")
        assert result[0] is None

    def test_load_new_layer_invalid(self, view_controller):
        view_controller.pcb.GBR_KEYS = ["top_copper"]
        view_controller.pcb.EXN_KEYS = ["drills"]
        result = view_controller.load_new_layer("invalid_layer", "/test/path.gbr")
        assert result[0] is None

    def test_load_new_layer_attribute_error(self, view_controller):
        view_controller.pcb.GBR_KEYS = ["top_copper"]
        view_controller.pcb.load_gerber = MagicMock(side_effect=AttributeError("test"))
        result = view_controller.load_new_layer("top_copper", "/test/path.gbr")
        assert result[0] is None

    def test_load_new_layer_value_error(self, view_controller):
        view_controller.pcb.GBR_KEYS = ["top_copper"]
        view_controller.pcb.load_gerber = MagicMock(side_effect=ValueError("test"))
        result = view_controller.load_new_layer("top_copper", "/test/path.gbr")
        assert result[0] is None

    def test_generate_new_path_gerber(self, view_controller):
        mock_layer = MagicMock()
        view_controller.pcb.get_gerber_layer = MagicMock(return_value=[mock_layer, False])
        with patch("controller.controller_view.MachinePath") as MockMP:
            mock_path = MagicMock()
            mock_path.get_path.return_value = ["path1", "path2"]
            MockMP.return_value = mock_path
            result = view_controller.generate_new_path("top_copper", {}, "gerber")
            assert result == ["path1", "path2"]

    def test_generate_new_path_drill(self, view_controller):
        mock_layer = MagicMock()
        view_controller.pcb.get_excellon_layer = MagicMock(return_value=[mock_layer, True])
        with patch("controller.controller_view.MachinePath") as MockMP:
            mock_path = MagicMock()
            mock_path.get_path.return_value = ["path1"]
            MockMP.return_value = mock_path
            result = view_controller.generate_new_path("drills", {}, "drill")
            assert result == ["path1"]

    def test_generate_new_path_profile(self, view_controller):
        mock_layer = MagicMock()
        view_controller.pcb.get_gerber_layer = MagicMock(return_value=[mock_layer, False])
        with patch("controller.controller_view.MachinePath") as MockMP:
            mock_path = MagicMock()
            mock_path.get_path.return_value = []
            MockMP.return_value = mock_path
            result = view_controller.generate_new_path("outline", {}, "profile")
            assert result == []

    def test_generate_new_gcode_file_with_mirror(self, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od = {"common": {"mirroring_axis": "X"}}
        mock_settings.gcf_settings.gcode_folder = "/test/gcode"
        with patch("controller.controller_view.PcbObj"), \
             patch("controller.controller_view.GCoder") as MockGC:
            mock_gcoder = MagicMock()
            mock_gcoder.compute.return_value = True
            mock_gcoder.get_file_name.return_value = "test.nc"
            MockGC.return_value = mock_gcoder
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            result = vc.generate_new_gcode_file("top_copper", {}, "gerber", [])
            mock_gcoder.write.assert_called_once()

    def test_generate_new_gcode_file_without_mirror(self, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od = {"common": {}}
        mock_settings.gcf_settings.gcode_folder = "/test/gcode"
        with patch("controller.controller_view.PcbObj"), \
             patch("controller.controller_view.GCoder") as MockGC:
            mock_gcoder = MagicMock()
            mock_gcoder.compute.return_value = True
            mock_gcoder.get_file_name.return_value = "test.nc"
            MockGC.return_value = mock_gcoder
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            result = vc.generate_new_gcode_file("top_copper", {}, "gerber", [])
            mock_gcoder.write.assert_called_once()

    def test_generate_new_gcode_file_compute_fails(self, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od = {"common": {}}
        mock_settings.gcf_settings.gcode_folder = "/test/gcode"
        with patch("controller.controller_view.PcbObj"), \
             patch("controller.controller_view.GCoder") as MockGC:
            mock_gcoder = MagicMock()
            mock_gcoder.compute.return_value = False
            MockGC.return_value = mock_gcoder
            from controller.controller_view import ViewController
            vc = ViewController(mock_settings)
            result = vc.generate_new_gcode_file("top_copper", {}, "gerber", [])
            mock_gcoder.write.assert_not_called()