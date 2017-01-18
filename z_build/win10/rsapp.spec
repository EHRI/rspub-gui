# -*- mode: python -*-

# ## usage: $ pyinstaller rsapp.spec

block_cipher = None

added_files = [
         ( '..\\..\\conf\\', 'conf\\' ),
         ( '..\\..\\i18n\\', 'i18n\\' )
         ]


a = Analysis(['..\\..\\rsapp\\gui\\app.py'],
             pathex=['..\\..\\..\\rspub-gui', '..\\..\\..\\rspub-core'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='MetadataPublishingTool',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MetadataPublishingTool')
