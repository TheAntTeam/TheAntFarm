from unittest.mock import MagicMock

from app.services.streaming_service import StreamingService
from app.services.transport_coordinator_service import TransportCoordinatorService


def test_process_ok_ack_returns_noop_when_nothing_acknowledged():
    coordinator = TransportCoordinatorService()
    streaming = StreamingService()
    macro = MagicMock()
    macro.macro_on = False

    result = coordinator.process_ok_ack(streaming, macro, lambda line: line, {}, [])

    assert result == {
        "acknowledged": False,
        "send_command": None,
        "finished_file": False,
        "file_progress": 0.0,
    }


def test_process_ok_ack_sends_next_regular_command():
    coordinator = TransportCoordinatorService()
    streaming = StreamingService(remote_rx_buffer_max_size=32)
    streaming.start(["G0 X0\n", "G1 X1\n"])
    streaming.advance_content_line()
    streaming.record_sent_command("G0 X0\n")
    macro = MagicMock()
    macro.macro_on = False

    result = coordinator.process_ok_ack(streaming, macro, lambda line: line, {}, [])

    assert result["acknowledged"] is True
    assert result["send_command"] == "G1 X1\n"
    assert result["finished_file"] is False
    assert streaming.sent_lines == 2
    assert streaming.content_line == 2


def test_process_ok_ack_honors_wait_tag_decoding():
    coordinator = TransportCoordinatorService()
    streaming = StreamingService(remote_rx_buffer_max_size=32)
    streaming.start(["MACRO\n", "G1 X1\n"])
    streaming.advance_content_line()
    streaming.record_sent_command("$#\n")
    macro = MagicMock()
    macro.macro_on = False

    def prepare(_line):
        streaming.wait_tag_decoding = True
        return "$#\n"

    result = coordinator.process_ok_ack(streaming, macro, prepare, {}, [])

    assert result["acknowledged"] is True
    assert result["send_command"] is None
    assert result["finished_file"] is False


def test_process_ok_ack_finishes_file_at_eof():
    coordinator = TransportCoordinatorService()
    streaming = StreamingService(remote_rx_buffer_max_size=32)
    streaming.start(["G0 X0\n"])
    streaming.advance_content_line()
    streaming.record_sent_command("G0 X0\n")
    macro = MagicMock()
    macro.macro_on = False

    result = coordinator.process_ok_ack(streaming, macro, lambda line: line, {}, [])

    assert result["acknowledged"] is True
    assert result["send_command"] is None
    assert result["finished_file"] is True
    assert streaming.sending_file is False
    assert streaming.eof_wait_for_idle is True