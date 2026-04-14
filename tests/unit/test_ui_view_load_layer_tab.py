import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock





class TestHideShowLayers:
    def test_hide_show_layers_true(self):
        mock_chb = MagicMock()
        from TheAntFarm.ui_manager.ui_view_load_layer_tab import UiViewLoadLayerTab
        ui = UiViewLoadLayerTab.__new__(UiViewLoadLayerTab)
        ui.layers_chb = {"top": mock_chb}
        ui.hide_show_layers(True)
        mock_chb.setChecked.assert_called_once_with(True)

    def test_hide_show_layers_false(self):
        mock_chb = MagicMock()
        from TheAntFarm.ui_manager.ui_view_load_layer_tab import UiViewLoadLayerTab
        ui = UiViewLoadLayerTab.__new__(UiViewLoadLayerTab)
        ui.layers_chb = {"top": mock_chb}
        ui.hide_show_layers(False)
        mock_chb.setChecked.assert_called_once_with(False)


class TestSetLayerVisible:
    def test_set_layer_visible(self):
        mock_vis_layer = MagicMock()
        from TheAntFarm.ui_manager.ui_view_load_layer_tab import UiViewLoadLayerTab
        ui = UiViewLoadLayerTab.__new__(UiViewLoadLayerTab)
        ui.vis_layer = mock_vis_layer
        ui.set_layer_visible("top", True)
        mock_vis_layer.set_layer_visible.assert_called_with("top", True)


class TestGetLoadedLayers:
    def test_get_loaded_layers_with_data(self):
        mock_main_win = MagicMock()
        mock_main_win.ui.top_file_le.text.return_value = "/test/file.gbr"
        from TheAntFarm.ui_manager.ui_view_load_layer_tab import UiViewLoadLayerTab
        ui = UiViewLoadLayerTab.__new__(UiViewLoadLayerTab)
        ui.ui = mock_main_win.ui
        ui.lay_tags = ("top",)
        ui.layers_te = {"top": mock_main_win.ui.top_file_le}
        result = ui.get_loaded_layers()
        assert "top" in result