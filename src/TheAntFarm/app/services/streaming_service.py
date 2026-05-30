from __future__ import annotations

from typing import List, Optional


class StreamingService:
    def __init__(self, remote_rx_buffer_max_size: int = 128) -> None:
        self.remote_rx_buffer_max_size = remote_rx_buffer_max_size
        self.stop()

    def start(self, lines: List[str], buffered_size: int = 0) -> None:
        self.file_content = lines
        self.file_progress = 0.0
        self.cmds_to_ack = 0
        self.sent_lines = 0
        self.content_line = 0
        self.ack_lines = 0
        self.tot_lines = len(lines)
        self.eof_wait_for_idle = False
        self.wait_tag_decoding = False
        self.buffered_cmds = []
        self.buffered_size = buffered_size
        self.sending_file = bool(lines)

    def stop(self) -> None:
        self.file_content: List[str] = []
        self.sending_file = False
        self.content_line = 0
        self.file_progress = 0.0
        self.sent_lines = 0
        self.ack_lines = 0
        self.tot_lines = 0
        self.buffered_cmds: List[str] = []
        self.buffered_size = 0
        self.cmds_to_ack = 0
        self.eof_wait_for_idle = False
        self.wait_tag_decoding = False

    def has_file_to_send(self) -> bool:
        return self.content_line < self.tot_lines

    def current_line(self) -> Optional[str]:
        if self.has_file_to_send():
            return self.file_content[self.content_line]
        return None

    def advance_content_line(self) -> None:
        if self.has_file_to_send():
            self.content_line += 1

    def can_buffer(self, cmd: str) -> bool:
        return (self.buffered_size + len(cmd)) < self.remote_rx_buffer_max_size

    def record_sent_command(self, cmd: str) -> None:
        self.buffered_cmds.append(cmd)
        self.buffered_size += len(cmd)
        self.sent_lines += 1
        self.cmds_to_ack += 1

    def acknowledge_command(self) -> bool:
        if not self.sending_file or self.cmds_to_ack <= 0 or not self.buffered_cmds:
            return False
        self.cmds_to_ack -= 1
        self.ack_lines += 1
        self.buffered_size -= len(self.buffered_cmds[0])
        self.buffered_cmds.pop(0)
        self.file_progress = self.progress_percent()
        return True

    def progress_percent(self) -> float:
        if self.tot_lines <= 0:
            return 0.0
        return (self.content_line / self.tot_lines) * 100

    def finish_file(self) -> None:
        self.eof_wait_for_idle = True
        self.sending_file = False
        self.file_progress = self.progress_percent()