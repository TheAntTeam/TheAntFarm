"""The left column of the Control tab keeps its width whatever the serial ports and the connection state."""

import pytest

PORTS = ["COM3", "/dev/cu.usbserial-A10KBJ8Z", "GRBL simulator"]


@pytest.fixture
def ui(qapp):
    from PySide6.QtWidgets import QMainWindow
    from ui_the_ant_farm import Ui_MainWindow

    window = QMainWindow()
    form = Ui_MainWindow()
    form.setupUi(window)
    form.main_tab_widget.setCurrentWidget(form.control_tab)
    form.ctrl_tab_widget.setCurrentWidget(form.sender_tab)
    form.jog_probe_tab_widget.setCurrentWidget(form.probe_terminal_tab)
    form.window = window
    yield form
    window.close()
    window.deleteLater()


def show(ui, qapp) -> None:
    ui.window.show()
    qapp.processEvents()


class TestPortBox:
    def test_the_port_box_cuts_on_the_left(self, ui):
        from combobox_elide_left import ComboBoxElideLeft

        assert isinstance(ui.serial_ports_cb, ComboBoxElideLeft)

    def test_its_width_does_not_follow_the_ports(self, ui, qapp):
        ports = ui.serial_ports_cb
        empty = ports.sizeHint().width()

        ports.addItems(PORTS)
        show(ui, qapp)

        assert ports.isVisible()
        assert ports.sizeHint().width() == empty


class TestBaudBox:
    def test_its_width_does_not_follow_the_rates(self, ui, qapp):
        bauds = ui.serial_baud_cb
        empty = bauds.sizeHint().width()

        bauds.addItems(["9600", "115200", "4000000", "1000000000000"])
        show(ui, qapp)

        assert bauds.isVisible()
        assert bauds.sizeHint().width() == empty


class TestConnectionRow:
    CONNECTION_WIDGETS = ("serial_ports_cb", "serial_baud_cb", "refresh_pb", "connect_pb")

    def test_it_is_outside_the_tabs(self, ui):
        for name in self.CONNECTION_WIDGETS:
            assert not ui.ctrl_tab_widget.isAncestorOf(getattr(ui, name)), name

    @pytest.mark.parametrize("tab", ["gcode_load", "sender_tab"])
    def test_it_is_visible_on_every_tab_of_the_left_column(self, ui, qapp, tab):
        ui.ctrl_tab_widget.setCurrentWidget(getattr(ui, tab))
        show(ui, qapp)

        for name in self.CONNECTION_WIDGETS:
            assert getattr(ui, name).isVisible(), name

    def test_it_is_a_box_in_the_right_column_under_the_status(self, ui, qapp):
        from PySide6.QtWidgets import QGroupBox

        show(ui, qapp)
        status = ui.status_l.geometry()
        box = ui.connection_box.geometry()

        assert isinstance(ui.connection_box, QGroupBox)
        assert box.left() == status.left()
        assert status.bottom() < box.top()
        assert box.bottom() < ui.unlock_tb.geometry().top()

    def test_the_box_holds_the_widgets_one_under_the_other(self, ui, qapp):
        show(ui, qapp)
        previous_bottom = -1

        for name in self.CONNECTION_WIDGETS:
            widget = getattr(ui, name)
            assert widget.parent() is ui.connection_box, name
            assert widget.geometry().top() > previous_bottom, name
            assert ui.connection_box.rect().contains(widget.geometry()), name
            previous_bottom = widget.geometry().bottom()

    def test_the_box_is_as_wide_as_the_machine_buttons(self, ui, qapp):
        ui.serial_ports_cb.addItems(PORTS)
        show(ui, qapp)

        assert ui.connection_box.width() == ui.homing_tb.width()

    def test_the_terminal_keeps_the_send_row(self, ui, qapp):
        show(ui, qapp)

        for name in ("send_cb", "send_pb", "clear_terminal_pb"):
            assert ui.probe_terminal_tab.isAncestorOf(getattr(ui, name)), name
            assert getattr(ui, name).isVisible(), name


class TestJogTab:
    def test_the_overrides_do_not_widen_the_column(self, ui, qapp):
        ui.jog_probe_tab_widget.setCurrentWidget(ui.jog_tab)
        show(ui, qapp)

        assert ui.overridesGridLayout.sizeHint().width() <= ui.probe_terminal_tab.sizeHint().width()
        assert ui.jog_tab.sizeHint().width() <= ui.probe_terminal_tab.sizeHint().width()


class TestTooltips:
    ICON_ONLY = (
        "soft_reset_tb",
        "unlock_tb",
        "homing_tb",
        "play_tb",
        "pause_resume_tb",
        "stop_tb",
        "tool_change_tb",
        "upload_temp_tb",
        "open_gcode_tb",
        "remove_gcode_tb",
        "load_align_layer_tb",
        "add_point_tb",
        "remove_point_tb",
        "apply_alignment_tb_2",
    )

    def test_the_buttons_that_show_no_readable_text_have_a_tooltip(self, ui):
        missing = [name for name in self.ICON_ONLY if not getattr(ui, name).toolTip()]

        assert missing == []


class TestLabels:
    def test_the_divide_buttons_do_not_read_as_plus(self, ui):
        for name in ("xy_div_10_pb", "z_div_10_pb", "xy_div_10_pb_2", "z_div_10_pb_2"):
            assert getattr(ui, name).text() == "/10"


class TestShortWindow:
    MACHINE_BUTTONS = ("unlock_tb", "homing_tb", "play_tb", "pause_resume_tb", "stop_tb", "tool_change_tb")

    def test_the_machine_buttons_can_shrink(self, ui):
        from machine_tool_button import MachineToolButton

        assert all(isinstance(getattr(ui, name), MachineToolButton) for name in self.MACHINE_BUTTONS)

    def test_the_connection_box_keeps_its_height_in_the_smallest_window(self, ui, qapp):
        ui.window.resize(ui.window.minimumSize())
        show(ui, qapp)

        assert ui.connection_box.height() >= ui.connection_box.sizeHint().height()

    def test_the_machine_buttons_keep_their_full_height_in_a_tall_window(self, ui, qapp):
        ui.window.resize(1400, 1100)
        show(ui, qapp)

        assert [getattr(ui, name).iconSize().height() for name in self.MACHINE_BUTTONS] == [64, 64, 64, 64, 64, 72]
