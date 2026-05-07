# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# Coleta automática de arquivos de dados e dicionários
datas_ctk, binaries_ctk, hiddenimports_ctk = collect_all('customtkinter')
datas_spell, binaries_spell, hiddenimports_spell = collect_all('spellchecker')

block_cipher = None

a = Analysis(
    ['gerador_relatorio.py'],  # Nome exato do seu script
    pathex=[],
    binaries=binaries_ctk + binaries_spell,
    datas=datas_ctk + datas_spell,
    hiddenimports=hiddenimports_ctk + hiddenimports_spell,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Gerador de Relatorio', # Nome do .exe final
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'C:\Users\gustavob.rodrigues\Documents\Codigos\Python\Gerador-de-relatorio\assets\icone_relatorio.ico'
)