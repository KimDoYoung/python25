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

def get_base_path():
    """PyInstaller 실행 환경에서도 올바른 경로 반환"""
    if getattr(sys, 'frozen', False):  # PyInstaller로 실행될 경우
        return sys._MEIPASS  # PyInstaller 임시 폴더 반환
    return os.path.abspath(os.path.dirname(__file__))  # 개발 환경에서는 현재 파일의 디렉토리 반환


# 🔹 프로젝트 기본 경로
BASE_PATH = get_base_path()


def pngimg(filename):
    """이미지 파일 경로를 간단히 참조하는 함수"""
    return os.path.join(BASE_PATH, "images", filename + ".png")

# def env_path():
#     """.env 파일의 경로 반환"""
#     return os.path.join(os.path.dirname(sys.executable), ".env")

def env_path():
    """PyInstaller 실행 환경에서도 올바른 .env 경로 반환"""
    if getattr(sys, 'frozen', False):  # PyInstaller로 실행될 경우
        return os.path.join(os.path.dirname(sys.executable), ".env")  # .exe와 같은 폴더
    return os.path.abspath(".env")  # 개발 환경에서는 현재 디렉토리의 .env

def log_path():
    """
        Git Bash 실행 시: auto_esafe.py가 있는 폴더/log
        PyInstaller 실행 시: auto_esafe.exe가 있는 폴더/log
    """
    
    if getattr(sys, 'frozen', False):  # PyInstaller로 실행된 경우
        base_dir = os.path.dirname(sys.executable)  # exe 파일이 있는 디렉터리
    else:  # 일반 Python 스크립트 실행 (Git Bash 등)
        base_dir = os.path.dirname(os.path.abspath(__file__))  # .py 파일이 있는 디렉터리

    return os.path.join(base_dir, "log")
