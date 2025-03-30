from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QWheelEvent
from PySide6.QtCore import Signal


class QCameraLabel(QLabel):
    mouse_wheel_up_or_down_s = Signal(int)

    def __init__(self, parent):
        super(QCameraLabel, self).__init__(parent)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().x() > 0 or event.angleDelta().y() > 0:
            self.mouse_wheel_up_or_down_s.emit(1)
        elif event.angleDelta().x() < 0 or event.angleDelta().y() < 0:
            self.mouse_wheel_up_or_down_s.emit(-1)
        else:
            pass  # todo: this event should never be catched, an error could be raised
