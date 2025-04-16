from enum import Enum
from typing import Optional, Tuple


class RegionName(Enum):
    LEFT_ONE_THIRD = 1
    RIGHT_ONE_THIRD = 2
    TOP_ONE_THIRD = 3
    BOTTOM_ONE_THIRD = 4
    LEFT_TOP = 5
    RIGHT_TOP = 6
    RIGHT_BOTTOM = 7
    LEFT_BOTTOM = 8
    CENTER = 9
    LEFT = 10
    RIGHT = 11
    TOP = 12
    BOTTOM = 13

def get_region(region_name: RegionName, base_region: Optional[Tuple[int, int, int, int]] = None) -> Tuple[int, int, int, int]:

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