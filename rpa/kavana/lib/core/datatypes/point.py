from lib.core.datatypes.kavana_datatype import KavanaDataType

class Point(KavanaDataType):
    def __init__(self, x: int, y: int):
        super().__init__((x, y))  # ✅ value를 (x, y) 튜플로 설정
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        """Point 객체 비교"""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def move(self, dx: int, dy: int):
        """Point 좌표를 이동시키는 메서드"""
        self.x += dx
        self.y += dy
        self.value = (self.x, self.y)  # ✅ value 업데이트
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
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

