from __future__ import annotations

import re


class RxLineService:
    STATUS_PATTERN = re.compile(r"^<.*>\s*$")
    SQUARE_PATTERN = re.compile(r"^\[.*\]\s*$")
    OK_PATTERN = re.compile(r"^ok\s*$", re.IGNORECASE)

    def classify(self, element: str) -> str:
        if not element:
            return "empty"
        if self.STATUS_PATTERN.match(element):
            return "status"
        if self.SQUARE_PATTERN.match(element):
            return "square"
        if self.OK_PATTERN.match(element):
            return "ok"
        if "error" in element.lower():
            return "error"
        return "console"