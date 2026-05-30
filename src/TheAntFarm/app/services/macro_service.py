from __future__ import annotations

from typing import Any, Dict, Optional, Type

from shape_core.gcode_manager import GCodeMacro


class MacroService:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.macro_on = False
        self.macro_obj = None

    def prepare_command(
        self,
        cmd_to_send: str,
        ack_lines: int,
        sent_lines: int,
        wpos: Any,
        mpos: Any,
        local_path: str,
        gcr: Any,
        macro_cls: Type[GCodeMacro] = GCodeMacro,
    ) -> Dict[str, Any]:
        result = {
            "command": cmd_to_send,
            "wait_tag_decoding": False,
            "total_lines_delta": 0,
        }

        if not gcr.is_macro(cmd_to_send):
            return result

        macro_type = cmd_to_send.strip()
        if ack_lines != sent_lines:
            result["wait_tag_decoding"] = True
            return result

        freeze_dro = {
            "WPO": wpos.copy(),
            "MPO": mpos.copy(),
        }
        self.macro_obj = macro_cls(freeze_dro, macro_type, gcr, local_path=local_path)
        self.macro_on = True
        result["command"] = "$#\n"
        result["total_lines_delta"] = 1
        return result

    def next_command(self, wsp: Any, probe_data: Any, buffered_size: int, remote_rx_buffer_max_size: int) -> Dict[str, Any]:
        result = {
            "command": None,
            "finished": False,
            "wait_tag_decoding": False,
            "total_lines_delta": 0,
            "buffer_available": False,
        }
        if not self.macro_on or self.macro_obj is None:
            return result

        cmd_to_send = self.macro_obj.get_next_line(wsp, probe_data)
        if cmd_to_send is None:
            self.reset()
            result["finished"] = True
            result["total_lines_delta"] = -1
            return result

        result["command"] = cmd_to_send
        result["buffer_available"] = (buffered_size + len(cmd_to_send)) < remote_rx_buffer_max_size
        return result