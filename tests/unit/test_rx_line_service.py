from app.services.rx_line_service import RxLineService


def test_classify_status_line():
    service = RxLineService()
    assert service.classify("<Idle|MPos:1.0,2.0,3.0>") == "status"


def test_classify_square_line():
    service = RxLineService()
    assert service.classify("[PRB:1.0,2.0,3.0:1]") == "square"


def test_classify_ok_line():
    service = RxLineService()
    assert service.classify("ok") == "ok"


def test_classify_error_line():
    service = RxLineService()
    assert service.classify("error:2") == "error"


def test_classify_console_line():
    service = RxLineService()
    assert service.classify("Grbl 1.1h ['$' for help]") == "console"


def test_classify_empty_line():
    service = RxLineService()
    assert service.classify("") == "empty"