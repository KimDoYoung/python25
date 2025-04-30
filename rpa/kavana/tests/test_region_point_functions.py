import pytest
from lib.core.builtins.builtin_consts import PointName, RegionName
# ---------------------- Enum 정의 ----------------------


# ---------------------- Mock 객체 ----------------------

class MockPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = (x, y)

class MockRegion:
    def __init__(self, x, y, w, h):
        self.value = (x, y, w, h)

class MockTokenUtil:
    @staticmethod
    def region_to_token(x, y, w, h):
        return type("RegionToken", (), {
            "data": MockRegion(x, y, w, h),
            "status": "EVALUATED"
        })()

class MockPointToken:
    def __init__(self, pt):
        self.data = MockPoint(pt.x, pt.y)
        self.status = "EVALUATED"

# ---------------------- 실제 테스트 대상 클래스 ----------------------

class RegionPointFunctions:
    @staticmethod
    def POINT_OF_REGION(region, point_name: str):
        x, y, width, height = region
        point_name = point_name.lower()
        pt = None
        if point_name == PointName.CENTER.value:
            pt = MockPoint(x + width // 2, y + height // 2)
        elif point_name == PointName.TOP_LEFT.value:
            pt = MockPoint(x, y)
        elif point_name == PointName.TOP_CENTER.value:
            pt = MockPoint(x + width // 2, y)
        elif point_name == PointName.TOP_RIGHT.value:
            pt = MockPoint(x + width, y)
        elif point_name == PointName.MIDDLE_LEFT.value:
            pt = MockPoint(x, y + height // 2)
        elif point_name == PointName.MIDDLE_RIGHT.value:
            pt = MockPoint(x + width, y + height // 2)
        elif point_name == PointName.BOTTOM_LEFT.value:
            pt = MockPoint(x, y + height)
        elif point_name == PointName.BOTTOM_CENTER.value:
            pt = MockPoint(x + width // 2, y + height)
        elif point_name == PointName.BOTTOM_RIGHT.value:
            pt = MockPoint(x + width, y + height)
        else:
            raise ValueError(f"Unknown point name: {point_name}")
        return MockPointToken(pt)

    @staticmethod
    def REGION_OF_REGION(region, region_name: str):
        x, y, width, height = region
        region_name = region_name.lower()
        if region_name == RegionName.LEFT_ONE_THIRD.value:
            return MockTokenUtil.region_to_token(x, y, width // 3, height)
        elif region_name == RegionName.RIGHT_ONE_THIRD.value:
            return MockTokenUtil.region_to_token(x + 2 * (width // 3), y, width // 3, height)
        elif region_name == RegionName.TOP_ONE_THIRD.value:
            return MockTokenUtil.region_to_token(x, y, width, height // 3)
        elif region_name == RegionName.BOTTOM_ONE_THIRD.value:
            return MockTokenUtil.region_to_token(x, y + 2 * (height // 3), width, height // 3)
        elif region_name == RegionName.TOP_LEFT.value:
            return MockTokenUtil.region_to_token(x, y, width // 2, height // 2)
        elif region_name == RegionName.TOP_RIGHT.value:
            return MockTokenUtil.region_to_token(x + width // 2, y, width // 2, height // 2)
        elif region_name == RegionName.BOTTOM_RIGHT.value:
            return MockTokenUtil.region_to_token(x + width // 2, y + height // 2, width // 2, height // 2)
        elif region_name == RegionName.BOTTOM_LEFT.value:
            return MockTokenUtil.region_to_token(x, y + height // 2, width // 2, height // 2)
        elif region_name == RegionName.CENTER.value:
            return MockTokenUtil.region_to_token(x + width // 3, y + height // 3, width // 3, height // 3)
        elif region_name == RegionName.LEFT.value:
            return MockTokenUtil.region_to_token(x, y, width // 2, height)
        elif region_name == RegionName.RIGHT.value:
            return MockTokenUtil.region_to_token(x + width // 2, y, width // 2, height)
        elif region_name == RegionName.TOP.value:
            return MockTokenUtil.region_to_token(x, y, width, height // 2)
        elif region_name == RegionName.BOTTOM.value:
            return MockTokenUtil.region_to_token(x, y + height // 2, width, height // 2)
        else:
            raise ValueError(f"Unknown region name: {region_name}")

# ---------------------- 테스트 코드 ----------------------

@pytest.mark.parametrize("point_name,expected", [
    ("center", (50, 50)),
    ("top-left", (0, 0)),
    ("top-center", (50, 0)),
    ("top-right", (100, 0)),
    ("middle-left", (0, 50)),
    ("middle-right", (100, 50)),
    ("bottom-left", (0, 100)),
    ("bottom-center", (50, 100)),
    ("bottom-right", (100, 100)),
])
def test_POINT_OF_REGION(point_name, expected):
    region = (0, 0, 100, 100)
    token = RegionPointFunctions.POINT_OF_REGION(region, point_name)
    assert token.data.value == expected

@pytest.mark.parametrize("region_name,expected", [
    ("left-one-third", (0, 0, 33, 100)),
    ("right-one-third", (66, 0, 33, 100)),
    ("top-one-third", (0, 0, 100, 33)),
    ("bottom-one-third", (0, 66, 100, 33)),
    ("top-left", (0, 0, 50, 50)),
    ("top-right", (50, 0, 50, 50)),
    ("bottom-right", (50, 50, 50, 50)),
    ("bottom-left", (0, 50, 50, 50)),
    ("center", (33, 33, 33, 33)),
    ("left", (0, 0, 50, 100)),
    ("right", (50, 0, 50, 100)),
    ("top", (0, 0, 100, 50)),
    ("bottom", (0, 50, 100, 50)),
])
def test_REGION_OF_REGION(region_name, expected):
    region = (0, 0, 100, 100)
    token = RegionPointFunctions.REGION_OF_REGION(region, region_name)
    assert token.data.value == expected
