# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Localizar la carpeta libs de pyreportjasper
_venv_sp = os.path.join('.venv', 'Lib', 'site-packages')
_pyreportjasper_dir = os.path.join(_venv_sp, 'pyreportjasper')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Resources', 'Resources'),
        ('Views', 'Views'),
        ('Models', 'Models'),
        ('Controllers', 'Controllers'),
        ('reports', 'reports'),
        ('translations', 'translations'),
        ('reloj_digital.py', '.'),
        (os.path.join(_pyreportjasper_dir, 'libs'), os.path.join('pyreportjasper', 'libs')),
    ],
    hiddenimports=['pyreportjasper', 'pyreportjasper.pyreportjasper', 'pyreportjasper.config', 'pyreportjasper.db', 'pyreportjasper.report', 'pyreportjasper.application_class_path'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GestionTorneoFutbol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GestionTorneoFutbol',
)
