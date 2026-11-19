"""The feed rate and spindle speed fields accept only values that GRBL can run.

F0 is error:22 and a negative F or S is error:4 (#132, #135); S0 is allowed, it keeps the spindle stopped.
"""

import pytest

JOBS = ("top", "bottom", "profile", "drill", "nc_top", "nc_bottom")
JOB_FEED_FIELDS = [f"{job}_{axis}_feed_rate_dsb" for job in JOBS for axis in ("xy", "z")]
MACHINE_FEED_FIELDS = ["feedrate_xy_dsb", "feedrate_z_dsb", "feedrate_probe_dsb"]
SPINDLE_SPEED_FIELDS = [f"{job}_spindle_speed_dsb" for job in JOBS]


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


def _fields_named(ui, part: str) -> set:
    return {widget.objectName() for widget in ui.window.findChildren(ui.spin_box_type) if part in widget.objectName()}


def test_every_feed_rate_field_is_listed(ui) -> None:
    assert _fields_named(ui, "feed") == set(JOB_FEED_FIELDS + MACHINE_FEED_FIELDS)


def test_every_spindle_speed_field_is_listed(ui) -> None:
    assert _fields_named(ui, "spindle_speed") == set(SPINDLE_SPEED_FIELDS)


@pytest.mark.parametrize("name", JOB_FEED_FIELDS + MACHINE_FEED_FIELDS)
def test_feed_rate_field_refuses_zero_and_negative_values(ui, name: str) -> None:
    field = getattr(ui, name)

    assert field.minimum() > 0
    field.setValue(0.0)
    assert field.value() > 0
    field.setValue(-40.0)
    assert field.value() > 0


@pytest.mark.parametrize("name", SPINDLE_SPEED_FIELDS)
def test_spindle_speed_field_accepts_zero_and_refuses_negative_values(ui, name: str) -> None:
    field = getattr(ui, name)

    assert field.minimum() == 0
    field.setValue(0.0)
    assert field.value() == 0
    field.setValue(-1000.0)
    assert field.value() == 0
