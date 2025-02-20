from dataclasses import dataclass
from typing import Tuple

@dataclass
class Point:
    """2D 좌표를 표현하는 데이터 클래스"""
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        """(x, y) 튜플 형태로 반환"""
        return self.x, self.y

@dataclass
class Region:
    """화면의 영역을 표현하는 데이터 클래스"""
    x: int
    y: int
    width: int
    height: int

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """(x, y, width, height) 튜플 형태로 반환"""
        return self.x, self.y, self.width, self.height

    def contains(self, point: Point) -> bool:
        """Point가 현재 Region 내부에 있는지 확인"""
        return self.x <= point.x < self.x + self.width and self.y <= point.y < self.y + self.height

    def center(self) -> Point:
        """영역의 중앙 좌표 반환"""
        return Point(self.x + self.width // 2, self.y + self.height // 2)
