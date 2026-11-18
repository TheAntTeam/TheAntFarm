"""The Control tab asks before the actions that move the machine or its work zero."""

from unittest.mock import Mock, patch

import pytest

BBOX = (-1.0, -2.0, -0.1, 45.0, 30.0, 2.0)


@pytest.fixture
def ui_tab(qapp):
    from PySide6.QtCore import QObject

    from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

    ui_tab = UiControlTab.__new__(UiControlTab)
    QObject.__init__(ui_tab)
    ui_tab.ui = Mock()
    ui_tab.ui.wpos_x_l.text.return_value = "1.000"
    ui_tab.ui.wpos_y_l.text.return_value = "2.000"
    ui_tab.ui.wpos_z_l.text.return_value = "3.000"
    ui_tab.ui.status_l.text.return_value = "Idle"
    ui_tab.ui.gcode_tw.cellWidget.return_value.toolTip.return_value = "/jobs/top_gerber.gcode"
    ui_tab.controlWo = Mock()
    ui_tab.controlWo.get_gcode_bbox.return_value = BBOX
    ui_tab.app_settings = Mock(confirm_play=True, confirm_homing=True, confirm_tool_change=True, confirm_zero=True)
    ui_tab.machine_settings = Mock(tool_change_homing_warning=True)
    ui_tab.controlWo.homed = True
    ui_tab.job_running = False
    ui_tab.serial_connection_status = True
    ui_tab.get_selected_file = Mock(return_value=0)
    ui_tab.enable_gcode_rb = Mock()
    ui_tab._confirm = Mock(return_value=True)
    ui_tab.commands = []
    ui_tab.sent_files = []
    ui_tab.ui_send_cmd_s.connect(lambda name, args: ui_tab.commands.append((name, args)))
    ui_tab.send_gcode_s.connect(ui_tab.sent_files.append)
    return ui_tab


class TestConfirmDialog:
    @pytest.fixture
    def message_box(self):
        with patch("TheAntFarm.ui_manager.ui_control_tab.QMessageBox") as message_box:
            buttons = {"Start": Mock(), "Cancel": Mock()}
            message_box.return_value.addButton.side_effect = lambda text, role: buttons[text]
            message_box.buttons = buttons
            yield message_box

    @pytest.fixture
    def real_confirm(self, ui_tab):
        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        return lambda *args: UiControlTab._confirm(ui_tab, *args)

    def test_the_accept_button_confirms(self, real_confirm, message_box):
        message_box.return_value.clickedButton.return_value = message_box.buttons["Start"]

        assert real_confirm("Title", "Text", "Details", "Start") is True
        message_box.return_value.setInformativeText.assert_called_once_with("Details")

    def test_cancel_declines_and_is_the_default(self, real_confirm, message_box):
        cancel = message_box.buttons["Cancel"]
        message_box.return_value.clickedButton.return_value = cancel

        assert real_confirm("Title", "Text", "", "Start") is False
        message_box.return_value.setDefaultButton.assert_called_once_with(cancel)
        message_box.return_value.setEscapeButton.assert_called_once_with(cancel)
        message_box.return_value.setInformativeText.assert_not_called()

    def test_a_closed_dialog_declines(self, real_confirm, message_box):
        message_box.return_value.clickedButton.return_value = None

        assert real_confirm("Title", "Text", "", "Start") is False


class TestPlay:
    def test_the_question_shows_the_file_the_area_and_the_position(self, ui_tab):
        ui_tab.play_send_file()

        _title, text, details, _label = ui_tab._confirm.call_args.args
        assert "top_gerber.gcode" in text
        assert "X from -1.000 to 45.000" in details
        assert "Y from -2.000 to 30.000" in details
        assert "Z from -0.100 to 2.000" in details
        assert "X 1.000  Y 2.000  Z 3.000" in details

    def test_confirming_sends_the_file(self, ui_tab):
        ui_tab.play_send_file()

        assert ui_tab.sent_files == ["/jobs/top_gerber.gcode"]
        assert ui_tab.job_running is True

    def test_declining_sends_nothing(self, ui_tab):
        ui_tab._confirm.return_value = False

        ui_tab.play_send_file()

        assert ui_tab.sent_files == []
        assert ui_tab.job_running is False

    def test_an_unknown_area_is_left_out(self, ui_tab):
        ui_tab.controlWo.get_gcode_bbox.return_value = None

        ui_tab.play_send_file()

        details = ui_tab._confirm.call_args.args[2]
        assert "Coordinates of the job" not in details
        assert "X 1.000  Y 2.000  Z 3.000" in details

    def test_the_setting_turns_the_question_off(self, ui_tab):
        ui_tab.app_settings.confirm_play = False

        ui_tab.play_send_file()

        ui_tab._confirm.assert_not_called()
        assert ui_tab.sent_files == ["/jobs/top_gerber.gcode"]

    def test_the_question_says_it_can_be_turned_off(self, ui_tab):
        ui_tab.play_send_file()

        assert ui_tab.TURN_OFF_NOTE in ui_tab._confirm.call_args.args[2]

    def test_nothing_is_asked_while_disconnected(self, ui_tab):
        ui_tab.serial_connection_status = False

        ui_tab.play_send_file()

        ui_tab._confirm.assert_not_called()
        assert ui_tab.sent_files == []


class TestHomingAndToolChange:
    def test_confirmed_homing_is_sent(self, ui_tab):
        ui_tab.handle_homing()

        assert ui_tab.commands == [("homing", (None, None, None))]

    def test_declined_homing_is_not_sent(self, ui_tab):
        ui_tab._confirm.return_value = False

        ui_tab.handle_homing()

        assert ui_tab.commands == []

    def test_confirmed_tool_change_starts(self, ui_tab):
        ui_tab.handle_tool_change_start()

        ui_tab.controlWo.send_tool_change_s.emit.assert_called_once_with()
        assert ui_tab.job_running is True

    def test_declined_tool_change_does_not_start(self, ui_tab):
        ui_tab._confirm.return_value = False

        ui_tab.handle_tool_change_start()

        ui_tab.controlWo.send_tool_change_s.emit.assert_not_called()
        assert ui_tab.job_running is False

    def test_the_setting_turns_the_homing_question_off(self, ui_tab):
        ui_tab.app_settings.confirm_homing = False

        ui_tab.handle_homing()

        ui_tab._confirm.assert_not_called()
        assert ui_tab.commands == [("homing", (None, None, None))]

    def test_the_setting_turns_the_tool_change_question_off(self, ui_tab):
        ui_tab.app_settings.confirm_tool_change = False

        ui_tab.handle_tool_change_start()

        ui_tab._confirm.assert_not_called()
        ui_tab.controlWo.send_tool_change_s.emit.assert_called_once_with()

    @pytest.mark.parametrize("handler", ["handle_homing", "handle_tool_change_start"])
    def test_the_question_says_it_can_be_turned_off(self, ui_tab, handler):
        getattr(ui_tab, handler)()

        assert ui_tab.TURN_OFF_NOTE in ui_tab._confirm.call_args.args[2]


class TestToolChangeWithoutHoming:
    @pytest.fixture(autouse=True)
    def not_homed(self, ui_tab):
        ui_tab.controlWo.homed = False

    def test_the_question_warns_about_the_homing(self, ui_tab):
        ui_tab.handle_tool_change_start()

        _title, text, details, label = ui_tab._confirm.call_args.args
        assert "not been homed" in text
        assert ui_tab.HOMING_WARNING_NOTE in details
        assert label == "Start anyway"

    def test_confirming_starts_the_tool_change(self, ui_tab):
        ui_tab.handle_tool_change_start()

        ui_tab.controlWo.send_tool_change_s.emit.assert_called_once_with()
        assert ui_tab.job_running is True

    def test_declining_does_not_start_it(self, ui_tab):
        ui_tab._confirm.return_value = False

        ui_tab.handle_tool_change_start()

        ui_tab.controlWo.send_tool_change_s.emit.assert_not_called()
        assert ui_tab.job_running is False

    def test_the_warning_is_asked_also_without_the_tool_change_question(self, ui_tab):
        ui_tab.app_settings.confirm_tool_change = False

        ui_tab.handle_tool_change_start()

        ui_tab._confirm.assert_called_once()
        assert "not been homed" in ui_tab._confirm.call_args.args[1]

    def test_the_warning_is_asked_only_once(self, ui_tab):
        ui_tab.handle_tool_change_start()

        ui_tab._confirm.assert_called_once()

    def test_the_setting_turns_the_warning_off(self, ui_tab):
        ui_tab.machine_settings.tool_change_homing_warning = False

        ui_tab.handle_tool_change_start()

        text = ui_tab._confirm.call_args.args[1]
        assert text == "Start a tool change?"

    def test_both_settings_off_start_at_once(self, ui_tab):
        ui_tab.machine_settings.tool_change_homing_warning = False
        ui_tab.app_settings.confirm_tool_change = False

        ui_tab.handle_tool_change_start()

        ui_tab._confirm.assert_not_called()
        ui_tab.controlWo.send_tool_change_s.emit.assert_called_once_with()

    def test_a_homed_machine_gets_the_usual_question(self, ui_tab):
        ui_tab.controlWo.homed = True

        ui_tab.handle_tool_change_start()

        assert ui_tab._confirm.call_args.args[1] == "Start a tool change?"


class TestSoftReset:
    def test_it_is_confirmed_at_rest(self, ui_tab):
        ui_tab._confirm.return_value = False

        ui_tab.handle_soft_reset()

        ui_tab._confirm.assert_called_once()
        assert ui_tab.commands == []

    def test_a_confirmed_reset_is_sent(self, ui_tab):
        ui_tab.handle_soft_reset()

        assert ui_tab.commands == [("soft_reset", (None, None, None))]

    @pytest.mark.parametrize("status", ["Run", "Jog", "Hold:0", "Alarm", "Home", "Door:1"])
    def test_it_is_immediate_when_the_machine_is_not_idle(self, ui_tab, status):
        ui_tab.ui.status_l.text.return_value = status

        ui_tab.handle_soft_reset()

        ui_tab._confirm.assert_not_called()
        assert ui_tab.commands == [("soft_reset", (None, None, None))]

    def test_it_is_immediate_during_a_job(self, ui_tab):
        ui_tab.job_running = True

        ui_tab.handle_soft_reset()

        ui_tab._confirm.assert_not_called()
        assert ui_tab.commands == [("soft_reset", (None, None, None))]


ZERO_CASES = [
    ("handle_x_0", "X", (0.0, None, None)),
    ("handle_y_0", "Y", (None, 0.0, None)),
    ("handle_z_0", "Z", (None, None, 0.0)),
    ("handle_xy_0", "X and Y", (0.0, 0.0, None)),
]


class TestZero:
    @pytest.mark.parametrize("handler, axes, target", ZERO_CASES)
    def test_a_confirmed_zero_is_set(self, ui_tab, handler, axes, target):
        getattr(ui_tab, handler)()

        text = ui_tab._confirm.call_args.args[1]
        assert f"work zero of {axes} " in text
        assert ui_tab.commands == [("set_wps", target)]

    @pytest.mark.parametrize("handler, axes, target", ZERO_CASES)
    def test_a_declined_zero_is_not_set(self, ui_tab, handler, axes, target):
        ui_tab._confirm.return_value = False

        getattr(ui_tab, handler)()

        assert ui_tab.commands == []

    @pytest.mark.parametrize("handler, axes, target", ZERO_CASES)
    def test_the_setting_turns_the_question_off(self, ui_tab, handler, axes, target):
        ui_tab.app_settings.confirm_zero = False

        getattr(ui_tab, handler)()

        ui_tab._confirm.assert_not_called()
        assert ui_tab.commands == [("set_wps", target)]


class TestGcodeBbox:
    def test_a_loaded_file_has_a_bounding_box(self):
        from TheAntFarm.controller.controller_manager import ControllerWorker

        worker = ControllerWorker.__new__(ControllerWorker)
        worker.control_controller = Mock()
        worker.control_controller.get_boundary_box.return_value = BBOX

        assert worker.get_gcode_bbox("job.gcode") == BBOX

    def test_an_unknown_file_has_none(self):
        from TheAntFarm.controller.controller_manager import ControllerWorker

        worker = ControllerWorker.__new__(ControllerWorker)
        worker.control_controller = Mock()
        worker.control_controller.get_boundary_box.side_effect = KeyError("job.gcode")

        assert worker.get_gcode_bbox("job.gcode") is None
