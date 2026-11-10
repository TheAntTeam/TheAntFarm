"""The fixed font sizes of the window are scaled on macOS, where a point is drawn smaller than on Windows."""

from unittest.mock import patch

import pytest
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QMainWindow, QWidget


@pytest.fixture
def widgets(qapp):
    parent = QWidget()
    sized = QLabel("sized", parent)
    font = QFont()
    font.setPointSize(8)
    sized.setFont(font)
    bold = QLabel("bold", parent)
    font = QFont()
    font.setBold(True)
    bold.setFont(font)
    plain = QLabel("plain", parent)
    yield parent, sized, bold, plain
    parent.deleteLater()


class TestScaleFixedFontSizes:
    def test_a_size_set_on_the_widget_is_scaled(self, widgets):
        from style_manager import StyleManager

        parent, sized, _, _ = widgets

        StyleManager.scale_fixed_font_sizes(parent, 2)

        assert sized.font().pointSizeF() == 16

    def test_inherited_sizes_are_left_alone(self, widgets):
        from style_manager import StyleManager

        parent, _, bold, plain = widgets
        before = plain.font().pointSizeF()

        StyleManager.scale_fixed_font_sizes(parent, 2)

        assert plain.font().pointSizeF() == before
        assert bold.font().pointSizeF() == before
        assert bold.font().bold()

    def test_inherited_sizes_follow_a_scaled_parent(self, widgets):
        from style_manager import StyleManager

        parent, _, _, plain = widgets
        font = QFont()
        font.setPointSize(10)
        parent.setFont(font)

        StyleManager.scale_fixed_font_sizes(parent, 2)

        assert parent.font().pointSizeF() == 20
        assert plain.font().pointSizeF() == 20

    def test_pixel_sizes_are_left_alone(self, qapp):
        from style_manager import StyleManager

        label = QLabel("pixels")
        font = QFont()
        font.setPixelSize(12)
        label.setFont(font)

        StyleManager.scale_fixed_font_sizes(label, 2)

        assert label.font().pixelSize() == 12


class TestFontSizesOfTheWindow:
    """On the real window: the sizes chosen on Windows keep their size relative to the default text on macOS."""

    @pytest.fixture
    def window(self, qapp):
        from ui_the_ant_farm import Ui_MainWindow

        window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        yield window, ui
        window.deleteLater()

    def test_fixed_sizes_are_scaled_for_macos(self, window):
        from style_manager import StyleManager

        main_window, ui = window
        default_size = ui.homing_tb.font().pointSizeF()

        StyleManager.scale_fixed_font_sizes(main_window, StyleManager.MACOS_FONT_SCALE)

        assert ui.xy_mul_10_pb.font().pointSizeF() == pytest.approx(8 * 96 / 72)
        assert ui.status_l.font().pointSizeF() == pytest.approx(10 * 96 / 72)
        assert ui.layer_colors_section_la.font().pointSizeF() == pytest.approx(12 * 96 / 72)
        assert ui.homing_tb.font().pointSizeF() == default_size

    def test_the_status_uses_the_default_font_family(self, window):
        _, ui = window

        assert ui.status_l.font().family() == QFont().family()


class TestMainWindowFontSizes:
    """The main window scales its fixed font sizes when it starts on macOS, and only there."""

    @staticmethod
    def _main_window(system):
        from TheAntFarm.the_ant_farm import MainWindow

        managers = ("SettingsHandler", "ControllerWorker", "SerialWorker", "UiManager", "QThread")
        patches = [patch(f"TheAntFarm.the_ant_farm.{name}") for name in managers]
        for started in patches:
            started.start()
        try:
            with patch("TheAntFarm.the_ant_farm.platform.system", return_value=system):
                return MainWindow()
        finally:
            for started in patches:
                started.stop()

    def test_fixed_sizes_are_scaled_on_macos(self, qapp):
        window = self._main_window("Darwin")

        assert window.ui.xy_mul_10_pb.font().pointSizeF() == pytest.approx(8 * 96 / 72)
        window.deleteLater()

    @pytest.mark.parametrize("system", ["Windows", "Linux"])
    def test_fixed_sizes_are_kept_elsewhere(self, qapp, system):
        window = self._main_window(system)

        assert window.ui.xy_mul_10_pb.font().pointSizeF() == 8
        window.deleteLater()
