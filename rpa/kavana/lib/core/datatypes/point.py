from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from lib.core.datatypes.kavana_datatype import KavanaDataType

if TYPE_CHECKING:
    from lib.core.datatypes.region import Region  # 순환 참조 방지용

@dataclass
class Point(KavanaDataType):
    x: int
    y: int
    value: tuple = field(init=False)  # ✅ value 속성 추가
    
    def move(self, dx: int, dy: int):
        """Point 좌표를 이동시키는 메서드"""
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __post_init__(self):
        self.value = ({self.x}, {self.y})

    @property
    def to_string(self):
        """항상 문자열(str)로 변환"""
        return self.__str__()

    @property
    def to_python_type(self):
        """Python 기본 타입 변환 (Point는 튜플로 변환)"""
        return (self.x, self.y)