from app.services.streaming_service import StreamingService


def test_start_initializes_stream_state():
    service = StreamingService(remote_rx_buffer_max_size=32)

    service.start(["G0 X0\n", "G1 X1\n"], buffered_size=3)

    assert service.sending_file is True
    assert service.file_content == ["G0 X0\n", "G1 X1\n"]
    assert service.buffered_size == 3
    assert service.tot_lines == 2
    assert service.cmds_to_ack == 0
    assert service.current_line() == "G0 X0\n"


def test_record_and_acknowledge_command_updates_counters():
    service = StreamingService(remote_rx_buffer_max_size=32)
    service.start(["G0 X0\n", "G1 X1\n"])
    service.advance_content_line()

    service.record_sent_command("G0 X0\n")

    assert service.buffered_cmds == ["G0 X0\n"]
    assert service.buffered_size == len("G0 X0\n")
    assert service.sent_lines == 1
    assert service.cmds_to_ack == 1
    assert service.acknowledge_command() is True
    assert service.ack_lines == 1
    assert service.cmds_to_ack == 0
    assert service.buffered_cmds == []
    assert service.file_progress == 50.0


def test_can_buffer_checks_remote_capacity():
    service = StreamingService(remote_rx_buffer_max_size=10)
    service.start(["G0\n"], buffered_size=5)

    assert service.can_buffer("12\n") is True
    assert service.can_buffer("12345\n") is False


def test_finish_and_stop_reset_stream_state():
    service = StreamingService(remote_rx_buffer_max_size=32)
    service.start(["G0 X0\n"])
    service.advance_content_line()

    service.finish_file()

    assert service.sending_file is False
    assert service.eof_wait_for_idle is True
    assert service.file_progress == 100.0

    service.stop()

    assert service.sending_file is False
    assert service.file_content == []
    assert service.buffered_cmds == []
    assert service.buffered_size == 0
    assert service.tot_lines == 0