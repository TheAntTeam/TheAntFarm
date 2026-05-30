from app.services.file_send_service import FileSendService
from app.services.streaming_service import StreamingService


def test_begin_send_initializes_streaming_state():
    svc = FileSendService()
    streaming = StreamingService(remote_rx_buffer_max_size=64)

    state = svc.begin_send(streaming, ["G0 X0\n", "G1 X1\n"], buffered_size=3)

    assert state["has_content"] is True
    assert state["total_lines"] == 2
    assert streaming.buffered_size == 3
    assert streaming.sending_file is True


def test_prepare_initial_command_records_first_send_when_buffer_allows():
    svc = FileSendService()
    streaming = StreamingService(remote_rx_buffer_max_size=64)
    svc.begin_send(streaming, ["G0 X0\n"], buffered_size=0)

    result = svc.prepare_initial_command(streaming, lambda line: line)

    assert result["command"] == "G0 X0\n"
    assert streaming.sent_lines == 1
    assert streaming.content_line == 1
    assert streaming.cmds_to_ack == 1


def test_prepare_initial_command_skips_when_no_content_or_no_buffer():
    svc = FileSendService()
    streaming = StreamingService(remote_rx_buffer_max_size=5)
    svc.begin_send(streaming, [], buffered_size=0)
    assert svc.prepare_initial_command(streaming, lambda line: line)["command"] is None

    svc.begin_send(streaming, ["G0 X0\n"], buffered_size=4)
    assert svc.prepare_initial_command(streaming, lambda line: line)["command"] is None


def test_stop_send_returns_reset_commands_and_resets_stream():
    svc = FileSendService()
    streaming = StreamingService(remote_rx_buffer_max_size=64)
    svc.begin_send(streaming, ["G0 X0\n"], buffered_size=0)

    state = svc.stop_send(streaming, send_soft_reset=True)

    assert state["reset_commands"] == [b"!", b"\030"]
    assert state["next_send_soft_reset"] is True
    assert streaming.sending_file is False