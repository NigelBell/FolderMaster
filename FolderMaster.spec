# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['FolderMaster.py'],
    pathex=[],
    binaries=[],
    #datas=[('app_logo.ico', '.')],
    datas=[('images', 'images')], #tuple is (source_folder, destination_folder)
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts, 
    [],
    exclude_binaries=True,
    name='FolderMaster',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None, 
    icon='images/app_logo.ico'
)

excluded_files = [
    '_asyncio',
    '_bz2',
    '_ctypes',
    '_decimal',
    '_hashlib',
    '_lzma',
    '_multiprocessing',
    '_overlapped',
    '_queue',
    '_ssl',
    'd3dcompiler_47.dll',
    'libcrypto-1_1.dll',
    'libEGL.dll',
    'libffi-7.dll',
    'libGLESv2.dll',
    'libssl-1_1.dll',
    'MSVCP140.dll',
    'MSVCP140_1.dll',
    'opengl32sw.dll',
    'pyexpat',
    'Qt5DBus.dll',
    'Qt5Network.dll',
    'Qt5Qml.dll',
    'Qt5QmlModels.dll',
    'Qt5Quick.dll',
    'Qt5Svg.dll',
    'Qt5WebSockets.dll',
    'unicodedata',
    'VCRUNTIME140.dll',
    'VCRUNTIME140_1.dll'
]
a.binaries = TOC([x for x in a.binaries if x[0] not in excluded_files])

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas, 
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FolderMaster'
)