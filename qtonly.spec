# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['qtonly.py'],
             pathex=['voila-qt'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='qtonly',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='qtonly')

app = BUNDLE(coll,
             name='qtonly.app',
             bundle_identifier='org.qt-project.Qt.QtWebEngineCore')
