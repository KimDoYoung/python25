# path_utils.py
"""
모듈 설명: 
    - pyinstaller를 사용하기 위한 경로 설정 및 이미지 파일 경로 참조 함수
주요 기능:
    - get_base_path: PyInstaller 실행 시에도 올바른 경로 반환
    - pngimg: 이미지 파일 경로를 간단히 참조하는 함수
    - env_path: .env 파일의 경로를 반환
    - log_path: 로그 파일 경로 반환

작성자: 김도영
작성일: 2025-02-11
버전: 1.0
"""
import os
import sys

# def get_base_path():
#     """PyInstaller 실행 시에도 올바른 경로 반환"""
#     if getattr(sys, 'frozen', False):  # PyInstaller로 실행되는 경우
#         return sys._MEIPASS  # PyInstaller가 사용하는 임시 폴더 경로
#     return os.path.abspath(os.path.dirname(__file__))  # 개발 환경에서는 현재 파일의 디렉토리 반환
def get_base_path():
    """PyInstaller 환경에서도 올바른 경로 반환"""
    if getattr(sys, 'frozen', False):  # PyInstaller로 실행되는 경우
        return os.path.dirname(sys.executable)  # 실행 파일(.exe)의 경로
    return os.path.abspath(os.path.dirname(__file__))  # 개발 환경에서는 현재 파일의 디렉토리 반환

# 🔹 프로젝트 기본 경로
BASE_PATH = get_base_path()


def pngimg(filename):
    """이미지 파일 경로를 간단히 참조하는 함수"""
    return os.path.join(BASE_PATH, "images", filename + ".png")

def env_path():
    """.env 파일의 경로를 반환"""
    return os.path.join(BASE_PATH, ".env")

def log_path():
    """로그 파일 경로 반환"""
    return os.path.join(BASE_PATH, "log")
