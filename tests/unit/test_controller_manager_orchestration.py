from unittest.mock import MagicMock


def test_parse_rx_queue_status_line_updates_status_and_dro(controller_worker, qtbot):
    worker, control, rx_queue = controller_worker
    rx_queue.put("<Idle|MPos:1.000,2.000,3.000|WPos:0.000,0.000,0.000>")

    with qtbot.waitSignal(worker.update_status_s, timeout=1000) as blocker:
        worker.parse_rx_queue()

    assert blocker.args[0]["state"] == "Idle"
    assert worker.dro_status_updated is True
    control.parse_bracket_angle.assert_called_once()


def test_parse_rx_queue_square_line_acks_probe(controller_worker, qtbot):
    worker, control, rx_queue = controller_worker
    control.process_probe_and_abl.return_value = [True, False, False, False]
    worker.ack_probe = MagicMock()

    rx_queue.put("[PRB:1.000,2.000,3.000:1]")

    with qtbot.waitSignal(worker.touched_probe_s, timeout=1000):
        worker.parse_rx_queue()

    worker.ack_probe.assert_called_once()
    control.parse_bracket_square.assert_called_once()


def test_parse_rx_queue_ok_line_sends_next_command(controller_worker):
    worker, _control, rx_queue = controller_worker
    worker.send_to_tx_queue = MagicMock()
    worker._rx_coordinator.process_line = MagicMock(
        return_value={
            "kind": "ok",
            "acknowledged": True,
            "send_command": "G1 X1\n",
            "finished_file": False,
            "file_progress": 10.0,
        }
    )

    rx_queue.put("ok")
    worker.parse_rx_queue()

    worker.send_to_tx_queue.assert_called_once_with("G1 X1\n")


def test_parse_rx_queue_error_line_emits_console_text(controller_worker, qtbot):
    worker, _control, rx_queue = controller_worker
    rx_queue.put("error:2")

    with qtbot.waitSignal(worker.update_console_text_s, timeout=1000) as blocker:
        worker.parse_rx_queue()

    assert blocker.args[0] == "error:2"