# config.py
"""
모듈 설명: 
    - Config 클래스: 환경 설정 및 상수 관리

작성자: 김도영
작성일: 2025-02-12
버전: 1.0
"""
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

from path_utils import env_path, log_path

# .env 파일 로드
load_dotenv(env_path())

class Config:
    """환경 설정 및 상수 관리"""
    VERSION = "1.1.3"

    # 프로그램 실행 경로
    PROGRAM_PATH = os.getenv("PROGRAM_PATH")
    PROCESS_NAME = os.getenv("PROCESS_NAME")
    WINDOWN_TITLE = os.getenv("WINDOWN_TITLE")

    # 로그 설정
    LOG_LEVEL_ENV = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_LEVEL = getattr(logging, LOG_LEVEL_ENV, logging.INFO)  # 기본값 INFO
    LOG_DIR = log_path()
    LOG_FILE_FORMAT = "auto_esafe_%Y_%m_%d.log"
    SAVE_AS_PATH1 = os.getenv("SAVE_AS_PATH1")

    # 보안 환경변수
    CERTI_LOCATION = os.getenv("CERTI_LOCATION")
    USERNAME = os.getenv("CERTI_USERNAME")
    PASSWORD = os.getenv("CERTI_PASSWORD")
    
    # SFTP 설정
    SFTP_HOST = os.getenv("SFTP_HOST")
    SFTP_PORT = os.getenv("SFTP_PORT", 22)
    SFTP_USER = os.getenv("SFTP_USER")
    SFTP_PASS = os.getenv("SFTP_PASS")
    SFTP_REMOTE_DIR = os.getenv("SFTP_REMOTE_DIR")

    #GODATA api key
    GODATA_API_KEY = os.getenv("GODATA_API_KEY")
    HOLIDAY_FILE = os.getenv("HOLIDAY_FILE")

    @classmethod
    def get_log_file_path(cls):
        """오늘 날짜에 맞는 로그 파일 경로 반환"""
        filename = datetime.now().strftime(cls.LOG_FILE_FORMAT)
        return os.path.join(cls.LOG_DIR, filename)

# 로그 폴더 생성 (필요 시)
os.makedirs(Config.LOG_DIR, exist_ok=True)

# 저장폴더가 없으면 생성
os.makedirs(Config.SAVE_AS_PATH1, exist_ok=True)
