# -*- mode: python -*-

block_cipher = None

a = Analysis(['C:\\Users\\pradeeav\\OneDrive\\Documents\\Learn\\DataScience\\Projects\\FailoverRCA\\ClusterRCA\main.py'],
             pathex=['c:\\Python35\\Scripts'],
             binaries=[(r'C:\Python35\Scripts\7z.exe',r'.'),(r'C:\Python35\Scripts\7z.dll',r'.')],
             datas=None,
             hiddenimports=['unzipfiles'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('7z.dll', '7z.dll', 'DATA')]
a.datas += [('7z.exe', '7z.exe', 'DATA')]             
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ClusterRCA',
          icon='C:\\Users\\pradeeav\\OneDrive\\Documents\\Learn\\DataScience\\Projects\\FailoverRCA\\ClusterRCA\\cluster.ico',
          debug=False,
          strip=False,
          upx=False,
          console=True )
