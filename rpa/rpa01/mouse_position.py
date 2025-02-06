'''
마우스 포지션 표시
'''
import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n종료합니다.")