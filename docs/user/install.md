# Installation

The Ant Farm runs on Windows, Linux and macOS. It can be used as a ready-made executable or run from the
sources with Python.

## Executable

The [releases page](https://github.com/TheAntTeam/TheAntFarm/releases) has an archive for each system. Extract
it in a folder where you can write: the application keeps its settings (`configurations/`), the generated
G-code (`gcode_temp_dir/`) and the tool change procedures (`macros/`) next to the executable.

On Linux the executable needs the OpenGL libraries of the 3D view:

```bash
sudo apt install libglu1-mesa freeglut3
```

### Linux: launcher icon

The Linux archive contains the executable, the `the_ant_farm.desktop` entry and the icons of the theme. An
ELF executable cannot carry an icon, so the launcher gets it from the desktop entry; the icon of the
application window is embedded and works without this step.

```bash
tar -xzf the_ant_farm-linux.tar.gz -C ~/.local/opt/the_ant_farm
ln -s ~/.local/opt/the_ant_farm/the_ant_farm ~/.local/bin/the_ant_farm   # must be in PATH

# desktop entry and icon theme (the size of the icons is in the folder name)
cp ~/.local/opt/the_ant_farm/the_ant_farm.desktop ~/.local/share/applications/
cp -r ~/.local/opt/the_ant_farm/icons/* ~/.local/share/icons/hicolor/
update-desktop-database ~/.local/share/applications 2>/dev/null || true
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor 2>/dev/null || true
```

If the executable is not in `PATH`, replace `Exec=the_ant_farm` in the desktop entry with its absolute path.
The same entry makes the icon appear in the application menu and in the dock of GNOME, KDE and Xfce.

## From the sources

You need Python 3.10, 3.11 or 3.12, and Git (or the zip of the repository).

1. Get the code:

   ```bash
   git clone https://github.com/TheAntTeam/TheAntFarm.git
   cd TheAntFarm
   ```

2. Create a virtual environment and activate it.

   Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Linux and macOS:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python src/TheAntFarm/the_ant_farm.py
   ```

Activate the virtual environment again in each new terminal before starting the application.

### Linux: system libraries

PySide6 and the 3D view need these libraries (Debian and Ubuntu names):

```bash
sudo apt-get install -y \
  libegl1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
  libxcb-xinerama0 libxcb-xfixes0 libxcb-cursor0 \
  libxkbcommon-x11-0 libgl1-mesa-dev libegl1-mesa-dev \
  libxcb1 libx11-xcb-dev libglu1-mesa-dev libxrender-dev \
  libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
```

### VS Code

1. **File › Open Folder** and choose the `TheAntFarm` folder.
2. **Terminal › New Terminal**, then create and activate the virtual environment as in step 2 above.
3. Open `src/TheAntFarm/the_ant_farm.py`. If the status bar does not show the interpreter of `venv`, click
   the Python version there and choose it.
4. Install the packages and start the application as in steps 3 and 4.

### macOS

The macOS archive contains an executable for Apple Silicon (arm64). It is a plain executable, not an `.app`
bundle (see [#133](https://github.com/TheAntTeam/TheAntFarm/issues/133)), it is not signed, and it has not been
tried on a Mac yet. If it does not start, run the application from the sources as described above.

## Linux: access to the serial port

If connecting to the machine fails with "permission denied", add your user to the `dialout` group:

```bash
sudo usermod -a -G dialout $USER
```

Log out and in again, then check that `dialout` is listed by:

```bash
groups $USER
```

On some distributions ModemManager also grabs the USB serial adapters as they are plugged in. If the port
is still busy, disable it and reboot:

```bash
sudo systemctl disable ModemManager.service
```

## Next

[Quick start](quick-start.md) goes from a Gerber file to a milled board.
