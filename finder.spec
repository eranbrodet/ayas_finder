# -*- mode: python -*-
a = Analysis(['finder.py'],
             pathex=['C:\\Eran\\Coding\\Python\\aya'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='finder.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
