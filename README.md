# The Ant Farm

[![Python 3.10 | 3.12](https://img.shields.io/badge/python-3.10%20|%203.12-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/TheAntTeam/TheAntFarm/actions/workflows/python-app.yml/badge.svg)](https://github.com/TheAntTeam/TheAntFarm/actions/workflows/python-app.yml)
[![Codecov](https://codecov.io/gh/TheAntTeam/TheAntFarm/branch/main/graph/badge.svg)](https://codecov.io/gh/TheAntTeam/TheAntFarm)
[![Version](https://img.shields.io/github/v/release/TheAntTeam/TheAntFarm)](https://github.com/TheAntTeam/TheAntFarm/releases)

**The Ant Farm** simplifies PCB manufacturing using CNC machines. It combines CAM features with machine control in a single application — import Gerber/Excellon files, generate G-code, and control GRBL-based CNC machines.

---

## Features

- **Load** Gerber (top, bottom, profile) and Excellon (drill) files and look at the layers from either side.
- **Create jobs**: isolation milling with several passes, board cut-out with tabs, drilling with several bits
  and milling of the large holes, with an optimised order of the holes.
- **Control** a GRBL 1.1 machine over a serial port: jog, work zero, probing, bed levelling, feed, spindle and
  rapid overrides, progress of the job.
- **Tool change** procedures with probing, for jobs with more than one tool.
- **Align** the bottom side of double-sided boards, with a camera or with the tool.
- **GRBL simulator**, to try everything without a machine.
- Windows, Linux and macOS, dark and light themes.

Tested with Gerber and drill files from Autodesk Eagle and KiCad, on machines with GRBL 1.1.

---

## Getting started

- [Installation](docs/user/install.md)
- [Quick start](docs/user/quick-start.md): from a Gerber file to a milled board

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

The [documentation](docs/index.md) has a user guide (installation, jobs, machine control, tool change,
alignment, settings, troubleshooting) and a developer guide (architecture, CAM core, macros, testing, releasing).

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
