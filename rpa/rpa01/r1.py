'''
1. 한국투자증권HTS 프로그램을 실행하고 공인인증서로 로그인 한 후에 종료
2. 팝업처리는 안함.
'''
import os
import subprocess
import sys
from typing import Optional, Tuple
import pyautogui
import time
import ctypes
import psutil
from dotenv import load_dotenv
from enum import Enum

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
    """
    지정된 영역 이름과 기준 영역에 따라 영역을 계산해 반환합니다.

    :param region_name: 계산할 영역의 이름 (RegionName 열거형)
    :param base_region: 기준 영역 (left, top, width, height). None인 경우 전체 화면을 기준으로 함.
    :return: 계산된 영역 (left, top, width, height)
    """

    # base_region이 None인 경우 전체 화면을 기준으로 설정
    if base_region is None:
        screen_width, screen_height = pyautogui.size()
        base_region = (0, 0, screen_width, screen_height)

    left, top, width, height = base_region

    # 영역 계산
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
        center_left = left + width // 3
        center_top = top + height // 3
        return (center_left, center_top, width // 3, height // 3)
    else:
        raise ValueError("잘못된 RegionName 값입니다.")

def is_admin():
    """
    현재 프로세스가 관리자 권한으로 실행 중인지 확인합니다.
    Windows에서 관리자 권한이면 True를 반환합니다.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"관리자 권한 확인 오류: {e}")
        return False
    
def run_as_admin(executable_path):
    """
    관리자 권한으로 지정한 프로그램을 실행합니다.
    """
    try:
        # "runas" 명령을 사용하면 관리자 권한으로 실행
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", executable_path, None, None, 1)
        if int(ret) <= 32:
            print("프로그램 실행에 실패하였습니다.")
        else:
            print("프로그램이 관리자 권한으로 실행되었습니다.")
    except Exception as e:
        print(f"예외 발생: {e}")

def wait_for_image(image_path, timeout=60, confidence=0.8, region=None):
    """
    주어진 이미지가 화면에 나타날 때까지 최대 timeout(초) 동안 대기합니다.
    이미지를 찾으면 해당 영역(Box 객체)를 반환하고, timeout 이내에 찾지 못하면 None을 반환합니다.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            # 이미지가 아직 화면에 없으면 예외가 발생하므로 그냥 무시하고 계속 대기합니다.
            pass
        time.sleep(1)
    return None

def find_for_image(image_path, confidence=0.8, region = None):
    """
    주어진 이미지가 화면에 존재하면 해당 영역(Box 객체)를 반환하고,
    존재하지 않으면 None을 반환합니다.
    
    :param image_path: 찾을 이미지 파일 경로 (예: 'signkorea.png')
    :param confidence: 이미지 인식 신뢰도 (0.0 ~ 1.0, OpenCV가 설치되어 있어야 합니다.)
    :return: 이미지 영역(Box 객체) 또는 None
    """
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        return location  # 이미지가 발견되면 해당 영역을 반환합니다.
    except pyautogui.ImageNotFoundException:
        # 이미지가 없으면 예외가 발생하므로, None을 반환합니다.
        return None

def is_hts_running(process_name="HTS.exe"):
    """
    주어진 프로세스 이름을 가진 HTS 프로그램이 실행 중인지 확인합니다.
    실행 중이면 True, 아니면 False를 반환합니다.
    """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False

if __name__ == "__main__":
    load_dotenv()
    KIS_CERTI_PW = os.getenv("KIS_CERTI_PW")
    
    if not is_admin():
        print("관리자 권한으로 실행 중이 아닙니다. HTS는 관리자권한이 필요합니다.")
        sys.exit(0)
    if is_hts_running(process_name="efriendplus.exe"):
        print("HTS 프로그램이 이미 실행 중입니다.")
        sys.exit(0)    
    # HTS 실행 파일의 경로를 실제 경로로 변경하세요.
    print("한국투자증권 HTS 프로그램을 실행합니다.")
    efriendplus_path = r"C:\eFriend Plus\efriendplus\efriendplus.exe"
    hts_process = subprocess.Popen(efriendplus_path)
    # run_as_admin(efriendplus_path)
    # 공동인증서로_로그인.png
    # 예시: 10초 대기 후 종료
    time.sleep(10)
    print("로그인 화면 대기 중...")
    login_button = wait_for_image('./images/login_button.png')
    if login_button is None:
        print("로그인 화면이 나타나지 않았습니다.")
        sys.exit(0)
    button_center = pyautogui.center(login_button)
    print(f"버튼 중앙 좌표: {button_center}")
        
    # 해당 좌표로 마우스 이동 후 클릭
    pyautogui.moveTo(button_center.x, button_center.y, duration=0.5)
    pyautogui.click()
    print("로그인 버튼 클릭 완료!")        

    print("공인인증서 선택 창 대기 중...")
    certificate_window = wait_for_image('./images/signkorea.png')
    if certificate_window is None:
        print("공인인증서 선택 창이 나타나지 않았습니다.")
        sys.exit(0)

    print("공인인증서 선택 창이 나타났습니다.")
    
    user = wait_for_image('./images/user.png')
    if user is None:
        print("사용자 입력창이 나타나지 않았습니다.")
        sys.exit(0)
    user_center = pyautogui.center(user)
    pyautogui.moveTo(user_center.x, user_center.y, duration=0.5)
    pyautogui.click()
    pyautogui.write(KIS_CERTI_PW)
    certify_button = find_for_image('./images/certify_click1.png')
    if certify_button is None:
        print("인증 버튼이 나타나지 않았습니다.")
        sys.exit(0)
    certify_center = pyautogui.center(certify_button)
    print(f"버튼 중앙 좌표: {certify_center}")
    pyautogui.moveTo(certify_center.x, certify_center.y, duration=0.5)
    pyautogui.click()
    print("인증 버튼 클릭 완료! 메인이 나올 때까지 대기")
    
    efriendplus = wait_for_image('./images/efriend_plus.png')
    if efriendplus is None:
        print("HTS  메인 화면이 나타나지 않았습니다.")
        sys.exit(0)
    print("HTS 메인 화면이 나타났습니다. 10초 대기")
    # 10초 대기
    time.sleep(10)
    
    setting_button = find_for_image('./images/menu_setting.png')
    if setting_button is None:
        print("설정 버튼이 나타나지 않았습니다.")
        sys.exit(0)
    setting_center = pyautogui.center(setting_button)
    pyautogui.moveTo(setting_center.x, setting_center.y, duration=0.5)
    pyautogui.click()
    print("설정 버튼 클릭 완료!")
    time.sleep(2)
    quit_button = find_for_image('./images/menu_quit.png')
    if quit_button is None:
        print("종료 버튼이 나타나지 않았습니다.")
        sys.exit(0)
    quit_center = pyautogui.center(quit_button)
    pyautogui.moveTo(quit_center.x, quit_center.y, duration=0.5)
    pyautogui.click()
    
    time.sleep(1)
    confirm_quit_button = find_for_image('./images/confirm_quit.png')
    if confirm_quit_button is None:
        print("종료 확인 버튼이 나타나지 않았습니다.")
        sys.exit(0)
    confirm_quit_center = pyautogui.center(confirm_quit_button)
    pyautogui.moveTo(confirm_quit_center.x, confirm_quit_center.y, duration=0.5)
    pyautogui.click()
    print("HTS 종료 완료!")