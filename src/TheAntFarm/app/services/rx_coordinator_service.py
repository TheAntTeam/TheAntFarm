from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Tuple

from app.services.rx_dispatch_service import RxDispatchService
from app.services.transport_coordinator_service import TransportCoordinatorService


class RxCoordinatorService:
    def __init__(self) -> None:
        self._dispatch = RxDispatchService()
        self._transport = TransportCoordinatorService()

    def process_line(
        self,
        line_kind: str,
        element: str,
        *,
        dro_status_updated: bool = False,
        status_payload: Any = None,
        square_flags: Optional[Tuple[bool, bool, bool, bool]] = None,
        streaming: Any = None,
        macro: Any = None,
        prepare_file_command: Optional[Callable[[str], str]] = None,
        workspace_parameters: Any = None,
        probe_data: Any = None,
    ) -> Dict[str, Any]:
        if line_kind == "status":
            result = self._dispatch.handle_status(status_payload, dro_status_updated)
            result["kind"] = "status"
            return result

        if line_kind == "square":
            ack_prb_flag, ack_abl_flag, send_next, other_cmd_flag = square_flags or (False, False, False, False)
            result = self._dispatch.handle_square(
                element,
                ack_prb_flag,
                ack_abl_flag,
                send_next,
                other_cmd_flag,
            )
            result["kind"] = "square"
            return result

        if line_kind == "ok":
            result = self._transport.process_ok_ack(
                streaming,
                macro,
                prepare_file_command,
                workspace_parameters,
                probe_data,
            )
            result["kind"] = "ok"
            return result

        if line_kind == "error":
            return {"kind": "error", "console_text": element}

        return {"kind": "console", "console_text": element}