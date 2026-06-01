# The Ant Farm

[![Python 3.10 | 3.12](https://img.shields.io/badge/python-3.10%20|%203.12-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/TheAntTeam/TheAntFarm/actions/workflows/python-app.yml/badge.svg)](https://github.com/TheAntTeam/TheAntFarm/actions/workflows/python-app.yml)
[![Codecov](https://codecov.io/gh/TheAntTeam/TheAntFarm/branch/main/graph/badge.svg)](https://codecov.io/gh/TheAntTeam/TheAntFarm)
[![Version](https://img.shields.io/github/v/release/TheAntTeam/TheAntFarm)](https://github.com/TheAntTeam/TheAntFarm/releases)

**The Ant Farm** simplifies PCB manufacturing using CNC machines. It combines CAM features with machine control in a single application — import Gerber/Excellon files, generate G-code, and control GRBL-based CNC machines.

---

## Features

### View Tab
- Import Gerber (TOP, BOTTOM) and Excellon (DRILL, EDGE) files
- Visualize and inspect PCB layers
- Generate optimized G-code from imported designs

### Control Tab
- Connect to CNC machines via serial port (GRBL v1.1)
- Load and execute G-code files
- Real-time progress tracking with elapsed time and percentage
- Tool change automation and feedrate control

### Align Tab
- Double-sided PCB alignment using camera
- Manual point selection and optical alignment
- Path optimization algorithms (genetic, nearest insertion, 2-opt)

### Development & Testing
- Virtual serial port simulator for testing G-code without hardware
- Cross-platform: Windows, Linux, macOS

---

## Development Status

**Version 0.3.2** — active development.

| Tab | Status | Notes |
|-----|--------|-------|
| **View** | Stable | Gerber import, gcode generation, visualization |
| **Control** | Functional | GRBL v1.1 control, gcode execution, progress tracking |
| **Align** | Functional | Double-sided alignment via camera, path optimization |

**Compatibility:** Tested with Gerber/drill files from Autodesk Eagle and KiCad EDA. CNC machines using GRBL v1.1 firmware.

---

## Screenshots
<!-- TODO: Add screenshots -->
<!-- ![Main UI](docs/images/screenshot.png) -->

---

## Installation

See [docs/INSTALL.md](docs/INSTALL.md) for prerequisites and setup instructions.

---

## Quick Start

1. **Import** a Gerber file — the View tab renders the PCB
2. **Configure tools** — set tool diameter, feed rate, depths
3. **Generate G-code** — export to a `.nc` file
4. **Connect CNC** — select port and baud rate in the Control tab
5. **Run** — load the G-code and start machining

---

## Project Structure

```
src/TheAntFarm/
├── the_ant_farm.py              # Application entry point
├── controller/
│   ├── controller_manager.py    # Main controller orchestrator
│   ├── controller_view.py       # View tab logic
│   ├── controller_control.py    # Control tab logic
│   ├── controller_align.py      # Alignment tab logic
│   └── controller_signals.py    # Signal definitions
├── serial_manager.py            # Serial port communication
├── virtual_serial_port.py       # GRBL simulator (dev/testing)
├── settings_manager/
│   ├── settings_manager.py      # Settings coordinator
│   ├── settings_app.py          # Application settings
│   ├── settings_machine.py      # Machine configuration
│   ├── settings_job.py          # Job parameters
│   └── settings_gcode_files.py  # G-code file settings
├── ui_manager/
│   ├── ui_manager.py            # Main UI coordinator
│   ├── ui_view_load_layer_tab.py
│   ├── ui_control_tab.py
│   ├── ui_align_tab.py
│   └── ui_settings_preferences.py
├── shape_core/                  # Gerber/shape processing engine
├── resources/                   # Application resources
└── configurations/              # User configuration files
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language  | Python 3.10 – 3.12 |
| UI        | PySide6 (Qt6) |
| 3D Rendering | vispy / PyOpenGL |
| CNC Protocol | GRBL v1.1 |
| PCB Parsing | gerbyx |
| Image Processing | OpenCV |
| Math/Numerics | numpy, scipy, Shapely |

---

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md) — Installation guide
- [CHANGELOG.md](CHANGELOG.md) — Release history
- [CONTRIBUTING.md](CONTRIBUTING.md) — Contributor guide
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community guidelines
- [SECURITY.md](SECURITY.md) — Security policy
- [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature request](.github/ISSUE_TEMPLATE/feature_request.md)
- [Improvement](.github/ISSUE_TEMPLATE/improvement.md)

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, code style, testing, and pull request guidelines. All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## Credits

**The Ant Team** — [GitHub](https://github.com/TheAntTeam)

---

## Disclaimer

The providers of this software decline any responsibility for damages to persons or things deriving from its use, and they will not be liable for any damages you may suffer in connection with using, modifying, or distributing this software.

---

## Donation

This project requires a lot of work and often expensive hardware for testing (CNC machines). Please consider a safe, secure and highly appreciated donation via the PayPal link below.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=BTRCVPZUZYW2E)
