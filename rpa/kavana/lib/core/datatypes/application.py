import subprocess
import psutil
from pywinauto import Application as PywinautoApp
from lib.core.datatypes.kavana_datatype import KavanaDataType

class Application(KavanaDataType):
    def __init__(self, path: str):
        self.path = path  # 실행 파일 경로
        self.pid = None  # 프로세스 ID
        self.title = None  # 창 제목
        self.process = None  # subprocess 프로세스 핸들
        self.app = None  # pywinauto Application 객체

    def launch(self, maximize=False):
        """애플리케이션 실행"""
        try:
            self.process = subprocess.Popen(self.path)
            self.pid = self.process.pid
            self.app = PywinautoApp().connect(process=self.pid)
            self.title = self.app.top_window().window_text()

            if maximize:
                self.app.top_window().maximize()

            print(f"[INFO] {self.path} 실행됨 (PID: {self.pid}, Title: {self.title})")
        except Exception as e:
            print(f"[ERROR] 애플리케이션 실행 실패: {e}")

    def close_child_windows(self):
        """모든 자식 윈도우 닫기"""
        try:
            for window in self.app.windows():
                if window != self.app.top_window():
                    window.close()
            print("[INFO] 모든 자식 윈도우 닫기 완료.")
        except Exception as e:
            print(f"[ERROR] 자식 윈도우 닫기 실패: {e}")

    def close(self):
        """프로세스 종료"""
        try:
            if self.process:
                parent = psutil.Process(self.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
                print(f"[INFO] {self.path} 종료됨.")
            else:
                print("[WARNING] 프로세스가 존재하지 않습니다.")
        except Exception as e:
            print(f"[ERROR] 프로세스 종료 실패: {e}")

    def __str__(self):
        return f"Application(name={self.path}, pid={self.pid}, title={self.title})"

    @property
    def string(self):
        return self.path

    @property
    def primitive(self):
        return self.path
