from app.services.rx_dispatch_service import RxDispatchService


def test_handle_status_marks_first_dro_update():
    result = RxDispatchService.handle_status({"state": "Idle"}, False)

    assert result == {
        "status_payload": {"state": "Idle"},
        "mark_dro_updated": True,
        "check_eof_and_idle": True,
    }


def test_handle_status_preserves_existing_dro_update_state():
    result = RxDispatchService.handle_status({"state": "Run"}, True)

    assert result["status_payload"] == {"state": "Run"}
    assert result["mark_dro_updated"] is False
    assert result["check_eof_and_idle"] is True


def test_handle_square_maps_probe_and_abl_actions():
    result = RxDispatchService.handle_square("[PRB:1,2,3:1]", True, True, True, False)

    assert result == {
        "touched_probe": True,
        "ack_probe": True,
        "ack_auto_bed_levelling": True,
        "send_next_abl": True,
        "console_text": None,
    }


def test_handle_square_emits_console_text_for_other_command():
    result = RxDispatchService.handle_square("[MSG:info]", False, False, False, True)

    assert result["touched_probe"] is False
    assert result["ack_probe"] is False
    assert result["ack_auto_bed_levelling"] is False
    assert result["send_next_abl"] is False
    assert result["console_text"] == "[MSG:info]"