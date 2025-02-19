
import re
import time
import ctypes
import pyautogui
import psutil
from typing import Callable, Optional, Tuple

import pyperclip
from lib.kavana_types import Point, Region
from logger import Logger
import keyboard

log = Logger()

def click_on_point(point: Point, duration: float = 0.5):
    """ 주어진 좌표를 클릭하는 함수 """
    pyautogui.moveTo(point.x, point.y, duration=duration)
    pyautogui.click()

def press_key_on_point(key: str):
    ''' 주어진 키를 누르는 함수 '''
    def _press_key(point: Point):
        pyautogui.press(key)
    return _press_key

def wait_for_image(
    image_path: str,
    timeout: int = 60,
    confidence: float = 0.8,
    region: Optional[Region] = None,
    grayscale: bool = False,
    post_wait_time: int = 0,
    on_found: Optional[Callable[[Point], None]] = None  # ✅ 이미지 찾으면 실행할 콜백 함수
) -> Optional[Point]:
    """ 
    지정된 이미지가 화면에 나타날 때까지 대기 후 중앙 좌표 반환. 
    `on_found`가 주어지면, 이미지를 찾았을 때 실행할 동작 수행.
    """
    start_time = time.time()
    search_region = region.to_tuple() if region else None

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=search_region, grayscale=grayscale)
            if location:
                center = Point(*pyautogui.center(location))
                if on_found:
                    on_found(center)  # ✅ 이미지 찾으면 동작 실행
                time.sleep(post_wait_time)
                return center  # ✅ 중앙 좌표 반환
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)

    return None  # 이미지 찾기 실패 시 None 반환

def find_image_center(image_path: str, confidence: float = 0.8, region: Optional[Region] = None, grayscale: bool = False) -> Optional[Point]:
    """ 화면에서 이미지를 찾으면 중앙 좌표를 반환, 없으면 None """
    try:
        search_region = region.to_tuple() if region else None
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=search_region, grayscale=grayscale)
        if location:
            center_x, center_y = pyautogui.center(location)
            return Point(center_x, center_y)  # ✅ 우리가 정의한 Point 타입으로 변환
    except pyautogui.ImageNotFoundException:
        return None


def press_multiple_keys(keys, delay=0.2, post_wait_time=1):
    """
    여러 개의 키를 순차적으로 입력하는 함수.
    
    :param keys: 입력할 키들의 리스트 (예: ['down', 'down', 'enter'])
    :param delay: 각 키 입력 후 대기 시간 (기본값: 0.2초)
    :param wait_seconds: 모든 키 입력 후 추가 대기 시간 (기본값: 1초)
    """
    for key in keys:
        pyautogui.press(key)
        time.sleep(delay)
    
    time.sleep(post_wait_time)  # 모든 키 입력 후 추가 대기


def execute_key_commands(command_str, interval=0.2, sleep_time=0.5):
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


def get_text_from_input_field(wait_time: float = 0.2) -> str:
    """
    현재 포커스된 입력창의 텍스트를 클립보드에서 가져오는 함수.

    :param wait_time: 각 동작 후 대기 시간 (기본값: 0.2초)
    :return: 입력 필드에서 복사한 텍스트 문자열
    """
    try:
        # 기존 클립보드 내용 저장
        original_clipboard = pyperclip.paste()

        # 텍스트 복사 수행
        pyautogui.hotkey('ctrl', 'a')  
        time.sleep(wait_time)  
        pyautogui.hotkey('ctrl', 'c')  
        time.sleep(wait_time)  

        # 클립보드에서 텍스트 가져오기
        copied_text = pyperclip.paste().strip()

        # 원래 클립보드 내용 복원
        pyperclip.copy(original_clipboard)

        if copied_text:
            log.info(f"텍스트 복사 성공: {copied_text[:50]}...")  # 너무 긴 텍스트는 앞부분만 로그 남기기
        else:
            log.warning("복사된 텍스트가 없습니다.")

        return copied_text

    except Exception as e:
        log.error(f"텍스트 복사 실패: {e}")
        return ""
