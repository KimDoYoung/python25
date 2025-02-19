from typing import Optional, Tuple
import pyautogui
from lib.enums  import PointName, RegionName

def get_point(region , point_name: PointName):
    ''' region 에서 point_name 에 해당하는 좌표를 반환한다.'''
    x, y, w, h = region
    if point_name == PointName.LEFT_TOP:
        return x, y
    elif point_name == PointName.RIGHT_TOP:
        return x+w, y
    elif point_name == PointName.RIGHT_BOTTOM:
        return x+w, y+h
    elif point_name == PointName.LEFT_BOTTOM:
        return x, y+h
    elif point_name == PointName.TOP_MIDDLE:
        return x+w//2, y
    elif point_name == PointName.BOTTOM_MIDDLE:
        return x+w//2, y+h
    elif point_name == PointName.LEFT_MIDDLE:
        return x, y+h//2
    elif point_name == PointName.RIGHT_MIDDLE:
        return x+w, y+h//2
    elif point_name == PointName.CENTER:
        return x+w//2, y+h//2
    else:
        raise ValueError('Invalid point_name: %s' % point_name)

def get_region(region_name: RegionName, base_region: Optional[Tuple[int, int, int, int]] = None) -> Tuple[int, int, int, int]:
    """ 지정된 RegionName에 따라 주어진 base_region을 기준으로 영역을 계산합니다. base_region이 없으면 화면 전체 크기를 기준으로 합니다. """
    if base_region is None:
        screen_width, screen_height = pyautogui.size()
        base_region = (0, 0, screen_width, screen_height)

    left, top, width, height = base_region

    if region_name == RegionName.LEFT_ONE_THIRD:
        return (left, top, width // 3, height)
    elif region_name == RegionName.RIGHT_ONE_THIRD:
        return (left + 2 * (width // 3), top, width // 3, height)
    elif region_name == RegionName.TOP_ONE_THIRD:
        return (left, top, width, height // 3)
    elif region_name == RegionName.BOTTOM_ONE_THIRD:
        return (left, top + 2 * (height // 3), width, height // 3)
    elif region_name == RegionName.LEFT_TOP:
        return (left, top, width // 2, height // 2)
    elif region_name == RegionName.RIGHT_TOP:
        return (left + width // 2, top, width // 2, height // 2)
    elif region_name == RegionName.RIGHT_BOTTOM:
        return (left + width // 2, top + height // 2, width // 2, height // 2)
    elif region_name == RegionName.LEFT_BOTTOM:
        return (left, top + height // 2, width // 2, height // 2)
    elif region_name == RegionName.CENTER:
        return (left + width // 3, top + height // 3, width // 3, height // 3)
    elif region_name == RegionName.LEFT:
        return (left, top, width // 2, height)
    elif region_name == RegionName.RIGHT:
        return (left + width // 2, top, width // 2, height)
    elif region_name == RegionName.TOP:
        return (left, top, width, height // 2)
    elif region_name == RegionName.BOTTOM:
        return (left, top + height // 2, width, height // 2)
    else:
        raise ValueError("잘못된 RegionName 값입니다.")