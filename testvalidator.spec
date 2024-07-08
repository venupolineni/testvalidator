# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['code/testvalidator.py'],  # Check and ensure this is the correct path to your main script
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openai', 'six'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(
    a.pure,  # Pure Python modules
    a.zipped_data,  # Python modules compressed into a .zip
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,  # Python scripts
    a.binaries,  # Non-Python binaries
    a.datas,  # Data files included in the distribution
    [],
    name='testvalidator',
    debug=False,  # Toggle this to True if you need to debug the executable
    bootloader_ignore_signals=False,
    strip=False,  # Set to True to reduce the size of the executable
    upx=True,  # Use UPX to compress the executable
    upx_exclude=[],  # List of files to exclude from UPX compression
    runtime_tmpdir=None,  # Temporary directory for the runtime, or None to use the default
    console=True,  # Set to False for windowed applications
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)