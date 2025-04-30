import pygetwindow as gw
from lib.core.datatypes.kavana_datatype import KavanaDataType

class Window(KavanaDataType):
    def __init__(self, title: str, hwnd: int, class_name: str = None):
        self.title = title
        self.hwnd = hwnd  # Window handle
        self.value = title  # ✅ value를 title로 설정
        self.class_name = class_name  # 클래스 이름
        self.value = f"{title} ({hwnd}){class_name}"  # ✅ value를 title과 hwnd로 설정
        self._initialize_window()
    
    def __eq__(self, other):
        if not isinstance(other, Window):
            return NotImplemented
        if  self.title == other.title and self.hwnd == other.hwnd and self.class_name == other.class_name:
            return True

    def _initialize_window(self):
        """창을 찾고 핸들을 저장"""
        win = self._find_window()
        if win:
            self.hwnd = win._hWnd

    def _find_window(self):
        """제목으로 창 찾기"""
        windows = gw.getWindowsWithTitle(self.title)
        return windows[0] if windows else None

    def activate(self):
        """창을 활성화 (포커스)"""
        win = self._find_window()
        if win:
            win.activate()

    def move(self, x: int, y: int):
        """창 이동"""
        win = self._find_window()
        if win:
            win.moveTo(x, y)

    def resize(self, width: int, height: int):
        """창 크기 조절"""
        win = self._find_window()
        if win:
            win.resizeTo(width, height)

    def close(self):
        """창 닫기"""
        win = self._find_window()
        if win:
            win.close()

    def get_region(self):
        """창의 위치 및 크기를 Region 객체로 반환"""
        win = self._find_window()
        if win:
            from lib.core.datatypes.region import Region
            return Region(win.left, win.top, win.width, win.height)
        return None

    def __str__(self):
        return f"Window(title={self.title}, hwnd={self.hwnd})"

    @property
    def string(self):
        """윈도우 제목을 문자열로 변환"""
        return self.title

    @property
    def primitive(self):
        """Python 기본 타입 변환 (윈도우는 제목 문자열로 변환)"""
        return self.title