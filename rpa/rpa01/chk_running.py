'''
이미 실행 중인지 확인
'''
import psutil
def list_running_programs():
    for proc in psutil.process_iter(['pid', 'name']):
        print(proc.info)
        
def is_program_running(program_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 프로세스 이름을 확인하여 프로그램이 실행 중인지 확인
            if proc.info['name'] == program_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def kill_program(program_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == program_name:
                pid = proc.info['pid']
                process = psutil.Process(pid)
                process.terminate()  # 종료 시도
                process.wait(timeout=3)  # 프로세스가 종료될 때까지 대기
                print(f"{program_name} (PID: {pid}) has been terminated.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    print(f"{program_name} is not running.")
    return False

# 확인하려는 프로그램 이름 (예: notepad.exe)
program_name = "notepad.exe"

list_running_programs()

if is_program_running(program_name):
    print(f"{program_name} is running.")
    kill_program(program_name)
else:
    print(f"{program_name} is not running.")

import psutil



# 종료하려는 프로그램 이름 (예: notepad.exe)
program_name = "notepad.exe"

# 프로그램 종료 시도
