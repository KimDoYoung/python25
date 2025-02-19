# point_region.py
"""
모듈 설명: 
    - point와 region에 관련된 함수를 제공하는 모듈
주요 기능:
    - get_point_on_region: region에서 point_name에 해당하는 좌표를 반환한다.
    - get_region: 지정된 RegionName에 따라 주어진 base_region을 기준으로 영역을 계산합니다.
    - get_point_with_region: region에서 부터 지정된 방향과 픽셀(px) 거리만큼 떨어진 좌표를 반환.
    - get_point_in_region: region 내에서 특정 좌표로 이동한 위치를 반환하는 함수.

작성자: 김도영
작성일: 2025-02-19
버전: 1.0
"""
from typing import Optional, Tuple
import pyautogui
from lib.enums  import Direction, PointName, RegionName

def get_point_on_region(region , point_name: PointName):
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

def get_point_with_region(region: Tuple[int, int, int, int], direction: Direction, px: int) -> Tuple[int, int]:
    """
    지정된 방향과 픽셀(px) 거리만큼 떨어진 좌표를 반환.

    :param region: (x, y, width, height) 형태의 튜플
    :param direction: 이동 방향 (Direction Enum)
    :param px: 이동할 거리 (픽셀)
    :return: 이동한 좌표 (x, y)
    """
    x, y, w, h = region
    center_x, center_y = x + w // 2, y + h // 2

    if direction == Direction.RIGHT or direction == Direction.EAST:
        return (x + w + px, center_y)
    elif direction == Direction.LEFT or direction == Direction.WEST:
        return (x - px, center_y)
    elif direction == Direction.UP or direction == Direction.NORTH:
        return (center_x, y - px)
    elif direction == Direction.DOWN or direction == Direction.SOUTH:
        return (center_x, y + h + px)
    else:
        raise ValueError("Invalid direction")
    

def get_point_in_region(region: Optional[Tuple[int, int, int, int]], offset_x: int, offset_y: int) -> Optional[Tuple[int, int]]:
    """
    영역(region) 내에서 특정 좌표로 이동한 위치를 반환하는 함수.

    :param region: (x, y, width, height) 형태의 튜플 (pyautogui.locateOnScreen의 반환값)
    :param offset_x: location의 좌측 상단 (0,0) 기준 x축 이동 거리
    :param offset_y: location의 좌측 상단 (0,0) 기준 y축 이동 거리
    :return: 이동한 (absolute_x, absolute_y) 좌표 튜플, location이 None이면 None 반환
    :raises ValueError: 계산된 좌표가 영역을 벗어나면 예외 발생
    """
    if region is None:
        return None  # 이미지 찾기 실패 시 None 반환

    x, y, width, height = region  # (left, top, width, height)
    abs_x, abs_y = x + offset_x, y + offset_y

    # 좌표가 region을 벗어나는 경우 예외 발생
    if not (x <= abs_x < x + width and y <= abs_y < y + height):
        raise ValueError(f"계산된 좌표 ({abs_x}, {abs_y})가 영역 {region}을 벗어났습니다.")

    return (abs_x, abs_y)
