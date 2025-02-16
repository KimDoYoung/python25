import ctypes

def get_laptop_dpi():
    try:
        # DPI 인식 모드를 변경 (Windows 10 이상)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 프로세스를 시스템 DPI Aware 모드로 설정
    except Exception as e:
        print(f"DPI 설정 오류: {e}")

    # 화면 핸들 가져오기
    hdc = ctypes.windll.user32.GetDC(0)

    # DPI 가져오기 (LOGPIXELSX)
    dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)

    # 배율 계산 (96 DPI가 100% 기준)
    scale_factor = dpi_x / 96  
    return scale_factor * 100  # % 단위 변환

# 실행
dpi_percent = get_laptop_dpi()
print(f"노트북 DPI 배율: {dpi_percent}%")
