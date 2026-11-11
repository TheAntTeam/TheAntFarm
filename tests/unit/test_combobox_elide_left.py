"""A combo box that cuts a long current text on the left, so its last part stays visible."""

import pytest
from PySide6.QtWidgets import QComboBox, QStyleOptionComboBox

LONG_PORT = "/dev/cu.usbserial-A10KBJ8Z"
SHORT_PORT = "COM3"


@pytest.fixture
def box(qapp):
    from combobox_elide_left import ComboBoxElideLeft

    combo = ComboBoxElideLeft()
    combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
    combo.setMinimumContentsLength(8)
    combo.resize(combo.sizeHint())
    yield combo
    combo.deleteLater()


def displayed(combo) -> str:
    option = QStyleOptionComboBox()
    combo.initStyleOption(option)
    return combo.displayed_text(option)


class TestDisplayedText:
    def test_a_short_name_is_shown_whole(self, box):
        box.addItem(SHORT_PORT)

        assert displayed(box) == SHORT_PORT

    def test_a_long_name_keeps_its_last_part(self, box):
        box.addItem(LONG_PORT)

        shown = displayed(box)

        assert shown.startswith("…")
        assert len(shown) > 1
        assert LONG_PORT.endswith(shown[1:])

    def test_the_list_keeps_the_full_name(self, box):
        box.addItem(LONG_PORT)

        assert box.currentText() == LONG_PORT
        assert box.itemText(0) == LONG_PORT

    def test_the_box_is_painted(self, box):
        box.addItem(LONG_PORT)

        assert not box.grab().isNull()
