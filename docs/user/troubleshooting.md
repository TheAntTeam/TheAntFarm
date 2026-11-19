# Troubleshooting

## The application does not start

- From the sources: activate the virtual environment first, and start it from the folder of the repository
  ([Installation](install.md#from-the-sources)).
- On Linux: install the system libraries listed in [Installation](install.md#linux-system-libraries).
- On Windows, a problem with the camera of the Align tab can come from a PySide6 bug
  ([PYSIDE-2935](https://bugreports.qt.io/browse/PYSIDE-2935)); the application includes a workaround.

The log of the application is in `app_logs/app_logs.log`, next to the application.

## The machine does not connect

- Check that the machine is connected and switched on, then press **Refresh**.
- Choose the right baud rate: 115200 for GRBL.
- On Linux, "permission denied" means your user cannot open the port: see
  [Installation](install.md#linux-access-to-the-serial-port).
- Close other programs that use the port (another sender, a serial monitor, the Arduino IDE).
- To try the application without a machine, use the [GRBL simulator](simulator.md).

If the connection drops during use, the console shows serial errors. After **Serial Error Critical
Threshold** consecutive errors the port is closed ([Settings](settings.md#application-settings)): check the
USB cable, and keep it away from the spindle and motor wires.

## Alarms and errors

GRBL answers each line with `ok` or with `error:n`, and reports a serious problem with `ALARM:n`. An alarm
stops the job and locks the machine: every line is then refused with `error:9` until **UNLOCK** or **HOME**.

### Alarms

| Alarm | Meaning | What to do |
|---|---|---|
| `ALARM:1` | hard limit: a limit switch was hit | move away from the switch, then **HOME**; check the work zero and the size of the job |
| `ALARM:2` | soft limit: the move would leave the machine area | check the work zero and the size of the job |
| `ALARM:3` | reset while moving: the position may be lost | **HOME** before going on |
| `ALARM:4` | probe already in contact before probing | check the probe and its wiring |
| `ALARM:5` | probe did not touch anything | check the probe, its wiring and the probing limit |
| `ALARM:6`–`9` | homing failed | check the limit switches and the homing settings of the controller |

After `ALARM:4` and `ALARM:5` the position is still right; after the others, home the machine.

### Errors

| Error | Meaning |
|---|---|
| `error:8` | a `$` command was sent while the machine was moving |
| `error:9` | the machine is locked by an alarm: **UNLOCK** or **HOME** |
| `error:20` | a G-code the controller does not support (`M6` is handled by the application) |
| `error:22` | feed rate missing: the line has no `F` and none was set before |
| `error:33` | the move has an invalid target, often an arc that cannot be drawn |

The full list is in the
[GRBL documentation](https://github.com/gnea/grbl/blob/master/doc/markdown/interface.md).

During a job, a rejected line holds the machine and asks whether to go on without it: see
[Running a job](running-a-job.md#when-the-machine-rejects-a-line).

## A job is in the wrong place or at the wrong depth

- The job is drawn from the work zero: set X = 0, Y = 0 on the corner of the board and Z = 0 on the copper
  ([Running a job](running-a-job.md#setting-the-work-zero)).
- The confirmation of **PLAY** shows the area of the job and the current position: compare them before
  starting.
- After a tool change, check the probe positions of the [tool change](tool-change.md#settings).
- If the copper is not removed evenly, use the [bed levelling](running-a-job.md#bed-levelling-abl).
- On the bottom side, apply the [alignment](alignment.md) and check the Mirroring axis.
