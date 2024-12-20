# sailor_tools.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['C:\\Users\\pkroll\\projects\\sailor-sleep\\src'],
    binaries=[],
    datas=[
        ('src/images/*.png', 'images'),
        ('src/images/*.ico', 'images'),
        ('src/Globals.py', '.'),  # Include Globals.py
        ('src/Utilities.py', '.'),  # Include Utilities.py
        ('src/ConfigManager.py', '.'),  # Include ConfigManager.py
        ('src/Routines.py', '.'),  # Include Routines.py
        ('src/Input.py', '.'),  # Include Input.py
        ('src/Display.py', '.'),  # Include Display.py
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sailor-sleep',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)