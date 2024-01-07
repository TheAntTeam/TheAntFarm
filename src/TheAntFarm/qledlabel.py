from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QResizeEvent


class QLedLabel(QLabel):

    grey_ss = "color: white;background-color: qlineargradient(spread:pad, x1:0.145, " \
              "y1:0.16, x2:1, y2:1, stop:0 rgba(200, 200, 200, 120), stop:1 rgba(220, 220, 220, 255)); "
    green_ss = "color: white;background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, " \
               "x2:1, y2:1, stop:0 rgba(20, 252, 7, 255), stop:1 rgba(25, 134, 5, 255));"
    red_ss = "color: white;background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16" \
             ", x2:0.92, y2:0.988636, stop:0 rgba(255, 12, 12, 255), stop:0.869347 rgba(103, 0, 0, 255));"
    orange_ss = "color: white;background-color: qlineargradient(spread:pad, x1:0.232, y1:0.272, " \
                "x2:0.98, y2:0.959773, stop:0 rgba(255, 113, 4, 255), stop:1 rgba(91, 41, 7, 255)) "
    blue_ss = "color: white;background-color: qlineargradient(spread:pad, x1:0.04, y1:0.0565909, " \
              "x2:0.799, y2:0.795, stop:0 rgba(203, 220, 255, 255), stop:0.41206 rgba(0, 115, 255, 255), stop:1 rgba(" \
              "0, 49, 109, 255)); "

    led_colors = {"grey": grey_ss, "green": green_ss, "red": red_ss, "orange": orange_ss, "blue": blue_ss }

    def __init__(self, parent):
        super(QLedLabel, self).__init__(parent)
        self.setMinimumSize(self.sizeHint())
        self.actual_color = "grey"
        self.set_led_color(self.actual_color)

    def set_led_color(self, state_color):
        """Set color of led with correct border-radius.
           Hypothesis: minimum height and width of the led are equals."""
        if state_color in self.led_colors:
            self.actual_color = state_color
            state_ss = "QLabel{ " + self.led_colors[state_color] + "border-radius: " + str(self.minimumHeight()/2) + \
                       "px;}"
            self.setStyleSheet(state_ss)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """On resize event make sure the border-radius resizes accordingly. """
        self.set_led_color(self.actual_color)
