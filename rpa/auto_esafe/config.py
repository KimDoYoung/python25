import os
from dotenv import load_dotenv
from datetime import datetime

# .env 파일 로드
load_dotenv()

class Config:
    """환경 설정 및 상수 관리"""

    # 로그 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 실행 파일 위치
    LOG_DIR = os.path.join(BASE_DIR, "log")  # log 폴더
    LOG_FILE_FORMAT = "auto_esafe_%Y_%m_%d.log"
    PROGRAM_PATH = os.getenv("PROGRAM_PATH")
    SAVE_AS_PATH1 = os.getenv("SAVE_AS_PATH1")

    # 보안 환경변수
    PASSWORD = os.getenv("CERTI_PASSWORD")

    @classmethod
    def get_log_file_path(cls):
        """오늘 날짜에 맞는 로그 파일 경로 반환"""
        filename = datetime.now().strftime(cls.LOG_FILE_FORMAT)
        return os.path.join(cls.LOG_DIR, filename)

# 로그 폴더 생성 (필요 시)
os.makedirs(Config.LOG_DIR, exist_ok=True)

# 저장폴더가 없으면 생성
os.makedirs(Config.SAVE_AS_PATH1, exist_ok=True)
