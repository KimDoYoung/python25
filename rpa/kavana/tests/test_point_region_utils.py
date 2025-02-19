import pyautogui
import pytest
from lib.enums import RegionName, PointName
from lib.point_region_utils import get_point,  get_region

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
    assert get_point(region, point_name) == expected

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