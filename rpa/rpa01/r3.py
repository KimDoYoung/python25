import subprocess
import time
import win32gui

program_path = "C:\\Users\\deHong\\Desktop\\eSAFE2019.exe"

# 프로그램 실행
hts_process = subprocess.Popen(program_path)
time.sleep(3)  # 실행될 시간을 줌

hwnd = win32gui.GetForegroundWindow()
if hwnd:
    title = win32gui.GetWindowText(hwnd)
    print(f"현재 활성화된 창: {title}")
else:
    print("활성화된 창을 찾을 수 없습니다.")
