import pygetwindow as gw
import pyautogui
from screeninfo import get_monitors
import time

# 이전 마우스 위치 저장 변수
prev_x, prev_y = None, None

try:
    while True:
        # 1. 현재 마우스 위치 가져오기
        x, y = pyautogui.position()

        # 2. 이전 위치와 다를 때만 출력
        if (x, y) != (prev_x, prev_y):
            prev_x, prev_y = x, y  # 현재 위치를 저장
            
            # 현재 활성 창 가져오기
            active_window = gw.getActiveWindow()
            if active_window:
                win_x, win_y, win_width, win_height = (
                    active_window.left, active_window.top, 
                    active_window.width, active_window.height
                )
                print(f"창 위치: x={win_x}, y={win_y}, width={win_width}, height={win_height}")
            else:
                print("활성 창을 찾을 수 없습니다.")

            # 현재 마우스 위치가 속한 모니터 찾기
            current_monitor = None
            for monitor in get_monitors():
                if monitor.x <= x < monitor.x + monitor.width and monitor.y <= y < monitor.y + monitor.height:
                    current_monitor = monitor
                    break
            
            if current_monitor:
                print(f"현재 모니터: x={current_monitor.x}, y={current_monitor.y}, width={current_monitor.width}, height={current_monitor.height}")

            # 마우스 위치 출력
            print(f"마우스 위치: x={x}, y={y}")
            print("-" * 50)

        time.sleep(0.1)  # CPU 부하 방지를 위해 약간의 딜레이 추가

except KeyboardInterrupt:
    print("\nCtrl + C 감지됨. 프로그램을 종료합니다.")
