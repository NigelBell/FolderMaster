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
    excludes=[
        "distutils"

    ],
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

coll = COLLECT(
    exe,
    a.binaries - TOC([
        ('_asyncio', None, None),
        ('_bz2', None, None),
        ('_ctypes', None, None),
        ('_decimal', None, None),
        ('_hashlib', None, None),
        ('_lzma', None, None),
        ('_multiprocessing', None, None),
        ('_overlapped', None, None),
        ('_queue', None, None),
        ('_ssl', None, None),
        ('d3dcompiler_47.dll', None, None),
        ('libcrypto-1_1.dll', None, None),
        ('libEGL.dll', None, None), #CAN'T REMOVE
        ('libffi-7.dll', None, None),
        ('libGLESv2.dll', None, None), #CAN'T REMOVE
        ('libssl-1_1.dll', None, None),
        ('MSVCP140.dll', None, None), #CAN'T REMOVE
        ('MSVCP140_1.dll', None, None), #CAN'T REMOVE
        ('opengl32sw.dll', None, None),
        ('pyexpat', None, None),
        ('Qt5DBus.dll', None, None), #CAN'T REMOVE
        ('Qt5Network.dll', None, None), #CAN'T REMOVE
        ('Qt5Qml.dll', None, None), #CAN'T REMOVE
        ('Qt5QmlModels.dll', None, None), #CAN'T REMOVE
        ('Qt5Quick.dll', None, None), #CAN'T REMOVE
        ('Qt5Svg.dll', None, None), #CAN'T REMOVE
        ('Qt5WebSockets.dll', None, None), #CAN'T REMOVE
        ('unicodedata', None, None),
        ('VCRUNTIME140.dll', None, None), #CAN'T REMOVE
        ('VCRUNTIME140_1.dll', None, None), #CAN'T REMOVE
    ]),
    a.zipfiles,
    a.datas, 
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FolderMaster'
)
