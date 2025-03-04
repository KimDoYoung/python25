from dataclasses import dataclass, field
from lib.actions.enums import PointName
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.point import Point
@dataclass
class Region(KavanaDataType):
    x: int
    y: int
    width: int
    height: int
    value : tuple = field(init=False)

    def contains(self, point: Point) -> bool:
        """해당 Region이 특정 Point를 포함하는지 여부"""
        return  self.x <= point.x <= self.x + self.width and \
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
        return Rectangle(self.point_with_name(PointName.LEFT_TOP), self.point_with_name(PointName.RIGHT_BOTTOM))    
    
    def __str__(self):
        return f"Region(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
    
    def __post_init__(self):
        self.value = (self.x, self.y, self.width, self.height)
    
    @property
    def to_string(self):
        return f"[{self.x}, {self.y}, {self.width}, {self.height}]"
    
    @property
    def to_python_type(self):
        return (self.x, self.y, self.width, self.height)