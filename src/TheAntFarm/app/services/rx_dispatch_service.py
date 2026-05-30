from __future__ import annotations

from typing import Any, Dict


class RxDispatchService:
    @staticmethod
    def handle_status(status_payload: Any, dro_status_updated: bool) -> Dict[str, Any]:
        return {
            "status_payload": status_payload,
            "mark_dro_updated": not dro_status_updated,
            "check_eof_and_idle": True,
        }

    @staticmethod
    def handle_square(
        element: str,
        ack_prb_flag: bool,
        ack_abl_flag: bool,
        send_next: bool,
        other_cmd_flag: bool,
    ) -> Dict[str, Any]:
        return {
            "touched_probe": ack_prb_flag,
            "ack_probe": ack_prb_flag,
            "ack_auto_bed_levelling": ack_abl_flag,
            "send_next_abl": send_next,
            "console_text": element if other_cmd_flag and element else None,
        }