import subprocess
import psutil
import platform
from pywinauto import Application
from lib.actions.logger import Logger  # Logger 클래스를 가져오기

# Logger 인스턴스 생성
log = Logger(log_name="process_logger")

if platform.system() == "Windows":
    import win32gui
    import win32process
    import win32con


def start_process(program_path: str) -> bool:
    """ 주어진 프로그램을 실행하고 실행 여부를 반환합니다. """
    try:
        subprocess.Popen(program_path, shell=True)
        return True
    except Exception as e:
        print(f"프로세스 실행 실패: {e}")
        return False

def get_all_windows():
    """ 현재 실행 중인 모든 창의 핸들 및 제목을 반환합니다. """
    hwnds = []
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if title:
            hwnds.append((hwnd, title))
        return True
    win32gui.EnumWindows(callback, None)
    return hwnds


def list_running_programs() -> list:
    """ 현재 실행 중인 프로그램 목록을 반환합니다. """
    try:
        programs = [proc.info for proc in psutil.process_iter(['pid', 'name'])]
        log.info(f"실행 중인 프로그램 목록: {programs}")
        return programs
    except Exception as e:
        log.error(f"프로세스 목록을 가져오는 중 오류 발생: {e}")
        return []

def is_process_running(program_name: str) -> bool:
    """ 주어진 프로그램 이름이 실행 중인지 확인합니다. """
    try:
        running = any(proc.info['name'].lower() == program_name.lower() for proc in psutil.process_iter(['pid', 'name']))
        log.info(f"프로세스 {program_name} 실행 여부: {running}")
        return running
    except Exception as e:
        log.error(f"프로세스 확인 중 오류 발생: {e}")
        return False

def kill_process(process_name: str) -> bool:
    """ 주어진 프로그램 이름을 가진 프로세스를 종료합니다. 정상 종료 시 True, 실패 시 False를 반환합니다. """
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                proc.wait(timeout=3)
                log.info(f"{process_name} (PID: {proc.info['pid']}) 종료됨.")
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        log.warning(f"프로세스 종료 실패: {e}")
    return False

def get_window_title_by_process(process_name: str):
    """ 주어진 프로세스 이름을 가진 프로그램의 창 제목을 반환합니다. """
    if platform.system() != "Windows":
        log.error("이 기능은 Windows에서만 사용할 수 있습니다.")
        raise NotImplementedError("이 기능은 Windows에서만 사용할 수 있습니다.")

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                pid = proc.info['pid']

                def callback(hwnd, hwnds):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        hwnds.append(win32gui.GetWindowText(hwnd))
                    return True

                hwnds = []
                win32gui.EnumWindows(callback, hwnds)
                result = [title for title in hwnds if title]
                log.info(f"{process_name} 창 제목 검색 결과: {result}")
                return result
    except Exception as e:
        log.error(f"창 제목 검색 중 오류 발생: {e}")
    return None

def get_main_window_handle(process_name: str, title_keyword: str = None):
    """ 주어진 프로세스명과 (선택적으로) 제목 키워드를 포함하는 창의 핸들과 제목을 반환합니다. """
    if platform.system() != "Windows":
        log.error("이 기능은 Windows에서만 사용할 수 있습니다.")
        raise NotImplementedError("이 기능은 Windows에서만 사용할 수 있습니다.")

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                pid = proc.info['pid']

                def callback(hwnd, hwnds):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            hwnds.append((hwnd, title))
                    return True

                hwnds = []
                win32gui.EnumWindows(callback, hwnds)

                if not hwnds:
                    log.warning(f"{process_name}에 대한 창을 찾지 못함.")
                    return None

                if title_keyword:
                    for hwnd, title in hwnds:
                        if title_keyword.lower() in title.lower():
                            log.info(f"{process_name} - 키워드 {title_keyword} 포함된 창 찾음: {title}")
                            return hwnd, title

                main_window = max(hwnds, key=lambda x: len(x[1]))
                log.info(f"{process_name} - 가장 긴 제목의 창 선택: {main_window[1]}")
                return main_window
    except Exception as e:
        log.error(f"창 핸들 검색 중 오류 발생: {e}")
    return None

def maximize_window(process_name: str, title: str):
    """ 주어진 프로세스명과 창 제목을 가진 창을 찾아서 최대화합니다. """
    if platform.system() != "Windows":
        log.error("이 기능은 Windows에서만 사용할 수 있습니다.")
        raise NotImplementedError("이 기능은 Windows에서만 사용할 수 있습니다.")

    try:
        result = get_main_window_handle(process_name, title)
        if result:
            hwnd, _ = result
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            log.info(f"{process_name} - 창 {title} 최대화됨.")
            return True
    except Exception as e:
        log.error(f"창 최대화 중 오류 발생: {e}")
    return False

def minimize_window(process_name: str, title: str):
    """ 주어진 프로세스명과 창 제목을 가진 창을 찾아서 최소화합니다. """
    result = get_main_window_handle(process_name, title)
    if result:
        hwnd, _ = result
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        return True
    return False

def close_all_children_window(title: str) -> bool:
    """
    주어진 프로그램의 MDIClient 내 모든 자식 창을 닫는 함수.

    :param title: 프로그램의 메인 창 제목 (예: "eFriend Plus")
    :return: 성공 여부 (True: 모든 창 닫음, False: 실패)
    """
    try:
        # HTS 프로그램 실행 또는 연결
        log.info(f"{title} 프로그램에 연결 중...")
        app = Application().connect(title=title)
        main_window = app.window(title=title)

        # MDIClient 컨트롤 찾기
        mdi_client = main_window.child_window(class_name="MDIClient")

        # 모든 자식 창 닫기
        children = mdi_client.children()
        if not children:
            log.info(f"{title} - 닫을 자식 창이 없습니다.")
            return True

        for child in children:
            log.info(f"창 닫기 시도: {child.window_text()}")
            try:
                child.close()
                log.info(f"성공적으로 닫음: {child.window_text()}")
            except Exception as e:
                log.warning(f"창 닫기 실패: {child.window_text()}, 오류: {e}")

        log.info(f"{title} - 모든 자식 창 닫기 완료.")
        return True
    except Exception as e:
        log.error(f"{title} - MDIClient 창 닫기 중 오류 발생: {e}")
        return False