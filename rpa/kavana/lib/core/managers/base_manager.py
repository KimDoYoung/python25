import os
import tempfile
import threading
#TODO:  모든 command는 result를 반환해야하지 않을까?
#TODO: option들을 체크하는 로직에 포함되어야할 문자들을 체크해야한다.
#TODO: browser pandas를 이용해서 tables를 가져온다. list of dict로 변환한다.

class BaseManager:
    """공통 매니저 기능을 제공하는 기본 클래스 (싱글톤)"""
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """싱글톤 객체 생성"""
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self, executor=None):
        """한 번만 실행되는 초기화 코드"""
        if not hasattr(self, "_initialized"):  # ✅ 중복 실행 방지
            self._initialized = True
            self.executor = executor

            if executor:
                executor.log_command("INFO", f"[{self.__class__.__name__}] Manager Initialized.")
            else:
                print(f"[{self.__class__.__name__}] Manager Initialized (No Executor)")

    def log(self, level: str, message: str):
        """✅ 로그 기록 헬퍼 함수"""
        if self.executor:
            self.executor.log_command(level, message)
        else:
            print(f"[{level}] {message}")  # executor가 없을 때 기본 출력

    def raise_error(self, message):
        """✅ 예외 발생 헬퍼 함수"""
        if self.executor:
            self.executor.raise_command(message)
        else:
            print(f"[ERROR] {message}")  # 기본 오류 출력
        raise RuntimeError(message)

    def _get_temp_file_path(self, suffix=".png", prefix="tmp_", dir=None):
        """임시 파일 경로를 생성하고 반환 (파일 생성은 안 함)"""
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
        os.close(tmp_fd)  # 파일 디스크립터는 닫아줌 (파일은 그대로 있음)
        return tmp_path