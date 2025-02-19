# logger.py
"""
모듈 설명: 
    - 로그 관리를 위한 싱글톤 Logger 클래스
주요 기능:
    - 사용: log = Logger()
    - Logger(log_dir="custom_logs", log_level=logging.DEBUG, log_file_format="%Y-%m-%d_%H-%M.log")
작성자: 김도영
작성일: 2025-02-12
버전: 1.0
"""
import codecs
import os
import logging
from datetime import datetime
import sys

class Logger:
    """로그 관리를 위한 싱글톤 Logger 클래스"""
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, log_dir="logs", log_level=logging.INFO, log_file_format="%Y-%m-%d.log", log_name="kavana"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_dir, log_level, log_file_format, log_name)
        return cls._instance

    def _initialize(self, log_dir, log_level, log_file_format, log_name):
        """Logger 초기화 (최초 1회만 실행)"""
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)  # 로그 폴더 생성

        log_filename = datetime.now().strftime(log_file_format)
        self.log_path = os.path.join(self.log_dir, log_filename)

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        # 중복 핸들러 방지
        if not self.logger.handlers:
            # 파일 핸들러 추가
            file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

            # 콘솔 출력 핸들러 추가
            utf8_stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)            
            console_handler = logging.StreamHandler(utf8_stdout)
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