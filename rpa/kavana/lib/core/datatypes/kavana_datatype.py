from datetime import datetime
from typing import Any

class KavanaDataType:
    """Kavana의 모든 데이터 타입의 기본 클래스"""
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

class Integer(KavanaDataType):
    '''정수형 데이터 타입'''
    def __init__(self, value: int):
        self.value = value

class Float(KavanaDataType):
    '''실수형 데이터 타입'''
    def __init__(self, value: float):
        self.value = value

class Boolean(KavanaDataType):
    '''boolean 데이터 타입'''
    def __init__(self, value: bool):
        self.value = value

class String(KavanaDataType):
    '''문자열 데이터 타입'''
    def __init__(self, value: str):
        self.value = value

class NoneType(KavanaDataType):
    '''None 데이터 타입'''
    def __init__(self):
        self.value = None

class Date(KavanaDataType):
    '''날짜 데이터 타입'''
    def __init__(self, value: datetime):
        self.value = value
