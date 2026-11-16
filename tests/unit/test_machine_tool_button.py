"""An icon button of the machine column that shrinks its icon with its height."""

import pytest
from PySide6.QtCore import QSize


@pytest.fixture
def button(qapp):
    from machine_tool_button import MachineToolButton

    widget = MachineToolButton()
    widget.setIconSize(QSize(64, 64))
    widget.setMinimumSize(120, 52)
    yield widget
    widget.deleteLater()


def test_it_asks_for_the_height_of_the_full_icon_even_when_short(button):
    button.resize(120, 52)

    assert button.sizeHint().height() >= 80


@pytest.mark.parametrize("height, side", [(52, 36), (60, 44), (80, 64), (200, 64)])
def test_the_icon_follows_the_height(button, height, side):
    button.resize(120, height)
    button.show()

    assert button.iconSize() == QSize(side, side)


@pytest.mark.parametrize("height, side", [(52, 44), (80, 72), (120, 72)])
def test_a_larger_icon_keeps_its_size_at_full_height(button, height, side):
    button.setIconSize(QSize(72, 72))
    button.resize(120, height)
    button.show()

    assert button.iconSize() == QSize(side, side)
    assert button.full_icon_side() == 72


def test_the_icon_never_gets_smaller_than_the_minimum(button):
    button.setMinimumSize(0, 0)
    button.resize(120, 10)
    button.show()

    assert button.iconSize() == QSize(16, 16)
