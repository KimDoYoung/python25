import subprocess
import time
import pyautogui
from logger import Logger
from config import Config
from datetime import datetime
from rpa_misc import get_text_from_input_field
from rpa_utils import *

# Logger 인스턴스 생성
log = Logger()

def exception_handler(error_message):
    """ 예외 발생 시 처리: 화면 캡처 및 로그 기록 """
    log_dir = Config.LOG_DIR
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    screenshot_path = f"{log_dir}/error_{timestamp}.png"
    pyautogui.screenshot(screenshot_path)
    log.error(f"{error_message} - 스크린샷 저장: {screenshot_path}")



def main():
    global hts_process  # finally에서 접근하기 위해 전역 변수 사용
    hts_process = None  # 실행한 프로세스 핸들러

    log.info("프로그램 실행 및 인증서 선택")
    program_path = Config.PROGRAM_PATH
    hts_process = subprocess.Popen(program_path)
    time.sleep(5)

    region = get_region(RegionName.CENTER)

    # 로그인 버튼 클릭
    find_and_click('./images/login_button.png', region=region, wait_seconds=2)
    
    # 사용자 선택
    find_and_click('./images/user.png', region=region)

    # 비밀번호 입력
    pyautogui.write(Config.PASSWORD)

    # 인증서 선택 버튼 클릭
    find_and_click('./images/certi_select_button.png', grayscale=True, wait_seconds=3)


    log.info("업무구분 선택")
    find_and_click('./images/work_type.png', grayscale=True)
    find_and_click('./images/work_type_confirm.png', grayscale=True)

    log.info("메인화면 로딩중...")
    time.sleep(5)

    # 메인 화면 체크
    region = get_region(RegionName.LEFT_TOP)
    #find_and_click('./images/main_logo.png', region=region)
    wait_for_image('./images/main_logo.png', region=region)

    log.info("메인화면 로딩 완료")
    log.info("화면번호 입력 500068 입력 후 엔터")
    # 화면번호 입력
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.write("500068")
    pyautogui.press('enter')

    time.sleep(5)
    log.info("기준가1 작업시작")
    # 펀드 전체 체크박스 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click('./images/fund_all_checkbox.png', region=region, grayscale=True)

    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click('./images/download_combo.png', region=region, grayscale=True, wait_seconds=2)

    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click('./images/query.png', region=region, wait_seconds=3)

    # 조회 완료 확인
    query_finish_check = wait_for_image('./images/query_finish_check.png', region=region)
    time.sleep(3)

    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click('./images/download_combo.png', region=region, grayscale=True)
    press_keys(['down','down','enter'], wait_seconds=2)
    
    # Save As 파일명 입력
    file_name = wait_for_image('./images/file_name.png', grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    pyautogui.press('enter')
    log.info(f"파일 저장 경로(기준가1): {saved_file_path}")
    time.sleep(5)
    # 저장완료 Alert 확인
    region = get_region(RegionName.CENTER)
    find_and_press_key('./images/alert_icon.png', 'space', region=region)
    log.info("기준가1 작업종료")
    #-------------------------기준가2
    log.info("기준가2 작업시작")
    # move 493,89 close 기준가조회화면닫기
    mouse_move_and_click(493, 89, wait_seconds=2)
    # move 1793,53 click and enter
    mouse_move_and_click(1793, 53, wait_seconds=2)
    pyautogui.press('enter')
    # 443, 275기준가조회2 클릭
    mouse_move_and_click(443, 275, 5)
    # 펀드전체 클릭
    region = get_region(RegionName.RIGHT_TOP)
    move_and_click('./images/fund_all_checkbox.png', region=region, grayscale=True)
    # 파일다운로드 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click('./images/download_combo.png',  region=region, grayscale=True)
    
    # 조회버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    move_and_click('./images/query.png', region=region, wait_seconds=3)
    # 기준가 조회 체크까지 기다림
    query_finish_check = wait_for_image('./images/query_finish_check.png', region=region)
    time.sleep(3)
    # 파일 다운로드 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click('./images/download_combo.png', region=region, grayscale=True)
    # 다운로드 옵션 클릭
    press_keys(['down','down','enter'], wait_seconds=2)
    # 파일명 입력
    file_name = wait_for_image('./images/file_name.png', grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    pyautogui.press('enter')
    log.info(f"CSV 파일 저장 경로(기준가2) : {saved_file_path}")

    time.sleep(5)
    # 종료 확인 버튼 클릭
    region = get_region(RegionName.CENTER)
    find_and_press_key('./images/alert_icon.png', 'space', region=region)
    # excel 저장
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click('./images/download_combo.png', region=region, grayscale=True)
    # 다운로드 옵션 클릭
    press_keys(['down','down','down', 'enter'], wait_seconds=2)
    # 파일명 입력
    file_name = wait_for_image('./images/file_name.png', grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    pyautogui.press('enter')
    log.info(f"Excel 파일 저장 경로(기준가2) : {saved_file_path}")

    time.sleep(5)
        
    # 종료 확인 버튼 클릭
    region = get_region(RegionName.CENTER)
    find_and_press_key('./images/alert_icon.png', 'space', region=region)
    log.info("기준가2 작업 종료")
    # 프로그램 종료
    mouse_move_and_click(1901, 16, wait_seconds=1)
    pyautogui.press('space')

if __name__ == "__main__":
    log.info("------------------------------------------------------")
    log.info("프로그램 시작")
    log.info("------------------------------------------------------")
    
    try:
        main()
    except Exception as e:
        exception_handler(str(e))
    finally:
        # 프로그램이 실행 중이라면 종료
        if 'hts_process' in globals() and hts_process:
            log.info("프로그램 종료 중...")
            hts_process.terminate()
    
    log.info("------------------------------------------------------")
    log.info("프로그램 종료")
    log.info("------------------------------------------------------")
