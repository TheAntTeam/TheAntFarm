# Running a job

The **CONTROL** tab connects to the machine, moves it, sets the work zero and sends the jobs. The Ant Farm
talks to controllers with GRBL 1.1 firmware over a serial port.

The machine buttons are in the column on the right:

| Button | Action |
|---|---|
| **HOME** | homing cycle (`$H`), on machines with limit switches |
| **UNLOCK** | clears an alarm (`$X`) |
| **PLAY** | starts the selected job |
| **PAUSE/RESUME** | feed hold, then cycle start |
| **STOP** | stops the job |
| **TOOL CHANGE** | runs the [tool change](tool-change.md) procedure by hand |
| **SOFT RESET** | resets the controller; it also stops any move at once |

The status next to them shows the state of the machine (Idle, Run, Hold, Alarm, ...).

## Connecting

1. Connect the machine and switch it on.
2. In the connection box, press **Refresh**, choose the serial port and the baud rate (115200 for GRBL).
3. Press **Connect**. The status changes from "Not Connected" to the state of the machine.

With no port listed, see [Troubleshooting](troubleshooting.md#the-machine-does-not-connect). To try the
application without a machine, use the [GRBL simulator](simulator.md).

If the machine starts in Alarm, home it with **HOME**, or press **UNLOCK** on a machine without limit
switches.

## Moving the machine

The **Sender › Jog** tab moves the machine:

- the arrows move X and Y, **Z+** and **Z-** move Z;
- **XY step** and **Z step** set the length of each move; **x10**, **/10**, **+1.0** and **-1.0** change it;
- **Center** goes to X = 0, Y = 0 of the work zero.

The position is shown above, as machine position (**MPos**) and work position (**WPos**, from the work zero).

## Setting the work zero

The jobs are drawn from the work zero: X = 0, Y = 0 is the corner of the board, Z = 0 the copper surface.

1. Jog the tool to the corner of the board and press **XY = 0** (or **X = 0** and **Y = 0**).
2. Bring the tool down to the copper and press **Z = 0**, or use the probe (below).

Each button asks for a confirmation, unless Confirm Work Zero is off in the [settings](settings.md).

### Probing Z

With a probe connected (a clip on the tool and the board as contact), the **Sender › Probe/Terminal** tab finds
the copper surface:

- **PROBE** moves Z down until the contact, at most to the **Min** Z, and shows the result;
- with **Z=0 After Probe** in the [settings](settings.md#jobsmachine-settings), the touched height becomes Z = 0;
- with **Hold On Probe**, the machine waits for cycle start before probing, so you can attach the clip.

### Bed levelling (ABL)

A board is never perfectly flat. **ABL** probes a grid of points and corrects the Z of the job with the
measured heights:

1. Select the job, then press **GET BBOX** to take the area of the job (or type **Min** and **Max** of X and Y).
2. Choose the number of points per axis (**N**); **Step** shows the distance between them.
3. Press **ABL** and wait for the end of the probing.

The correction is applied to the selected job and drawn in the view.

## Sending a job

1. In the **GCode** tab, add the files: **Add generated G-code** takes the jobs made in
   [Creating a job](creating-a-job.md), **Open G-code files** any `.gcode` or `.nc` file, **Remove selected**
   takes them out of the list.
2. Select the job to send. It is drawn in the view, over the work area.
3. Press **PLAY**. A confirmation shows the area of the job from the work zero and the current position:
   check the work zero, the tool and the spindle, then press **Start**.

The progress bar shows the part of the job sent and the elapsed time.

### During the job

- **PAUSE/RESUME** holds the machine and starts it again.
- **STOP** holds the machine, waits for it to stop, then resets the controller and ends the job.
- The **Feed**, **Spindle** and **Rapid** overrides, on the Jog tab, change the speeds while the job runs.
  Feed and Spindle go from 10 % to 200 %, Rapid can be 25 %, 50 % or 100 %.
- An `M6` in the job starts the [tool change](tool-change.md).

### When the machine rejects a line

If the controller refuses a line of the job (an `error:` reply), the job is put on hold, the spindle stops and a
window shows the line:

- **Resume** restarts the spindle and, after the Spindle Restart Delay, goes on **without** that line: the
  machine moves straight to the next point;
- **Stop** ends the job.

### When the machine raises an alarm

An alarm (a missed probe, a limit switch, ...) stops the job at once, and the console shows
"Machine alarm (ALARM:n). Job stopped." Find the cause, then **UNLOCK** or **HOME** before going on: see
[Troubleshooting](troubleshooting.md#alarms-and-errors).

## The console

**Console › Hide/Show Console** shows the messages exchanged with the machine. The **Probe/Terminal** tab sends
a command typed by hand (**Send**) and clears the console (**Clear**). **Console › Set Level** chooses how many
messages of the application are shown.
