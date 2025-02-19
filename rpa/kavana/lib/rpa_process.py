import psutil
import win32gui
import win32process
import win32con

def list_running_programs() -> list:
    '''현재 실행 중인 프로그램 목록을 출력합니다.'''
    process_info = []
    for proc in psutil.process_iter(['pid', 'name']):
        process_info.append(proc.info)
    return process_info
        
def is_process_running(program_name) -> bool:
    ''' 주어진 프로그램 이름이 실행 중인지 확인합니다. '''
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 프로세스 이름을 확인하여 프로그램이 실행 중인지 확인
            if proc.info['name'] == program_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def kill_process(process_name) -> bool:
    ''' 주어진 프로그램 이름을 가진 프로세스를 종료합니다. 정상종료시 True, 그렇지 않으면 False를 반환합니다. '''
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                pid = proc.info['pid']
                process = psutil.Process(pid)
                process.terminate()  # 종료 시도
                process.wait(timeout=3)  # 프로세스가 종료될 때까지 대기
                print(f"{process_name} (PID: {pid}) has been terminated.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    #print(f"{program_name} is not running.")
    return False

def get_window_title_by_process(process_name):
    ''' 주어진 프로세스 이름을 가진 프로그램의 창 제목을 반환합니다. '''
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']  # 해당 프로세스의 PID 가져오기

            def callback(hwnd, hwnds):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)  # ✅ 수정된 부분
                if found_pid == pid:
                    hwnds.append((hwnd, win32gui.GetWindowText(hwnd)))
                return True

            hwnds = []
            win32gui.EnumWindows(callback, hwnds)

            return [title for hwnd, title in hwnds if title]  # 빈 타이틀 제외하고 반환
    
    return None

def get_main_window_handle(process_name, title_keyword=None):
    """
    주어진 프로세스명과 (선택적으로) 제목 키워드를 포함하는 창의 핸들과 제목을 반환하는 함수.
    
    :param process_name: 실행 중인 프로세스 이름 (예: "notepad.exe")
    :param title_keyword: 찾고자 하는 창 제목의 키워드 (예: "e-SAFE"), 없으면 가장 긴 제목 선택
    :return: (창 핸들(HWND), 창 제목) 또는 None
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']

            def callback(hwnd, hwnds):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    title = win32gui.GetWindowText(hwnd)
                    if title:  # 빈 타이틀 제거
                        hwnds.append((hwnd, title))
                return True

            hwnds = []
            win32gui.EnumWindows(callback, hwnds)

            if not hwnds:
                return None  # 창을 찾지 못한 경우

            # 🔥 특정 키워드가 포함된 창 찾기
            if title_keyword:
                for hwnd, title in hwnds:
                    if title_keyword in title:
                        return hwnd, title  # ✅ 키워드가 포함된 창 반환
            
            # 🔥 가장 긴 타이틀을 가진 창 선택 (보통 메인 창일 가능성이 높음)
            main_window = max(hwnds, key=lambda x: len(x[1]))
            return main_window

    return None  # 프로세스를 찾지 못한 경우

def maximize_window(process_name, title):
    ''' 주어진 창을 최대화합니다. '''
    result = get_main_window_handle(process_name, title)
    hwnd, title = result
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # ✅ 창 최대화