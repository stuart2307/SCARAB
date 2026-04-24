from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

block_cipher = None

a = Analysis(
    ['SCARAB.py'],                          # Entry point
    pathex=['.'],
    binaries=[],
    datas=[('Images/**/*', 'Images'),('Modules/*.py', 'Modules'),('SCARAB_Logic/*', 'SCARAB_Logic'),('didyouknow.txt', '.'),('SCARAB_GUI.py', '.'),('GUI_Screens/*', 'GUI_Screens'),('GUI_Wrappers/*', 'GUI_Wrappers')],
    hiddenimports=['PySide6.QtCore','PySide6.QtWidgets','PySide6.QtGui',],
    hookspath=[],
    haskPath=None,
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
    [],
    exclude_binaries=True,
    name='SCARAB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,           # False = no terminal window (GUI app)
    icon='Images/logo.ico',  # Optional: path to your .ico file
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SCARAB',
)

import shutil

shutil.copytree('Images', 'dist/SCARAB/Images', dirs_exist_ok=True)
shutil.copytree('Modules', 'dist/SCARAB/Modules', dirs_exist_ok=True)
shutil.copy('didyouknow.txt', 'dist/SCARAB/didyouknow.txt')