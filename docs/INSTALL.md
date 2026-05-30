# Installation Guide

## Prerequisites

- **Python 3.10 – 3.12** (3.12 recommended for builds)
- **pip** (comes with Python)
- **virtual environment** (recommended)
- **Git** (to clone the repository)

---

## Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/TheAntTeam/TheAntFarm.git
cd TheAntFarm
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python src/TheAntFarm/the_ant_farm.py
```

---

## Platform-Specific Notes

### Linux

Install system libraries required by PySide6:

```bash
sudo apt-get install -y \
  libegl1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
  libxcb-xinerama0 libxcb-xfixes0 libxcb-cursor0 \
  libxkbcommon-x11-0 libgl1-mesa-dev libegl1-mesa-dev \
  libxcb1 libx11-xcb-dev libglu1-mesa-dev libxrender-dev \
  libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
```

### Windows

- The application auto-configures the Qt plugin path for PySide6.
- If using a build environment, ensure Visual Studio Build Tools are installed.

### macOS

- Executable generation for ARM64 (Apple Silicon) is temporarily unavailable.
- The application runs natively using Python.

---

## Building an Executable

To build a standalone executable with PyInstaller:

```bash
pip install pyinstaller
cd src/TheAntFarm
pyinstaller the_ant_farm.spec
```

The executable will be created in `src/TheAntFarm/dist/`.

---

## Running Tests

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Run all tests:

```bash
python -m pytest tests -v
```

Run with coverage:

```bash
python -m pytest tests -v --cov=src/TheAntFarm --cov-report=term-missing
```

---

## Troubleshooting

### PySide6 multimedia bug (Windows)

If you encounter issues with camera functionality, see [Qt bug PYSIDE-2935](https://bugreports.qt.io/browse/PYSIDE-2935). The application includes a workaround for this.

### Import errors

Ensure you are in the project root directory when running the application and that the virtual environment is activated.

### Serial port not found

- Check that your CNC machine is connected and powered on.
- On Linux, ensure your user has permission to access serial devices (`dialout` group).
- Use the virtual serial port for testing without hardware.
