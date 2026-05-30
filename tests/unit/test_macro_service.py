from unittest.mock import MagicMock

from app.services.macro_service import MacroService


def test_prepare_command_returns_plain_command_for_non_macro():
    service = MacroService()
    gcr = MagicMock()
    gcr.is_macro.return_value = False

    result = service.prepare_command("G0 X0\n", 0, 0, MagicMock(), MagicMock(), "root", gcr)

    assert result == {
        "command": "G0 X0\n",
        "wait_tag_decoding": False,
        "total_lines_delta": 0,
    }
    assert service.macro_on is False


def test_prepare_command_waits_when_machine_queue_not_empty():
    service = MacroService()
    gcr = MagicMock()
    gcr.is_macro.return_value = True

    result = service.prepare_command("MACRO\n", 1, 2, MagicMock(), MagicMock(), "root", gcr)

    assert result["command"] == "MACRO\n"
    assert result["wait_tag_decoding"] is True
    assert result["total_lines_delta"] == 0
    assert service.macro_on is False


def test_prepare_command_starts_macro_when_queue_is_empty():
    service = MacroService()
    gcr = MagicMock()
    gcr.is_macro.return_value = True
    wpos = MagicMock()
    mpos = MagicMock()
    wpos.copy.return_value = [1, 2, 3]
    mpos.copy.return_value = [4, 5, 6]
    macro_cls = MagicMock()
    macro_instance = MagicMock()
    macro_cls.return_value = macro_instance

    result = service.prepare_command("MACRO\n", 2, 2, wpos, mpos, "root", gcr, macro_cls=macro_cls)

    assert result["command"] == "$#\n"
    assert result["wait_tag_decoding"] is False
    assert result["total_lines_delta"] == 1
    assert service.macro_on is True
    assert service.macro_obj is macro_instance


def test_next_command_finishes_macro_when_no_more_lines():
    service = MacroService()
    service.macro_on = True
    service.macro_obj = MagicMock()
    service.macro_obj.get_next_line.return_value = None

    result = service.next_command({}, [], 0, 128)

    assert result["finished"] is True
    assert result["total_lines_delta"] == -1
    assert result["command"] is None
    assert service.macro_on is False
    assert service.macro_obj is None


def test_next_command_returns_next_macro_line_and_buffer_check():
    service = MacroService()
    service.macro_on = True
    service.macro_obj = MagicMock()
    service.macro_obj.get_next_line.return_value = "G1 X1\n"

    result = service.next_command({}, [], 10, 32)

    assert result["command"] == "G1 X1\n"
    assert result["finished"] is False
    assert result["buffer_available"] is True