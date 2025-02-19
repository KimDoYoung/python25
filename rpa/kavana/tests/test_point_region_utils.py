from typing import Tuple
import pyautogui
import pytest
from lib.enums import Direction, RegionName, PointName
from lib.point_region import get_point_on_region, get_point_in_region, get_point_with_region,  get_region

@pytest.mark.parametrize("region, point_name, expected", [
    ((10, 20, 100, 200), PointName.LEFT_TOP, (10, 20)),
    ((10, 20, 100, 200), PointName.RIGHT_TOP, (110, 20)),
    ((10, 20, 100, 200), PointName.RIGHT_BOTTOM, (110, 220)),
    ((10, 20, 100, 200), PointName.LEFT_BOTTOM, (10, 220)),
    ((10, 20, 100, 200), PointName.TOP_MIDDLE, (60, 20)),
    ((10, 20, 100, 200), PointName.BOTTOM_MIDDLE, (60, 220)),
    ((10, 20, 100, 200), PointName.LEFT_MIDDLE, (10, 120)),
    ((10, 20, 100, 200), PointName.RIGHT_MIDDLE, (110, 120)),
    ((10, 20, 100, 200), PointName.CENTER, (60, 120)),
])

def test_get_point_name(region, point_name, expected):
    assert get_point_on_region(region, point_name) == expected

@pytest.mark.parametrize(
    "region_name, base_region, expected",
    [
        # 기본 전체 화면을 기준으로 한 테스트
        (RegionName.LEFT_ONE_THIRD, None, (0, 0, pyautogui.size()[0] // 3, pyautogui.size()[1])),
        (RegionName.RIGHT_ONE_THIRD, None, (2 * (pyautogui.size()[0] // 3), 0, pyautogui.size()[0] // 3, pyautogui.size()[1])),
        (RegionName.TOP_ONE_THIRD, None, (0, 0, pyautogui.size()[0], pyautogui.size()[1] // 3)),
        (RegionName.BOTTOM_ONE_THIRD, None, (0, 2 * (pyautogui.size()[1] // 3), pyautogui.size()[0], pyautogui.size()[1] // 3)),
        (RegionName.LEFT_TOP, None, (0, 0, pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)),
        (RegionName.RIGHT_TOP, None, (pyautogui.size()[0] // 2, 0, pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)),
        (RegionName.RIGHT_BOTTOM, None, (pyautogui.size()[0] // 2, pyautogui.size()[1] // 2, pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)),
        (RegionName.LEFT_BOTTOM, None, (0, pyautogui.size()[1] // 2, pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)),
        (RegionName.CENTER, None, (pyautogui.size()[0] // 3, pyautogui.size()[1] // 3, pyautogui.size()[0] // 3, pyautogui.size()[1] // 3)),
        (RegionName.LEFT, None, (0, 0, pyautogui.size()[0] // 2, pyautogui.size()[1])),
        (RegionName.RIGHT, None, (pyautogui.size()[0] // 2, 0, pyautogui.size()[0] // 2, pyautogui.size()[1])),
        (RegionName.TOP, None, (0, 0, pyautogui.size()[0], pyautogui.size()[1] // 2)),
        (RegionName.BOTTOM, None, (0, pyautogui.size()[1] // 2, pyautogui.size()[0], pyautogui.size()[1] // 2)),

        # 특정 base_region을 기준으로 한 테스트
        (RegionName.LEFT_ONE_THIRD, (0, 0, 900, 600), (0, 0, 300, 600)),
        (RegionName.RIGHT_ONE_THIRD, (0, 0, 900, 600), (600, 0, 300, 600)),
        (RegionName.CENTER, (0, 0, 900, 600), (300, 200, 300, 200)),
    ]
)
def test_get_region(region_name, base_region, expected):
    """get_region 함수가 올바른 영역을 반환하는지 테스트"""
    assert get_region(region_name, base_region) == expected

def test_get_region_invalid():
    """잘못된 RegionName이 주어졌을 때 ValueError가 발생하는지 테스트"""
    with pytest.raises(ValueError, match="잘못된 RegionName 값입니다."):
        get_region("INVALID_REGION")    
        

@pytest.mark.parametrize(
    "region, direction, px, expected",
    [
        # 오른쪽으로 이동
        ((100, 100, 50, 50), Direction.RIGHT, 10, (160, 125)),
        ((200, 200, 100, 100), Direction.RIGHT, 20, (320, 250)),

        # 왼쪽으로 이동
        ((100, 100, 50, 50), Direction.LEFT, 10, (90, 125)),
        ((200, 200, 100, 100), Direction.LEFT, 20, (180, 250)),

        # 위쪽으로 이동
        ((100, 100, 50, 50), Direction.UP, 10, (125, 90)),
        ((200, 200, 100, 100), Direction.UP, 20, (250, 180)),

        # 아래쪽으로 이동
        ((100, 100, 50, 50), Direction.DOWN, 10, (125, 160)),
        ((200, 200, 100, 100), Direction.DOWN, 20, (250, 320)),
    ]
)
def test_get_point_with_location(region: Tuple[int, int, int, int], direction: Direction, px: int, expected: Tuple[int, int]):
    """get_point_with_location 함수가 올바른 좌표를 반환하는지 테스트"""
    assert get_point_with_region(region, direction, px) == expected

def test_get_point_with_location_invalid():
    """잘못된 방향이 주어졌을 때 ValueError가 발생하는지 테스트"""
    with pytest.raises(ValueError, match="Invalid direction"):
        get_point_with_region((100, 100, 50, 50), "INVALID_DIRECTION", 10) 
        

@pytest.mark.parametrize(
    "region, offset_x, offset_y, expected",
    [
        # 정상적인 좌표 이동 테스트
        ((100, 100, 50, 50), 10, 10, (110, 110)),
        ((200, 200, 100, 100), 50, 50, (250, 250)),
        ((300, 300, 150, 150), 0, 0, (300, 300)),  # 이동 없음
    ]
)
def test_get_point_in_region_valid(region: Tuple[int, int, int, int], offset_x: int, offset_y: int, expected: Tuple[int, int]):
    """ 정상적인 좌표 계산 테스트 """
    assert get_point_in_region(region, offset_x, offset_y) == expected

def test_get_point_in_region_none():
    """ region이 None일 때 None 반환 테스트 """
    assert get_point_in_region(None, 10, 10) is None

@pytest.mark.parametrize(
    "region, offset_x, offset_y",
    [
        ((100, 100, 50, 50), -10, -10),  # 왼쪽 위로 벗어남
        ((100, 100, 50, 50), 60, 10),    # 오른쪽으로 벗어남
        ((100, 100, 50, 50), 10, 60),    # 아래쪽으로 벗어남
        ((200, 200, 100, 100), -5, -5),  # 경계 바깥으로 벗어남
        ((200, 200, 100, 100), 100, 100), # 오른쪽 아래로 벗어남
    ]
)
def test_get_point_in_region_out_of_bounds(region: Tuple[int, int, int, int], offset_x: int, offset_y: int):
    """ 좌표가 region을 벗어났을 때 예외 발생 테스트 """
    with pytest.raises(ValueError, match="계산된 좌표 .*가 영역 .*을 벗어났습니다."):
        get_point_in_region(region, offset_x, offset_y)
        