from PySide6.QtWidgets import QComboBox
from PySide6 import QtCore


class ComboBoxFilterEnter(QComboBox):
    """Custom combobox class that handles Enter key events."""

    key_event_cb = QtCore.Signal(int, name='key_event')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.key_event_cb.emit(event.key())
            event.accept()
        else:
            super(ComboBoxFilterEnter, self).keyPressEvent(event)
