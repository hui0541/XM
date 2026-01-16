# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../启动器主程序.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../服务定义.yaml', '.'),  # 将配置文件打包到根目录
        ('../resources/*.ico', 'resources') # 假设有图标
    ],
    hiddenimports=['PySide6'],
    hookspath=[],
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
    [],
    exclude_binaries=True,
    name='SpeedTrader_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 关闭黑框
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../resources/app.ico' # 如果有图标
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SpeedTrader_Launcher',
)