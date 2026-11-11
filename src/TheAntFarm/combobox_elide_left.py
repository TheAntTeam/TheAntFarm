from PySide6.QtCore import Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QComboBox, QStyle, QStyleOptionComboBox, QStylePainter


class ComboBoxElideLeft(QComboBox):
    """Combo box that cuts a current text too long for it on the left, so its last part stays visible.

    The drop-down list still shows the full texts.
    """

    def displayed_text(self, option: QStyleOptionComboBox) -> str:
        """The current text as it fits the edit field of the box."""
        field = self.style().subControlRect(
            QStyle.ComplexControl.CC_ComboBox, option, QStyle.SubControl.SC_ComboBoxEditField, self
        )
        return self.fontMetrics().elidedText(option.currentText, Qt.TextElideMode.ElideLeft, field.width() - 2)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QStylePainter(self)
        option = QStyleOptionComboBox()
        self.initStyleOption(option)
        painter.drawComplexControl(QStyle.ComplexControl.CC_ComboBox, option)
        option.currentText = self.displayed_text(option)
        painter.drawControl(QStyle.ControlElement.CE_ComboBoxLabel, option)
