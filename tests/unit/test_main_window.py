import threading
import time
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject, Qt, QThread, Signal, Slot


class TestCloseEvent:
    """Test MainWindow.closeEvent with unsaved settings changes dialog."""

    @pytest.fixture(autouse=True)
    def meta_object(self):
        with patch("TheAntFarm.the_ant_farm.QMetaObject") as meta_object:
            self.meta_object = meta_object
            yield meta_object

    def assert_port_closed_in_the_serial_thread(self, main_window):
        self.meta_object.invokeMethod.assert_called_once_with(
            main_window.serialWo, "close_port", Qt.BlockingQueuedConnection
        )

    def setup_main_window(self, has_unsaved=True):
        from TheAntFarm.the_ant_farm import MainWindow

        main_window = MainWindow.__new__(MainWindow)
        main_window.ui_manager = MagicMock()
        main_window.ui = MagicMock()
        main_window.serialWo = MagicMock()
        main_window.controlWo = MagicMock()
        main_window.serial_thread = MagicMock()
        main_window.control_thread = MagicMock()

        main_window.ui_manager.ui_settings_tab_m.has_unsaved_changes.return_value = has_unsaved
        main_window.ui_manager.ui_control_tab_m.job_running = False
        main_window.ui_manager.ui_control_tab_m.serial_connection_status = False

        mock_event = MagicMock()

        return main_window, mock_event

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_clean_no_dialog(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=False)

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        mock_msgbox.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_called_once()
        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        self.assert_port_closed_in_the_serial_thread(main_window)
        main_window.controlWo.stop_timers.assert_called_once_with()
        mock_event.ignore.assert_not_called()

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_save_saves_and_closes(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = save_btn

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_called_once()
        main_window.ui_manager.save_all_settings.assert_not_called()
        self.assert_port_closed_in_the_serial_thread(main_window)
        main_window.controlWo.stop_timers.assert_called_once_with()
        mock_event.ignore.assert_not_called()

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_discard_closes(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = discard_btn

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_called_once()
        self.assert_port_closed_in_the_serial_thread(main_window)
        main_window.controlWo.stop_timers.assert_called_once_with()
        mock_event.ignore.assert_not_called()

    @patch("TheAntFarm.the_ant_farm.QMessageBox")
    def test_close_cancel_ignores(self, mock_msgbox):
        main_window, mock_event = self.setup_main_window(has_unsaved=True)

        mock_dialog = MagicMock()
        mock_msgbox.return_value = mock_dialog

        save_btn = MagicMock()
        discard_btn = MagicMock()
        cancel_btn = MagicMock()
        mock_dialog.addButton.side_effect = [save_btn, discard_btn, cancel_btn]
        mock_dialog.clickedButton.return_value = cancel_btn

        with patch.object(main_window, "close"):
            main_window.closeEvent(mock_event)

        main_window.ui_manager.ui_settings_tab_m.save_settings_preferences.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_not_called()
        mock_event.ignore.assert_called_once()
        self.meta_object.invokeMethod.assert_not_called()


class _Worker(QObject):
    """A worker whose slot keeps its thread busy, like a blocking serial write."""

    busy_s = Signal(float)

    def __init__(self):
        super().__init__()
        self.started = threading.Event()
        self.busy_s.connect(self.busy)
        self.stop_timers = MagicMock()

    @Slot(float)
    def busy(self, seconds):
        self.started.set()
        time.sleep(seconds)

    @Slot()
    def close_port(self):
        pass


class TestStopThreads:
    """The worker threads get a realistic shared timeout when the application closes."""

    @pytest.fixture
    def main_window(self, qapp):
        from TheAntFarm.the_ant_farm import MainWindow

        main_window = MainWindow.__new__(MainWindow)
        main_window.ui = MagicMock()
        main_window.serialWo, main_window.controlWo = _Worker(), _Worker()
        main_window.serial_thread, main_window.control_thread = QThread(), QThread()
        for worker, thread in (
            (main_window.serialWo, main_window.serial_thread),
            (main_window.controlWo, main_window.control_thread),
        ):
            worker.moveToThread(thread)
            thread.start()
        yield main_window
        for thread in (main_window.serial_thread, main_window.control_thread):
            thread.quit()
            thread.wait(5000)

    def _keep_busy(self, worker, seconds):
        worker.busy_s.emit(seconds)
        assert worker.started.wait(2)

    def test_a_busy_thread_is_waited_for(self, main_window, caplog):
        self._keep_busy(main_window.serialWo, 0.3)

        main_window.stop_threads()

        assert not main_window.serial_thread.isRunning()
        assert not main_window.control_thread.isRunning()
        assert "still running" not in caplog.text

    def test_a_stuck_thread_is_logged_and_the_close_goes_on(self, main_window, caplog):
        main_window.THREAD_STOP_TIMEOUT_MS = 200
        self._keep_busy(main_window.controlWo, 1.5)

        started = time.perf_counter()
        main_window.stop_threads()

        assert time.perf_counter() - started < 1.0
        assert "Control thread still running 200 ms after the close" in caplog.text
        assert "Serial thread still running" not in caplog.text

    def test_the_timers_of_the_gui_thread_are_stopped(self, main_window):
        main_window.stop_threads()

        main_window.controlWo.stop_timers.assert_called_once_with()


class TestConfirmClose:
    """Closing while connected or during a job asks first, with Cancel as the default."""

    @pytest.fixture
    def message_box(self):
        with patch("TheAntFarm.the_ant_farm.QMessageBox") as message_box:
            buttons = {}

            def add_button(text, role):
                buttons[text] = MagicMock(name=text)
                return buttons[text]

            message_box.return_value.addButton.side_effect = add_button
            message_box.buttons = buttons
            yield message_box

    @pytest.fixture
    def main_window(self):
        from TheAntFarm.the_ant_farm import MainWindow

        main_window = MainWindow.__new__(MainWindow)
        main_window.ui_manager = MagicMock()
        main_window.ui_manager.ui_settings_tab_m.has_unsaved_changes.return_value = False
        main_window.controlWo = MagicMock()
        main_window.stop_threads = MagicMock()
        main_window.tab = main_window.ui_manager.ui_control_tab_m
        main_window.tab.job_running = False
        main_window.tab.serial_connection_status = False
        return main_window

    def _close(self, main_window, message_box, answer):
        event = MagicMock()
        prompt = message_box.return_value
        prompt.exec.side_effect = lambda: setattr(prompt, "answer", message_box.buttons[answer])
        prompt.clickedButton.side_effect = lambda: prompt.answer
        with patch("TheAntFarm.the_ant_farm.QMetaObject") as meta_object, patch.object(main_window, "close"):
            main_window.closeEvent(event)
        return event, meta_object

    def test_not_connected_closes_without_asking(self, main_window, message_box):
        event = MagicMock()
        with patch.object(main_window, "close"):
            main_window.closeEvent(event)

        message_box.assert_not_called()
        main_window.stop_threads.assert_called_once_with()
        event.ignore.assert_not_called()

    def test_connected_cancel_keeps_the_application_open(self, main_window, message_box):
        main_window.tab.serial_connection_status = True

        event, meta_object = self._close(main_window, message_box, "Cancel")

        event.ignore.assert_called_once_with()
        main_window.stop_threads.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_not_called()
        meta_object.invokeMethod.assert_not_called()

    def test_connected_close_disconnects_without_resetting(self, main_window, message_box):
        main_window.tab.serial_connection_status = True

        event, meta_object = self._close(main_window, message_box, "Close")

        event.ignore.assert_not_called()
        main_window.stop_threads.assert_called_once_with()
        meta_object.invokeMethod.assert_not_called()
        assert "disconnected" in message_box.return_value.setInformativeText.call_args.args[0]

    def test_cancel_is_the_default_and_the_escape_button(self, main_window, message_box):
        main_window.tab.serial_connection_status = True

        self._close(main_window, message_box, "Cancel")

        prompt = message_box.return_value
        prompt.setDefaultButton.assert_called_once_with(message_box.buttons["Cancel"])
        prompt.setEscapeButton.assert_called_once_with(message_box.buttons["Cancel"])

    @pytest.fixture
    def window_calls(self, main_window):
        with (
            patch.object(main_window, "setEnabled") as set_enabled,
            patch.object(main_window, "statusBar") as status_bar,
        ):
            yield set_enabled, status_bar

    def test_running_job_is_stopped_without_blocking_and_the_close_waits(self, main_window, message_box, window_calls):
        set_enabled, status_bar = window_calls
        main_window.tab.serial_connection_status = True
        main_window.tab.job_running = True

        event, meta_object = self._close(main_window, message_box, "Stop and Close")

        meta_object.invokeMethod.assert_called_once_with(
            main_window.controlWo, "stop_job_for_close", Qt.QueuedConnection
        )
        event.ignore.assert_called_once_with()
        main_window.stop_threads.assert_not_called()
        main_window.ui_manager.save_all_settings.assert_not_called()
        set_enabled.assert_called_once_with(False)
        status_bar.return_value.showMessage.assert_called_once_with("Stopping the job…")

    def test_a_close_while_stopping_is_ignored(self, main_window, message_box, window_calls):
        main_window.tab.serial_connection_status = True
        main_window.tab.job_running = True
        self._close(main_window, message_box, "Stop and Close")
        event = MagicMock()

        main_window.closeEvent(event)

        event.ignore.assert_called_once_with()
        assert message_box.call_count == 1
        main_window.stop_threads.assert_not_called()

    def test_the_window_closes_without_asking_again_when_the_stop_has_ended(
        self, main_window, message_box, window_calls
    ):
        set_enabled, _ = window_calls
        main_window.tab.serial_connection_status = True
        main_window.tab.job_running = True
        self._close(main_window, message_box, "Stop and Close")
        event = MagicMock()

        closes = []

        def close_once():
            closes.append(1)
            if len(closes) == 1:  # Qt does not run the close event again from inside it
                main_window.closeEvent(event)

        with patch.object(main_window, "close", side_effect=close_once):
            main_window.close_after_stop()

        assert len(closes) == 2
        set_enabled.assert_called_with(True)
        event.ignore.assert_not_called()
        assert message_box.call_count == 1
        main_window.ui_manager.save_all_settings.assert_called_once_with()
        main_window.stop_threads.assert_called_once_with()

    def test_a_stop_that_is_not_for_the_close_does_not_close(self, main_window, window_calls):
        with patch.object(main_window, "close") as close:
            main_window.close_after_stop()

        close.assert_not_called()

    def test_running_job_cancel_leaves_the_job_alone(self, main_window, message_box):
        main_window.tab.serial_connection_status = True
        main_window.tab.job_running = True

        event, meta_object = self._close(main_window, message_box, "Cancel")

        meta_object.invokeMethod.assert_not_called()
        event.ignore.assert_called_once_with()

    def test_cancel_comes_before_the_unsaved_settings_dialog(self, main_window, message_box):
        main_window.tab.serial_connection_status = True
        main_window.ui_manager.ui_settings_tab_m.has_unsaved_changes.return_value = True

        self._close(main_window, message_box, "Cancel")

        assert message_box.call_count == 1
        main_window.ui_manager.ui_settings_tab_m.has_unsaved_changes.assert_not_called()
