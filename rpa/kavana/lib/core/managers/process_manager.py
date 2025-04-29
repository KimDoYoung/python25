import psutil
from time import sleep
import win32gui
import win32process
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

    def get_pid_by_process_name(self, name: str) -> Optional[int]:
        """✅ 특정 프로세스 이름으로 PID 찾기"""
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                if proc.info["name"].lower() == name.lower():
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def is_running(self, name: str, pid: int = None) -> bool:
        """✅ 특정 프로세스가 실행 중인지 확인"""
        if pid:
            return psutil.pid_exists(pid)
        return bool(self.get_pid_by_process_name(name))

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
    
    def find_top_modal_window(self, process_name: str) -> Optional[WindowInfo]:
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