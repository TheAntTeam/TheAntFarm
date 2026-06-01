from PySide6.QtCore import QByteArray, QFile, QIODevice, QObject, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPalette, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QStyleFactory, QWidgetAction


class IconManager:
    def __init__(self) -> None:
        self._cache: dict[str, QIcon] = {}

    def make_icon(self, resource_path: str, color: QColor) -> QIcon:
        cache_key = f"{resource_path}:{color.name()}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        pixmap = self._render_colored(resource_path, color)
        icon = QIcon(pixmap)
        self._cache[cache_key] = icon
        return icon

    def clear_cache(self) -> None:
        self._cache.clear()

    @staticmethod
    def _render_colored(path: str, color: QColor) -> QPixmap:
        f = QFile(path)
        f.open(QIODevice.ReadOnly)
        data = QByteArray(f.readAll())
        f.close()
        renderer = QSvgRenderer(data)
        size = renderer.defaultSize()
        if size.isNull() or size.isEmpty():
            size = QPixmap(512, 512).size()
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pixmap


class StyleManager(QObject):
    """Style manager class"""

    theme_changed = Signal(QColor, QColor)  # icon_color, disabled_color

    def __init__(self, app_ptr):
        super().__init__()
        self.app_ptr = app_ptr
        self.native_styles = QStyleFactory.keys()
        self.default_palette = QPalette()
        self.default_style = "Fusion"
        self.dark_palette_action = None
        self.light_palette_action = None
        self.icon_man = IconManager()
        self.current_icon_color = Qt.white
        self.current_disabled_color = QColor(128, 128, 128)

    def list_styles(self):
        """List the available application styles for the current OS."""
        return self.native_styles

    def add_styles_to_menu(self, main_win, menu_style, style_group, palette_group):
        """Add all the available styles to the Menu styles in the bar menu in a mutually exclusive action group."""
        style_list = self.list_styles()
        if style_list:
            fusion_list = [style_list.index(x) for x in style_list if x.lower() == "fusion"]
            if fusion_list:
                self.default_style = style_list[fusion_list[0]]
            else:
                self.default_style = style_list[0]
            for st in style_list:
                style_action = QWidgetAction(main_win)
                style_action.setObjectName(st)
                style_action.setCheckable(True)
                style_action.setText(st)
                if st == self.default_style:
                    style_action.setChecked(True)
                menu_style.addAction(style_action)
                style_group.addAction(style_action)
                if st.lower() == "fusion":
                    menu_style.addSeparator()

                    # Light palette action
                    self.light_palette_action = QWidgetAction(main_win)
                    self.light_palette_action.setObjectName("Light")
                    self.light_palette_action.setText("Light")
                    self.light_palette_action.setCheckable(True)
                    self.light_palette_action.setChecked(True)
                    self.light_palette_action.setEnabled(True)
                    menu_style.addAction(self.light_palette_action)
                    palette_group.addAction(self.light_palette_action)

                    # Dark palette action
                    self.dark_palette_action = QWidgetAction(main_win)
                    self.dark_palette_action.setObjectName("Dark")
                    self.dark_palette_action.setText("Dark")
                    self.dark_palette_action.setCheckable(True)
                    self.dark_palette_action.setEnabled(True)
                    menu_style.addAction(self.dark_palette_action)
                    palette_group.addAction(self.dark_palette_action)

    def change_style(self, new_style):
        """Set the new style"""
        self.app_ptr.setStyle(new_style)

    def set_default_style(self):
        self.change_style(self.default_style)

    def set_default_palette(self):
        self.light_palette_action.setChecked(True)
        self.set_light_palette()

    def connect_palette_actions(self, action_dark, action_light):
        """Connect the palette actions to their respective palette methods."""
        action_dark.triggered.connect(self.set_dark_palette)
        action_light.triggered.connect(self.set_light_palette)

    def set_palette(self):
        """Set light or dark palette according to menu selection."""
        if self.dark_palette_action.isChecked():
            self.set_dark_palette()
        else:
            self.set_light_palette()

    def set_light_palette(self):
        """Set the light palette (default system colors)."""
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(QPalette.Base, Qt.white)
        light_palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))
        light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        light_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_palette.setColor(QPalette.Text, Qt.black)
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, Qt.black)
        light_palette.setColor(QPalette.Link, QColor(0, 0, 255))
        light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.HighlightedText, Qt.white)

        light_palette.setColor(QPalette.Active, QPalette.Button, QColor(220, 220, 220))
        light_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 128, 128))
        light_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(128, 128, 128))
        light_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
        light_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(240, 240, 240))

        self.app_ptr.setPalette(light_palette)
        self.current_icon_color = QColor(50, 50, 50)
        self.current_disabled_color = QColor(180, 180, 180)
        self.icon_man.clear_cache()
        self.theme_changed.emit(self.current_icon_color, self.current_disabled_color)

    def set_dark_palette(self):
        dark_gray = QColor(53, 53, 53)
        gray = QColor(128, 128, 128)
        black = QColor(25, 25, 25)
        blue = QColor(42, 130, 218)

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, dark_gray)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, black)
        dark_palette.setColor(QPalette.AlternateBase, dark_gray)
        dark_palette.setColor(QPalette.ToolTipBase, blue)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, dark_gray)
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Link, blue)
        dark_palette.setColor(QPalette.Highlight, blue)
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        dark_palette.setColor(QPalette.Active, QPalette.Button, gray.darker())
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, gray)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, gray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, gray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Light, dark_gray)

        self.app_ptr.setPalette(dark_palette)
        self.current_icon_color = Qt.white
        self.current_disabled_color = gray
        self.icon_man.clear_cache()
        self.theme_changed.emit(self.current_icon_color, self.current_disabled_color)

    @staticmethod
    def set_radio_btn_style_sheet():
        radio_btn_ss = (
            "QRadioButton{ color: white; margin-left:50%; margin-right:50%;} "
            + "QRadioButton::indicator { width: 11px;"
            + "height: 11px;"
            + "border-radius: 5px;} "
            + "QRadioButton::indicator::unchecked{border: 1px solid;"
            + "border-color: rgb(132,132,132);"
            + "border-radius: 5px;"
            + "background-color: white;"
            + "width: 11px;"
            + "height: 11px;} "
            + "QRadioButton::indicator::checked{border: 3px solid;"
            + "border-color: white;"
            + "border-radius: 6px;"
            + "background-color: rgb(0,116,188);"
            + "width: 7px;"
            + "height: 7px;}"
        )
        return radio_btn_ss

    @staticmethod
    def set_button_color(bg_color="dark_gray", color="white"):
        push_btn_ss = (
            "QPushButton { background-color: "
            + bg_color
            + ";color: "
            + color
            + "; border: : 3px solid; font-weight: bold;}"
        )
        return push_btn_ss

    @staticmethod
    def set_tool_button_color(bg_color="dark_gray", color="white"):
        tool_btn_ss = (
            "QToolButton { background-color: "
            + bg_color
            + ";color: "
            + color
            + "; border: : 3px solid; font-weight: bold;}"
        )
        return tool_btn_ss


if __name__ == "__main__":
    pass
