"""
Test suite for UI Control Tab selection functionality.
Tests focus on the simplified gcode table row selection behavior.
"""

from unittest.mock import Mock

import pytest


@pytest.mark.usefixtures("qapp")
class TestSelectGcodeRowImplementation:
    """Test select_gcode_row method logic"""

    def test_select_row_when_not_selected(self):
        """Verify selecting row when not selected"""
        mock_ui = Mock()
        mock_ui.gcode_tw = Mock()
        mock_selection_model = Mock()
        mock_selection_model.selectedRows.return_value = []  # No rows selected
        mock_ui.gcode_tw.selectionModel.return_value = mock_selection_model

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        # Create partial instance for method testing
        ui_tab = UiControlTab.__new__(UiControlTab)
        ui_tab.ui = mock_ui

        # Call method
        ui_tab.select_gcode_row(0)

        # Verify selectRow was called
        mock_ui.gcode_tw.selectRow.assert_called_once_with(0)

    def test_deselect_single_row_when_selected(self):
        """Verify deselecting only the clicked row when it's selected"""
        from unittest.mock import MagicMock

        mock_ui = Mock()
        mock_ui.gcode_tw = Mock()

        # Mock a selected row at index 0
        mock_index = Mock()
        mock_index.row.return_value = 0
        mock_selection_model = MagicMock()
        mock_selection_model.selectedRows.return_value = [mock_index]  # Row 0 is selected
        mock_ui.gcode_tw.selectionModel.return_value = mock_selection_model
        mock_ui.gcode_tw.model.return_value = Mock()

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        # Create partial instance for method testing
        ui_tab = UiControlTab.__new__(UiControlTab)
        ui_tab.ui = mock_ui

        # Call method
        ui_tab.select_gcode_row(0)

        # Verify selectionModel.select was called with Deselect flag
        mock_selection_model.select.assert_called_once()
        # Verify clearSelection was NOT called (only this row should be deselected)
        mock_ui.gcode_tw.clearSelection.assert_not_called()


class TestDeselectAllGcodeRowImplementation:
    """Test deselect_all_gcode_row method logic"""

    def test_clears_selection(self):
        """Verify clearSelection is called"""
        mock_ui = Mock()
        mock_ui.gcode_tw = Mock()

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        # Create partial instance for method testing
        ui_tab = UiControlTab.__new__(UiControlTab)
        ui_tab.ui = mock_ui

        # Call method
        ui_tab.deselect_all_gcode_row()

        # Verify clearSelection was called
        mock_ui.gcode_tw.clearSelection.assert_called_once()


class TestSelectMethodCodeQuality:
    """Test code quality and simplification of selection methods"""

    def test_select_gcode_row_no_mode_switching(self):
        """Verify select_gcode_row doesn't use setSelectionMode"""
        import inspect

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        source = inspect.getsource(UiControlTab.select_gcode_row)

        # Should not contain mode switching - this proves simplification
        assert "setSelectionMode" not in source, "select_gcode_row should not switch modes"
        assert "setSelectionBehavior" not in source, "select_gcode_row should not set behavior"

    def test_deselect_all_gcode_row_no_mode_switching(self):
        """Verify deselect_all_gcode_row doesn't use setSelectionMode"""
        import inspect

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        source = inspect.getsource(UiControlTab.deselect_all_gcode_row)

        # Should not contain mode switching - this proves simplification
        assert "setSelectionMode" not in source, "deselect_all_gcode_row should not switch modes"
        assert "setSelectionBehavior" not in source, "deselect_all_gcode_row should not set behavior"


class TestInitialization:
    """Test initialization configuration"""

    def test_multiselection_mode_configured(self):
        """Verify NoSelection mode is used with cellClicked handler for column 0 only"""
        import inspect

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        source = inspect.getsource(UiControlTab.__init__)

        # Check for NoSelection mode (to prevent default row selection on any click)
        assert "QAbstractItemView.NoSelection" in source, "NoSelection mode should be configured"
        # Check that cellClicked is connected (for custom column-specific selection)
        assert (
            "cellClicked.connect(self._handle_table_cell_click)" in source
        ), "cellClicked should be connected to _handle_table_cell_click"
