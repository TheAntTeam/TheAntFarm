"""Tests for the icons drawn in the colours of the theme."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import Mock

import pytest
from PySide6.QtCore import QFile
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QToolButton

APP_DIR = Path(__file__).parents[2] / "src" / "TheAntFarm"
WHITE = QColor(255, 255, 255)
RED = QColor(255, 0, 0)


@pytest.fixture
def resources(qapp):
    import app_resources_rc  # noqa: F401  registers the :/resources paths


@pytest.fixture
def style_manager(resources):
    from style_manager import StyleManager

    return StyleManager(qapp_mock())


def qapp_mock():
    return Mock()


def icon_path(name):
    from style_manager import ICON_RESOURCE_PATH

    return ICON_RESOURCE_PATH.format(name)


def colors_of(pixmap):
    """The colours of the visible pixels of ``pixmap``."""
    image = pixmap.toImage()
    colors = set()
    for x in range(0, image.width(), 4):
        for y in range(0, image.height(), 4):
            pixel = image.pixelColor(x, y)
            if pixel.alpha() == 255:
                colors.add(pixel.name())
    return colors


def icon_colors(icon, mode=QIcon.Normal):
    return colors_of(icon.pixmap(64, 64, mode))


class TestIconManager:
    def test_every_visible_pixel_gets_the_colour(self, resources):
        from style_manager import IconManager

        pixmap = IconManager().make_pixmap(icon_path("home"), RED)

        assert colors_of(pixmap) == {RED.name()}

    def test_transparent_pixels_stay_transparent(self, resources):
        from style_manager import IconManager

        image = IconManager().make_pixmap(icon_path("home"), RED).toImage()

        assert image.pixelColor(0, 0).alpha() == 0

    def test_icons_are_rendered_large_enough_to_stay_sharp(self, resources):
        from style_manager import IconManager

        pixmap = IconManager().make_pixmap(icon_path("refresh"), RED)

        assert max(pixmap.width(), pixmap.height()) == IconManager.RENDER_SIZE

    def test_pixmaps_are_cached_per_colour(self, resources):
        from style_manager import IconManager

        icon_manager = IconManager()
        first = icon_manager.make_pixmap(icon_path("home"), RED)

        assert icon_manager.make_pixmap(icon_path("home"), QColor(RED)) is first
        assert icon_manager.make_pixmap(icon_path("home"), WHITE) is not first

    def test_missing_icon_gives_an_empty_pixmap(self, resources, caplog):
        from style_manager import IconManager

        pixmap = IconManager().make_pixmap(icon_path("no-such-icon"), RED)

        assert pixmap.isNull()
        assert "no-such-icon" in caplog.text


class TestThemedIcons:
    def test_icon_has_the_theme_colour_and_a_disabled_colour(self, style_manager):
        icon = style_manager.themed_icon("home")

        assert icon_colors(icon) == {style_manager.current_icon_color.name()}
        assert icon_colors(icon, QIcon.Disabled) == {style_manager.current_disabled_color.name()}

    def test_widget_follows_the_theme(self, style_manager):
        button = QToolButton()
        style_manager.set_themed_icon(button, "home")

        style_manager.set_light_palette()
        light = icon_colors(button.icon())
        style_manager.set_dark_palette()
        dark = icon_colors(button.icon())

        assert light == {style_manager.LIGHT_ICON_COLOR.name()}
        assert dark == {style_manager.DARK_ICON_COLOR.name()}

    def test_new_icon_of_a_widget_replaces_the_old_one_after_a_theme_change(self, style_manager):
        button = QToolButton()
        style_manager.set_themed_icon(button, "pause-multimedia-big-gross-symbol-lines")
        style_manager.set_themed_icon(button, "play-and-pause-button")

        style_manager.set_light_palette()

        expected = style_manager.themed_icon("play-and-pause-button").pixmap(64, 64).toImage()
        assert button.icon().pixmap(64, 64).toImage() == expected

    def test_theme_change_is_signalled(self, style_manager):
        received = []
        style_manager.theme_changed.connect(lambda icon, disabled: received.append((icon.name(), disabled.name())))

        style_manager.set_light_palette()

        assert received == [(style_manager.LIGHT_ICON_COLOR.name(), style_manager.LIGHT_DISABLED_ICON_COLOR.name())]


class TestThemedIconsOfTheWindow:
    """The themed icons of the UI manager exist, and so do the icons the .ui file uses."""

    @pytest.fixture
    def ui_widgets(self):
        root = ET.parse(APP_DIR / "the_ant_farm.ui").getroot()
        return {widget.get("name") for widget in root.iter("widget")}

    def test_every_themed_widget_is_in_the_ui_file(self, ui_widgets):
        from ui_manager.ui_manager import UiManager

        assert set(UiManager.THEMED_ICONS) <= ui_widgets

    def test_every_themed_icon_is_a_resource(self, resources):
        from ui_manager.ui_manager import UiManager

        names = set(UiManager.THEMED_ICONS.values()) | {"play-and-pause-button"}

        assert [name for name in sorted(names) if not QFile.exists(icon_path(name))] == []

    def test_every_icon_of_the_ui_file_is_a_resource(self, resources):
        text = (APP_DIR / "the_ant_farm.ui").read_text(encoding="utf-8")
        paths = set(re.findall(r":/resources/resources/icons/[\w.-]+", text))

        assert paths
        assert [path for path in sorted(paths) if not QFile.exists(path)] == []


class TestPauseResumeIcon:
    def _tab(self, style_manager):
        from ui_manager.ui_control_tab import UiControlTab

        tab = UiControlTab.__new__(UiControlTab)
        tab.ui = Mock()
        tab.style_manager = style_manager
        return tab

    def test_hold_icon_is_drawn_in_the_theme(self):
        style_manager = Mock()
        tab = self._tab(style_manager)

        tab._set_pause_resume_icon("play-and-pause-button")

        style_manager.set_themed_icon.assert_called_once_with(tab.ui.pause_resume_tb, "play-and-pause-button")

    def test_without_a_style_manager_the_plain_icon_is_used(self, resources):
        tab = self._tab(None)

        tab._set_pause_resume_icon("play-and-pause-button")

        icon = tab.ui.pause_resume_tb.setIcon.call_args.args[0]
        assert not icon.isNull()
