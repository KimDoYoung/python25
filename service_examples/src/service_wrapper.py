# src/service_wrapper.py
import win32serviceutil
import win32service
import win32event
import servicemanager
import threading
import sys
import os

from threading import Event

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
import main  # run_loop(stop_event)

class SimplePrintService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SimplePrintService"
    _svc_display_name_ = "Simple Print (5-minute) Service"
    _svc_description_ = "매 5분마다 현재 시각을 출력하는 데모 서비스"

    def __init__(self, args):
        super().__init__(args)
        self.hStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_event = Event()          # ← 파이썬용 이벤트
        self.worker = None

    def SvcDoRun(self):
        # 서비스 시작 로그
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        # 작업 스레드 시작
        self.worker = threading.Thread(
            target=main.run_loop, args=(self.stop_event,), daemon=True
        )
        self.worker.start()

        # SCM(SCM = Service Control Manager)으로부터 중단 신호를 기다림
        win32event.WaitForSingleObject(self.hStop, win32event.INFINITE)

    def SvcStop(self):
        # SCM에 "곧 멈춘다" 알림
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 파이썬 루프 종료 지시
        self.stop_event.set()
        win32event.SetEvent(self.hStop)
        # 최대 5초 대기 후 강제 종료
        self.worker.join(timeout=5)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(SimplePrintService)
