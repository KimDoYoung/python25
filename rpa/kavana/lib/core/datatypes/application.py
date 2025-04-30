import os
import subprocess
import time
import psutil
from pywinauto import Application as PywinautoApp
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.managers.process_manager import ProcessManager
import win32process  # 추가된 import
import win32con
import win32gui  # 추가된 import

class Application(KavanaDataType):
    def __init__(self, path: str, process_name: str):
        self.path = path  # 실행 파일 경로
        self.pid = None  # 프로세스 ID
        self.app = None  # pywinauto Application 객체
        self.title = None  # 창 제목
        self.process = None  # subprocess 프로세스 핸들
        # path에서 실행파일명을 추출 process_name으로 한다. 
        self.process_name = process_name
        self.value = f"{path} ({process_name})"  # ✅ value를 path와 process_name으로 설정
    
    def __eq__(self, other):
        if not isinstance(other, Application):
            return NotImplemented
        return self.path == other.path and self.process_name == other.process_name

    def launch(self, executor = None, maximize=False, focus=True, process_name=None):
        """애플리케이션 실행"""
        try:
            self.process = subprocess.Popen(self.path, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
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
                connected = self.try_connect_app()
                if not connected:
                    executor.log_command("WARN", f"{self.process_name}에 연결할 수 없습니다.")

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

    def try_connect_app(self, max_retries=5, delay=1.0):
        for i in range(max_retries):
            try:
                self.app = PywinautoApp().connect(process=self.pid)
                self.title = self.app.top_window().window_text()
                return True
            except Exception as e:
                time.sleep(delay)
        return False
    
    def force_close_windows_by_pid(pid):
        def callback(hwnd, extra):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                try:
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                except Exception as e:
                    print(f"❌ 창 닫기 실패: {e}")
        win32gui.EnumWindows(callback, None)
    
    def reconnect(self, executor=None, focus=False):
        """애플리케이션 재연결"""
        try:
            process_manager = ProcessManager(executor)
            pid = process_manager.get_pid_by_process_name(self.process_name)
            if not pid:
                raise RuntimeError(f"PID를 찾을 수 없습니다. {self.process_name}")
            self.pid = pid
            self.app = PywinautoApp().connect(process=self.pid)
            self.title = self.app.top_window().window_text()
            if focus and self.app:  
                try:
                    self.app.top_window().set_focus()
                    if executor:
                        executor.log_command("INFO", "포커스 설정 완료")
                except Exception as e:
                    if executor:
                        executor.log_command("WARN", f"포커스 설정 실패: {e}")                            
            if executor:
                executor.log_command("INFO", f"애플리케이션 '{self.title}'에 재연결됨.")
        except Exception as e:
            if executor:
                executor.raise_command(f"애플리케이션 재연결 실패: {e}")

    def close_child_windows(self, executor=None):
        """모든 자식 윈도우 닫기 (MDI용 광고창 등 포함)"""
        try:
            #-----------------------------------------------
            executor.log_command("INFO", "child windows---->>>")
            for w in self.app.windows():
                executor.log_command("INFO", w.window_text())
            executor.log_command("INFO", "child windows<<<----")
            #-----------------------------------------------
            
            closed_count = 0

            if self.app:
                top = self.app.top_window()
                executor.log_command("INFO", f"top window: {top.window_text()}")
                for window in self.app.windows():
                    title = window.window_text()
                    if window != top:
                        try:
                            if "안내" in title or "알람" in title:
                                window.close()
                                executor.log_command("INFO", f"윈도우 닫기 성공: {title}")
                                closed_count += 1
                        except Exception as close_err:
                            if executor:
                                executor.log_command("WARN", f"{window.window_text()} 닫기 실패: {str(close_err)}")
            else:
                self.force_close_windows_by_pid(self.pid)  # 별도 강제종료 로직

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
