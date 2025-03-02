from dataclasses import dataclass
from typing import Any
from datetime import datetime

@dataclass
class KavanaDataType:
    """Kavana의 모든 데이터 타입의 기본 클래스"""
    # value: Any  # 모든 데이터 타입을 지원하는 `value` 필드
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
    
    @property
    def primitive(self):
        """항상 Python 기본 타입(int, float, str, bool, None 등)만 반환"""
        return self.__dict__.get("value")

@dataclass
class Integer(KavanaDataType):
    """정수형 데이터 타입"""
    value: int
@dataclass
class Float(KavanaDataType):
    """실수형 데이터 타입"""
    value: float

@dataclass
class Boolean(KavanaDataType):
    """논리형 데이터 타입"""
    value: bool

@dataclass
class String(KavanaDataType):
    """문자열 데이터 타입"""
    value: str

@dataclass
class NoneType(KavanaDataType):
    """None 데이터 타입"""
    value: None = None  # 기본값을 None으로 설정

@dataclass
class Date(KavanaDataType):
    """날짜 데이터 타입"""
    value: datetime
