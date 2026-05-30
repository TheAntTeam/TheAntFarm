from app.services.manager_adapter_service import ManagerAdapterService


def test_prepare_tx_payload_uses_decoder():
    result = ManagerAdapterService.prepare_tx_payload("G0 X0", lambda data: f"{data}\n")
    assert result == "G0 X0\n"


def test_get_poll_payload():
    assert ManagerAdapterService.get_poll_payload() == b"?"


def test_format_elapsed_time_without_start_time():
    assert ManagerAdapterService.format_elapsed_time(None) == "00:00:00"


def test_format_elapsed_time_with_now_time_override():
    assert ManagerAdapterService.format_elapsed_time(10.0, now_time=3730.0) == "01:02:00"