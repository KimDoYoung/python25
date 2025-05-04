from datetime import date, datetime, timedelta
from dataclasses import dataclass

from lib.core.datatypes.kavana_datatype import KavanaDataType

@dataclass
class YmdTime(KavanaDataType):
    """YMD(년월일) + 시간 정보 포함한 데이터 타입"""
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

    @property
    def year(self) -> int:
        return self.value.year

    @property
    def month(self) -> int:
        return self.value.month

    @property
    def day(self) -> int:
        return self.value.day
    
    @property
    def hour(self) -> int:
        return self.value.hour
    
    @property
    def minute(self) -> int:
        return self.value.minute
    
    @property
    def second(self) -> int:
        return self.value.second

    def __add__(self, days: int):
        """YmdTime + int 지원 (N일 추가)"""
        if isinstance(days, int):
            new_date = self.value + timedelta(days=days)
            return YmdTime(new_date.year, new_date.month, new_date.day, new_date.hour, new_date.minute, new_date.second)
        raise TypeError(f"YmdTime + {type(days)} 지원되지 않음")

    def __sub__(self, other):
        """YmdTime - YmdTime 지원 (일 단위 차이 반환)"""
        if isinstance(other, YmdTime):
            return (self.value - other.value).days
        raise TypeError(f"YmdTime - {type(other)} 지원되지 않음")

    @classmethod
    def from_datetime(cls, dt: datetime) -> "YmdTime":
        """datetime 객체를 YmdTime으로 변환"""
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    

@dataclass
class Ymd(KavanaDataType):
    """✅ YMD(년-월-일)만 포함한 데이터 타입"""
    value: date  # ✅ 시간 정보 없이 `date` 타입만 사용

    def __init__(self, year: int, month: int, day: int):
        self.value = date(year, month, day)

    def __eq__(self, other):
        """✅ Ymd 객체 비교"""
        if isinstance(other, Ymd):
            return self.value == other.value
        return False

    @property
    def string(self) -> str:
        """✅ 항상 문자열(str)로 변환"""
        return self.value.strftime("%Y-%m-%d")

    @property
    def primitive(self) -> date:
        """✅ Python 기본 타입 변환"""
        return self.value

    @property
    def year(self):
        return self.value.year

    @property
    def month(self):
        return self.value.month

    @property
    def day(self):
        return self.value.day

    def __add__(self, days: int):
        """✅ Ymd + int 지원 (N일 추가)"""
        if isinstance(days, int):
            new_date = self.value + timedelta(days=days)
            return Ymd(new_date.year, new_date.month, new_date.day)
        raise TypeError(f"Ymd + {type(days)} 지원되지 않음")

    def __sub__(self, other):
        """✅ Ymd - Ymd 지원 (일 단위 차이 반환)"""
        if isinstance(other, Ymd):
            return (self.value - other.value).days
        raise TypeError(f"Ymd - {type(other)} 지원되지 않음")

    @classmethod
    def from_date(cls, dt: date) -> "Ymd":
        """✅ `date` 객체를 `Ymd`로 변환"""
        return cls(dt.year, dt.month, dt.day)
