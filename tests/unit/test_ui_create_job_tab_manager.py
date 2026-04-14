import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock, patch


class TestUiCreateJobLayerTabConstants:
    def test_taps_type_text_contains_none(self):
        from TheAntFarm.ui_manager.ui_create_job_tab_manager import UiCreateJobLayerTab
        assert "None" in UiCreateJobLayerTab.TAPS_TYPE_TEXT

    def test_taps_type_text_contains_left_right(self):
        from TheAntFarm.ui_manager.ui_create_job_tab_manager import UiCreateJobLayerTab
        assert "1 Left + 1 Right" in UiCreateJobLayerTab.TAPS_TYPE_TEXT


class TestAddDrillTool:
    def test_add_drill_tool(self):
        mock_ui = MagicMock()
        mock_ui.drill_tw.insertRow = MagicMock()
        mock_ui.drill_tw.rowCount.return_value = 0
        mock_ui.drill_tw.setCellWidget = MagicMock()
        with patch("TheAntFarm.ui_manager.ui_create_job_tab_manager.QLabel"), \
             patch("TheAntFarm.ui_manager.ui_create_job_tab_manager.QDoubleSpinBox"):
            from TheAntFarm.ui_manager.ui_create_job_tab_manager import UiCreateJobLayerTab
            ui = UiCreateJobLayerTab.__new__(UiCreateJobLayerTab)
            ui.ui = mock_ui
            ui.current_drill_tool_idx = 0
            ui.add_drill_tool("TestTool", 0.5)
            mock_ui.drill_tw.insertRow.assert_called_once()


class TestRemoveDrillTool:
    def test_remove_drill_tool(self):
        mock_ui = MagicMock()
        mock_ui.drill_tw.selectedIndexes.return_value = [MagicMock(row=MagicMock(return_value=0))]
        mock_ui.drill_tw.removeRow = MagicMock()
        mock_ui.drill_tw.rowCount.return_value = 1
        from TheAntFarm.ui_manager.ui_create_job_tab_manager import UiCreateJobLayerTab
        ui = UiCreateJobLayerTab.__new__(UiCreateJobLayerTab)
        ui.ui = mock_ui
        ui.remove_drill_tool()
        mock_ui.drill_tw.removeRow.assert_called_once()


class TestVisualizeActiveLayer:
    def test_visualize_active_layer(self):
        mock_ui = MagicMock()
        mock_ui.layer_choice_cb.currentText.return_value = "TOP"
        mock_vis_layer = MagicMock()
        mock_ui.jobs_sw = MagicMock()
        from TheAntFarm.ui_manager.ui_create_job_tab_manager import UiCreateJobLayerTab
        ui = UiCreateJobLayerTab.__new__(UiCreateJobLayerTab)
        ui.ui = mock_ui
        ui.vis_layer = mock_vis_layer
        ui.lay_tags = ("top", "bottom", "profile", "drill")
        ui.lay_names = ("TOP", "BOTTOM", "PROFILE", "DRILL")
        ui.visualize_active_layer()
        mock_vis_layer.set_layer_visible.assert_called()


