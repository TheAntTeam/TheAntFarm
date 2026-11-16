from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QToolButton, QWidget


class MachineToolButton(QToolButton):
    """Icon button of the machine column that may get shorter than its full height, shrinking its icon with it.

    It always asks for its full height, so a tall window keeps the buttons as designed and only a short one makes
    the buttons, not the widgets around them, give way. The icon loses as many pixels as the button is below its
    full height.
    """

    FULL_HEIGHT = 80
    ICON_MIN = 16

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._full_icon_side = super().iconSize().height()

    def setIconSize(self, size: QSize) -> None:
        """Set the icon size of the full height; the shown icon is smaller while the button is shorter."""
        self._full_icon_side = max(size.width(), size.height())
        self._fit_icon()

    def full_icon_side(self) -> int:
        return self._full_icon_side

    def sizeHint(self) -> QSize:
        hint = super().sizeHint()
        return QSize(hint.width(), max(hint.height(), self.FULL_HEIGHT))

    def icon_side(self) -> int:
        """The side of the icon that fits the current height."""
        missing = max(0, self.FULL_HEIGHT - self.height())
        return max(self.ICON_MIN, min(self._full_icon_side, self._full_icon_side - missing))

    def _fit_icon(self) -> None:
        side = self.icon_side()
        if super().iconSize() != QSize(side, side):
            super().setIconSize(QSize(side, side))

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._fit_icon()
        super().resizeEvent(event)
