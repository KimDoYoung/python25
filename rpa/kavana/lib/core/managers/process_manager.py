import threading
import subprocess
import psutil
from time import sleep

from lib.core.managers.base_manager import BaseManager

class ProcessManager(BaseManager):
    """프로세스 관리 기능을 제공하는 매니저 클래스"""
    
    def __init__(self, executor=None):
        """초기화 (싱글톤 유지)"""
        super().__init__(executor)
        self.processes = {}  # 실행 중인 프로세스 저장 (이름: PID)

    def get_pid_by_process_name(self, name):
        """✅ 특정 프로세스 이름으로 PID 찾기"""
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"].lower() == name.lower():
                return proc.info["pid"]
        return None

    def is_running(self, name, pid=None):
        """✅ 특정 프로세스가 실행 중인지 확인"""
        if pid:
            return psutil.pid_exists(pid)
        return bool(self.get_pid_by_process_name(name))

