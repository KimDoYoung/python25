from lib.core.builtins.builtin_consts import PointName
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.point import Point
class Region(KavanaDataType):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = (x, y, width, height)  # ✅ (x, y, width, height)로 설정

    def contains(self, point: Point) -> bool:
        """해당 Region이 특정 Point를 포함하는지 여부"""
        return self.x <= point.x <= self.x + self.width and \
               self.y <= point.y <= self.y + self.height

    def point_with_name(self, name: PointName) -> Point:
        """해당 Region의 특정 위치에 해당하는 Point를 반환"""
        if name == PointName.LEFT_TOP:
            return Point(self.x, self.y)
        elif name == PointName.RIGHT_TOP:
            return Point(self.x + self.width, self.y)
        elif name == PointName.RIGHT_BOTTOM:
            return Point(self.x + self.width, self.y + self.height)
        elif name == PointName.LEFT_BOTTOM:
            return Point(self.x, self.y + self.height)
        elif name == PointName.TOP_MIDDLE:
            return Point(self.x + self.width // 2, self.y)
        elif name == PointName.BOTTOM_MIDDLE:
            return Point(self.x + self.width // 2, self.y + self.height)
        elif name == PointName.LEFT_MIDDLE:
            return Point(self.x, self.y + self.height // 2)
        elif name == PointName.RIGHT_MIDDLE:
            return Point(self.x + self.width, self.y + self.height // 2)
        elif name == PointName.CENTER:
            return Point(self.x + self.width // 2, self.y + self.height // 2)
        else:
            raise ValueError(f"Invalid PointName: {name}")

    def to_rectangle(self):
        """Region을 Rectangle 객체로 변환"""
        from lib.core.datatypes.rectangle import Rectangle
        return Rectangle.from_points(
            self.point_with_name(PointName.LEFT_TOP),
            self.point_with_name(PointName.RIGHT_BOTTOM)
        )

    def __str__(self):
        return f"Region(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height

    @property
    def string(self):
        """Region을 문자열로 변환"""
        return f"[{self.x}, {self.y}, {self.width}, {self.height}]"

    @property
    def primitive(self):
        """Python 기본 타입 변환 (Region은 `(x, y, width, height)` 튜플로 변환)"""
        return (self.x, self.y, self.width, self.height)
