from datetime import datetime, timedelta
from dataclasses import dataclass

from lib.core.datatypes.kavana_datatype import KavanaDataType

@dataclass
class Datetime(KavanaDataType):
    """날짜 및 시간 데이터 타입"""
    value: datetime

    def __init__(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0):
        self.value = datetime(year, month, day, hour, minute, second)

    @property
    def string(self) -> str:
        """항상 문자열(str)로 변환"""
        return self.value.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def primitive(self) -> datetime:
        """Python 기본 타입 변환"""
        return self.value

    def __add__(self, days: int):
        """Datetime + int 지원 (N일 추가)"""
        if isinstance(days, int):
            new_date = self.value + timedelta(days=days)
            return Datetime(new_date.year, new_date.month, new_date.day, new_date.hour, new_date.minute, new_date.second)
        raise TypeError(f"Datetime + {type(days)} 지원되지 않음")

    def __sub__(self, other):
        """Datetime - Datetime 지원 (일 단위 차이 반환)"""
        if isinstance(other, Datetime):
            return (self.value - other.value).days
        raise TypeError(f"Datetime - {type(other)} 지원되지 않음")
