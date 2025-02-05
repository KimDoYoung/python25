'''
1. UHD 3840x2160 화면에서 캡쳐한 이미지를 사용함
2. HTS 프로그램 실행 전 관리자 권한으로 실행해야 함. 
3. HTS 프로그램 실행 여부 확인을 자동화함.
4. HTS 프로그램 실행 후 로그인, 공인인증서 선택, 비밀번호 입력, 인증 버튼 클릭, HTS 메인 화면 대기, 종료 버튼 클릭, 종료 확인 버튼 클릭을 자동화함.
'''
import os
import time
import subprocess
import sys
import pyautogui
from rpa_utils import *

def main():
    if not is_admin():
        print("관리자 권한으로 실행 중이 아닙니다. HTS 실행을 위해 관리자 권한이 필요합니다.")
        sys.exit(0)

    if is_hts_running():
        print("HTS 프로그램이 이미 실행 중입니다.")
        sys.exit(0)

    print("HTS 프로그램 실행 중...")
    efriendplus_path = r"C:\eFriend Plus\efriendplus\efriendplus.exe"
    hts_process = subprocess.Popen(efriendplus_path)
    
    time.sleep(10)
    print("로그인 화면 대기 중...")
    
    # 로그인 버튼 클릭
    login_button = wait_for_image('./images/login_button.png')
    if not login_button:
        print("로그인 화면이 나타나지 않았습니다.")
        sys.exit(0)
    pyautogui.click(pyautogui.center(login_button))
    print("로그인 버튼 클릭 완료!")

    # 공인인증서 선택
    print("공인인증서 선택 창 대기 중...")
    certificate_window = wait_for_image('./images/signkorea.png')
    if not certificate_window:
        print("공인인증서 선택 창이 나타나지 않았습니다.")
        sys.exit(0)

    # 비밀번호 입력
    user = wait_for_image('./images/user.png')
    if user:
        pyautogui.click(pyautogui.center(user))
        pyautogui.write(KIS_CERTI_PW)

    # 인증 버튼 클릭
    certify_button = find_for_image('./images/certify_click1.png')
    if certify_button:
        pyautogui.click(pyautogui.center(certify_button))
        print("인증 버튼 클릭 완료!")

    # HTS 메인 화면 대기
    efriendplus = wait_for_image('./images/efriend_plus.png')
    if not efriendplus:
        print("HTS 메인 화면이 나타나지 않았습니다.")
        sys.exit(0)
    
    print("HTS 실행 완료! 10초 대기 후 종료")
    time.sleep(10)

    # 종료 버튼 클릭
    setting_button = find_for_image('./images/menu_setting.png')
    if setting_button:
        pyautogui.click(pyautogui.center(setting_button))

    quit_button = find_for_image('./images/menu_quit.png')
    if quit_button:
        pyautogui.click(pyautogui.center(quit_button))

    confirm_quit_button = find_for_image('./images/confirm_quit.png')
    if confirm_quit_button:
        pyautogui.click(pyautogui.center(confirm_quit_button))

    print("HTS 종료 완료!")

if __name__ == "__main__":
    main()
