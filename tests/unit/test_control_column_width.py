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


class TestConnectionRows:
    def test_the_port_row_is_shown_first(self, ui, qapp):
        show(ui, qapp)

        assert ui.serial_row_sw.currentWidget() is ui.serial_connect_page
        assert ui.serial_ports_cb.isVisible()
        assert not ui.send_cb.isVisible()

    def test_the_column_keeps_its_width_on_both_rows(self, ui, qapp):
        ui.serial_ports_cb.addItems(PORTS)
        show(ui, qapp)
        with_port_row = ui.ctrl_tab_widget.sizeHint().width()

        ui.serial_row_sw.setCurrentWidget(ui.serial_send_page)
        qapp.processEvents()

        assert ui.send_cb.isVisible()
        assert ui.ctrl_tab_widget.sizeHint().width() == with_port_row


class TestJogTab:
    def test_the_overrides_do_not_widen_the_column(self, ui, qapp):
        ui.jog_probe_tab_widget.setCurrentWidget(ui.jog_tab)
        show(ui, qapp)

        assert ui.overridesGridLayout.sizeHint().width() <= ui.probe_terminal_tab.sizeHint().width()
        assert ui.jog_tab.sizeHint().width() <= ui.probe_terminal_tab.sizeHint().width()
