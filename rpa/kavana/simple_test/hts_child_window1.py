import win32gui
import win32con

# # 활성화 된 윈도우 찾기
# hwnd = win32gui.GetForegroundWindow()  # 현재 최상단(활성) 창
# title = win32gui.GetWindowText(hwnd)
# cls = win32gui.GetClassName(hwnd)

# print(f"활성 창: HWND={hwnd}, 타이틀={title}, 클래스={cls}")
# 타이틀 구하기
def enum_all_windows():
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            cls = win32gui.GetClassName(hwnd)
            if title.strip():  # 타이틀이 있는 윈도우만
                print(f"HWND: {hwnd}, 클래스: {cls}, 타이틀: {title}")
    win32gui.EnumWindows(callback, None)

# enum_all_windows()
# exit()

# 1. HTS 메인 윈도우 핸들 찾기 (타이틀이 정확히 일치해야 함)
main_hwnd = win32gui.FindWindow(None, "eFriend Plus")  # 예: '영웅문4'

# 2. 자식 윈도우(MDI Client) 탐색
def enum_child_windows(parent):
    children = []
    def callback(hwnd, _):
        children.append(hwnd)
    win32gui.EnumChildWindows(parent, callback, None)
    return children

child_windows = enum_child_windows(main_hwnd)

# 3. 특정 클래스명/타이틀 조건으로 원하는 서브 윈도우 찾기
# 보통 HTS 화면은 생성 후 잠깐 동안만 타이틀이 "0002 종목조회" 등으로 되어 있을 수 있음
for hwnd in child_windows:
    title = win32gui.GetWindowText(hwnd)
    cls = win32gui.GetClassName(hwnd)
    print(f"윈도우: {hwnd}, 클래스: {cls}, 타이틀: {title}")

    # 조건: 예) 화면 번호가 포함된 창 제목
    if "0808" in title:
        rect = win32gui.GetClientRect(hwnd)  # (left, top, right, bottom)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        print(f"클라이언트 영역 크기: {width} x {height}")
        break
