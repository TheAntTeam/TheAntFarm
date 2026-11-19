# Architecture

The Ant Farm is a PySide6 (Qt 6) desktop application in `src/TheAntFarm`. It has three parts: the CAM core,
which turns PCB files into G-code; the controller, which talks to the machine; and the user interface.

## Threads

```
          main thread                      control thread                 serial thread
  +---------------------------+     +-------------------------+     +----------------------+
  | MainWindow, ui_manager/*  | <-> | ControllerWorker        | <-> | SerialWorker         |
  | vispy views               |     | (controller_manager.py) |     | (serial_manager.py)  |
  +---------------------------+     +-------------------------+     +----------------------+
           signals and slots          serialTxQueue / serialRxQueue        QSerialPort or
                                                                           GrblSimulator
```

- `the_ant_farm.py` builds the window, moves `ControllerWorker` and `SerialWorker` to their own `QThread`
  and connects them.
- The UI and the controller talk with signals and slots. The UI also reads a few attributes of the worker
  directly (for example `homed`, `get_gcode_bbox`).
- The controller and the serial worker exchange lines through two queues. The serial worker writes and
  reads the port; with the [GRBL simulator](../user/simulator.md) selected, it talks to `GrblSimulator`
  instead of a port.

## Packages

| Package or file | Content |
|---|---|
| `shape_core/` | CAM core, without Qt: Gerber and Excellon parsing, toolpaths, G-code writing and reading, alignment, bed levelling, tool change macros. See [shape_core](shape_core.md). |
| `controller/` | `ControllerWorker` and the controllers of the tabs: streaming, status reports, probing, alignment data |
| `ui_manager/` | one class per tab (`ui_view_load_layer_tab.py`, `ui_create_job_tab_manager.py`, `ui_control_tab.py`, `ui_align_tab.py`, `ui_settings_preferences.py`) and `ui_manager.py`, which wires them |
| `settings_manager/` | the four `.ini` files of `configurations/`: application, machine, jobs, G-code folder |
| `macros/` | the tool change procedures, see [Macros](macros.md) |
| `serial_manager.py` | `SerialWorker` |
| `grbl_simulator.py` | simulated GRBL 1.1 controller |
| `the_ant_farm.ui` | the window, edited with Qt Designer; `ui_the_ant_farm.py` is generated from it |
| `app_resources.qrc` | icons and images; `app_resources_rc.py` is generated from it |
| `style_manager.py` | dark and light themes |

`ui_the_ant_farm.py` and `app_resources_rc.py` are generated: change the `.ui` or the `.qrc` and regenerate
them with `python build.py ui` from `src/TheAntFarm`, never edit them by hand.

## Streaming a job

`ControllerWorker` sends one line of the job and waits for its `ok` before sending the next. So at most one
line is waiting in the controller, and an `error:` or an `ALARM:` always refers to a known line:

- `ALARM:n` stops the job;
- `error:9` (G-code locked in alarm) stops the job;
- any other `error:` holds the machine and asks the user to resume without the line or to stop.

An `M6` in the job is not sent: it starts the tool change macro, which is expanded and sent line by line in
the same way. See [Macros](macros.md).

## Data folders

`executable_path_checker.py` finds the folder of the application. `configurations/`, `gcode_temp_dir/` and
`macros/` live there; for an executable, `macros/` is copied there on the first start.
