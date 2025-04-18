from dataclasses import dataclass
from typing import Any
from datetime import datetime

@dataclass
class KavanaDataType:
    """Kavana의 모든 데이터 타입의 기본 클래스"""
    value: Any

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def type_name(self) -> str:
        return self.__class__.__name__
    
    @property
    def primitive(self):
        """Python 기본 타입(int, float, str, list 등)으로 변환"""
        return self.value

    @property
    def string(self):
        """항상 문자열(str)로 변환"""
        return str(self.primitive)

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

