"""Start The Ant Farm, fill its canvases with sample data and save screenshots in the dark and light themes.

Used by the "UI screenshots" workflow to look at the interface on Linux, Windows and macOS. It can also run
locally: ``python tools/ui_screenshots.py --out ui_screenshots``.
"""

import argparse
import os
import shutil
import sys
import tempfile
import time
from typing import Callable, List

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(REPO, "src", "TheAntFarm")
SAMPLE_GERBER = os.path.join(REPO, "tests", "test_data", "gerbers", "metric_trace.gbr")
SAMPLE_DRILL = os.path.join(REPO, "tests", "test_data", "gerbers", "simple_drill.drl")
# A board outline in millimetres around the samples (the inch samples are not converted to millimetres)
SAMPLE_PROFILE_GERBER = """%FSLAX46Y46*%
%MOMM*%
%ADD10C,0.100*%
D10*
X-1000000Y-1000000D02*
X4500000Y-1000000D01*
X4500000Y3000000D01*
X-1000000Y3000000D01*
X-1000000Y-1000000D01*
M02*
"""
STATUSES = ["Not Connected", "Idle", "Run", "Hold:0", "Jog", "Alarm", "Door:0", "Check", "Home", "Sleep"]
ALIGNMENT_STATES = [("not_ready", False, 1), ("ready", False, 4), ("applied", True, 4)]

sys.path.insert(0, APP_DIR)

from PySide6.QtGui import QColor, QImage, QPainter  # noqa: E402
from PySide6.QtTest import QTest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402


def wait_for(condition: Callable[[], bool], timeout_s: float, label: str) -> bool:
    """Process events until ``condition`` is true; report it and return False if it never becomes true."""
    start = time.monotonic()
    while time.monotonic() - start < timeout_s:
        QTest.qWait(50)
        if condition():
            return True
    print(f"ERROR: {label} not ready after {timeout_s} s")
    return False


def tile(images: List[QImage], path: str) -> None:
    """Save ``images`` side by side, on a magenta background that shows where each one ends."""
    width = sum(image.width() + 6 for image in images)
    height = max(image.height() for image in images)
    out = QImage(width, height, QImage.Format_RGB32)
    out.fill(QColor(255, 0, 255))
    painter = QPainter(out)
    x = 0
    for image in images:
        painter.drawImage(x, 0, image)
        x += image.width() + 6
    painter.end()
    out.save(path)


def gcode_sample() -> list:
    """A few working and travel moves, in the vector format of the G-code parser."""
    from shape_core.gcode_manager import GcodePoint

    def point(x: float, y: float, travel: bool) -> GcodePoint:
        p = GcodePoint()
        p.coords = np.array([x, y, 0.0])
        p.type = p.TRAVEL if travel else p.WORKING
        return p

    moves = [point(0, 0, True), point(10, 0, True)]
    for i in range(6):
        x = 10.0 + 5 * i
        moves += [point(x, 0, False), point(x, 20, False), point(x + 2, 20, False), point(x + 2, 0, True)]
    return moves


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="ui_screenshots", help="folder for the PNG files")
    args = parser.parse_args()
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    # The application keeps its settings next to its data: use a scratch copy, not the source tree.
    local_path = tempfile.mkdtemp(prefix="the_ant_farm_")
    shutil.copytree(os.path.join(APP_DIR, "macros"), os.path.join(local_path, "macros"))
    sample_profile = os.path.join(local_path, "profile.gbr")
    with open(sample_profile, "w", encoding="utf-8") as profile_file:
        profile_file.write(SAMPLE_PROFILE_GERBER)
    os.chdir(APP_DIR)

    import the_ant_farm

    the_ant_farm.config_os()
    app = QApplication(sys.argv)
    style = the_ant_farm.StyleManager(app)
    window = the_ant_farm.MainWindow(local_path=local_path, style_manager=style)
    window.ui_manager.ui_settings_tab_m.has_unsaved_changes = lambda: False
    style.change_style("Fusion")
    style.set_dark_palette()
    window.resize(1400, 900)
    window.show()
    QTest.qWait(500)

    ui = window.ui
    manager = window.ui_manager
    for tag, path in (("top", SAMPLE_GERBER), ("profile", sample_profile), ("drill", SAMPLE_DRILL)):
        manager.ui_load_layer_m.load_layer_s.emit(tag, path)
    ready = wait_for(lambda: {"top", "profile", "drill"} <= set(manager.vis_layer.meshes), 30, "layers")
    ui.prepare_widget.setCurrentWidget(ui.create_job_tab)
    QTest.qWait(200)
    manager.ui_create_job_m.generate_top_path()
    ready &= wait_for(lambda: "top" in manager.vis_layer.paths, 60, "toolpath")
    manager.ctrl_layer.add_gcode("gcode", gcode_sample())
    manager.ui_align_tab_m.load_align_layer_s.emit("drill", SAMPLE_DRILL)
    ready &= wait_for(lambda: "drill" in manager.vis_align_layer.meshes, 30, "drill layer on the Align tab")

    tabs = ui.main_tab_widget
    for theme, action in (("dark", ui.actionDark), ("light", ui.actionLight)):
        action.trigger()
        QTest.qWait(300)
        for index in range(tabs.count()):
            tabs.setCurrentIndex(index)
            name = f"{theme}_tab{index}_" + tabs.tabText(index).lower().replace(" ", "_").replace("/", "_")
            if tabs.widget(index).isAncestorOf(ui.prepare_widget):
                for sub_tab in (ui.load_layers_tab, ui.create_job_tab):
                    ui.prepare_widget.setCurrentWidget(sub_tab)
                    QTest.qWait(300)
                    window.grab().save(os.path.join(out_dir, f"{name}_{sub_tab.objectName()}.png"))
            else:
                QTest.qWait(300)
                window.grab().save(os.path.join(out_dir, f"{name}.png"))

        tabs.setCurrentWidget(ui.control_tab)
        statuses = []
        for status in STATUSES:
            ui.status_l.setText(status)
            manager.ui_control_tab_m.update_status_colors(status)
            QTest.qWait(50)
            statuses.append(ui.status_l.grab().toImage())
        tile(statuses, os.path.join(out_dir, f"{theme}_statuses.png"))
        ui.status_l.setText("Not Connected")
        manager.ui_control_tab_m.update_status_colors("Not Connected")

        tabs.setCurrentWidget(ui.align_tab)
        toggles = []
        for _, applied, points in ALIGNMENT_STATES:
            manager.ui_align_tab_m.update_ui_alignment_applied(applied, points)
            for button in (ui.apply_alignment_tb, ui.apply_alignment_tb_2):
                button.setChecked(applied)
            QTest.qWait(50)
            toggles += [ui.apply_alignment_tb.grab().toImage(), ui.apply_alignment_tb_2.grab().toImage()]
        tile(toggles, os.path.join(out_dir, f"{theme}_alignment_toggles.png"))
        manager.ui_align_tab_m.update_ui_alignment_applied(False, 0)

    window.close()
    QTest.qWait(200)
    shutil.rmtree(local_path, ignore_errors=True)
    saved = sorted(os.listdir(out_dir))
    print(f"Saved {len(saved)} screenshots in {out_dir}:")
    for name in saved:
        print(f"  {name}")
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())
