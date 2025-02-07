# rpa_utils.py
"""
모듈 설명
    - RPA 프로그램에 사용하는 유틸리티 함수 모음
    
주요 기능:
    - get_region: 지정된 RegionName에 따라 주어진 base_region을 기준으로 영역을 계산합니다.
    - is_admin: 현재 프로세스가 관리자 권한으로 실행 중인지 확인합니다.
    - is_process_running: 프로그램이 실행 중인지 확인합니다.
    - wait_for_image: 지정된 이미지가 화면에 나타날 때까지 대기합니다.
    - find_for_image: 화면에서 이미지를 찾으면 반환, 없으면 None
    - get_point_in_region: 찾은 영역(location) 내에서 특정 좌표로 이동한 위치를 반환하는 함수.

작성자: 김도영
작성일: 2025-02-06
버전: 1.0
"""

import os
import time
import ctypes
import pyautogui
import psutil
from dotenv import load_dotenv
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

class Direction(Enum):
    RIGHT = "Right"
    LEFT = "Left"
    UP = "Up"
    DOWN = "Down"    

def get_point_with_location(location: Tuple[int, int, int, int], direction: Direction, px: int) -> Tuple[int, int]:
    """
    지정된 방향과 픽셀(px) 거리만큼 떨어진 좌표를 반환.

    :param location: (x, y, width, height) 형태의 튜플
    :param direction: 이동 방향 (Direction Enum)
    :param px: 이동할 거리 (픽셀)
    :return: 이동한 좌표 (x, y)
    """
    x, y, w, h = location
    center_x, center_y = x + w // 2, y + h // 2

    if direction == Direction.RIGHT:
        return (x + w + px, center_y)
    elif direction == Direction.LEFT:
        return (x - px, center_y)
    elif direction == Direction.UP:
        return (center_x, y - px)
    elif direction == Direction.DOWN:
        return (center_x, y + h + px)
    else:
        raise ValueError("Invalid direction")

def get_region(region_name: RegionName, base_region: Optional[Tuple[int, int, int, int]] = None) -> Tuple[int, int, int, int]:
    """ 지정된 RegionName에 따라 주어진 base_region을 기준으로 영역을 계산합니다. """
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

def is_admin():
    """ 현재 프로세스가 관리자 권한으로 실행 중인지 확인합니다. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"관리자 권한 확인 오류: {e}")
        return False

def is_process_running(process_name="efriendplus.exe"):
    """ 프로그램이 실행 중인지 확인합니다. """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False

def wait_for_image(image_path, timeout=60, confidence=0.8, region=None, grayscale=False):
    """ 지정된 이미지가 화면에 나타날 때까지 대기합니다. """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region, grayscale=grayscale)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)
    return None

def find_for_image(image_path, confidence=0.8, region=None, grayscale=False):
    """ 화면에서 이미지를 찾으면 반환, 없으면 None """
    try:
        return pyautogui.locateOnScreen(image_path, confidence=confidence, region=region, grayscale=grayscale)
    except pyautogui.ImageNotFoundException:
        return None

def get_point_in_region(location: Optional[Tuple[int, int, int, int]], offset_x: int, offset_y: int) -> Optional[Tuple[int, int]]:
    """
    찾은 영역(location) 내에서 특정 좌표로 이동한 위치를 반환하는 함수.

    :param location: (x, y, width, height) 형태의 튜플 (pyautogui.locateOnScreen의 반환값)
    :param offset_x: location의 좌측 상단 (0,0) 기준 x축 이동 거리
    :param offset_y: location의 좌측 상단 (0,0) 기준 y축 이동 거리
    :return: 이동한 (absolute_x, absolute_y) 좌표 튜플, location이 None이면 None 반환
    """
    if location is None:
        return None  # 이미지 찾기 실패 시 None 반환

    x, y, _, _ = location  # (left, top, width, height) 중 x, y만 사용
    return (x + offset_x, y + offset_y)