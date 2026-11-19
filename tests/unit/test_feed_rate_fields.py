"""The feed rate fields accept only values that GRBL can run (#132): F0 is error:22, a negative F is error:4."""

import pytest

JOB_FEED_FIELDS = [
    f"{job}_{axis}_feed_rate_dsb"
    for job in ("top", "bottom", "profile", "drill", "nc_top", "nc_bottom")
    for axis in ("xy", "z")
]
MACHINE_FEED_FIELDS = ["feedrate_xy_dsb", "feedrate_z_dsb", "feedrate_probe_dsb"]


@pytest.fixture
def ui(qapp):
    from PySide6.QtWidgets import QDoubleSpinBox, QMainWindow
    from ui_the_ant_farm import Ui_MainWindow

    window = QMainWindow()
    form = Ui_MainWindow()
    form.setupUi(window)
    form.window = window
    form.spin_box_type = QDoubleSpinBox
    yield form
    window.close()
    window.deleteLater()


def test_every_feed_rate_field_is_listed(ui) -> None:
    feed_fields = {
        widget.objectName() for widget in ui.window.findChildren(ui.spin_box_type) if "feed" in widget.objectName()
    }

    assert feed_fields == set(JOB_FEED_FIELDS + MACHINE_FEED_FIELDS)


@pytest.mark.parametrize("name", JOB_FEED_FIELDS + MACHINE_FEED_FIELDS)
def test_feed_rate_field_refuses_zero_and_negative_values(ui, name: str) -> None:
    field = getattr(ui, name)

    assert field.minimum() > 0
    field.setValue(0.0)
    assert field.value() > 0
    field.setValue(-40.0)
    assert field.value() > 0
