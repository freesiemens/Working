# -*- mode: python -*-
a = Analysis(['pdl_tool.py'],
             pathex=['C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working'],
             hiddenimports=['[scipy.special._ufuncs_cxx,sklearn.utils.lgamma,sklearn.tree._utils]'],
             hookspath=None,
             runtime_hooks=None)
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pdl_tool.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
