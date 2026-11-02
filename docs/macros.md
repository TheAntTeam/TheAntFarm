# Macro system: state, design and backlog

This document describes the macro system of The Ant Farm as it is after the
`dev` branch commits `6515c82..c3df73e`, and lists the work that is still open
in a form that can be resumed without redoing the analysis.

Firmware behaviour described here was verified on the sources of
[gnea/grbl](https://github.com/gnea/grbl) (GRBL 1.1) and
[bdring/FluidNC](https://github.com/bdring/FluidNC) (main); the file and the
symbol of every statement are written next to it so that it can be re-checked
in a couple of minutes.

---

## 1. What is implemented

| Area | State |
|---|---|
| Placeholder expansion | `shape_core/macros_manager.py`, single catalog `TAGS` |
| Template validation | `validate_template()`, errors with file and line |
| Machine state for the resolvers | `MacroContext` (cfg, wsp, dro, probe data) |
| Macro registry with variants | `MACROS`, `tool_change_mode = wcs \| tlo \| setter` |
| Tool change procedures | `macros/tool_change_wcs.gcode`, `tool_change_tlo.gcode`, `tool_change_setter.gcode` |
| Macro start / abort | `controller/controller_manager.py` (`macro_check`, `get_next_macro_line`, `abort_job_for_macro_error`) |
| `$#` report parsing | `controller/controller_control.py` (`parse_tlo_report`, `parse_probe_report`) |
| Tests | `tests/unit/test_macros_manager.py`, `test_controller_manager.py`, `test_controller_control.py` |

Golden tests freeze the full expansion of the three templates
(`GOLDEN_WCS`, `GOLDEN_TLO`, `GOLDEN_SETTER` in
`tests/unit/test_macros_manager.py`): any change to a procedure shows up as a
line by line diff.

---

## 2. How it works

### 2.1 Data flow of a tool change

```
GCoder.go_tool_change()             writes  "T<n>"  and  "M6"  into the job file
        |
        v   (the job is streamed line by line)
ControllerWorker.macro_check(line)  is_macro("M6") -> yes
        |                             - if the machine still has unacked lines: return None,
        |                               the M6 line is NOT consumed and is retried on the next ok
        |                             - otherwise: freeze the DRO (WPO/MPO), create GCodeMacro,
        |                               send "$#" to read the workspace parameters, macro_on = True
        v   (on every "ok")
GCodeMacro.get_next_line(wsp, probe) -> GCoder.compute_tag -> Macros.expand
        |                             one line at a time, tags resolved with the CURRENT
        |                             machine state (a PROBE_VALUE tag sees the probe of
        |                             the previous line of the same macro)
        v
line queued to the TX buffer -> machine
```

A macro that cannot be loaded, or a line that cannot be resolved, calls
`abort_job_for_macro_error()`: the streaming stops, the file line is not
consumed, nothing else is queued and the reason is written in the console.
Skipping the macro (the old behaviour) would continue the job with the wrong
tool or the wrong tool length offset.

### 2.2 Constraints to keep when editing macros

1. **One tag = one line.** The streamer sends a single line and waits for one
   `ok` for it; a tag that expands to `M5\nG4 P1` would desynchronise the ack
   accounting (`cmds_to_ack`). Keep every resolver single line (there is a test:
   `test_no_tag_expands_to_more_than_one_line`).
2. **`@...@` only.** Text outside a pair of `@` is never touched, so a comment
   may contain any word. An unbalanced `@` is a template error.
3. **Coordinates.** `PROBE_*_POS` and `CHANGE_*_POS` may be machine (G53) or
   work (G54) positions, selected by `tool_probe_working`,
   `tool_setter_working` and `tool_change_working`. Probe *values* are always
   converted to work coordinates by `MacroContext.probe()`.
4. **Probe data** is a `deque(maxlen=2)` of machine coordinates: index 0 is the
   last probing cycle, index 1 the previous one.
5. **`G53` requires homing.** GRBL does not report the homed state, see M-02.

### 2.3 Placeholders

`shape_core/macros_manager.py:235` (`TAGS`). Each entry is a
`Tag(name, resolver, description)`.

| Group | Placeholders |
|---|---|
| Probe position | `PROBE_POS_X`, `PROBE_POS_Y`, `PROBE_POS_MIN`, `PROBE_TYPE_POS` |
| Feed rates | `PROBE_FEED_XY`, `PROBE_FEED_FAST`, `PROBE_FEED_SLOW`, `CHANGE_FEED_FAST`, `CHANGE_FEED_SLOW` |
| Probing | `PROBE_HOLD_BEFORE`, `PROBE_BACKOFF` |
| Measured values (work coordinates) | `PROBE_VALUE_PREX/Y/Z` (previous cycle), `PROBE_VALUE_ACTX/Y/Z` (last cycle) |
| Tool change position | `CHANGE_POS_X`, `CHANGE_POS_Y`, `CHANGE_POS_Z`, `CHANGE_TYPE_POS` |
| Tool setter | `SETTER_POS_X`, `SETTER_POS_Y`, `SETTER_TYPE_POS` |
| Safety / machine | `SAFE_POS_Z`, `PRE_POS_X`, `PRE_POS_Y`, `PRE_POS_Z`, `SPINDLE_STOP`, `SPINDLE_DWELL`, `SPINDLE_START` |
| Tool length | `TLO_TYPE_A` (current TLO + measured difference), `TLO_TYPE_N` (measured difference only) |

Adding a placeholder means adding one `Tag(...)` entry: template validation,
the golden tests and the "single line" test pick it up automatically.

### 2.4 Configuration

`DEFAULT_CFG` at `shape_core/macros_manager.py:137`. `Macros.load_cfg()` merges
the application configuration on top of it into a **copy** (missing keys cannot
raise `KeyError`, the caller dictionary is not modified).

| Key | Default | Meaning |
|---|---|---|
| `tool_probe_pos` | `(-1, -1, -11)` | probe position (work or machine, see below) |
| `tool_probe_working` | `True` | probe position in work (`G54`) or machine (`G53`) coordinates |
| `tool_probe_min` | `-11.0` | lowest Z allowed while probing, in the same frame as the probe position |
| `tool_probe_feedrate` | `(300, 80, 50)` | XY travel, fast approach, slow measuring move |
| `tool_probe_backoff` | `1.5` | retract between the fast and the slow probing move |
| `tool_probe_hold` | `False` | insert `M0` before probing |
| `tool_probe_zero` | `False` | (commands manager only) zero Z after probing |
| `tool_change_pos` | `(-41.2, -120.88, -1)` | tool change position, machine coordinates |
| `tool_change_working` | falls back to `tool_probe_working` | frame of the change position |
| `tool_change_feedrate` | falls back to `tool_probe_feedrate` | feed rates of the change moves |
| `safe_pos` | `(-1, -1, -1)` | safe Z (machine coordinates) |
| `tool_change_mode` | `wcs` | `wcs`, `tlo` or `setter` |
| `tool_setter_pos` | falls back to the probe X, Y | fixed tool setter position |
| `tool_setter_working` | `False` | setter position in work or machine coordinates |
| `spindle_stop_dwell` | `1.0` | dwell after `M5`, before moving |
| `spindle` | absent | spindle speed used by `SPINDLE_START`; if absent only `M3` is emitted |

The application fills these keys in `ControllerWorker.update_gerber_cfg()`
(`controller/controller_manager.py:674`) from `settings_machine.py`. The keys
that the settings do not provide yet fall back to the defaults, see M-01.

### 2.5 The three procedures

| Variant | Probing reference | Correction | Work zero |
|---|---|---|---|
| `wcs` (default) | the workpiece | `G10 P1 L20 Z<previous probe>` | modified |
| `tlo` | the workpiece | `G43.1 Z<TLO + difference>` | untouched |
| `setter` | the fixed tool setter | `G43.1 Z<TLO + difference>` | untouched |

All three: `G21`, `G49`, spindle stop with dwell, two stage probing, explicit
`M0` message, spindle restart at the end. `tlo` and `setter` accumulate the
measured difference on the tool length offset reported by `$#` at the beginning
of the macro, so consecutive changes keep adding up (the `G49` in the header
clears the machine state, the accumulated value is re-applied by `TLO_TYPE_A`).

---

## 3. Firmware capabilities (verified)

| Capability | GRBL 1.1 | FluidNC | Source |
|---|---|---|---|
| `G43.1 Z<off>` / `G49` | yes, **Z only** | yes, one offset per axis | `grbl/gcode.c` `TOOL_LENGTH_OFFSET_AXIS`, `FluidNC/src/GCode.cpp` `gc_state.tool_length_offset[]` |
| `G43` with `H` | not supported | not supported | `grbl/gcode.c` `[14. Cutter length compensation]` |
| `$#` → `[TLO:...]` | `[TLO:<value>]` | `[TLO:x,y,z]` (per axis) | `grbl/report.c` `report_ngc_parameters`; `FluidNC/src/Report.cpp` `report_ngc_parameters` iterates `CoordIndex` |
| `$#` → `[PRB:...]` | `[PRB:x,y,z:success]`, **machine coordinates** | same format | `grbl/report.c` `system_convert_array_steps_to_mpos(sys_probe_position)`; `FluidNC/src/Report.cpp:195` |
| `M6` | **error:20** (unsupported), M-code switch `default: FAIL` | executed: `T`/`M6`/`M61`, `switchSpindle`, `spindle->tool_change()`, `deferred_ack` | `grbl/gcode.c` M-code switch; `FluidNC/src/GCode.cpp` (`gc_block.modal.tool_change`, `case 6`) |
| Tool number tracking | no | `gc_state.selected_tool` / `current_tool` | `FluidNC/src/GCode.cpp` |
| Firmware macros | no | `startup_line0/1`, `after_homing`, `after_reset`, `after_unlock`, `macros0..3`, per spindle `m6_macro` | `FluidNC/src/Machine/Macros.h`, `FluidNC/src/Spindles/Spindle.h` (`handler.item("m6_macro", _m6_macro)`) |
| Macro syntax (firmware) | – | plain G-code, `&` = newline, `#xx` = realtime char escape, **no arithmetic, no variables** | `FluidNC/src/Machine/Macros.cpp` `MacroChannel::readLine` |
| Persistent tool table | no | no (only ATC modules) | – |

Consequences:

* on GRBL the interception of `M6` in the application is mandatory (it is what
  `macro_check` does), otherwise the job stops with `error:20`;
* the tool length correction can be computed only on the PC, because the
  firmware has no arithmetic: a firmware macro can contain the fixed sequence
  but not the difference between two probing results.

---

## 4. Backlog

Items are ordered by priority. Each one lists what to change, where, and how to
know that it is done.

### M-01 — Expose the macro configuration in the settings and in the UI

**Why** the new keys (`tool_change_mode`, `tool_setter_pos`,
`tool_setter_working`, `tool_probe_backoff`, `spindle_stop_dwell`,
`tool_change_working`, `tool_change_feedrate`) work when passed in the
configuration but the application never provides them: today the setter mode
can only be enabled by editing the code.

**Where**
* `settings_manager/settings_machine.py`: defaults near the other
  `tool_probe_*` values (lines 44-70), `load_machine_settings()` (from line 88),
  `write_all_machine_settings()` (line 149, `DEFAULT` section at line 162).
* `controller/controller_manager.py:694` (`update_gerber_cfg`): add the new keys
  to the `Od({...})` that feeds `GCoder.load_cfg`.
* `ui_manager/ui_settings_preferences.py`: the probe widgets are wired at lines
  61-70; the `.ui` file (`the_ant_farm.ui`) needs the new widgets (mode combo,
  setter X/Y, working flag, backoff, spindle dwell).

**How** add the values as machine settings (they are per machine, not per job),
read them in `update_gerber_cfg`, and let the preferences write them. Validate
the mode against `MACROS["M6"].variants` and show a message box for an invalid
value instead of failing at job start.

**Done when** selecting a mode in the preferences changes the template that runs
(a test can check `update_gerber_cfg()["tool_change_mode"]`), and an invalid
mode is refused by the preferences.

**Effort** ~3 h, low risk (settings are covered by `test_settings_machine.py`).

### M-02 — Refuse to start the macro when the machine is not homed

**Why** the three procedures use absolute machine coordinates (`G53`) for the
safe Z, the probe/setter XY and the change position. Without homing those
coordinates are meaningless and the machine can move into the fixture.

**Where** `controller/controller_manager.py` (`macro_check`, line 289) and
`controller/controller_control.py` (state tracking).

**How** track the homed state per connection: `homed = False` on connect, on
soft reset and on `ALARM`, `homed = True` after a `$H` that ends with `ok`.
GRBL does not report the flags, so the state has to be derived from the
commands the application sends; FluidNC reports it too (verify with `$State`
before relying on it). In `macro_check`, when `not homed`, call
`abort_job_for_macro_error` with a clear message.

**Done when** a job that contains `M6` on a non homed machine stops before
moving, with a message that says why.

**Effort** ~2 h, medium risk (state machine of the connection).

### M-03 — Handle probe failures and alarms while streaming

**Why** a probing cycle that does not touch the workpiece makes GRBL raise
`ALARM:5` and clear the planner. The lines that are still in the TX buffer are
answered with `error:9` (machine locked), so `cmds_to_ack` never reaches zero,
`check_eof_and_idle()` never fires and the job stays "sending" forever. The
failed measurement itself is already discarded (`parse_probe_report`), but the
stream is left in an inconsistent state.

**Where** `controller/controller_manager.py`, `parse_rx_queue` (the `ok`,
`error` and `ALARM` branches, from line 165).

**How** factor the abort of M-03/item 3 into a generic
`abort_job(reason)` (the current `abort_job_for_macro_error` already does the
right state cleanup) and call it when, while `sending_file` is true, an
`ALARM:*` line or an `error:9` is received. Emit the reason in the console.

**Done when** a simulated `ALARM:5` during a job stops the streaming, clears
the buffers and reports the alarm; covered by a unit test that feeds the lines
to `parse_rx_queue`.

**Effort** ~2 h, low risk.

### M-04 — Tool table and tool number

**Why** with the `setter` variant the length of every tool is measured twice per
change (old and new). With a tool table the length of a tool is stored the first
time it is measured and the change only needs the `G43.1 Z<len[tool] - len[ref]>`
line, which is what makes unattended changes possible.

**Where**
* `controller/controller_manager.py`: capture `T<n>` while streaming (a line
  matching `^T(\d+)` is already written by `GCoder.go_tool_change`), keep
  `self.current_tool` and pass it in the macro configuration.
* `settings_machine.py` or a new `settings_tools.py`: `{tool number: length}`,
  persisted.
* `shape_core/macros_manager.py`: new placeholders `TOOL_NUMBER`,
  `TOOL_LENGTH`, `TLO_FROM_TABLE`; new variant `tool_change_table.gcode`.
* The `M0` comment can then say which tool to mount: `(Change the tool: T<n>)`.

**Done when** two changes in a row with two tools need a single probing cycle
per tool and the lengths survive an application restart.

**Effort** ~1 day, medium risk.

### M-05 — Leverage the FluidNC firmware (exploratory)

**Why** on FluidNC `M6` is executed by the firmware (`switchSpindle` +
`spindle->tool_change()`), and the fixed part of the procedure can live in the
`m6_macro` configuration item, so the tool change no longer depends on the PC
being connected and the round trips per changed line disappear.

**How** detect the firmware at connection time (`$I` returns `[VER:...]`: the
FluidNC build strings contain `FluidNC`), and offer an option "let the firmware
run the fixed part": the application writes the expanded template (without the
tags that need live values) to the `m6_macro` setting, waits for the macro to
finish, then sends the single `G43.1 Z<value>` line computed from the reported
`[PRB:]`. Note that `m6_macro` is a configuration item and changing it at
runtime means writing the configuration, which requires care (backup + reload).

**Alternative to evaluate** `$LocalFS/Run=<file>`: the expanded macro is
uploaded once on the controller file system and run from there; the
application only sends the final offset line. This removes the per line
streaming without touching the configuration.

**Done when** on a FluidNC machine the tool change runs with the PC connected
but without streaming (verified with `$` logs), and on GRBL the current path is
still used.

**Effort** 1-2 days, high risk. Not needed for the first release of the feature.

### M-06 — Preview of the expanded macro

**Why** the golden tests show what will be sent, but the user cannot. A CNC
macro that moves in machine coordinates and requires a manual action should be
reviewable before it runs.

**Where** `ui_manager/ui_control_tab.py` (or the job creation tab) +
`Macros.expand_lines()`.

**How** build a `MacroContext` with the current DRO/probe data (or with
placeholder values when the machine is not connected, showing `<probe z>` for
the values that do not exist yet) and show the expanded text in a read only
dialog, for the selected variant.

**Done when** the dialog shows the three variants and the text matches the
golden test for the same inputs.

**Effort** ~4 h (the expansion already exists), low risk.

### M-07 — Batch the macro lines

**Why** the macro is streamed one line per acknowledgement: a 37 line tool
change is 37 round trips (about 2-3 s at 115200 baud).

**Where** `GCodeMacro.get_next_line` / `controller_manager.parse_rx_queue`.

**How** add `get_next_lines(max_bytes)` and send N lines as one block, counting
the acknowledgements per line (`cmds_to_ack += number of lines`) and keeping
`buffered_size` correct. Only worth doing after M-03, because it changes the
same accounting.

**Done when** the acknowledgement accounting stays correct with a macro of 37
lines sent in blocks of 5, and the golden test still passes.

**Effort** ~4 h, medium risk (shared with the streaming state machine).

### M-08 — Cleanup left from the shape_core review (done)

Completed in the commits `ad2ae24..1c565bf` of the `dev` branch, before the
macro work was continued:

* the `print` calls of `shape_core` are now `logger` calls (there are none left
  in the module);
* `plot_stuff.py` (193 lines, matplotlib, never imported) is deleted;
* `geometry_manager.py` lost the unreachable pyclipper implementation
  (`use_shapely` branches, `offset_polygon_old`, `_offset_polylist`,
  `_offset_multiple_polylist`, `_merge_polylist`, `_clip_polylist`,
  `get_max_distance`), 629 -> 405 lines;
* `PcbObj.get_gerber_layer` / `get_excellon_layer` use the layer cache and the
  loaders invalidate it;
* `pcb_manager.py` no longer raises the gerbyx logger to INFO and reads the
  files with an explicit encoding;
* the `__main__` blocks with hardcoded paths, the unused members
  (`VisualLayer.add_triploy`, `translucent_filter`, `GCodeLeveler.apply`,
  `GCodeLeveler.abl_to_working_pos`, the duplicated `GCodeParser` accessors)
  and the unused imports are gone;
* `GCoder.format_float` no longer writes `-0.0000`;
* `VisualLayer.add_gcode` no longer consumes the vector list of the parser (it
  removed the first vector from the model used to regenerate the G-code).

What is left of that review is the structural part, tracked in
`docs/macros.md` §4 of this document under "Structural backlog" below.

### M-09 — Test isolation

`tests/unit/test_controller_align.py` patches `double_side_manager.DoubleSideManager`
and imports `controller.controller_align` inside the `with` block: the fixture
only works if no other test module imported `controller_align` first (the truth
is bound at import time). `tests/unit/test_controller_manager.py` therefore
imports the worker lazily inside its fixture (see the comment there). The proper
fix is to patch `controller.controller_align.DoubleSideManager` and import at
module level.

**Effort** ~30 min, low risk.

### Structural backlog (was "A9" in the review)

| Item | Why | Risk |
|---|---|---|
| Public API in `shape_core/__init__.py` (still empty) | the consumers import from the submodules (`from shape_core.gcode_manager import GCoder`) and `tests/conftest.py` has to inject two paths in `sys.path` | low |
| `ToolPath` dataclass instead of `((tool, type), [LineString], [invalid_ids])` | the tuple is an implicit contract between `path_manager`, `gcode_manager` and `visual_manager.add_path` (`len(d) > 2`) | medium, touches the controllers |
| Single configuration object for `MachinePath.cfg`, `GCoder.cfg` and `Macros.DEFAULT_CFG` | the same defaults are copied in three places and a missing key is still a `KeyError` | medium |
| `Geom` / `FakeGeom` as a dataclass with a validated geometry, and `FakeGeom` removed in favour of plain shapely geometries | a degenerate polygon raises a shapely `ValueError` without saying which primitive produced it | low |
| `GcodePoint.get_string` uses 3 decimals while `GCoder.DIGITS` is 4 | two resolutions for the same coordinate | low |

---

## 5. Bench verification checklist

Run these once on the machine before trusting the procedures. Each item can be
undone without consequences.

1. **`$#` format.** Send `$#` from the console and look at the `[TLO:...]` and
   `[PRB:...]` lines:
   * GRBL: `[TLO:0.000]` and `[PRB:0.000,0.000,0.000:1]`;
   * FluidNC: `[TLO:0.000,0.000,0.000]` and the same `[PRB:...]`.
   If the format is different, update `parse_tlo_report` (and the test).
2. **Probe coordinate space.** Touch the probe, read `?` (MPos and WPos) and the
   `[PRB:]` value: `PRB` must equal `MPos` of the same instant, not `WPos`.
   `MacroContext.probe()` assumes machine coordinates.
3. **`G43.1` sign.** Put a dial indicator under the tool, send
   `G43.1 Z10`, then `G0 Z0`: the axis must move **up** by 10 mm (GRBL applies
   the offset to the machine position). If it moves down, invert the sign in
   `_tlo()`.
4. **Two stage probing repeatability.** Run five probing cycles with the fast
   + slow sequence and with the slow only, with a dial indicator on the same
   spot: expected about ±0.005 mm and ±0.02 mm.
5. **Spindle stop timing.** With `spindle_stop_dwell = 1.0`, check that the
   spindle is still when the macro reaches the change position. Increase the
   dwell for big routers.
6. **`M5` on GRBL.** Confirm that `M5` followed by `G4 P1` really stops the
   spindle before `M0` (some VFDs need more time).
7. **Failed probe.** Interrupt the probe (no contact): the console must show the
   "Probe not triggered" error, the measurement must not be used, and after
   M-03 the job must stop cleanly.

---

## 6. Running the tests

```
cd <repo>
PYTHONPATH=src python -m pytest tests/unit -q
```

Required packages: `shapely`, `pyclipper`, `numpy`, `scipy`, `gerbyx`,
`PySide6`, `qimage2ndarray`, `opencv-python-headless` (or `opencv-python`),
`PyOpenGL`, `vispy`, `pytest`, `pytest-qt`. `matplotlib` is not needed
(`plot_stuff.py` is not imported).

`tests/conftest.py` adds `src` and `src/TheAntFarm` to `sys.path`; do not use
`--confcutdir`, or the controller tests cannot import the packages.

---

## 7. Files

| File | Content |
|---|---|
| `shape_core/macros_manager.py` | catalog, context, validation, registry, expansion |
| `shape_core/gcode_manager.py` | `GCodeMacro`: line iterator over the expanded template |
| `macros/*.gcode` | the three procedures |
| `controller/controller_manager.py` | macro start, deferral, abort, streaming |
| `controller/controller_control.py` | `$#` and status report parsing |
| `tests/unit/test_macros_manager.py` | catalog, validation, golden templates |
| `tests/unit/test_controller_manager.py` | start / deferral / abort of the macro |
| `tests/unit/test_controller_control.py` | TLO and PRB report parsing |
