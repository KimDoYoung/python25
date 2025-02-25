from dataclasses import dataclass
import pyautogui
import pygetwindow as gw

@dataclass
class Window:
    title: str
    hwnd: int = None  # Window handle (자동으로 가져옴)

    def __post_init__(self):
        """창을 찾고 핸들을 저장"""
        win = self.find_window()
        if win:
            self.hwnd = win._hWnd

    def find_window(self):
        """제목으로 창 찾기"""
        windows = gw.getWindowsWithTitle(self.title)
        return windows[0] if windows else None

    def activate(self):
        """창을 활성화 (포커스)"""
        win = self.find_window()
        if win:
            win.activate()

    def move(self, x: int, y: int):
        """창 이동"""
        win = self.find_window()
        if win:
            win.moveTo(x, y)

    def resize(self, width: int, height: int):
        """창 크기 조절"""
        win = self.find_window()
        if win:
            win.resizeTo(width, height)

    def close(self):
        """창 닫기"""
        win = self.find_window()
        if win:
            win.close()

    def get_region(self):
        """창의 위치 및 크기를 Region 객체로 반환"""
        win = self.find_window()
        if win:
            from lib.core.datatypes.region import Region
            return Region(win.left, win.top, win.width, win.height)
        return None

    def __str__(self):
        return f"Window(title={self.title}, hwnd={self.hwnd})"
