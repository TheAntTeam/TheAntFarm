import pytest
import math
from collections import OrderedDict as Od
from unittest.mock import MagicMock


class TestUiAlignTabConstants:
    def test_min_alignment_points_number(self):
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        assert UiAlignTab.MIN_ALIGNMENT_POINTS_NUMBER == 4


class TestUpdateCameraZoom:
    def test_update_camera_zoom_no_increment_at_max(self):
        mock_main_win = MagicMock()
        mock_main_win.ui.camera_zoom_cb.currentIndex.return_value = 4
        mock_main_win.ui.camera_zoom_cb.count.return_value = 5
        mock_main_win.ui.camera_zoom_cb.currentText.return_value = "5x"
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.ui = mock_main_win.ui
        ui.update_camera_zoom(1)
        mock_main_win.ui.camera_zoom_cb.setCurrentIndex.assert_not_called()


class TestUpdateZoomValue:
    def test_update_zoom_value(self):
        mock_control_wo = MagicMock()
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.update_zoom_value_s = MagicMock()
        ui.update_zoom_value(2)
        ui.update_zoom_value_s.emit.assert_called_once_with(2)


class TestRemovePoint:
    def test_remove_point(self):
        mock_main_win = MagicMock()
        mock_sel_model = MagicMock()
        mock_sel_model.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=1))]
        mock_main_win.ui.align_points_tw.selectionModel.return_value = mock_sel_model
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.ui = mock_main_win.ui
        ui.remove_point_rows = MagicMock()
        ui.remove_point()
        ui.remove_point_rows.emit.assert_called_once()


class TestUpdateCameraImage:
    def test_update_camera_image_valid(self):
        mock_main_win = MagicMock()
        mock_pixmap = MagicMock()
        mock_pixmap.isNull.return_value = False
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.ui = mock_main_win.ui
        ui.update_camera_image(mock_pixmap)
        mock_main_win.ui.camera_la.setPixmap.assert_called()

    def test_update_camera_image_null(self):
        mock_main_win = MagicMock()
        mock_pixmap = MagicMock()
        mock_pixmap.isNull.return_value = True
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.ui = mock_main_win.ui
        ui.update_camera_image(mock_pixmap)
        mock_main_win.ui.camera_la.clear.assert_called()


class TestUpdateToolOrCamera:
    def test_update_tool_or_camera_tool(self):
        mock_main_win = MagicMock()
        mock_main_win.ui.tool_or_camera_tb.isChecked.return_value = False
        mock_main_win.ui.tool_or_camera_tb.setText = MagicMock()
        mock_app_settings = MagicMock()
        mock_app_settings.camera_selected_or_tool = False
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.ui = mock_main_win.ui
        ui.app_settings = mock_app_settings
        ui.update_tool_or_camera()
        mock_main_win.ui.tool_or_camera_tb.setText.assert_called_with("TOOL_POSITION")

    def test_update_tool_or_camera_camera(self):
        mock_main_win = MagicMock()
        mock_main_win.ui.tool_or_camera_tb.isChecked.return_value = True
        mock_main_win.ui.tool_or_camera_tb.setText = MagicMock()
        mock_app_settings = MagicMock()
        mock_app_settings.camera_selected_or_tool = True
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.ui = mock_main_win.ui
        ui.app_settings = mock_app_settings
        ui.update_tool_or_camera()
        mock_main_win.ui.tool_or_camera_tb.setText.assert_called_with("CAMERA_POSITION")


class TestComputeOffsetPoint:
    def test_compute_offset_point(self):
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        x, y = UiAlignTab.compute_offset_point(10, 10, 5, 0)
        assert abs(x - 15.0) < 0.001


class TestFlipAlignLayer:
    def test_flip_align_layer(self):
        mock_vis_align_layer = MagicMock()
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab
        ui = UiAlignTab.__new__(UiAlignTab)
        ui.vis_align_layer = mock_vis_align_layer
        ui.flip_align_layer([True, False])
        mock_vis_align_layer.flip_camera.assert_called()