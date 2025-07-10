# src/main.py
"""
5분 간격으로 현재 시각 출력.
stop_event.set() 이 호출되면 즉시 루프를 종료.
"""
import time
from datetime import datetime
from threading import Event


def run_loop(stop_event: Event):
    # stop_event.is_set() == True 면 종료
    while not stop_event.is_set():
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Hello, Service!")
        # 5분 동안 대기하되, 중간에 stop_event 가 set 되면 즉시 탈출
        # wait() 은 True/False 반환 → True == stop_event 가 set 됨
        if stop_event.wait(timeout=300):
            break


# 콘솔에서 직접 실행할 때는 Ctrl-C 로 중단 가능
if __name__ == "__main__":
    try:
        run_loop(Event())
    except KeyboardInterrupt:
        pass
