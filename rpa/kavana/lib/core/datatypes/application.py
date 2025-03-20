import subprocess
import time
import psutil
from pywinauto import Application as PywinautoApp
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.managers.process_manager import ProcessManager

class Application(KavanaDataType):
    def __init__(self, path: str):
        self.path = path  # 실행 파일 경로
        self.pid = None  # 프로세스 ID
        self.app = None  # pywinauto Application 객체
        self.title = None  # 창 제목
        self.process = None  # subprocess 프로세스 핸들
        self.process_name = None # 프로세스 이름

    def launch(self, executor = None, maximize=False, focus=True, process_name=None):
        """애플리케이션 실행"""
        try:
            self.process = subprocess.Popen(self.path)
            time.sleep(1)  # ✅ 프로세스가 실행되기까지 잠시 대기
            # 현재 실행 중인 프로세스에서 'notepad.exe'의 PID 찾기
            if process_name is None:
                self.process_name = self.path.split("\\")[-1].lower()
            else:
                self.process_name = process_name.lower()
            self.pid = None
            self.app = None
            self.title = None
            process_manager = ProcessManager(executor)
            pid = process_manager.get_pid_by_process_name(self.process_name)
            if pid:
                self.pid = pid
                self.app = PywinautoApp().connect(process=self.pid)
                self.title = self.app.top_window().window_text()                    

            if self.app is None:
                executor.log_command("WARN",f"{process_name} 을 tasklist에서 찾을 수 없습니다!")

            # ✅ 최대화 옵션
            if maximize and self.app:
                self.app.top_window().maximize()

            # ✅ 포커스 옵션 추가
            if focus and self.app:
                self.app.top_window().set_focus()

            if executor:
                executor.log_command("INFO", f"애플리케이션 '{self.title}' 실행됨.")
            
        except Exception as e:
            if executor:
                executor.raise_command(f"애플리케이션 실행 실패: {e} : {self.string}")


    def close_child_windows(self, executor=None):
        """모든 자식 윈도우 닫기"""
        try:
            closed_count = 0
            for window in self.app.windows():
                if window != self.app.top_window():
                    window.close()
                    closed_count += 1

            # ✅ 성공 로그 기록
            if executor:
                executor.log_command("INFO", f"애플리케이션 {self.path}의 자식 윈도우 {closed_count}개 닫기 완료.")

        except Exception as e:
            error_message = f"애플리케이션 {self.path}의 자식 윈도우 닫기 실패: {str(e)}"
            if executor:
                executor.raise_command(error_message)
            raise RuntimeError(error_message)

    def close(self, executor=None):
        """프로세스 종료"""
        try:
            process_manager = ProcessManager(executor)
            if self.pid is None:
                self.pid = process_manager.get_pid_by_process_name(self.process_name)
            if self.process:
                parent = psutil.Process(self.pid)
                parent.terminate()
                parent.wait(3)
            else:
                if executor:
                    executor.log_command("INFO", "프로세스가 존재하지 않습니다.")
        except Exception as e:
            if executor:
                executor.raise_command(f"프로세스 종료 실패: {e}")

    def __str__(self):
        return f"Application(name={self.path}, pid={self.pid}, title={self.title})"

    @property
    def string(self):
        return self.path

    @property
    def primitive(self):
        return self.path
