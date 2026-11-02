# shape_core: API, design and the changes that need code outside the module

`shape_core` is the CAM core of The Ant Farm: it parses the PCB files, builds
the toolpaths and writes (and re-reads) the G-code. It has no dependency on Qt
and can be used in a headless process.

This document describes the module as it is after the refactor series on the
`dev` branch (`git log --oneline -- src/TheAntFarm/shape_core`), the rules to
follow when working on it, and — in §5 — the list of changes that **require
code outside `shape_core`**, with the file and the line to touch.

---

## 1. Public API

```python
from TheAntFarm.shape_core import (
    PcbObj,            # gerber/excellon loading, layer geometries
    MachinePath,       # toolpath generation (gerber, profile, pocketing, drill)
    ToolPath,          # one tool + one procedure + the paths to machine
    GCoder,            # G-code writer
    GCodeParser,       # G-code reader (vectors, bounding box)
    GCodeAlignment,    # alignment of a loaded G-code (thin plate spline)
    GCodeLeveler,      # auto bed levelling of a loaded G-code
    Macros, MacroContext, MacroError,
    Geom,              # a polygon/line with its polarity
    default_config, merge_config,
)
```

`shape_core/__init__.py` lists the exported names in `__all__`; the
visualization layer (`VisualLayer`, `GLUTess`) is imported on first access
because it pulls vispy and OpenGL. The old per-module imports
(`from shape_core.gcode_manager import GCoder`) keep working, so the
application does not have to be changed in the same commit (see §5.1).

## 2. Module layout

| File | Content |
|---|---|
| `config.py` | `COMMON_GCODE`, `GCODE_DEFAULTS`, `PATH_DEFAULTS`, `PROBE_DEFAULTS`, `default_config()`, `merge_config()` |
| `path_types.py` | `ToolPath` dataclass |
| `pcb_manager.py` | `PcbObj`: Gerber/Excellon → list of `Geom`, cached per layer |
| `geometry_manager.py` | `Geom`, merge and offset of polygons |
| `pyclipper2shapely.py` | vendored MIT helper (clipper poly tree → shapely), used by the merge |
| `path_manager.py` | `MachinePath` (the four procedures), `Gapper` (tabs), `remap_invalid_ids` |
| `drill_path_optimizer.py`, `gerber_path_optimizer.py` | travel optimization |
| `gcode_manager.py` | `GCoder`, `GCode`, `GCodeParser`, `GcodeLine`, `GcodePoint`, `GCodeAlignment`, `GCodeLeveler`, `GCodeMacro` |
| `macros_manager.py` | tag catalog, template validation, expansion (see `docs/macros.md`) |
| `commands_manager.py` | manual GRBL commands (jog, goto, probe, …) |
| `align_manager.py` | thin plate spline alignment |
| `gcode_drill_converter.py` | holes read back from a G-code file |
| `visual_manager.py` | vispy rendering (imported on demand) |

## 3. Rules to keep in `shape_core`

1. **Configurations are merged, never replaced.** Use
   `merge_config("path"|"gcode", machining_type, cfg)`: the defaults of
   `config.py` are complete, so a partial configuration coming from the
   settings manager cannot raise `KeyError` in the middle of a job. New keys
   are added to `config.py`, the job configuration may override them.
2. **No prints.** Use the module logger (`logger.debug` for the timings, `info`
   for the phases of a job, `warning`/`error` for the failures). The console of
   the application is the only output.
3. **The toolpaths are `ToolPath` objects**, not tuples: `tool_diameter`,
   `machining_type`, `paths`, `invalid_ids`.
4. **`PcbObj` returns `Geom` objects** and caches them per tag; the loaders
   invalidate the cache. A `MultiPolygon` is split into its parts, because the
   rest of the CAM works one polygon at a time.
5. **A geometry that cannot be built raises `ValueError`** with the kind, the
   number of points and the first point (`Geom._make_geom`), so the primitive
   that produced it can be identified.
6. **Coordinates**: `GCoder.DIGITS = 4` for the generated files,
   `POSITION_DIGITS = 3` (1 µm) when an existing file is rewritten
   (`GcodePoint.get_string`).
7. **Timings** use `time.perf_counter()`, logs use f-strings only when cheap or
   `logger.debug("... %s", value)` in the loops.

## 4. What the refactor changed (record)

* `geometry_manager`: 629 → 405 lines, the unreachable pyclipper implementation
  and an unused helper removed.
* `plot_stuff.py` (193 lines, matplotlib) deleted; `print` calls in the module:
  0.
* `PcbObj` caches the converted layer and no longer raises the gerbyx logger to
  INFO; the files are read with an explicit encoding.
* `VisualLayer.add_gcode` no longer removes the first vector from the model used
  to regenerate the G-code (it was a data corruption, not only a crash).
* `ToolPath` replaces the positional tuple; `GCoder.load_path` refuses the old
  structure.
* `config.py` holds the defaults of the two classes and of the probe managers;
  `load_cfg` merges.
* `Geom` validates its input and builds from an existing shapely geometry
  (`Geom.from_shapely`), which made `FakeGeom` unnecessary.
* `shape_core/__init__.py` publishes the API, `visual_manager` is lazy.
* `GCode.get_bbox` has one rule instead of four identical branches;
  `GCoder.format_float(-0.0)` writes `0.0000`; the dead members
  (`GCodeLeveler.apply`, `abl_to_working_pos`, `VisualLayer.add_triploy`,
  `translucent_filter`, the duplicated `GCodeParser` accessors) are gone.
* `MachinePath.execute_drill` returns `[]` (not `None`) when there is nothing
  to machine.

Tests: `tests/unit` (666 tests at the time of writing) run with
`PYTHONPATH=src python -m pytest tests/unit -q`.

---

## 5. Changes that need code outside `shape_core`

None of the items of §4 required touching the rest of the application: the
controllers pass the `ToolPath` lists, the `Geom` lists and the configuration
dictionaries through without inspecting them. The following changes are
outside the module and are **not** implemented yet; each one is independent.

### 5.1 Adopt the public API in the consumers (done)

The five consumers now import the classes from the package instead of the
module that contains them: 9 import lines became 5, and nothing else changed.

| File | Import |
|---|---|
| `controller/controller_control.py` | `from shape_core import GCodeAlignment, GCodeLeveler, GCodeParser, GCoder` |
| `controller/controller_manager.py` | `from shape_core import GCodeMacro, GCoder, MacroError` |
| `controller/controller_view.py` | `from shape_core import GCoder, MachinePath, PcbObj` |
| `controller/controller_align.py` | `from shape_core import DrillGcodeConverter, PcbObj` |
| `ui_manager/ui_manager.py` | `from shape_core import VisualLayer` (loaded lazily) |

Verified with the whole test suite (679 tests, UI and controller tests
included), by importing the four controllers, `UiManager` and the entry point
`the_ant_farm`, and by checking that `import shape_core` still does not load
vispy (`visual_manager` is imported on first access).

**Not done, and why**: the imports still use the top level package
`shape_core`, which is what `src/TheAntFarm` on `sys.path` provides. Using
`TheAntFarm.shape_core` (the fully qualified name) would require `src` on the
path instead, i.e. changing `the_ant_farm.py`, `tests/conftest.py`, the
`pathex` of the PyInstaller spec and the launch of the application, with no
functional gain. It is a separate task, to be done together with §5.6.

### 5.2 Expose the macro configuration in the settings and in the UI (done)

The tool change procedures need six values that the application did not
provide, so the macros always used the defaults of
`shape_core/config.py`: the `setter` procedure could not be selected and
`safe_pos` was the constant `-1`. They are now machine settings, exposed in
`Preferences -> Jobs/Machine Settings`:

| Setting (ini key) | Default | UI widget | Used by |
|---|---|---|---|
| `safe_z` | `-1.0` | `safe_z_dsb` (mm, machine coordinates) | `@SAFE_POS_Z@`, in all three procedures |
| `tool_change_mode` | `wcs` | `tool_change_mode_cb` (items from `MACROS["M6"].variants`) | chooses the template |
| `tool_setter_x` / `tool_setter_y` | `0.0` | `tool_setter_x_dsb` / `tool_setter_y_dsb` (mm) | `@SETTER_POS_X/Y@` |
| `tool_setter_relative_flag` | `False` | `tool_setter_wpos_chb` ("Setter WPos") | `@SETTER_TYPE_POS@` |
| `tool_probe_backoff` | `1.5` | `tool_probe_backoff_dsb` (mm) | `@PROBE_BACKOFF@` |
| `spindle_stop_dwell` | `1.0` | `spindle_stop_dwell_dsb` (s) | `@SPINDLE_DWELL@` |

`ControllerWorker.update_gerber_cfg()` passes them to the commander
configuration (`safe_pos` receives only the Z, which is what the macros
use), the setter fields are enabled only when the mode is `setter` and the
section is appended to the existing grid of the page, so no other row
changed. The COMBO is filled from the macro registry: a new procedure
appears in the preferences without touching the UI.

Not exposed on purpose: `tool_change_working` and `tool_change_feedrate`
(fall back to the probe values, the change position is already a machine
position in the settings), and the spindle speed for `@SPINDLE_START@` (the
job already programs `M3 S<speed>` before the change, a second value would
be a second place to keep in sync).

Verified with the tests of `settings_machine` (defaults, write/read
round-trip, restore), of the worker (`update_gerber_cfg` produces the six
keys and the macro configuration matches the settings, an invalid mode is
refused by the registry) and of the preferences (combo filled from the
registry, enabling of the setter fields, save/restore), plus a manual run of
the application on the `setter` procedure.

### 5.3 Stop the job when the machine raises an alarm while streaming

**Where** `controller/controller_manager.py`, `ControllerWorker.parse_rx_queue`
(the `ok`/`error` branches from line ~230).

**Why** a probing cycle that does not touch the workpiece makes GRBL raise
`ALARM:5` and clear the planner; the lines still in flight are answered with
`error:9`, so `cmds_to_ack` never reaches zero, `check_eof_and_idle()` never
fires and the job stays "sending" forever. The measurement itself is already
discarded (`ControllerControlController.parse_probe_report`), the stream is not.

**How** call `abort_job_for_macro_error` (or its generic version) when an
`ALARM:*` or `error:9` arrives while `sending_file` is true, and write the
reason in the console.

Detailed in `docs/macros.md` §4, item M-03.

### 5.4 Refuse to start a tool change on a non homed machine

**Where** `controller/controller_manager.py` (`macro_check`),
`controller/controller_control.py` (connection state).

**Why** the tool change procedures move in machine coordinates (`G53`); GRBL
does not report the homed state, so it has to be tracked from the commands the
application sends (`$H`) and reset on connect/reset/alarm.

Detailed in `docs/macros.md` §4, item M-02.

### 5.5 Packaging and dependencies (done)

Implemented on the `dev` branch (commit "Align the packaging with the
dependencies of the application").

| File | Change |
|---|---|
| `pyproject.toml` | `python = ">=3.10,<3.13"` (the `gerbyx` parser needs 3.10, the CI builds with 3.12); `shiboken2` → `shiboken6`; removed `cairocffi`, `cffi`, `pycparser` (they were dependencies of pcb-tools); `PyOpenGL` and `vispy` aligned to the `>=` of `requirements.txt`; removed the invalid `dynamic = ["version"]` stanza (the version is static) |
| `requirements.txt` | removed `cairocffi`, `cffi`, `pycparser`; `freetype-py` stays (dependency of `vispy`) |
| `src/TheAntFarm/the_ant_farm.spec` | the 23 `gerbyx` submodules used by the parser are collected with `collect_submodules`, excluding `gerbyx.cli` and `gerbyx.__main__` (they need typer and rich, the application does not use them) and `gerbyx.visualizer` (it needs matplotlib); `shiboken6.shiboken6` → `shiboken6.Shiboken` (the first name does not exist) |
| `.github/workflows/build-executable.yml` | it called `pyinstaller theantfarm.spec`, a file that does not exist, and expected `dist/theantfarm`: now it uses `the_ant_farm.spec` and `dist/the_ant_farm` (the name in the spec) |
| `.github/workflows/python-app.yml` | the shape core step is no longer `continue-on-error` and runs the whole core test set instead of three files |
| `.gitignore` | `/src/TheAntFarm/dist/` (the build output next to `build/`) |

**Verification** (Linux, Python 3.12, PyInstaller 6):

```
pyinstaller --noconfirm --workpath /tmp/pyi/build --distpath /tmp/pyi/dist the_ant_farm.spec
# exit 0, one file: /tmp/pyi/dist/the_ant_farm (212 MB)
grep -c gerbyx /tmp/pyi/build/the_ant_farm/Analysis-00.toc   -> 23 modules
grep typer|rich  ...                                          -> none
QT_QPA_PLATFORM=offscreen ./the_ant_farm                       -> starts, no traceback
```

Two warnings are left and are harmless: `scipy.special._cdflib` (a scipy
hook of PyInstaller) and the `.ico` icon, which PyInstaller only applies on
Windows and macOS.

**Residual note for the Linux artifact**: the triangulation of the layers uses
`OpenGL.GLU`/`GLUT`, so the executable needs the system libraries
`libGLU.so.0` and `libglut.so.0` at runtime (in Debian/Ubuntu: `libglu1-mesa`
and `freeglut3`). The build machine only needs the `-dev` packages, which the
workflow installs.

### 5.6 Test infrastructure

**Where** `tests/conftest.py:5-6` and `tests/unit/test_controller_align.py:16-22`.

**Why** `tests/conftest.py` imports `PySide6.QtCore` and
`PySide6.QtSerialPort` at module level, so the whole test suite needs Qt even
for the pure core tests. `test_controller_align.py` patches
`double_side_manager.DoubleSideManager` and imports
`controller.controller_align` inside the `with` block: the patch only works if
no other test module imported `controller_align` first, which is why
`tests/unit/test_controller_manager.py` imports the worker lazily (see the
comment in its fixture).

**How** move the PySide6 imports inside the `qapp` fixture (and the UI tests
into a directory with its own `conftest.py`); in `test_controller_align.py`
patch `controller.controller_align.DoubleSideManager` and import at module
level.

**Done when** `pytest tests/unit/test_config.py` runs in an environment without
Qt, and the order of the test modules no longer changes the result.

---

## 6. Ideas that were considered and not implemented

* Splitting `gcode_manager.py` (1099 lines, four responsibilities: writer,
  reader, alignment, levelling) into submodules. It is the natural next step
  for readability, but it touches the imports of the controllers, so it
  belongs to §5.1.
* A `typing.Protocol` for the "parent" of the macros (`format_float`,
  `DIGITS`): the managers accept any object today, and a protocol would make
  the contract explicit without changing the controllers.
* Profiling of the gerber merge on a real board: the merge and the offset are
  the two operations that dominate the path generation, and the module has no
  benchmark yet.
