import psutil
import win32gui
import win32process

from lib.core.managers.process_manager import ProcessManager

def process_main(process_name: str):
    pm = ProcessManager()
    windows = pm.get_window_info_list(process_name)

    for win in windows:
        print(win)

if __name__ == "__main__":
    process_name = "efplusmain.exe"  # 예시 프로세스 이름
    process_main(process_name)