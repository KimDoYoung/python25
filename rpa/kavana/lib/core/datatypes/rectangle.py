from dataclasses import dataclass, field

from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.point import Point
from lib.core.datatypes.region import Region


@dataclass
class Rectangle(KavanaDataType):
    p1: Point
    p2: Point
    value: tuple = field(init=False)
    
    def width(self) -> int:
        """사각형의 너비 계산"""
        return abs(self.p2.x - self.p1.x)

    def height(self) -> int:
        """사각형의 높이 계산"""
        return abs(self.p2.y - self.p1.y)

    def area(self) -> int:
        """사각형의 면적 계산"""
        return self.width() * self.height()

    def contains(self, point: Point) -> bool:
        """점이 사각형 안에 포함되는지 확인"""
        return self.p1.x <= point.x <= self.p2.x and self.p1.y <= point.y <= self.p2.y

    def to_region(self) -> Region:
        """Rectangle을 Region 객체로 변환"""
        x1, y1 = min(self.p1.x, self.p2.x), min(self.p1.y, self.p2.y)
        x2, y2 = max(self.p1.x, self.p2.x), max(self.p1.y, self.p2.y)
        return Region(x1, y1, x2 - x1, y2 - y1)

    def __str__(self):
        return f"Rectangle({self.p1}, {self.p2})"
    
    def __post_init__(self):
        self.value = ({self.p1}, {self.p2})
    
    @property
    def to_string(self):
        return f"[{self.p1.x}, {self.p1.y}, {self.p2.x}, {self.p2.y}]"
    
    @property
    def to_python_type(self):
        return self.value