import threading

class BaseManager:
    """공통 매니저 기능을 제공하는 기본 클래스"""
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, executor=None):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(BaseManager, cls).__new__(cls)
                cls._instances[cls]._initialize(executor)
        return cls._instances[cls]

    def _initialize(self, executor):
        """매니저 초기화 (서브클래스에서 오버라이드 가능)"""
        self.executor = executor
        if executor:
            executor.log_command("INFO", f"[{self.__class__.__name__}] Manager Initialized.")

    def log(self, level:str, message:str):
        """✅ 로그 기록 헬퍼 함수"""
        if self.executor:
            self.executor.log_command(level, message)

    def raise_error(self, message):
        """✅ 예외 발생 헬퍼 함수"""
        if self.executor:
            self.executor.raise_command(message)
        raise RuntimeError(message)
