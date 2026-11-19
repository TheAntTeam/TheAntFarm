# Tool change

A job with more than one tool, such as a drill job with several bits, contains `T<n>` and `M6` where the tool
must change. GRBL cannot change tools, so The Ant Farm stops sending the job at the `M6` and runs a tool change
procedure of its own. The **TOOL CHANGE** button runs the same procedure by hand.

Each procedure measures the tool before and after the change with the probe, and corrects the Z of the job by
the difference in length between the two tools. The job then goes on with the new tool at the right depth.

## What happens

1. The spindle stops, and the machine waits **Spindle Stop Dwell** seconds.
2. Z goes up to **Safe Z**, then the machine moves over the probe and measures the old tool: a fast probing
   move, a **Probe Backoff** retract, then a slow measuring move.
3. The machine goes to the **Tool Change** position and waits: the console shows
   "Change the tool, then press Cycle Start".
4. Change the tool and press **PAUSE/RESUME**.
5. The new tool is measured in the same way and the difference is applied.
6. The machine goes back to where the job stopped, restarts the spindle and the job goes on.

With **Hold On Probe** on, the machine also waits before each measurement, to attach the probe clip.

## The three procedures

Choose one in **Settings/Preferences › Jobs/Machine Settings › Tool Change Mode**:

| Mode | Measured on | How the difference is applied | Work zero |
|---|---|---|---|
| `wcs` (default) | the board, at the Tool Probe position | Z of the work zero moved by the difference | changed |
| `tlo` | the board, at the Tool Probe position | tool length offset (`G43.1`) | unchanged |
| `setter` | a fixed tool setter, at the Tool Setter position | tool length offset (`G43.1`) | unchanged |

`tlo` and `setter` keep the work zero you set, and add up the differences of consecutive changes. `setter`
needs a tool setter fixed on the machine bed.

## Settings

All in **Settings/Preferences › Jobs/Machine Settings**, section TOOL CHANGE PROCEDURE:

| Setting | Meaning |
|---|---|
| Tool Probe MPos / WPos | where the tool is measured; **Working Position** chooses work or machine coordinates |
| Get Tool Probe Position | takes the current position of the machine |
| Tool Probe Z Limit | lowest Z of the probing move; past it the probe is considered missed |
| Tool Change MPos | where the machine waits for the change, in machine coordinates |
| Get Tool Change Position | takes the current machine position |
| Tool Setter | position of the tool setter, for the `setter` mode |
| Safe Z MPos | height of the moves, in machine coordinates |
| Probe Backoff | retract between the fast and the slow probing move |
| Spindle Stop Dwell [s] | wait after stopping the spindle, before moving |
| Warn If Not Homed | ask for a confirmation when the machine has not been homed since the connection |

The feed rates of the moves are the XY, Z and Probe feed rates of the FEEDRATES section.

## Homing

The procedures move to absolute machine positions (`G53`). These are right only after a homing cycle: on a
machine with homing switches, home it after connecting. **Warn If Not Homed** (off by default) asks before a
tool change when the machine has not been homed since the connection.

## When something goes wrong

- **The probe does not touch** before the Tool Probe Z Limit: GRBL raises `ALARM:5` and the job stops. Check
  the probe wiring and the limit, then **UNLOCK**.
- **The procedure cannot be prepared** (a missing setting, an unreadable procedure file): the job stops before
  any move and the console says why.

The procedures are G-code files in the `macros` folder. They are described for developers in
[Macros](../dev/macros.md).
