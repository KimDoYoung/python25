from lib.core.datatypes.kavana_datatype import KavanaDataType

class Point(KavanaDataType):
    def __init__(self, x: int, y: int):
        super().__init__((x, y))  # ✅ value를 (x, y) 튜플로 설정
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        """Point 좌표를 이동시키는 메서드"""
        self.x += dx
        self.y += dy
        self.value = (self.x, self.y)  # ✅ value 업데이트

    def __str__(self):
        return f"({self.x}, {self.y})"

    @property
    def string(self):
        """항상 문자열(str)로 변환"""
        return self.__str__()

    @property
    def primitive(self):
        """Python 기본 타입 변환 (Point는 튜플로 변환)"""
        return self.value


# from dataclasses import dataclass, field
# from typing import TYPE_CHECKING
# from lib.core.datatypes.kavana_datatype import KavanaDataType

# if TYPE_CHECKING:
#     from lib.core.datatypes.region import Region  # 순환 참조 방지용


# class Point(KavanaDataType):
#     def __init__(self, x: int, y: int):
#         self.x = x
#         self.y = y
#         self.value = (x, y)  # ✅ value 속성 설정
    
#     def move(self, dx: int, dy: int):
#         """Point 좌표를 이동시키는 메서드"""
#         self.x += dx
#         self.y += dy

#     def __str__(self):
#         return f"({self.x}, {self.y})"

#     @property
#     def to_string(self):
#         """항상 문자열(str)로 변환"""
#         return self.__str__()

#     @property
#     def to_python_type(self):
#         """Python 기본 타입 변환 (Point는 튜플로 변환)"""
#         return (self.x, self.y)