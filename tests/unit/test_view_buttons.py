"""The Top View and Bottom View buttons keep their natural width, at the right under the canvas (#108)."""

import pytest


@pytest.fixture
def ui(qapp):
    from PySide6.QtWidgets import QMainWindow
    from ui_the_ant_farm import Ui_MainWindow

    window = QMainWindow()
    form = Ui_MainWindow()
    form.setupUi(window)
    form.main_tab_widget.setCurrentWidget(form.view_tab)
    window.resize(1400, 900)
    window.show()
    qapp.processEvents()
    form.window = window
    yield form
    window.close()
    window.deleteLater()


def test_the_spacer_is_horizontal(ui):
    from PySide6.QtCore import Qt

    assert ui.horizontalSpacer.expandingDirections() == Qt.Orientation.Horizontal


@pytest.mark.parametrize("name", ["top_view_pb", "bottom_view_pb"])
def test_the_buttons_keep_their_natural_width(ui, name):
    button = getattr(ui, name)

    assert button.isVisible()
    assert button.width() == button.sizeHint().width()
    assert button.width() < ui.viewCanvasWidget.width() / 4


def test_the_buttons_are_at_the_right_under_the_canvas(ui):
    canvas = ui.viewCanvasWidget.geometry()
    top = ui.top_view_pb.geometry()
    bottom = ui.bottom_view_pb.geometry()

    assert top.right() < bottom.left()
    assert abs(bottom.right() - canvas.right()) <= 2
    assert top.top() > canvas.bottom()


def test_no_empty_band_under_the_canvas(ui):
    canvas = ui.viewCanvasWidget.geometry()
    button = ui.top_view_pb.geometry()
    spacing = ui.verticalLayout_9.spacing()

    assert button.top() - canvas.bottom() <= max(spacing, 0) + 2
    assert ui.verticalLayout_9.geometry().bottom() - button.bottom() <= 2
