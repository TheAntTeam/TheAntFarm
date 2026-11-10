"""Every layer has a colour for the dark theme and one for the light theme."""

import configparser
from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QColor

from TheAntFarm.settings_manager.settings_app import AppSettingsHandler
from TheAntFarm.shape_core.visual_manager import VisualLayer


def lum(hex_color):
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first, second):
    high, low = sorted((lum(first), lum(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


@pytest.fixture
def app_settings(tmp_path):
    config_folder = tmp_path / "configurations"
    config_folder.mkdir()
    main_window = MagicMock()
    main_window.local_path = str(tmp_path)
    return AppSettingsHandler(str(config_folder), main_window)


def write_layers(app_settings, **values):
    config = configparser.ConfigParser()
    config["LAYERS"] = values
    with open(app_settings.app_config_path, "w") as config_file:
        config.write(config_file)


class TestDefaultLayerColors:
    @pytest.mark.parametrize("tag", AppSettingsHandler.LAYER_TAGS)
    def test_defaults_are_readable_on_their_canvas(self, tag):
        assert contrast(AppSettingsHandler.LAYER_COLOR_DEFAULTS[tag], VisualLayer.BACKGROUND_COLORS[True]) >= 3
        assert contrast(AppSettingsHandler.LAYER_COLOR_LIGHT_DEFAULTS[tag], VisualLayer.BACKGROUND_COLORS[False]) >= 3

    def test_a_new_configuration_has_both_sets(self, app_settings):
        assert dict(app_settings.layer_color) == AppSettingsHandler.LAYER_COLOR_DEFAULTS
        assert dict(app_settings.layer_color_light) == AppSettingsHandler.LAYER_COLOR_LIGHT_DEFAULTS
        assert app_settings.layer_colors_of("profile") == ("#FF8FAB", "#C2185B")


class TestReadLayerColors:
    def test_both_colours_are_read(self, app_settings):
        write_layers(app_settings, top_layer_color="#111111", top_layer_color_light="#222222")

        app_settings.read_all_app_settings()

        assert app_settings.layer_colors_of("top") == ("#111111", "#222222")

    def test_a_configuration_without_light_colours_gets_the_light_defaults(self, app_settings):
        write_layers(app_settings, top_layer_color="#111111")

        app_settings.read_all_app_settings()

        assert app_settings.layer_colors_of("top") == ("#111111", AppSettingsHandler.LAYER_COLOR_LIGHT_DEFAULTS["top"])

    @pytest.mark.parametrize("tag", ["profile", "nc_top", "nc_bottom"])
    def test_a_former_dark_default_is_replaced(self, app_settings, tag):
        old = AppSettingsHandler.OLD_LAYER_COLOR_DEFAULTS[tag].lower()
        write_layers(app_settings, **{f"{tag}_layer_color": old})

        app_settings.read_all_app_settings()

        assert app_settings.layer_color[tag] == AppSettingsHandler.LAYER_COLOR_DEFAULTS[tag]

    def test_a_colour_chosen_by_the_user_is_kept(self, app_settings):
        write_layers(app_settings, profile_layer_color="#123456")

        app_settings.read_all_app_settings()

        assert app_settings.layer_color["profile"] == "#123456"


class TestWriteLayerColors:
    def test_both_colours_are_written(self, app_settings):
        app_settings.layer_color["drill"] = "#010101"
        app_settings.layer_color_light["drill"] = "#020202"

        app_settings.write_all_app_settings()

        config = configparser.ConfigParser()
        config.read(app_settings.app_config_path)
        assert config["LAYERS"]["drill_layer_color"] == "#010101"
        assert config["LAYERS"]["drill_layer_color_light"] == "#020202"


class TestLayerMeshColors:
    """A layer with a (dark, light) colour pair is drawn in the colour of the background and follows it."""

    @staticmethod
    def _layer(dark=True):
        layer = object.__new__(VisualLayer)
        layer.canvas = MagicMock()
        layer.paths = {}
        layer.line_colors = {}
        layer.meshes = {}
        layer.mesh_colors = {}
        layer.meshes_geom = {}
        layer.dark_background = dark
        return layer

    @staticmethod
    def _mesh(layer, tag, color):
        mesh = MagicMock()
        mesh.mesh_data.n_faces = 2
        layer.meshes[tag] = mesh
        layer.mesh_colors[tag] = color
        return mesh

    @pytest.mark.parametrize("dark, expected", [(True, "#ff0000"), (False, "#0000ff")])
    def test_a_pair_gives_the_colour_of_the_background(self, dark, expected):
        layer = self._layer(dark)

        assert layer._resolve_layer_color(("#ff0000", "#0000ff")) == expected

    def test_a_single_colour_is_kept(self):
        assert self._layer()._resolve_layer_color("yellow") == "yellow"

    def test_a_new_layer_is_drawn_in_the_colour_of_the_background(self):
        layer = self._layer(dark=False)
        layer.canvas.view.camera.up = "+z"
        layer.create_mesh = MagicMock()
        layer._rebuild_index = MagicMock()

        layer.add_layer("top", [], ("#ff0000", "#0000ff"))

        assert layer.create_mesh.call_args.args[2] == "#0000ff"
        assert layer.mesh_colors["top"] == ("#ff0000", "#0000ff")

    def test_switching_theme_recolours_the_layers_with_a_pair(self):
        layer = self._layer()
        paired = self._mesh(layer, "top", ("#ff0000", "#0000ff"))
        single = self._mesh(layer, "selected", "yellow")

        layer.set_dark_background(False)

        colors = paired.mesh_data.set_face_colors.call_args.args[0]
        assert colors.shape == (2, 4)
        assert QColor.fromRgbF(*colors[0]).name() == "#0000ff"
        paired.mesh_data_changed.assert_called_once()
        single.mesh_data.set_face_colors.assert_not_called()

    def test_a_removed_layer_forgets_its_colours(self):
        layer = self._layer()
        self._mesh(layer, "top", ("#ff0000", "#0000ff"))
        layer.meshes_geom["top"] = []
        layer._rebuild_index = MagicMock()

        layer.remove_layer("top")

        assert "top" not in layer.mesh_colors


class TestPointerColors:
    """The tool position is drawn in a colour readable on the canvas of each theme, and follows the theme."""

    @pytest.mark.parametrize("dark", [True, False])
    def test_the_pointer_is_readable_on_its_canvas(self, dark):
        color = QColor(VisualLayer.POINTER_COLOR[0 if dark else 1]).name()

        assert contrast(color, VisualLayer.BACKGROUND_COLORS[dark]) >= 3

    def test_a_line_with_a_pair_gets_the_colour_of_the_background(self):
        layer = TestLayerMeshColors._layer(dark=False)

        assert layer._resolve_colors([("#ff0000", "#0000ff"), "red", layer.FOREGROUND]) == ["#0000ff", "red", "black"]

    def test_switching_theme_recolours_a_line_with_a_pair(self):
        layer = TestLayerMeshColors._layer()
        paired, single = MagicMock(), MagicMock()
        layer.paths = {"pointer": [paired], "other": [single]}
        layer.line_colors = {id(paired): [("#ff0000", "#0000ff")] * 3, id(single): ["red"] * 3}

        layer.set_dark_background(False)

        paired.set_data.assert_called_once_with(color=["#0000ff"] * 3)
        single.set_data.assert_not_called()


class TestTabsDrawLayersWithBothColours:
    """The View and Align tabs give the canvas the (dark, light) colours of the loaded layer."""

    def test_view_tab(self):
        from TheAntFarm.ui_manager.ui_view_load_layer_tab import UiViewLoadLayerTab

        tab = UiViewLoadLayerTab.__new__(UiViewLoadLayerTab)
        tab.vis_layer = MagicMock()
        tab.app_settings = MagicMock()
        tab.app_settings.layer_colors_of.return_value = ("#ff0000", "#0000ff")
        tab.layers_te = {"top": MagicMock()}

        tab.visualize_new_layer(["geometry"], "top", "top.gbr", False)

        tab.app_settings.layer_colors_of.assert_called_once_with("top")
        tab.vis_layer.add_layer.assert_called_once_with("top", "geometry", ("#ff0000", "#0000ff"), False)

    def test_align_tab(self):
        from TheAntFarm.ui_manager.ui_align_tab import UiAlignTab

        tab = UiAlignTab.__new__(UiAlignTab)
        tab.vis_align_layer = MagicMock()
        tab.app_settings = MagicMock()
        tab.app_settings.layer_colors_of.return_value = ("#ff0000", "#0000ff")

        tab.visualize_new_align_layer(["geometry"], "drill", "holes.drl", True)

        tab.vis_align_layer.add_layer.assert_called_once_with("drill", "geometry", ("#ff0000", "#0000ff"), True)
