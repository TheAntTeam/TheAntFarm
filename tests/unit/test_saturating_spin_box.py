"""A typed number outside the range of the spin box is saturated to the nearest limit."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest


@pytest.fixture
def spin_box(qapp):
    from saturating_spin_box import SaturatingSpinBox

    box = SaturatingSpinBox()
    box.setRange(10, 200)
    box.setSuffix("%")
    box.setKeyboardTracking(False)
    box.setValue(100)
    box.changes = []
    box.valueChanged.connect(box.changes.append)
    yield box
    box.deleteLater()


def type_and_confirm(box, text):
    line_edit = box.lineEdit()
    line_edit.selectAll()
    QTest.keyClicks(line_edit, text)
    QTest.keyClick(line_edit, Qt.Key_Return)


@pytest.mark.parametrize(
    "text, value",
    [("250", 200), ("999", 200), ("5", 10), ("0", 10), ("150", 150), ("200", 200), ("10", 10)],
)
def test_the_typed_number_is_saturated_to_the_range(spin_box, text, value):
    type_and_confirm(spin_box, text)

    assert spin_box.value() == value
    assert spin_box.lineEdit().text() == f"{value}%"


def test_one_value_is_emitted_when_the_text_is_confirmed(spin_box):
    type_and_confirm(spin_box, "250")

    assert spin_box.changes == [200]


def test_the_digits_beyond_the_maximum_are_kept_while_typing(spin_box):
    line_edit = spin_box.lineEdit()
    line_edit.selectAll()

    QTest.keyClicks(line_edit, "250")

    assert line_edit.text() == "250%"
    assert spin_box.changes == []


def test_letters_are_still_refused(spin_box):
    line_edit = spin_box.lineEdit()
    line_edit.selectAll()

    QTest.keyClicks(line_edit, "1a5")

    assert line_edit.text() == "15%"


def test_the_arrows_stop_at_the_limits(spin_box):
    spin_box.setValue(199)

    spin_box.stepBy(5)

    assert spin_box.value() == 200
