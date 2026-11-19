# Testing

## Setup

```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## Running the tests

```bash
python -m pytest tests -v
python -m pytest tests -v --cov=src/TheAntFarm --cov-report=term-missing
python -m pytest tests/unit/test_controller_manager.py -v
python -m pytest tests -k "alarm" -v
```

| Folder | Content |
|---|---|
| `tests/unit/` | one file per module, named after it (`test_<module>.py`) |
| `tests/integration/` | the whole chain, from a Gerber file to G-code |
| `tests/test_data/` | sample Gerber, Excellon and G-code files |
| `tests/conftest.py` | shared fixtures |

The UI tests create real widgets; `conftest.py` sets `QT_QPA_PLATFORM=offscreen`, so they also run without a
display.

## Formatting and linting

CI runs Ruff, as a non-blocking step:

```bash
ruff check src tests
ruff format --check --diff src tests
```

`ruff format src tests` formats the files. The generated files (`ui_the_ant_farm.py`, `app_resources_rc.py`)
and the vendored ones (`hook-vispy.py`, `vispy_qt_widget.py`) are excluded.

## CI

`.github/workflows/python-app.yml` runs the tests on Linux, Windows and macOS with Python 3.10 and 3.12 and
uploads the coverage to Codecov. A pull request gets a Codecov comment with the lines it leaves untested.

## The GRBL simulator

`GrblSimulator` (`src/TheAntFarm/grbl_simulator.py`) runs on simulated time and needs no Qt event loop: write
bytes with `receive()`, let time pass with `advance(seconds)` and read the replies with `read_output()`. It
follows the timing of GRBL 1.1h; what it simulates is listed in [GRBL simulator](../user/simulator.md#what-it-simulates).

`tests/unit/test_grbl_simulator.py` tests the simulator and streams jobs through the real `ControllerWorker`;
`tests/unit/test_controller_manager.py` uses it for the alarm, homing and tool change sequences.

## Screenshots

`tools/ui_screenshots.py` starts the application with sample data and saves a screenshot of every tab in the
dark and light themes:

```bash
python tools/ui_screenshots.py --out ui_screenshots
```

The **UI screenshots** workflow does the same on the three systems; run it from the Actions page, or add the
`screenshots` label to a pull request.
