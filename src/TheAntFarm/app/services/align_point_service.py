from __future__ import annotations

from typing import Any, Dict, Sequence, Tuple


class AlignPointService:
    @staticmethod
    def prepare_align_point(
        connected: bool,
        status: Any,
        geometry_point: Sequence[float],
        offset_flag: bool,
        camera_offset_xy: Tuple[float, float],
        flipping_view: Tuple[bool, bool],
    ) -> Dict[str, Any]:
        if not connected:
            return {"ok": False, "reason": "disconnected"}
        if not status:
            return {"ok": False, "reason": "invalid_status"}
        if "wpos" not in status:
            return {"ok": False, "reason": "invalid_wpos"}

        wpos = status["wpos"]
        working_position_point = [wpos[0], wpos[1]]
        if offset_flag:
            working_position_point[0] -= camera_offset_xy[0]
            working_position_point[1] -= camera_offset_xy[1]

        geom = [geometry_point[0], geometry_point[1]]
        if flipping_view[0]:
            geom[0] *= -1.0
        if flipping_view[1]:
            geom[1] *= -1.0

        return {
            "ok": True,
            "geometry_point": geom,
            "working_position_point": working_position_point,
        }