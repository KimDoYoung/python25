from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.point import Point
from lib.core.datatypes.region import Region
class Rectangle(KavanaDataType):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.value = (x1, y1, x2, y2)  # ✅ (x1, y1, x2, y2)로 설정

    def width(self) -> int:
        """사각형의 너비 계산"""
        return abs(self.p2.x - self.p1.x)

    def height(self) -> int:
        """사각형의 높이 계산"""
        return abs(self.p2.y - self.p1.y)

    def area(self) -> int:
        """사각형의 면적 계산"""
        return self.width() * self.height()

    def contains(self, x: int, y: int) -> bool:
        """점이 사각형 안에 포함되는지 확인"""
        return self.p1.x <= x <= self.p2.x and self.p1.y <= y <= self.p2.y

    def to_region(self) -> Region:
        """Rectangle을 Region 객체로 변환"""
        x1, y1 = min(self.p1.x, self.p2.x), min(self.p1.y, self.p2.y)
        width, height = self.width(), self.height()
        return Region(x1, y1, width, height)

    def __str__(self):
        return f"Rectangle({self.p1}, {self.p2})"

    def __iter__(self):
        yield self.p1.x
        yield self.p1.y
        yield self.p2.x
        yield self.p2.y

    @property
    def string(self):
        """사각형을 문자열로 변환"""
        return f"[{self.p1.x}, {self.p1.y}, {self.p2.x}, {self.p2.y}]"

    @property
    def primitive(self):
        """Python 기본 타입 변환 (Rectangle은 `(x, y, width, height)` 튜플로 변환)"""
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        return (x1, y1, x2, y2)

