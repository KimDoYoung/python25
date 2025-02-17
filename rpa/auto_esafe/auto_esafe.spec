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
    a.binaries,  # ✅ binaries 포함
    a.zipfiles,
    a.datas,  # ✅ datas 포함
    exclude_binaries=False,  # ✅ False로 변경 (필수)
    name='auto_esafe_1.0.8',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    onefile=True
)

