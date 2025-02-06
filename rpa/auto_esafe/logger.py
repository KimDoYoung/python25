import os
import logging
from datetime import datetime
from config import Config  # 설정값 가져오기

class Logger:
    """로그 관리를 위한 클래스"""

    def __init__(self, log_name="auto_esafe"):
        """Logger 초기화"""
        self.log_dir = Config.LOG_DIR
        os.makedirs(self.log_dir, exist_ok=True)  # 로그 폴더 생성

        log_filename = datetime.now().strftime(Config.LOG_FILE_FORMAT)
        self.log_path = os.path.join(self.log_dir, log_filename)

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)

        # 파일 핸들러 추가
        file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # 콘솔 출력 핸들러 추가 (선택 사항)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)  # 터미널에도 로그 출력

    def info(self, message):
        """INFO 레벨 로그 기록"""
        self.logger.info(message)

    def error(self, message):
        """ERROR 레벨 로그 기록"""
        self.logger.error("❌"+message)

    def warning(self, message):
        """WARNING 레벨 로그 기록"""
        self.logger.warning("⚠️" + message)
