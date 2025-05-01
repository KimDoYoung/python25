import pytest
from lib.core.builtins.region_point_functions import RegionPointFunctions
from lib.core.builtins.builtin_consts import PointName, RegionName

# Mock PointToken과 RegionToken이 TokenStatus.EVALUATED이고 value를 가지는지 확인
def get_point_value(token):
    assert token.status.name == "EVALUATED"
    return token.data.x, token.data.y

def get_region_value(token):
    assert token.status.name == "EVALUATED"
    return token.data.x, token.data.y, token.data.width, token.data.height

# ---------------------- POINT 테스트 ----------------------

@pytest.mark.parametrize("point_name,expected", [
    (PointName.CENTER.value, (50, 50)),
    (PointName.TOP_LEFT.value, (0, 0)),
    (PointName.TOP_CENTER.value, (50, 0)),
    (PointName.TOP_RIGHT.value, (100, 0)),
    (PointName.MIDDLE_LEFT.value, (0, 50)),
    (PointName.MIDDLE_RIGHT.value, (100, 50)),
    (PointName.BOTTOM_LEFT.value, (0, 100)),
    (PointName.BOTTOM_CENTER.value, (50, 100)),
    (PointName.BOTTOM_RIGHT.value, (100, 100)),
])
def test_POINT_OF_REGION(point_name, expected):
    region = (0, 0, 100, 100)
    token = RegionPointFunctions.POINT_OF_REGION(region, point_name)
    assert get_point_value(token) == expected

# ---------------------- REGION 테스트 ----------------------

@pytest.mark.parametrize("region_name,expected", [
    (RegionName.LEFT_ONE_THIRD.value, (0, 0, 33, 100)),
    (RegionName.RIGHT_ONE_THIRD.value, (66, 0, 33, 100)),
    (RegionName.TOP_ONE_THIRD.value, (0, 0, 100, 33)),
    (RegionName.BOTTOM_ONE_THIRD.value, (0, 66, 100, 33)),
    (RegionName.TOP_LEFT.value, (0, 0, 50, 50)),
    (RegionName.TOP_RIGHT.value, (50, 0, 50, 50)),
    (RegionName.BOTTOM_RIGHT.value, (50, 50, 50, 50)),
    (RegionName.BOTTOM_LEFT.value, (0, 50, 50, 50)),
    (RegionName.CENTER.value, (33, 33, 33, 33)),
    (RegionName.LEFT.value, (0, 0, 50, 100)),
    (RegionName.RIGHT.value, (50, 0, 50, 100)),
    (RegionName.TOP.value, (0, 0, 100, 50)),
    (RegionName.BOTTOM.value, (0, 50, 100, 50)),
])
def test_REGION_OF_REGION(region_name, expected):
    region = (0, 0, 100, 100)
    token = RegionPointFunctions.REGION_OF_REGION(region, region_name)
    assert get_region_value(token) == expected

@pytest.mark.parametrize("point, region, expected", [
    ((10, 10), (0, 0, 100, 100), True),   # 내부에 있음
    ((0, 0), (0, 0, 100, 100), True),     # 꼭짓점
    ((100, 100), (0, 0, 100, 100), True), # 오른쪽 하단 꼭짓점 포함
    ((101, 101), (0, 0, 100, 100), False),# 바깥
    ((-1, 10), (0, 0, 100, 100), False),  # 왼쪽 바깥
    ((50, 200), (0, 0, 100, 100), False), # 아래쪽 바깥
])
def test_is_point_in_region(point, region, expected):
    token = RegionPointFunctions.IS_POINT_IN_REGION(point, region)
    assert token.data.value == expected