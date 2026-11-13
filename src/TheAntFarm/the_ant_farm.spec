# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# gerbyx is the Gerber/Excellon parser of The Ant Team: shape_core imports its
# submodules, some of them inside functions, so they are collected explicitly.
# The command line interface of gerbyx (and its typer/rich dependency) and the
# matplotlib based visualizer are not used by the application and are kept out
# of the bundle.
_EXCLUDED_GERBYX = ("gerbyx.cli", "gerbyx.__main__", "gerbyx.visualizer")
gerbyx_modules = collect_submodules("gerbyx", filter=lambda name: name not in _EXCLUDED_GERBYX)


a = Analysis(
    ['the_ant_farm.py'],
    pathex=[],
    binaries=[],
    datas=[('controller','controller'),('macros','macros'),('settings_manager','settings_manager'),('shape_core','shape_core'),('ui_manager','ui_manager'),('style_manager.py', '.'),('double_side_manager.py', '.'),('log_manager.py', '.'),('serial_manager.py', '.'),('grbl_simulator.py', '.'),('ui_the_ant_farm.py', '.'),('vispy_qt_widget.py', '.'),('app_resources_rc.py', '.'),('the_ant_farm.ui', '.'),('executable_path_checker.py', '.'),('combobox_filter_enter.py', '.'),('combobox_elide_left.py', '.'),('qledlabel.py', '.'),('qcamera_label.py', '.'),('__init__.py', '.')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtSerialPort', 'PySide6.QtMultimedia', 'PySide6.QtSvg', 'shiboken6.Shiboken', 'vispy', 'vispy.app.backends._pyside6', 'vispy.app.qt', 'pyclipper', 'shapely', 'shapely.ops', 'shapely.validation', 'scipy.interpolate', 'qimage2ndarray', 'cv2', 'OpenGL', 'OpenGL.GL', 'OpenGL.GLU', 'OpenGL.GLUT', 'OpenGL.platform.egl'] + gerbyx_modules,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='the_ant_farm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # PyInstaller applies the icon only on Windows (.exe) and macOS (.app): on
    # Linux an ELF executable has no icon, it comes from the desktop entry in
    # packaging/linux (the window icon is set at runtime through Qt, see the_ant_farm.ui)
    icon='./resources/logo/the_ant_farm_logo.ico',
)
