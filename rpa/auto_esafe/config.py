import os
from dotenv import load_dotenv
from datetime import datetime

from path_utils import env_path, log_path

# .env 파일 로드
load_dotenv(env_path())

class Config:
    """환경 설정 및 상수 관리"""
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    VERSION = os.getenv("VERSION")
    # 프로그램 실행 경로
    PROGRAM_PATH = os.getenv("PROGRAM_PATH")
    PROCESS_NAME = os.getenv("PROCESS_NAME")
    WINDOWN_TITLE = os.getenv("WINDOWN_TITLE")
    # 로그 설정
    LOG_DIR = log_path()
    LOG_FILE_FORMAT = "auto_esafe_%Y_%m_%d.log"
    SAVE_AS_PATH1 = os.getenv("SAVE_AS_PATH1")

    # 보안 환경변수
    PASSWORD = os.getenv("CERTI_PASSWORD")
    
    # FTP 설정
    FTP_HOST = os.getenv("FTP_HOST")
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASS = os.getenv("FTP_PASS")
    FTP_REMOTE_DIR = os.getenv("FTP_REMOTE_DIR")

    #GODATA api key
    GODATA_API_KEY = os.getenv("GODATA_API_KEY")    

    @classmethod
    def get_log_file_path(cls):
        """오늘 날짜에 맞는 로그 파일 경로 반환"""
        filename = datetime.now().strftime(cls.LOG_FILE_FORMAT)
        return os.path.join(cls.LOG_DIR, filename)

# 로그 폴더 생성 (필요 시)
os.makedirs(Config.LOG_DIR, exist_ok=True)

# 저장폴더가 없으면 생성
os.makedirs(Config.SAVE_AS_PATH1, exist_ok=True)
