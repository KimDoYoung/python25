from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    def move(self, dx: int, dy: int):
        """Point 좌표를 이동시키는 메서드"""
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"({self.x}, {self.y})"


# 사용 예제
p1 = Point(10, 20)
print(f"초기 좌표: {p1}")

p1.move(5, -10)
print(f"이동 후 좌표: {p1}")

region1 = Region(0, 0, 50, 50)
print(f"Region 정보: {region1}")
print(f"Point {p1}이 Region 내부에 있는가? {region1.contains(p1)}")
