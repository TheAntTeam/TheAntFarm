from unittest.mock import MagicMock

from app.services.rx_coordinator_service import RxCoordinatorService
from app.services.streaming_service import StreamingService


def test_process_line_status_delegates_status_payload():
    service = RxCoordinatorService()

    result = service.process_line("status", "<Idle>", dro_status_updated=False, status_payload={"state": "Idle"})

    assert result["kind"] == "status"
    assert result["status_payload"] == {"state": "Idle"}
    assert result["mark_dro_updated"] is True


def test_process_line_square_maps_probe_actions():
    service = RxCoordinatorService()

    result = service.process_line("square", "[PRB:1,2,3:1]", square_flags=(True, False, True, False))

    assert result["kind"] == "square"
    assert result["touched_probe"] is True
    assert result["ack_probe"] is True
    assert result["ack_auto_bed_levelling"] is False
    assert result["send_next_abl"] is True


def test_process_line_ok_delegates_transport_flow():
    service = RxCoordinatorService()
    streaming = StreamingService(remote_rx_buffer_max_size=32)
    streaming.start(["G0 X0\n", "G1 X1\n"])
    streaming.advance_content_line()
    streaming.record_sent_command("G0 X0\n")
    macro = MagicMock()
    macro.macro_on = False

    result = service.process_line(
        "ok",
        "ok",
        streaming=streaming,
        macro=macro,
        prepare_file_command=lambda line: line,
        workspace_parameters={},
        probe_data=[],
    )

    assert result["kind"] == "ok"
    assert result["acknowledged"] is True
    assert result["send_command"] == "G1 X1\n"


def test_process_line_error_maps_console_text():
    service = RxCoordinatorService()

    result = service.process_line("error", "error:2")

    assert result == {"kind": "error", "console_text": "error:2"}


def test_process_line_console_maps_console_text():
    service = RxCoordinatorService()

    result = service.process_line("console", "Grbl ready")

    assert result == {"kind": "console", "console_text": "Grbl ready"}