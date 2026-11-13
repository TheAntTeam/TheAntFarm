from typing import Tuple

from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QAbstractSpinBox, QSpinBox


class SaturatingSpinBox(QSpinBox):
    """Spin box that accepts any typed number and saturates it to its range when the text is confirmed.

    A plain spin box refuses the key that takes the text above the maximum, so typing 250 in a box that
    ends at 200 leaves 25.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)

    def _number_text(self, text: str) -> str:
        if self.prefix() and text.startswith(self.prefix()):
            text = text[len(self.prefix()) :]
        if self.suffix() and text.endswith(self.suffix()):
            text = text[: -len(self.suffix())]
        return text.strip()

    def validate(self, text: str, pos: int) -> Tuple[QValidator.State, str, int]:
        number = self._number_text(text)
        if number.isdigit() and int(number) > self.maximum():
            return QValidator.State.Intermediate, text, pos
        return super().validate(text, pos)

    def fixup(self, text: str) -> str:
        number = self._number_text(text)
        if number.isdigit():
            value = min(max(int(number), self.minimum()), self.maximum())
            return self.prefix() + str(value) + self.suffix()
        return super().fixup(text)
