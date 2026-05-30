from app.services.align_point_service import AlignPointService


def test_prepare_align_point_rejects_disconnected():
    result = AlignPointService.prepare_align_point(False, {}, [1.0, 2.0], False, (0.0, 0.0), (False, False))
    assert result == {"ok": False, "reason": "disconnected"}


def test_prepare_align_point_rejects_invalid_status_and_wpos():
    assert AlignPointService.prepare_align_point(True, None, [1.0, 2.0], False, (0.0, 0.0), (False, False)) == {
        "ok": False,
        "reason": "invalid_status",
    }
    assert AlignPointService.prepare_align_point(True, {"state": "Idle"}, [1.0, 2.0], False, (0.0, 0.0), (False, False)) == {
        "ok": False,
        "reason": "invalid_wpos",
    }


def test_prepare_align_point_applies_offset_and_flip():
    status = {"wpos": [10.0, 20.0, 0.0]}

    result = AlignPointService.prepare_align_point(
        connected=True,
        status=status,
        geometry_point=[2.0, -3.0],
        offset_flag=True,
        camera_offset_xy=(1.5, 2.5),
        flipping_view=(True, True),
    )

    assert result["ok"] is True
    assert result["geometry_point"] == [-2.0, 3.0]
    assert result["working_position_point"] == [8.5, 17.5]