from __future__ import annotations

from typing import Any, Callable, Dict, List


class FileSendService:
    def begin_send(self, streaming: Any, lines: List[str], buffered_size: int) -> Dict[str, Any]:
        streaming.start(lines, buffered_size=buffered_size)
        return {
            "has_content": bool(streaming.file_content),
            "total_lines": streaming.tot_lines,
        }

    def prepare_initial_command(self, streaming: Any, prepare_command: Callable[[str], str]) -> Dict[str, Any]:
        if not streaming.has_file_to_send():
            return {"command": None}

        cmd = prepare_command(streaming.current_line())
        if not streaming.can_buffer(cmd):
            return {"command": None}

        streaming.record_sent_command(cmd)
        streaming.advance_content_line()
        return {"command": cmd}

    @staticmethod
    def stop_send(streaming: Any, send_soft_reset: bool) -> Dict[str, Any]:
        streaming.stop()
        return {
            "reset_commands": [b"!", b"\030"] if send_soft_reset else [],
            "next_send_soft_reset": True,
        }