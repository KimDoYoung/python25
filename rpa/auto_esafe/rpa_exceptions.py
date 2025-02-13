# rpa_exceptions.py
"""
모듈 설명: 
    - RPA에서 사용하는 사용자 정의 예외를 정의하는 모듈
주요 기능:
    - HolidayError: 휴일일때 발생하는 예외

작성자: 김도영
작성일: 2025-02-13
버전: 1.0
"""
class HolidayError(Exception):
    """휴일일때 발생하는 예외"""
    pass