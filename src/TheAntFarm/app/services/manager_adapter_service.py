from __future__ import annotations

import time
from typing import Any, Callable, Optional


class ManagerAdapterService:
    POLL_INTERVAL_MS = 120
    PROGRESS_INTERVAL_MS = 500

    @staticmethod
    def prepare_tx_payload(data: Any, decode_tag: Callable[[Any], Any]) -> Any:
        return decode_tag(data)

    @staticmethod
    def get_poll_payload() -> bytes:
        return b"?"

    @staticmethod
    def format_elapsed_time(start_time: Optional[float], now_time: Optional[float] = None) -> str:
        if start_time is None:
            return "00:00:00"
        now = time.time() if now_time is None else now_time
        elapsed_seconds = int(now - start_time)
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"