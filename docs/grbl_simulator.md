# GRBL simulator

The Ant Farm can connect to a simulated GRBL 1.1 controller, to try the sender
and test changes without a machine. The simulator lives in
`src/TheAntFarm/grbl_simulator.py`.

## Enabling it

In `Settings/Preferences -> Application Settings`, under `SERIAL SETTINGS`,
check `GRBL Simulator: List in the serial ports`, choose the `GRBL Simulator
Speed` and press `Save Settings/Preferences`. The port list in the Control tab then ends with
`GRBL simulator`; choose it and press Connect. The real ports keep working as
before.

The speed is how many times faster than real time the machine moves: `1` is
real time, `10` ten times faster (from `0.1` to `100`). A new speed applies at
once, also while connected. Unchecking the setting removes the simulator from
the list; a connection already open to it stays open until Disconnect.

The settings are stored as `grbl_simulator_enabled` and `grbl_simulator_speed`
in the `[GENERAL]` section of `app_config.ini`; the simulator is off by default.

## What it simulates

It follows the GRBL 1.1h source, so the timing seen by the sender is the real
one:

- `ok` is sent when a line is queued in the planner (15 blocks), not when it is
  executed. A line that needs the machine to be still (`G4`, `M0`, `M3`/`M5`,
  `G10`, `G92`, `G38.x`, ...) gets its `ok` only after the previous moves.
- `$#`, `$H`, `$I`, `$N` and settings are refused with `error:8` unless the
  machine is idle (or in alarm).
- Feed hold reports `Hold:1` while decelerating and `Hold:0` when complete. While
  the hold is complete no new line is read, so no `ok` arrives until cycle start.
  Cycle start is ignored during the deceleration.
- The spindle stop override (`0x9E`) works only on hold; cycle start restores
  the spindle.
- A soft reset while moving raises `ALARM:3` and the machine must be unlocked
  with `$X`; a reset after a complete hold raises nothing.
- Probing stops at the contact and reports `[PRB:x,y,z:1]`, or raises `ALARM:5`
  when nothing is touched (`G38.2`). The probe touches at machine Z `-5` by
  default.
- Status reports use the GRBL 1.1 format, with `WCO` and `Ov` refreshed as GRBL
  does, and `$10` selects machine or work position.
- G-code errors (`error:20`, `error:22`, ...), lines longer than 80 characters
  (`error:11`) and the 128 byte serial buffer (characters beyond it are lost).

It is simplified: moves run at constant speed (no acceleration), arcs move along
their chord in the time of the arc, homing is enabled but the machine starts
unlocked, and limit switches, safety door, check mode (`$C`), sleep and startup
lines are not simulated.

## Simulator commands

Lines starting with `$SIM=` control the simulator; they get no `ok`, so they can
be typed in the sender console while a job runs:

| Command | Effect |
|---|---|
| `$SIM=ERROR:20` | The next G-code line is rejected with `error:20` |
| `$SIM=ALARM:1` | `ALARM:1` now (hard limit: only a reset is accepted) |
| `$SIM=PROBE:-2` | The probe touches at machine Z `-2` |

## In tests

`GrblSimulator` runs on simulated time and needs no Qt event loop: write bytes
with `receive()`, let time pass with `advance(seconds)` and read the replies
with `read_output()`. See `tests/unit/test_grbl_simulator.py`, which also
streams jobs through the real `ControllerWorker`.
