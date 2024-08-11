# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['the_ant_farm.py'],
    pathex=[],
    binaries=[],
    datas=[('controller','controller'),('macros','macros'),('resources','resources'),('settings_manager','settings_manager'),('shape_core','shape_core'),('ui_manager','ui_manager'),('style_manager.py', '.'),('double_side_manager.py', '.'),('log_manager.py', '.'),('serial_manager.py', '.'),('ui_the_ant_farm.py', '.'),('vispy_qt_widget.py', '.'),('app_resources_rc.py', '.'),('the_ant_farm.ui', '.'),('serial_manager.py', '.'),('executable_path_checker.py', '.'),('combobox_filter_enter.py', '.'),('qledlabel.py', '.'),('qcamera_label.py', '.')],
    hiddenimports=['PySide2.QtCore', 'PySide2.QtGui', 'PySide2.QtSerialPort', 'shiboken2.shiboken2', 'vispy', 'vispy.app.backends._pyside2', 'vispy.app.qt', 'gerber', 'pyclipper', 'shapely', 'shapely.ops', 'shapely.validation', 'scipy.interpolate', 'qimage2ndarray', 'cv2'],
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
)
