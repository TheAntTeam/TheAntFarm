"""
Test suite for UI Control Tab selection functionality.
Tests focus on the simplified gcode table row selection behavior.
"""

from unittest.mock import Mock, patch

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
        assert "cellClicked.connect(self._handle_table_cell_click)" in source, (
            "cellClicked should be connected to _handle_table_cell_click"
        )


@pytest.mark.usefixtures("qapp")
class TestGrblSimulatorSettings:
    def _tab(self, enabled=False, speed=1.0):
        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        ui_tab = UiControlTab.__new__(UiControlTab)
        ui_tab.serialWo = Mock()
        ui_tab.app_settings = Mock(grbl_simulator_enabled=enabled, grbl_simulator_speed=speed)
        return ui_tab

    def test_startup_applies_the_stored_settings_then_lists_the_ports(self):
        ui_tab = self._tab(enabled=True, speed=4.0)

        ui_tab.init_serial_port_cb()

        ui_tab.serialWo.set_simulator_s.emit.assert_called_once_with(True, 4.0)
        ui_tab.serialWo.refresh_port_list_s.emit.assert_called_once_with()

    def test_new_settings_refresh_the_port_list(self):
        ui_tab = self._tab()

        ui_tab.apply_simulator_settings(False, 2.0)

        ui_tab.serialWo.set_simulator_s.emit.assert_called_once_with(False, 2.0)
        ui_tab.serialWo.refresh_port_list_s.emit.assert_called_once_with()


class TestRejectedLinePrompt:
    """The user decides how a job on hold for a rejected line goes on."""

    @pytest.fixture
    def message_box(self):
        with patch("TheAntFarm.ui_manager.ui_control_tab.QMessageBox") as message_box:
            buttons = {"Resume": Mock(), "Stop": Mock()}
            roles = {id(buttons["Resume"]): message_box.AcceptRole, id(buttons["Stop"]): message_box.RejectRole}
            prompt = message_box.return_value
            prompt.addButton.side_effect = lambda text, role: buttons[text]
            prompt.buttonRole.side_effect = lambda button: roles[id(button)]
            message_box.buttons = buttons
            yield message_box

    @pytest.fixture
    def ui_tab(self, message_box):
        from PySide6.QtCore import QObject

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        ui_tab = UiControlTab.__new__(UiControlTab)
        QObject.__init__(ui_tab)
        ui_tab.ui = Mock()
        ui_tab.rejected_line_prompt = None
        ui_tab.enable_gcode_rb = Mock()
        ui_tab.enable_after_send = Mock()
        ui_tab.resumes = []
        ui_tab.stops = []
        ui_tab.resume_rejected_line_s.connect(lambda: ui_tab.resumes.append(1))
        ui_tab.stop_gcode_s.connect(lambda: ui_tab.stops.append(1))
        return ui_tab

    def test_prompt_shows_the_error_and_the_line(self, ui_tab, message_box):
        ui_tab.show_rejected_line_prompt("error:20", "G1 X2.000 Y2.000 Z-0.100", 42)

        prompt = message_box.return_value
        text = prompt.setText.call_args.args[0]
        assert "error:20" in text
        assert "line 42" in text
        assert "G1 X2.000 Y2.000 Z-0.100" in text
        prompt.open.assert_called_once()

    def test_stop_is_the_default_and_the_escape_button(self, ui_tab, message_box):
        ui_tab.show_rejected_line_prompt("error:20", "G1 X2", 3)

        prompt = message_box.return_value
        prompt.setDefaultButton.assert_called_once_with(message_box.buttons["Stop"])
        prompt.setEscapeButton.assert_called_once_with(message_box.buttons["Stop"])

    def test_resume_button_resumes_the_job(self, ui_tab, message_box):
        ui_tab.show_rejected_line_prompt("error:20", "G1 X2", 3)

        ui_tab._on_rejected_line_prompt_clicked(message_box.buttons["Resume"])

        assert ui_tab.resumes == [1]
        assert ui_tab.stops == []
        assert ui_tab.rejected_line_prompt is None

    def test_stop_button_stops_the_job(self, ui_tab, message_box):
        ui_tab.show_rejected_line_prompt("error:20", "G1 X2", 3)

        ui_tab._on_rejected_line_prompt_clicked(message_box.buttons["Stop"])

        assert ui_tab.stops == [1]
        assert ui_tab.resumes == []
        assert ui_tab.rejected_line_prompt is None
        ui_tab.enable_after_send.assert_called_once()

    def test_job_stopped_elsewhere_closes_the_prompt(self, ui_tab, message_box):
        ui_tab.show_rejected_line_prompt("error:20", "G1 X2", 3)

        ui_tab.stop_send_file()

        message_box.return_value.hide.assert_called_once()
        assert ui_tab.rejected_line_prompt is None
        assert ui_tab.stops == [1]
        assert ui_tab.resumes == []


class FakeCombo:
    """The part of QComboBox used by the port selector (the tests run without a QApplication)."""

    def __init__(self, items=(), current=""):
        self.items = list(items)
        self.index = self.items.index(current) if current in self.items else (0 if self.items else -1)

    def clear(self):
        self.items, self.index = [], -1

    def addItems(self, items):
        self.items.extend(items)
        if self.index == -1 and self.items:
            self.index = 0

    def findText(self, text):
        return self.items.index(text) if text in self.items else -1

    def setCurrentIndex(self, index):
        self.index = index

    def currentText(self):
        return self.items[self.index] if 0 <= self.index < len(self.items) else ""


@pytest.mark.usefixtures("qapp")
class TestSerialPortSelector:
    BAUDS = [9600, 57600, 115200]

    def _tab(self, ports=(), port="", bauds=(), baud="", last_port="", last_baud=115200, connected=False):
        from PySide6.QtCore import QObject

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        ui_tab = UiControlTab.__new__(UiControlTab)
        QObject.__init__(ui_tab)
        ui_tab.ui = Mock()
        ui_tab.ui.serial_ports_cb = FakeCombo(ports, port)
        ui_tab.ui.serial_baud_cb = FakeCombo([str(b) for b in bauds], baud)
        ui_tab.app_settings = Mock(last_serial_port=last_port, last_serial_baud=last_baud)
        ui_tab.serial_connection_status = connected
        ui_tab.opened = []
        ui_tab.ui_serial_open_s.connect(lambda port_name, baud_rate: ui_tab.opened.append((port_name, baud_rate)))
        return ui_tab

    def test_refresh_keeps_the_selected_port_when_a_port_is_added_before_it(self):
        ui_tab = self._tab(["ttyUSB1"], "ttyUSB1", self.BAUDS, "115200")

        ui_tab.get_ports_and_bauds(["ttyACM0", "ttyUSB1"], self.BAUDS)

        assert ui_tab.ui.serial_ports_cb.currentText() == "ttyUSB1"
        assert ui_tab.ui.serial_baud_cb.currentText() == "115200"

    def test_refresh_falls_back_to_the_saved_port_when_the_selected_one_is_gone(self):
        ui_tab = self._tab(["COM3", "COM7"], "COM7", self.BAUDS, "9600", last_port="COM5")

        ui_tab.get_ports_and_bauds(["COM3", "COM5"], self.BAUDS)

        assert ui_tab.ui.serial_ports_cb.currentText() == "COM5"
        assert ui_tab.ui.serial_baud_cb.currentText() == "9600"

    def test_refresh_with_no_ports_empties_the_list(self):
        ui_tab = self._tab(["COM3"], "COM3", self.BAUDS, "115200")

        ui_tab.get_ports_and_bauds([], self.BAUDS)

        assert ui_tab.ui.serial_ports_cb.currentText() == ""
        ui_tab.ui.serial_te.append.assert_called_with("No serial ports available.")

    def test_connect_without_a_port_shows_a_message(self):
        ui_tab = self._tab()

        ui_tab.handle_connect_button()

        assert ui_tab.opened == []
        ui_tab.ui.serial_te.append.assert_called_once()
        assert "No serial port selected" in ui_tab.ui.serial_te.append.call_args[0][0]

    def test_connect_opens_the_selected_port(self):
        ui_tab = self._tab(["COM3"], "COM3", self.BAUDS, "115200")

        ui_tab.handle_connect_button()

        assert ui_tab.opened == [("COM3", 115200)]

    def test_serial_errors_while_disconnected_never_connect(self):
        ui_tab = self._tab(["COM3"], "COM3", self.BAUDS, "115200")

        ui_tab.close_for_error()

        assert ui_tab.opened == []

    def test_serial_errors_while_connected_disconnect(self):
        ui_tab = self._tab(["COM3"], "COM3", self.BAUDS, "115200", connected=True)
        ui_tab.act_on_disconnection = Mock()
        closed = []
        ui_tab.ui_serial_close_s.connect(lambda: closed.append(1))

        ui_tab.close_for_error()

        assert closed == [1]
        ui_tab.act_on_disconnection.assert_called_once()


class TestStatusColors:
    """Each machine state has its colours; Not Connected takes the colours of the theme."""

    @staticmethod
    def _style_for(status):
        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        ui_tab = UiControlTab.__new__(UiControlTab)
        ui_tab.ui = Mock()
        ui_tab.update_status_colors(status)
        return ui_tab.ui.status_l.setStyleSheet.call_args.args[0]

    def test_not_connected_follows_the_theme(self):
        assert self._style_for("Not Connected") == ""

    @pytest.mark.parametrize(
        "status, background, text",
        [
            ("Idle", "yellow", "black"),
            ("Run", "green", "white"),
            ("Jog", "blue", "white"),
            ("Alarm", "red", "white"),
            ("Hold:0", "gray", "white"),
        ],
    )
    def test_machine_states_have_readable_colours(self, status, background, text):
        style = self._style_for(status)

        assert f"background-color : {background};" in style
        assert f"color : {text};" in style


@pytest.mark.usefixtures("qapp")
class TestSerialRow:
    """The port row and the send row are the two pages of one box, which keeps one width."""

    @pytest.fixture
    def ui_tab(self):
        from PySide6.QtCore import QObject

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        ui_tab = UiControlTab.__new__(UiControlTab)
        QObject.__init__(ui_tab)
        ui_tab.ui = Mock()
        ui_tab.controlWo = Mock()
        ui_tab.ctrl_layer = Mock()
        ui_tab.is_gcode_rb_selected = Mock(return_value=False)
        ui_tab.enable_control_jog_elements = Mock()
        ui_tab.close_rejected_line_prompt = Mock()
        return ui_tab

    def test_connecting_shows_the_send_row(self, ui_tab):
        ui_tab.act_on_connection(True)

        ui_tab.ui.serial_row_sw.setCurrentWidget.assert_called_once_with(ui_tab.ui.serial_send_page)

    def test_disconnecting_shows_the_port_row(self, ui_tab):
        ui_tab.act_on_disconnection()

        ui_tab.ui.serial_row_sw.setCurrentWidget.assert_called_once_with(ui_tab.ui.serial_connect_page)

    def test_a_failed_connection_keeps_the_port_row(self, ui_tab):
        ui_tab.act_on_connection(False)

        ui_tab.ui.serial_row_sw.setCurrentWidget.assert_not_called()


class TestJobRunning:
    """The control tab knows when a job runs, for the close confirmation."""

    @pytest.fixture
    def ui_tab(self):
        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        ui_tab = UiControlTab.__new__(UiControlTab)
        ui_tab.ui = Mock()
        ui_tab.controlWo = Mock()
        ui_tab.job_running = False
        ui_tab.serial_connection_status = True
        ui_tab.get_selected_file = Mock(return_value=0)
        ui_tab.enable_gcode_rb = Mock()
        return ui_tab

    def test_a_file_job_runs_until_it_ends(self, ui_tab):
        ui_tab.disable_during_send()
        assert ui_tab.job_running is True

        ui_tab.enable_after_send()
        assert ui_tab.job_running is False

    def test_a_tool_change_is_a_running_job(self, ui_tab):
        ui_tab.handle_tool_change_start()

        assert ui_tab.job_running is True

    def test_no_job_runs_on_a_new_tab(self, qapp):
        from unittest.mock import MagicMock

        from PySide6.QtWidgets import QMainWindow
        from ui_the_ant_farm import Ui_MainWindow

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        tab = UiControlTab(ui, MagicMock(), MagicMock(), MagicMock(), MagicMock())

        assert tab.job_running is False
        tab.disable_during_send()
        assert tab.job_running is True
        tab.enable_after_send()
        assert tab.job_running is False
        window.deleteLater()
