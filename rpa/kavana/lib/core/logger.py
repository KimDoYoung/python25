"""
모듈 설명:
    - 로그 관리를 위한 싱글톤 Logger 클래스 (사용자 지정 폴더 & 파일명 지원)
주요 기능:
    - 사용: log = Logger(log_dir="custom_logs", log_prefix="app")
    - 기본 저장 위치: logs/kavana-YYYY-MM-DD.log
작성자: 김도영
작성일: 2025-02-12
버전: 1.1
"""

import os
import logging
from datetime import datetime
import sys
import codecs

class Logger:
    """로그 관리를 위한 싱글톤 Logger 클래스"""
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, log_dir="logs", log_prefix="kavana", log_level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_dir, log_prefix, log_level)
        return cls._instance

    def _initialize(self, log_dir, log_prefix, log_level):
        """Logger 초기화 (최초 1회 실행)"""
        self.log_dir = log_dir
        self.log_prefix = log_prefix

        os.makedirs(self.log_dir, exist_ok=True)  # 로그 폴더 생성

        log_filename = f"{self.log_prefix}-{datetime.now().strftime('%Y-%m-%d')}.log"
        self.log_path = os.path.join(self.log_dir, log_filename)

        self.logger = logging.getLogger(self.log_prefix)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            # 파일 핸들러 추가
            file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

            # 콘솔 핸들러 추가
            utf8_stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
            console_handler = logging.StreamHandler(utf8_stdout)
            console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def set_config(self, log_dir=None, log_prefix=None, log_level="INFO"):
        """사용자가 동적으로 로그 설정을 변경할 수 있도록 지원"""
        if log_dir:
            self.log_dir = log_dir
            os.makedirs(self.log_dir, exist_ok=True)  # 새 로그 폴더 생성

        if log_prefix:
            self.log_prefix = log_prefix

        if log_level:
            log_level = log_level.upper()  # ✅ 대문자로 변환하여 비교
            valid_levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR}
            if log_level not in valid_levels:
                raise ValueError(f"잘못된 로그 레벨: {log_level} (지원하는 값: DEBUG, INFO, WARNING, ERROR, CRITICAL)")
            self.log_level = log_level
            self.logger.setLevel(valid_levels[log_level])  # ✅ 로그 레벨 변경

        # 로그 파일 갱신
        log_filename = f"{self.log_prefix}-{datetime.now().strftime('%Y-%m-%d')}.log"
        self.log_path = os.path.join(self.log_dir, log_filename)

        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)  # 기존 핸들러 제거

        file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        utf8_stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
        console_handler = logging.StreamHandler(utf8_stdout)
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug("🐛 " + str(message))

    def info(self, message):
        self.logger.info("ℹ️ " + str(message))

    def warn(self, message):
        self.logger.warning("⚠️ " + str(message))

    def error(self, message):
        self.logger.error("❌ " + str(message))

    @classmethod
    def reset_instance(cls):
        """테스트 간 싱글톤과 핸들러 리셋"""
        if cls._instance:
            for handler in cls._handlers:
                handler.close()
                cls._instance.logger.removeHandler(handler)
            cls._handlers.clear()
        cls._instance = None
        logging.shutdown()