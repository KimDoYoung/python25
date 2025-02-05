# 📁 hts_utils.py
import os
import time
import ctypes
import pyautogui
import psutil
from dotenv import load_dotenv
from enum import Enum
from typing import Optional, Tuple

# 환경 변수 로드
load_dotenv()
KIS_CERTI_PW = os.getenv("KIS_CERTI_PW")

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
    else:
        raise ValueError("잘못된 RegionName 값입니다.")

def is_admin():
    """ 현재 프로세스가 관리자 권한으로 실행 중인지 확인합니다. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"관리자 권한 확인 오류: {e}")
        return False

def is_hts_running(process_name="efriendplus.exe"):
    """ HTS 프로그램이 실행 중인지 확인합니다. """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False

def wait_for_image(image_path, timeout=60, confidence=0.8, region=None):
    """ 지정된 이미지가 화면에 나타날 때까지 대기합니다. """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)
    return None

def find_for_image(image_path, confidence=0.8, region=None):
    """ 화면에서 이미지를 찾으면 반환, 없으면 None """
    try:
        return pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
    except pyautogui.ImageNotFoundException:
        return None
