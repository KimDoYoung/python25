import os
import logging
from datetime import datetime

class Logger:
    """로그 관리를 위한 싱글톤 Logger 클래스"""
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, log_name="auto_esafe"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_name)
        return cls._instance

    def _initialize(self, log_name):
        """Logger 초기화 (최초 1회만 실행)"""
        from config import Config  # import 순환 참조 방지

        self.log_dir = Config.LOG_DIR
        os.makedirs(self.log_dir, exist_ok=True)  # 로그 폴더 생성

        log_filename = datetime.now().strftime(Config.LOG_FILE_FORMAT)
        self.log_path = os.path.join(self.log_dir, log_filename)

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)  # DEBUG 레벨까지 출력하도록 설정

        # 중복 핸들러 방지
        if not self.logger.handlers:
            # 파일 핸들러 추가
            file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

            # 콘솔 출력 핸들러 추가
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message):
        """DEBUG 레벨 로그 기록 (개발 & 디버깅 용도)"""
        self.logger.debug("🐛 " + message)

    def info(self, message):
        """INFO 레벨 로그 기록"""
        self.logger.info("ℹ️ " + message)

    def warning(self, message):
        """WARNING 레벨 로그 기록"""
        self.logger.warning("⚠️ " + message)

    def error(self, message):
        """ERROR 레벨 로그 기록"""
        self.logger.error("❌ " + message)

# import os
# import logging
# from datetime import datetime
# from config import Config  # 설정값 가져오기

# class Logger:
#     """로그 관리를 위한 클래스"""

#     def __init__(self, log_name="auto_esafe"):
#         """Logger 초기화"""
#         self.log_dir = Config.LOG_DIR
#         os.makedirs(self.log_dir, exist_ok=True)  # 로그 폴더 생성

#         log_filename = datetime.now().strftime(Config.LOG_FILE_FORMAT)
#         self.log_path = os.path.join(self.log_dir, log_filename)

#         self.logger = logging.getLogger(log_name)
#         self.logger.setLevel(logging.INFO)

#         # 파일 핸들러 추가
#         file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
#         file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

#         # 콘솔 출력 핸들러 추가 (선택 사항)
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

#         self.logger.addHandler(file_handler)
#         self.logger.addHandler(console_handler)  # 터미널에도 로그 출력

#     def info(self, message):
#         """INFO 레벨 로그 기록"""
#         self.logger.info(message)

#     def error(self, message):
#         """ERROR 레벨 로그 기록"""
#         self.logger.error("❌"+message)

#     def warning(self, message):
#         """WARNING 레벨 로그 기록"""
#         self.logger.warning("⚠️" + message)
