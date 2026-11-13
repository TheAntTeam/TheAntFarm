"""The override sliders and the feed and spindle readout of the Jog tab."""

from collections import OrderedDict
from unittest.mock import MagicMock

import pytest
from PySide6.QtTest import QTest


def _status(**fields):
    status = OrderedDict(state="Run", mpos=(0.0, 0.0, 0.0), wpos=(0.0, 0.0, 0.0))
    status.update(fields)
    return status


@pytest.fixture
def tab(qapp):
    from PySide6.QtWidgets import QMainWindow
    from ui_the_ant_farm import Ui_MainWindow

    from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    control_tab = UiControlTab(ui, MagicMock(), MagicMock(), MagicMock(), MagicMock())
    control_tab.sent = []
    control_tab.override_s.connect(lambda kind, value: control_tab.sent.append((kind, value)))
    control_tab.act_on_connection(True)
    yield control_tab
    window.deleteLater()


def _settle(tab):
    QTest.qWait(tab.OVERRIDE_SEND_DELAY_MS + 100)


def _controls(tab):
    ui = tab.ui
    return [ui.feed_ov_sl, ui.feed_ov_sb, ui.spindle_ov_sl, ui.spindle_ov_sb, ui.rapid_ov_sl]


class TestSending:
    def test_the_slider_sends_once_it_has_settled(self, tab):
        for value in (110, 120, 130):
            tab.ui.feed_ov_sl.setValue(value)

        assert tab.sent == []
        _settle(tab)
        assert tab.sent == [("feed", 130)]

    def test_the_text_field_moves_the_slider_and_sends(self, tab):
        tab.ui.spindle_ov_sb.setValue(85)
        _settle(tab)

        assert tab.ui.spindle_ov_sl.value() == 85
        assert tab.sent == [("spindle", 85)]

    def test_the_slider_moves_the_text_field(self, tab):
        tab.ui.feed_ov_sl.setValue(150)

        assert tab.ui.feed_ov_sb.value() == 150

    @pytest.mark.parametrize("index, value", [(0, 25), (1, 50)])
    def test_the_rapid_slider_has_three_positions(self, tab, index, value):
        tab.ui.rapid_ov_sl.setValue(index)
        _settle(tab)

        assert tab.ui.rapid_ov_l.text() == f"{value}%"
        assert tab.sent == [("rapid", value)]

    def test_the_sliders_reach_the_controller(self, qapp):
        from PySide6.QtWidgets import QMainWindow
        from ui_the_ant_farm import Ui_MainWindow

        from TheAntFarm.ui_manager.ui_control_tab import UiControlTab

        window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        worker = MagicMock()
        control_tab = UiControlTab(ui, worker, MagicMock(), MagicMock(), MagicMock())
        control_tab.act_on_connection(True)

        ui.feed_ov_sb.setValue(90)
        _settle(control_tab)

        worker.set_override.assert_called_once_with("feed", 90)
        window.deleteLater()


class TestEnabling:
    def test_the_controls_are_disabled_until_connected(self, tab):
        tab.act_on_disconnection()
        assert not any(control.isEnabled() for control in _controls(tab))

        tab.act_on_connection(True)

        assert all(control.isEnabled() for control in _controls(tab))

    def test_the_controls_stay_enabled_during_a_job(self, tab):
        tab.disable_during_send()

        assert all(control.isEnabled() for control in _controls(tab))


class TestFollowingTheMachine:
    def test_the_sliders_show_the_reported_overrides(self, tab):
        tab.update_status(_status(OvFeed=90, OvRapid=50, OvSpindle=110))

        assert tab.ui.feed_ov_sb.value() == 90
        assert tab.ui.feed_ov_sl.value() == 90
        assert tab.ui.spindle_ov_sb.value() == 110
        assert tab.ui.rapid_ov_l.text() == "50%"
        _settle(tab)
        assert tab.sent == []

    def test_a_rapid_value_grbl_does_not_have_is_ignored(self, tab):
        tab.update_status(_status(OvRapid=30))

        assert tab.ui.rapid_ov_sl.value() == 2
        assert tab.ui.rapid_ov_l.text() == "100%"

    def test_a_target_is_kept_until_the_machine_reaches_it(self, tab):
        tab.ui.feed_ov_sb.setValue(70)
        _settle(tab)

        tab.update_status(_status(OvFeed=90))
        assert tab.ui.feed_ov_sb.value() == 70

        tab.update_status(_status(OvFeed=70))
        tab.update_status(_status(OvFeed=100))
        assert tab.ui.feed_ov_sb.value() == 100

    def test_a_target_never_reached_is_dropped(self, tab):
        tab.ui.feed_ov_sb.setValue(70)
        _settle(tab)
        target, sent_at = tab.override_pending["feed"]
        tab.override_pending["feed"] = (target, sent_at - tab.OVERRIDE_PENDING_S)

        tab.update_status(_status(OvFeed=100))

        assert tab.ui.feed_ov_sb.value() == 100

    def test_a_report_does_not_move_a_slider_being_changed(self, tab):
        tab.ui.feed_ov_sl.setValue(140)

        tab.update_status(_status(OvFeed=100))

        assert tab.ui.feed_ov_sl.value() == 140


class TestReadout:
    def test_nothing_is_shown_before_a_report(self, tab):
        assert tab.ui.cur_feed_l.text() == "F -"
        assert tab.ui.cur_spindle_l.text() == "S -"
        assert tab.ui.feed_ov_sb.value() == 100
        assert tab.ui.rapid_ov_l.text() == "100%"

    def test_a_report_shows_the_rates(self, tab):
        tab.update_status(_status(curfeed=300.0, curspindle=1000.0))

        assert tab.ui.cur_feed_l.text() == "F 300"
        assert tab.ui.cur_spindle_l.text() == "S 1000"

    def test_disconnecting_clears_the_readout(self, tab):
        tab.update_status(_status(curfeed=300.0, curspindle=1000.0, OvFeed=90, OvRapid=50, OvSpindle=110))
        tab.ui.spindle_ov_sb.setValue(120)

        tab.act_on_disconnection()
        _settle(tab)

        assert tab.ui.cur_feed_l.text() == "F -"
        assert tab.ui.cur_spindle_l.text() == "S -"
        assert tab.ui.feed_ov_sb.value() == 100
        assert tab.ui.spindle_ov_sb.value() == 100
        assert tab.ui.rapid_ov_l.text() == "100%"
        assert tab.sent == []


class TestTyping:
    def test_a_report_does_not_overwrite_a_field_being_typed(self, tab):
        tab.ui.feed_ov_sb.hasFocus = lambda: True
        tab.ui.feed_ov_sb.lineEdit().setText("7")

        tab.update_status(_status(OvFeed=90))

        assert tab.ui.feed_ov_sb.lineEdit().text() == "7%"

    def test_the_field_follows_the_machine_again_once_left(self, tab):
        tab.ui.feed_ov_sb.hasFocus = lambda: True
        tab.update_status(_status(OvFeed=90))
        tab.ui.feed_ov_sb.hasFocus = lambda: False

        tab.update_status(_status(OvFeed=90))

        assert tab.ui.feed_ov_sb.value() == 90


class TestTypingOutOfRange:
    @pytest.mark.parametrize("text, value", [("5", 10), ("250", 200)])
    def test_a_value_out_of_range_is_saturated(self, tab, text, value):
        from PySide6.QtCore import Qt

        line_edit = tab.ui.feed_ov_sb.lineEdit()
        line_edit.selectAll()
        QTest.keyClicks(line_edit, text)
        QTest.keyClick(line_edit, Qt.Key_Return)
        _settle(tab)

        assert tab.ui.feed_ov_sb.value() == value
        assert tab.sent == [("feed", value)]
