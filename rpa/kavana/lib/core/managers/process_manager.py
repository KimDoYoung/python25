import psutil
from time import sleep
import win32gui
import win32process
import win32con
from dataclasses import dataclass
from typing import List, Optional

from lib.core.managers.base_manager import BaseManager

@dataclass
class WindowInfo:
    hwnd: int
    title: str
    class_name: str

class ProcessManager(BaseManager):
    """프로세스 관리 기능을 제공하는 매니저 클래스"""
    
    def __init__(self, executor=None):
        """초기화 (싱글톤 유지)"""
        super().__init__(executor)
        self.processes = {}  # 실행 중인 프로세스 저장 (이름: PID)

    def get_process_list(self) -> List[dict]:
        """✅ 현재 실행 중인 프로세스 목록 반환"""
        process_list = []
        for proc in psutil.process_iter(attrs=["pid", "name", "username"]):
            try:
                process_list.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return process_list

    def get_pid_by_process_name(self, name: str) -> Optional[int]:
        """✅ 특정 프로세스 이름으로 PID 찾기"""
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                if proc.info["name"].lower() == name.lower():
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None


    def is_running(self, name: str) -> bool:
        """✅ 특정 프로세스가 실행 중인지 확인"""
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                if proc.info["name"].lower() == name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def kill_process_by_name(self, name: str) -> None:
        """프로세스 강제 종료"""
        name = name.lower()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == name:
                    proc.terminate()
                    proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    # def bring_process_to_front(self,target_name):
    #     for proc in psutil.process_iter(['pid', 'name']):
    #         if proc.info['name'] and target_name.lower() in proc.info['name'].lower():
    #             pid = proc.info['pid']

    #             def enum_window_callback(hwnd, _):
    #                 try:
    #                     _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
    #                     if found_pid == pid:
    #                         win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 최소화돼있을 경우 복원
    #                         win32gui.SetForegroundWindow(hwnd)
    #                         return False  # 더 이상 반복할 필요 없음
    #                 except Exception:
    #                     pass
    #                 return True

    #             win32gui.EnumWindows(enum_window_callback, None)
    #             return True
    #     return False

    def bring_process_to_foreground(self, process_name):
        """
        특정 프로세스 이름으로 윈도우를 찾아 최상단으로 가져옵니다.
        
        Args:
            process_name (str): 찾을 프로세스 이름 (예: 'hts.exe' 또는 'hts')
        
        Returns:
            bool: 프로세스를 찾아 최상단으로 가져왔으면 True, 실패했으면 False
        """
        # 프로세스 이름에 .exe가 없으면 추가
        if not process_name.lower().endswith('.exe'):
            process_name += '.exe'
        
        target_pids = []
        
        # 해당 이름의 프로세스 PID 찾기
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    target_pids.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if not target_pids:
            self.executor.log_command("WARN", f"프로세스 '{process_name}'를 찾을 수 없습니다.")
            return False
        
        # 각 윈도우 열거
        def enum_windows_callback(hwnd, result):
            if not win32gui.IsWindowVisible(hwnd):
                return True
            
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid in target_pids:
                # 윈도우가 최소화되어 있으면 복원
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                
                # 윈도우를 최상단으로 가져오기
                win32gui.SetForegroundWindow(hwnd)
                window_title = win32gui.GetWindowText(hwnd)
                self.executor.log_command("INFO",f"윈도우 '{window_title}' (PID: {found_pid})를 최상단으로 가져왔습니다.")
                result.append(hwnd)
                return False  # 첫 번째 찾은 윈도우만 처리
            return True
        
        result = []
        win32gui.EnumWindows(enum_windows_callback, result)
        
        if result:
            return True
        else:
            self.executor.log_command("ERROR", f"프로세스 '{process_name}'의 윈도우를 찾을 수 없습니다.")
            return False

    def get_window_info_list(self, process_name: str = None) -> List[WindowInfo]:
        """✅ 프로세스 이름 없으면 전체 창, 있으면 해당 프로세스만 반환"""

        matched_windows: List[WindowInfo] = []

        def callback(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)

                    if process_name:
                        if process.name().lower() == process_name.lower():
                            matched_windows.append(WindowInfo(hwnd, title, class_name))
                    else:
                        matched_windows.append(WindowInfo(hwnd, title, class_name))

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return True

        win32gui.EnumWindows(callback, None)
        return matched_windows


    def find_top_window_info(self) -> Optional[WindowInfo]:
        """✅ OS전체에서 현재 포커스(최상단) 윈도우 정보 반환 

        Returns:
            WindowInfo 또는 None
        """
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            self.executor.log_command("INFO",f"현재 포커스된 윈도우 → HWND: {hwnd}, Title: {title}, Class: {class_name}")
            return WindowInfo(hwnd=hwnd, title=title, class_name=class_name)
        else:
            self.executor.log_command("WARN",f"현재 포커스된 윈도우가 없습니다.")
            return None

    def find_mdi_top_window_info(self, main_hwnd) -> Optional[WindowInfo]:
        """메인 HWND 안에서 최상단 Active MDI Child 윈도우를 찾는다"""
        children = []

        def child_callback(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                lParam.append(hwnd)
            return True

        win32gui.EnumChildWindows(main_hwnd, child_callback, children)

        if not children:
            self.executor.log_command("WARN", "자식 창이 없습니다.")
            return None

        # 보통 가장 마지막에 추가된 것이 최상단
        top_child = children[-1]
        title = win32gui.GetWindowText(top_child)
        class_name = win32gui.GetClassName(top_child)
        self.executor.log_command("INFO", f"최상단 MDI Child HWND: {top_child}, Title: {title}, Class: {class_name}")
        return WindowInfo(top_child, title, class_name)

    def get_window_region(self, hwnd: int) -> tuple:
        """특정 윈도우의 (x, y, width, height) 정보 반환"""
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return (x, y, width, height)
    
    def find_top_modal_window_0(self, process_name: str) -> Optional[WindowInfo]:
        """주어진 프로세스 이름의 최상단 Modal 성격 창을 찾아 반환"""
        candidate_windows = []

        def callback(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    if process.name().lower() == process_name.lower():
                        title = win32gui.GetWindowText(hwnd)
                        class_name = win32gui.GetClassName(hwnd)
                        # 아주 간단한 필터링 추가 가능 (title 이 존재한다든가)
                        if title.strip():
                            lParam.append((hwnd, title, class_name))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return True

        win32gui.EnumWindows(callback, candidate_windows)

        if not candidate_windows:
            print(f"[WARN] 프로세스({process_name}) 창이 없습니다.")
            return None

        # 가장 마지막(최상단) 창을 기준으로 (혹은 활성 창을 따로 필터링해도 됨)
        top_hwnd, title, class_name = candidate_windows[-1]
        print(f"[INFO] 최상단 창: {title} (HWND: {top_hwnd})")
        return WindowInfo(top_hwnd, title, class_name)    
    
    def find_top_modal_window(self, process_name: str) -> Optional[WindowInfo]:
        """주어진 프로세스 이름의 최상단 Modal 성격 창을 찾아 반환"""
        window_list = self.get_window_info_list(process_name)
        if not window_list:
            self.log("WARN", f"프로세스({process_name}) 창이 없습니다.")
            return None
        
        return window_list[0]  # 가장 마지막(최상단) 창을 기준으로 (혹은 활성 창을 따로 필터링해도 됨)

    def find_window_by_title(self, title: str) -> Optional[WindowInfo]:
        """특정 제목을 가진 창 반환"""
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            class_name = win32gui.GetClassName(hwnd)
            return WindowInfo(hwnd=hwnd, title=title, class_name=class_name)
        else:
            self.log("WARN", f"제목({title})을 가진 창이 없습니다.")
            return None