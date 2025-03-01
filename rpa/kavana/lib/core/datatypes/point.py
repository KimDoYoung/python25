from dataclasses import dataclass
from typing import TYPE_CHECKING
from lib.core.datatypes.kavana_datatype import KavanaDataType

if TYPE_CHECKING:
    from lib.core.datatypes.region import Region  # 순환 참조 방지용

@dataclass
class Point(KavanaDataType):
    x: int
    y: int

    def move(self, dx: int, dy: int):
        """Point 좌표를 이동시키는 메서드"""
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"({self.x}, {self.y})"


