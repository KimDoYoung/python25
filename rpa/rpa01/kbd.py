
import ctypes

def set_keyboard_to_english():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.PostMessageW(hwnd, 0x50, 0, 0x4090409)

def is_korean_keyboard():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, None)
    klid = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    
    return hex(klid) == "0x4120412"  # 한국어 키보드 레이아웃 확인

if is_korean_keyboard():
    print("한국어 키보드 레이아웃입니다.")
else:
    print("한국어 키보드 레이아웃이 아닙니다.")
set_keyboard_to_english()
if is_korean_keyboard():
    print("한국어 키보드 레이아웃입니다.")
else:
    print("한국어 키보드 레이아웃이 아닙니다.")
    