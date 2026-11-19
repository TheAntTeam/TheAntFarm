# Settings

The settings are in the **Settings/Preferences** tab, which is hidden by default: show it with
**File › Show Settings/Preferences**.

Changes apply when you press **Save Settings/Preferences**. **Restore Settings/Preferences** goes back to the
last saved values. Closing the application with unsaved changes asks whether to save them.

The settings are stored in the `configurations` folder, next to the application:

| File | Content |
|---|---|
| `app_config.ini` | application settings, window, last folders |
| `machine_config.ini` | machine, probe and tool change settings |
| `jobs_sets_config.ini` | settings of each job, from the [Create Job](creating-a-job.md) tab |
| `gcode_files_config.ini` | folder of the generated G-code (`gcode_temp_dir` by default) |

## Application Settings

| Setting | Meaning |
|---|---|
| LAYER COLORS | colour of each layer in the views |
| Serial Error Warning Threshold | consecutive serial errors before a warning (default 3) |
| Serial Error Critical Threshold | consecutive serial errors before the port is closed (default 10) |
| GRBL Simulator | lists a simulated machine among the serial ports, see [GRBL simulator](simulator.md) |
| GRBL Simulator Speed | how much faster than real time the simulator moves |
| Confirm Play | ask before starting a job |
| Confirm Homing | ask before a homing cycle |
| Confirm Tool Change | ask before a tool change started with the TOOL CHANGE button |
| Confirm Work Zero | ask before the X = 0, Y = 0, Z = 0 buttons |

The confirmations are on by default. Each question says where it can be turned off.

## Jobs/Machine Settings

| Setting | Meaning |
|---|---|
| Mirroring axis | how the bottom side jobs are mirrored: X (top-down) or Y (left-right) |
| FEEDRATES | XY, Z and probing feed rates of the probe and of the tool change |
| Hold On Probe | wait for cycle start before each probing move, to attach the probe clip |
| Z=0 After Probe | set Z = 0 at the touched height after the PROBE button |
| TOOL CHANGE PROCEDURE | see [Tool change](tool-change.md#settings) |
| Spindle Restart Delay [s] | time given to the spindle to get back to speed after a [rejected line](running-a-job.md#when-the-machine-rejects-a-line) |

## Alignment Settings

| Setting | Meaning |
|---|---|
| Alignment Drill diameter [mm] | stored, not used by the application yet |
| Get Tool Camera Offset | stores the distance between the tool and the camera, see [Alignment](alignment.md#before-starting) |
| Flip Camera Horizontally / Vertically, Rotate Camera | orientation of the camera image |

## Menus

| Menu | Item |
|---|---|
| File | Show Align Tab, Show Settings/Preferences, Save Settings |
| Console | Hide/Show Console, Set Level (how many application messages are shown) |
| Style | Dark or Light theme |
| Help | About |
