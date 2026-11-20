# Notes for coding agents

Read these first; this file only adds what is easy to get wrong:

- [CONTRIBUTING.md](CONTRIBUTING.md): setup, Ruff, mypy, pull requests.
- [docs/dev/](docs/dev/): architecture, testing, releasing, G-code generation, macros.

## Branches and pull requests

- Branch from `dev` (`feature/...`, `bugfix/...`, `refactor/...`) and open the pull request into `dev`.
- Never edit `CHANGELOG.md` in a branch. Write the changelog lines under a `## Changelog` heading in the pull
  request description; the release workflow collects them (see `docs/dev/releasing.md`).

## Generated and vendored files

- `ui_the_ant_farm.py` and `app_resources_rc.py` are generated: change `the_ant_farm.ui` or
  `app_resources.qrc` and regenerate, never edit them by hand.
- `python build.py ui` runs the `pyside6-uic` found on the `PATH`. It must be the one of the virtual
  environment, with the same version as `PySide6` in `requirements.txt`; another version rewrites the whole
  file. Check that the diff of `ui_the_ant_farm.py` only holds the lines you changed in the `.ui`.
- `hook-vispy.py` and `vispy_qt_widget.py` come from third parties. Ruff and coverage skip all four files
  (`pyproject.toml`).

## Checks before a pull request

```bash
python -m pytest tests -q
ruff check src tests
ruff format --check src tests
```

The UI tests run off-screen (`QT_QPA_PLATFORM=offscreen` in `tests/conftest.py`). Tests must pass on Linux,
Windows and macOS with Python 3.10 and 3.12.

## G-code

The generated G-code is run by GRBL or FluidNC on a real machine: a wrong value can move the spindle into the
board or the clamps. When changing `shape_core/gcode_manager.py` or the macros, test the output lines, not only
that generation succeeds.
