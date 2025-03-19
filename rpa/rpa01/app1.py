import subprocess
import time
import psutil
from pywinauto import Application

class AppManager:
    def __init__(self, app_path):
        self.app_path = app_path
        self.process = None
        self.app = None

    def launch(self):
        """프로그램 실행"""
        try:
            self.process = subprocess.Popen(self.app_path)
            time.sleep(2)  # 실행 대기
            self.app = Application().connect(path=self.app_path)
            print(f"[INFO] {self.app_path} 실행 완료.")
        except Exception as e:
            print(f"[ERROR] 프로그램 실행 실패: {e}")

    def maximize_main_window(self):
        """메인 윈도우 최대화"""
        try:
            main_window = self.app.top_window()
            main_window.maximize()
            print("[INFO] 메인 윈도우 최대화 완료.")
        except Exception as e:
            print(f"[ERROR] 메인 윈도우 최대화 실패: {e}")

    def close_child_windows(self):
        """모든 자식 윈도우 닫기"""
        try:
            for window in self.app.windows():
                if window != self.app.top_window():
                    window.close()
                    time.sleep(0.5)
            print("[INFO] 모든 자식 윈도우 닫기 완료.")
        except Exception as e:
            print(f"[ERROR] 자식 윈도우 닫기 실패: {e}")

    def terminate_process(self):
        """프로세스 종료"""
        try:
            if self.process:
                parent = psutil.Process(self.process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()  # 모든 하위 프로세스 종료
                parent.terminate()  # 부모 프로세스 종료
                print(f"[INFO] {self.app_path} 프로세스 종료 완료.")
            else:
                print("[WARNING] 프로세스가 존재하지 않습니다.")
        except Exception as e:
            print(f"[ERROR] 프로세스 종료 실패: {e}")

# 실행 예제
if __name__ == "__main__":
    app_manager = AppManager("C:\\Windows\\System32\\notepad.exe")
    app_manager.launch()
    app_manager.maximize_main_window()
    time.sleep(3)  # 테스트를 위해 3초 대기
    app_manager.close_child_windows()
    time.sleep(2)  # 테스트를 위해 2초 대기
    app_manager.terminate_process()
