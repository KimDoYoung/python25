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

import re
import time
import ctypes
import pyautogui
import psutil
from enum import Enum
from typing import Optional, Tuple

import pyperclip
from config import Config
from logger import Logger
import keyboard

log = Logger()

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

def get_scale_factor() -> float:
    """ 현재 사용자의 화면 DPI 스케일 팩터를 반환합니다. """
    return ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

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

def wait_for_image(image_path, timeout=60, confidence=0.8, region=None, grayscale=False, wait_seconds=0):
    """ 지정된 이미지가 화면에 나타날 때까지 대기합니다. """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region, grayscale=grayscale)
            if location:
                log.debug(f"wait_for_image: 이미지 찾음: {image_path}")
                return location
        except pyautogui.ImageNotFoundException:
            log.warning(f"wait_for_image: 이미지 찾기 실패: {image_path}")
            pass
        time.sleep(1)
    if wait_seconds > 0:
        time.sleep(wait_seconds)    
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

def find_and_click(image_path, region=None, grayscale=True, confidence=0.8,wait_seconds=1, timeout=60):
    """ 이미지를 찾아 클릭하는 함수. 실패 시 Exception 발생 """
    element = wait_for_image(image_path, region=region, grayscale=grayscale, confidence=confidence, timeout=timeout)
    if not element:
        raise Exception(f"이미지 찾기 실패: {image_path}")
    
    center = pyautogui.center(element)
    pyautogui.moveTo(center.x, center.y, duration=0.5)
    pyautogui.click()
    time.sleep(wait_seconds)
    return center

def find_and_press_key(image_path: str, key: str, region: Optional[tuple] = None, grayscale: bool = True, confidence: float = 0.8, ignoreNotFound=False, timeout=60) -> bool :
    """
    특정 이미지를 찾으면 해당 키를 누르는 함수.

    :param image_path: 찾을 이미지 경로
    :param key: 찾았을 때 누를 키 (예: 'space', 'enter')
    :param region: 검색할 화면 영역 (기본값: 전체 화면)
    :param grayscale: 흑백 모드 사용 여부 (기본값: True)
    :param confidence: 이미지 유사도 임계값 (기본값: 0.8)
    :return: 이미지 찾으면 True, 못 찾으면 False
    """
    element = wait_for_image(image_path, region=region, grayscale=grayscale, confidence=confidence, timeout=timeout)
    if not element:
        if ignoreNotFound:
            return False
        else:
            raise Exception(f"이미지 찾기 실패: {image_path}") 
    pyautogui.press(key)
    time.sleep(1)
    return True

def move_and_click(image_path: str, region: Optional[Tuple[int, int, int, int]] = None, grayscale: bool = True, confidence: float = 0.8, duration: float = 0.5, wait_seconds=1) -> bool:
    """
    특정 이미지를 찾아서 해당 위치로 이동한 후 클릭하는 함수.

    :param image_path: 찾을 이미지 경로
    :param region: 검색할 화면 영역 (기본값: 전체 화면)
    :param grayscale: 흑백 모드 사용 여부 (기본값: True)
    :param confidence: 이미지 유사도 임계값 (기본값: 0.8)
    :param duration: 마우스 이동 시간 (기본값: 0.5초)
    :return: 성공적으로 클릭하면 True, 찾지 못하면 False
    """
    element = wait_for_image(image_path, region=region, grayscale=grayscale, confidence=confidence)
    if element:
        center = pyautogui.center(element)
        pyautogui.moveTo(center.x, center.y, duration=duration)
        pyautogui.click()
        time.sleep(wait_seconds)
    else:
        raise Exception(f"이미지 찾기 실패: {image_path}")

def mouse_move_and_click(x: int, y: int, duration: float = 0.5, wait_seconds=1) -> None:
    """
    지정한 좌표로 마우스를 이동한 후 클릭하는 함수.

    :param x: X 좌표
    :param y: Y 좌표
    :param duration: 마우스 이동 시간 (기본값: 0.5초)
    """
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()
    time.sleep(wait_seconds)

def press_keys(keys, delay=0.2, wait_seconds=1):
    """
    여러 개의 키를 순차적으로 입력하는 함수.
    
    :param keys: 입력할 키들의 리스트 (예: ['down', 'down', 'enter'])
    :param delay: 각 키 입력 후 대기 시간 (기본값: 0.2초)
    :param wait_seconds: 모든 키 입력 후 추가 대기 시간 (기본값: 1초)
    """
    for key in keys:
        pyautogui.press(key)
        time.sleep(delay)
    
    time.sleep(wait_seconds)  # 모든 키 입력 후 추가 대기

def move_and_press(x:int, y: int, key: str, duration: float = 0.5, wait_seconds=1):
    """
    특정 좌표로 이동한 후 키를 누르는 함수.

    :param x: X 좌표
    :param y: Y 좌표
    :param key: 누를 키 (예: 'space', 'enter')
    :param duration: 마우스 이동 시간 (기본값: 0.5초)
    """
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.press(key)
    time.sleep(wait_seconds)

def put_keys(command_str, interval=0.2, sleep_time=0.5):
    """
    문자열 기반 키 입력 자동화 함수 (pyperclip + pyautogui 사용)

    - 형식: `H:ctrl+shift+a | P:delete | W:"C:\\Users\\MyUser\\Documents\\file.txt" | P:enter`
    - H: 핫키 (여러 개 가능, 예: `H:ctrl+shift+a`)
    - P: 단일 키 입력 (예: `P:delete`, `P:enter`)
    - W: 문자열 입력 (예: `W:"abc"` → "abc" 입력, 클립보드 붙여넣기 방식)

    :param command_str: 매크로 스타일 명령어 문자열 (구분자: `|`)
    :param interval: 키 입력 간격 (기본값 0.2초)
    :param sleep_time: 입력 후 대기 시간 (기본값 0.5초)
    :raises ValueError: 지원되지 않는 명령어 형식일 경우 예외 발생
    """
    commands = command_str.split("|")  # '|' 기준으로 명령어 분리

    for cmd in commands:
        cmd = cmd.strip()

        if cmd.startswith("H:"):  # 핫키 (예: H:ctrl+shift+a)
            hotkeys = cmd[2:].split("+")  # '+' 기준으로 여러 키 분리
            pyautogui.hotkey(*hotkeys, interval=interval)

        elif cmd.startswith("P:"):  # 단일 키 입력 (예: P:delete)
            key = cmd[2:].strip()
            pyautogui.press(key, interval=interval)

        elif cmd.startswith("W:"):  # 문자열 입력 (예: W:"C:\경로\파일.txt")
            text_match = re.match(r'W:"(.*?)"', cmd)  # 큰따옴표 안의 문자열 추출
            if text_match:
                text = text_match.group(1)  # "..." 안의 내용만 가져옴
                pyperclip.copy(text)  # 클립보드에 복사
                time.sleep(0.1)  # 복사가 완료될 때까지 잠깐 대기
                pyautogui.hotkey("ctrl", "v")  # Ctrl+V로 붙여넣기
            else:
                raise ValueError(f"잘못된 문자열 입력 형식: {cmd}")

        else:
            raise ValueError(f"지원되지 않는 명령어: {cmd}")

        time.sleep(sleep_time)  # 각 동작 후 대기