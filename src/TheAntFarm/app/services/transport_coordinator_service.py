from __future__ import annotations

from typing import Any, Callable, Dict


class TransportCoordinatorService:
    def process_ok_ack(
        self,
        streaming: Any,
        macro: Any,
        prepare_file_command: Callable[[str], str],
        workspace_parameters: Any,
        probe_data: Any,
    ) -> Dict[str, Any]:
        result = {
            "acknowledged": False,
            "send_command": None,
            "finished_file": False,
            "file_progress": 0.0,
        }

        if not streaming.acknowledge_command():
            return result

        result["acknowledged"] = True
        cmd_to_send = None
        buff_available = False

        if macro.macro_on:
            macro_step = macro.next_command(
                workspace_parameters,
                probe_data,
                streaming.buffered_size,
                streaming.remote_rx_buffer_max_size,
            )
            streaming.wait_tag_decoding = macro_step["wait_tag_decoding"]
            streaming.tot_lines += macro_step["total_lines_delta"]
            cmd_to_send = macro_step["command"]
            buff_available = macro_step["buffer_available"]

        end_of_file = streaming.content_line >= streaming.tot_lines
        if not end_of_file:
            if not macro.macro_on:
                current_line = streaming.current_line()
                if current_line is not None:
                    cmd_to_send = prepare_file_command(current_line)
                    streaming.advance_content_line()
            if cmd_to_send is not None:
                buff_available = streaming.can_buffer(cmd_to_send)
        else:
            streaming.wait_tag_decoding = False
            buff_available = False

        if not end_of_file and buff_available and not streaming.wait_tag_decoding and cmd_to_send is not None:
            streaming.record_sent_command(cmd_to_send)
            result["send_command"] = cmd_to_send

        if end_of_file:
            streaming.finish_file()
            result["finished_file"] = True

        result["file_progress"] = streaming.file_progress
        return result