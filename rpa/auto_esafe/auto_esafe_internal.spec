# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['auto_esafe.py'],  # 메인 실행 파일
    pathex=['.'],
    binaries=[],
    datas=[
        ('images', 'images'),  # 이미지 폴더 포함
        ('config.py', '.'),  # 설정 파일 포함
        ('logger.py', '.'),  # 로거 파일 포함
        ('path_utils.py', '.'),  # 경로 유틸 파일 포함
        ('rpa_misc.py', '.'),  # RPA 관련 파일 포함
        ('rpa_process.py', '.'),  # RPA 관련 파일 포함
        ('rpa_utils.py', '.'),  # RPA 관련 파일 포함
        ('working_days.py', '.'),  # 영업일 계산 파일 포함
        ('excel_utils.py', '.'),  # excel to csv 변환
        ('rpa_exceptions.py', '.'),  # rpa exceptions
    ],
    hiddenimports=['pyscreeze', 'pillow', 'pyautogui', 'pyautogui._pyautogui_win', 'pyscreeze._screenshot', 'xlrd', 'openpyxl'],
    hookspath=[],
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
    name='auto_esafe',  # 실행 파일 이름
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # GUI 프로그램이면 False, 터미널 실행 필요하면 True로 변경
    onefile=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='auto_esafe',
)
