# -*- mode: python -*-
import os

block_cipher = None


a = Analysis(['../qtmain.py'],
             pathex=['/Users/t_waugs/Documents/Objeus repo/soul/creator'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('icon.gif', os.path.join(a.pathex[0], 'icon.gif'), 'DATA')]
a.datas += [('creator_logo.png', os.path.join(a.pathex[0], 'creator_logo.png'), 'DATA')]
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
a.datas += extra_datas('data')
a.datas += extra_datas('int')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='qtmain',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='qtmain')
app = BUNDLE(coll,
             name='Story Creator.app',
             icon=os.path.join(a.pathex[0], 'icon.icns'),
             bundle_identifier=None)
