# -*- mode: python -*-
a = Analysis(['hellotest.py'],
             pathex=['C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='hellotest.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
