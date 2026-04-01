import glob
import os
import subprocess
import sys
import time
import pyautogui
from logger import Logger
from config import Config
from datetime import datetime, timedelta
from path_utils import env_path, image_path, pngimg
from rpa_exceptions import CertiError, HolidayError
from rpa_misc import get_text_from_input_field
from rpa_utils import find_and_click, find_and_press_key, mouse_move_and_click, get_region, RegionName, Direction, get_point_with_location, put_keys, press_keys, move_and_click, move_and_press, wait_for_image, get_scale_factor
from rpa_process import is_process_running, kill_process, maximize_window
from ftplib import FTP
from paramiko import Transport, SFTPClient
from PIL import Image, ImageDraw, ImageFont

from working_days import get_prev_working_3day, get_prev_working_day, get_today, isHoliday,  todayYmd, get_prev_2month_day
from excel_utils import excel_to_csv

# Logger 인스턴스 생성
log = Logger()

def exception_handler(error_message):
    """ 예외 발생 시 처리: 화면 캡처 및 로그 기록 """
    log_dir = Config.LOG_DIR
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    screenshot_path = f"{log_dir}/error_{timestamp}.png"
    pyautogui.screenshot(screenshot_path)
    log.error(f"{error_message} - 스크린샷 저장: {screenshot_path}")

def ftp_upload_files(filenames):
    """여러 개의 파일을 FTP 서버에 업로드하는 함수"""
    FTP_HOST = Config.FTP_HOST
    FTP_USER = Config.FTP_USER
    FTP_PASS = Config.FTP_PASS
    FTP_REMOTE_DIR = Config.FTP_REMOTE_DIR #"/HDD1/esafe"
    try:
        with FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            ftp.cwd(FTP_REMOTE_DIR)  # 업로드할 디렉토리로 이동
            for local_file in filenames:
                remote_file = os.path.basename(local_file)  # 파일 이름만 추출
                with open(local_file, "rb") as file:
                    ftp.storbinary(f"STOR {remote_file}", file)
                log.info(f"✅ 업로드 완료: {remote_file}")
    except Exception as e:
        log.error(f"❌ 업로드 실패: {e}")

def sftp_upload_files(filenames):
    """여러 개의 파일을 SFTP 서버에 업로드하는 함수"""
    SFTP_HOST = Config.SFTP_HOST  # 기존 FTP 설정 그대로 사용
    SFTP_PORT = int(Config.SFTP_PORT)
    SFTP_USER = Config.SFTP_USER
    SFTP_PASS = Config.SFTP_PASS
    SFTP_REMOTE_DIR = Config.SFTP_REMOTE_DIR  # 예: "/HDD1/esafe"
    log.info(f"SFTP 서버 정보: {SFTP_HOST}:{SFTP_PORT}, 사용자: {SFTP_USER}, 원격 디렉토리: {SFTP_REMOTE_DIR}")
    try:
        # SFTP 연결 설정
        transport = Transport((SFTP_HOST, SFTP_PORT))  # 기본 SFTP 포트 22
        transport.connect(username=SFTP_USER, password=SFTP_PASS)

        # SFTP 클라이언트 생성
        sftp = SFTPClient.from_transport(transport)
        
        # 원격 디렉토리 이동
        sftp.chdir(SFTP_REMOTE_DIR)

        for local_file in filenames:
            remote_file = os.path.basename(local_file)  # 파일 이름만 추출
            sftp.put(local_file, f"{SFTP_REMOTE_DIR}/{remote_file}")  # 파일 업로드
            log.info(f"✅ 업로드 완료: {remote_file}")

        # 연결 종료
        sftp.close()
        transport.close()

    except Exception as e:
        log.error(f"❌ 업로드 실패: {e}")

    
def close_all_tabs_via_context_menu(tab_head_point, context_menu_image, close_all_image)->bool:
    """
    탭 헤드에서 우클릭하여 컨텍스트 메뉴가 나타나면 '전체 닫기' 버튼을 클릭하는 함수.
    
    :param tab_head_point: (x, y) 형식의 좌표 (탭 헤드에서 우클릭할 위치)
    :param context_menu_image: 컨텍스트 메뉴를 식별할 이미지 경로
    :param close_all_image: '전체 닫기' 버튼 이미지 경로
    """
    x, y = tab_head_point

    # 🔹 1. 특정 위치에서 우클릭 (탭 헤드 영역)
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.rightClick()
    log.info("✅ 탭 헤드에서 우클릭 완료.")
    time.sleep(3)  # 컨텍스트 메뉴가 뜰 시간을 줌
    

    # 🔹 2. 컨텍스트 메뉴 확인
    context_menu = None
    try:
        context_menu = pyautogui.locateOnScreen(context_menu_image, confidence=0.8, grayscale=True)
    except Exception as e:
        log.warning(f"🚨 탭은 Home밖에 없음: {e}")
        return False

    if context_menu is None:
        log.info("🚫 컨텍스트 메뉴가 나타나지 않았습니다. (탭이 없는 상태)")
        return False # 탭이 없으므로 종료

    log.info("✅ 컨텍스트 메뉴 감지 완료.")

    # 🔹 3. '전체 닫기' 버튼 찾기
    close_all_button = pyautogui.locateCenterOnScreen(close_all_image, confidence=0.8)
    
    if close_all_button:
        pyautogui.moveTo(close_all_button, duration=0.3)
        pyautogui.click()
        log.info("✅ '전체 닫기' 버튼 클릭 완료.")
        time.sleep(1)  # 탭이 닫힐 시간을 줌
        return True
    else:
        log.warning("❌ '전체 닫기' 버튼을 찾을 수 없습니다.")
        return False    
            
def work_start_main():
    global hts_process  # finally에서 접근하기 위해 전역 변수 사용
    program_path = Config.PROGRAM_PATH
    hts_process = subprocess.Popen(program_path)
    time.sleep(5)

    region = get_region(RegionName.CENTER)

    # 로그인 버튼 클릭
    find_and_click(pngimg('login_button'), grayscale=True, region=region, wait_seconds=3)

    location = Config.CERTI_LOCATION
    if location == "USB":
        mouse_move_and_click(801,444, wait_seconds=1)
    elif location == "HDD":
        mouse_move_and_click(1037, 444, wait_seconds=1)
    else:
        mouse_move_and_click(1037, 444, wait_seconds=1)
    # 사용자 선택
    find_and_click(pngimg('user'), region=region, grayscale=True, timeout=10)

    # 비밀번호 입력
    pyautogui.write(Config.PASSWORD)

    # 인증서 선택 버튼 클릭
    find_and_click(pngimg('certi_select_button'), grayscale=True, wait_seconds=3)

    error_alert = find_and_press_key(pngimg('certi_alert'), 'space', ignoreNotFound=True, grayscale=True,  timeout=5)    
    if error_alert:
        raise CertiError("인증서 사용자와 인증서 비밀번호가 일치 하지 않습니다")

    log.info("업무구분 선택")
    find_and_click(pngimg('work_type'), grayscale=True)
    find_and_click(pngimg('work_type_confirm'), grayscale=True)

    log.info("메인화면 로딩중...")
    time.sleep(5)
    # 메인 화면 체크
    region = get_region(RegionName.LEFT_TOP)
    #find_and_click(pngimg('main_logo'), region=region)
    wait_for_image(pngimg('main_logo_home'), region=(286,80,70, 25), grayscale=True, timeout=60, wait_seconds=5)
    log.info("메인화면 로딩 완료")
    # 최대화를 한다.
    log.info("화면을 최대화 시도")
    process_name = Config.PROCESS_NAME
    window_title = Config.WINDOWN_TITLE
    maximize_window(process_name, window_title)
    log.info("화면을 최대화 완료")
    
    
def work_500068_tab1():
    # 화면번호 입력
    log.info("화면번호 입력 500068 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.write("500068")
    pyautogui.press('enter')

    time.sleep(5)
    log.info("기준가1 작업시작")
    # 펀드 전체 체크박스 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('fund_all_checkbox'), region=region, grayscale=True)

    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True, wait_seconds=2)

    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=3)

    # 조회 완료 확인
    query_finish_check = wait_for_image(pngimg('query_finish_gun'), region=(1818,955,84,30), timeout=(60*10))
    time.sleep(10)

    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM) 
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','enter'], wait_seconds=2)
    
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500068_T1"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}"')
    time.sleep(1)    
    #--------------------------------
    pyautogui.press('enter')
    # time.sleep(10)
    log.info(f"파일 저장 경로(기준가1): {saved_file_path}")
    # warning과 alert체크
    find_and_press_key(pngimg('alert_icon'), 'space', grayscale=True, region=region, ignoreNotFound=True,  timeout=120)
    # warning_and_alert_check()
    time.sleep(5)
    #안전장치 alert에 대한
    log.info('안전장치 alert_icon.을 못 발견했었을 때를 위해서')
    move_and_press(800, 10, 'space', wait_seconds=1)
    
    return saved_file_path

def work_500068_tab2() -> list:
    filenames = []
    # move 493,89 close 기준가조회화면닫기
    mouse_move_and_click(493, 89, wait_seconds=2)
    # move 1793,53 click and enter
    mouse_move_and_click(1793, 53, wait_seconds=2)
    pyautogui.press('enter')
    # 443, 275기준가조회2 클릭
    mouse_move_and_click(443, 275, 0.5, wait_seconds=5)
    # 펀드전체 클릭
    region = get_region(RegionName.RIGHT_TOP)
    move_and_click(pngimg('fund_all_checkbox'), region=region, grayscale=True)
    # 파일다운로드 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click(pngimg('download_combo'),  region=region, grayscale=True)
    
    # 조회버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    move_and_click(pngimg('query'), region=region, wait_seconds=3)
    # 기준가 조회 체크까지 기다림
    # query_finish_check = wait_for_image(pngimg('query_finish_check'), region=region, timeout=120)
    query_finish_check = wait_for_image(pngimg('query_finish_gun'), region=(1818,955,84,30), timeout=(60*10))
    time.sleep(10)
    found_image = find_and_press_key(pngimg('error_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
    if found_image:
        log.error("기준가 tab2 조회 오류 발생")
        return []   

    # excel 저장
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click(pngimg('download_combo'), region=region, grayscale=True)
    # 다운로드 옵션 클릭
    press_keys(['down','down','down', 'enter'], wait_seconds=2)
    # 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500068_T2"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}"')
    time.sleep(1)
    #--------------------------------
    pyautogui.press('enter')
    filenames.append(saved_file_path)
    log.info(f"Excel 파일 저장 경로(기준가2) : {saved_file_path}")
    
    # warning과 alert체크
    warning_and_alert_check()
    time.sleep(5)
    
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True, ignoreNotFound=True, timeout=180)
    time.sleep(3)
    log.info('안전장치 alert_icon.을 못 발견했었을 때를 위해서')
    move_and_press(800, 10, 'space', wait_seconds=1)
    
    return filenames

def work_500038(prev_working_day: str) -> str:
    log.info("화면번호 입력 500038 입력 후 엔터")
    
    # prev_working_day = get_prev_working_day(*get_today())
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    log.info(f"날짜 범위 이전 영업일: {prev_working_day} ~ 어제: {yesterday}")
        
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("500038")
    pyautogui.press('enter')
    time.sleep(5)
    #날짜범위 입력
    mouse_move_and_click(1223, 135, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    pyautogui.write(prev_working_day) 
    mouse_move_and_click(1360, 135, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    pyautogui.write(yesterday) 
    
    # 펀드전체 체크
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('fund_all_checkbox'), region=region, grayscale=True)
    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True, wait_seconds=2)

    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=3)    
    
    # 조회 완료 확인
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', grayscale=True, region=region)
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','down','enter'], wait_seconds=2)
    
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500038"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}"')
    time.sleep(1)
    #--------------------------------    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)
    log.info(f"파일 저장 경로 : {saved_file_path}")
    warning_and_alert_check()

    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True, ignoreNotFound=True, timeout=120)
    time.sleep(3)
    log.info('안전장치 alert_icon.을 못 발견했었을 때를 위해서')
    move_and_press(800, 10, 'space', wait_seconds=1)
    
    return saved_file_path

def work_800008(prev_working_day: str, prev_2month_day: str) -> str:
    '''800008 종목발행현황'''
    today_ymd = datetime.now().strftime("%Y%m%d")
    # one_week_age = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    log.info(f"오늘 날짜: {today_ymd}, -3 영업일  날짜: {prev_working_day}")
    
    log.info("화면번호 입력 800008 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("800008")
    pyautogui.press('enter')
    time.sleep(5)

    # mouse_move_and_click(459, 136, wait_seconds=1)
    mouse_move_and_click(464, 136, wait_seconds=1)
    for _ in range(10):
        pyautogui.press('up')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    #--------------------설립일/발행일-----
    # mouse_move_and_click(951, 190, wait_seconds=1)
    mouse_move_and_click(980, 190, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    # pyautogui.write(prev_working_day)         
    pyautogui.write(prev_working_day)
    time.sleep(1)
    # mouse_move_and_click(1065, 190, wait_seconds=1)
    mouse_move_and_click(1108, 190, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    pyautogui.write(today_ymd)         
    time.sleep(1)
    #--------------------종목등록일-----
    mouse_move_and_click(980, 211, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    log.info(f"오늘 날짜: {today_ymd},  -2개월 전 날짜: {prev_2month_day}")
    pyautogui.write(prev_2month_day)
    time.sleep(1)
    # mouse_move_and_click(1065, 190, wait_seconds=1)
    mouse_move_and_click(1108, 211, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    pyautogui.write(today_ymd)         
    time.sleep(1)


    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True, wait_seconds=2)

    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=3)    

    # 조회 완료 확인
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True)
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','enter'], wait_seconds=2)    
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "800008"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}"')
    time.sleep(1)
    #--------------------------------
    pyautogui.press('enter')
    time.sleep(5)
    log.info(f"파일 저장 경로(8): {saved_file_path}")
    warning_and_alert_check()
    time.sleep(3)

    return saved_file_path

def work_800100() -> str:
    '''800100 일자별 일정현황 시작'''
    log.info("화면번호 입력 800100 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("800100")
    pyautogui.press('enter')
    time.sleep(5)
    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=5)
    region = get_region(RegionName.RIGHT_BOTTOM)
    # wait_for_image(pngimg('query_finish_chong'), region=region)
    wait_for_image(pngimg('query_finish_gun'), region=(1818,955,100,30))
    time.sleep(3)
    
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','enter'], wait_seconds=2)    
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "800100"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}"')
    time.sleep(1)
    #--------------------------------
    pyautogui.press('enter')
    
    log.info(f"파일 저장 경로(8): {saved_file_path}")    
    warning_and_alert_check()
    time.sleep(1)
    return saved_file_path    

def work_500086(is_pm:bool=False) -> str:
    ''' 500086 등록잔량서비스'''
    log.info("화면번호 입력 500086 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("500086")
    pyautogui.press('enter')
    time.sleep(5)
    
    # 먼저 download_combo 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click(pngimg('download_combo'),  region=region, grayscale=True)
        
    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=5)
    # wait_for_image(pngimg('query_finish_chong'), region=region)
    region = get_region(RegionName.RIGHT_BOTTOM)
    wait_for_image(pngimg('query_finish_gun'), region=(1818,955,100,30))
    time.sleep(3)
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True, ignoreNotFound=True, timeout=60)    
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','down', 'enter'], wait_seconds=5)    
    
    # Save As 파일명 입력
    region = get_region(RegionName.LEFT)
    file_name = wait_for_image(pngimg('file_name'), grayscale=True, region=region)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500086"
    if is_pm:
        screen_no = "500086N"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}" | P:enter')
    time.sleep(1)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True, ignoreNotFound=True, timeout=60)        
    
    log.info(f"파일 저장 경로(8): {saved_file_path}")    
    warning_and_alert_check()
    time.sleep(1)
    return saved_file_path


def work_500874(is_pm:bool=False) -> str:
    ''' 500874 외국 납수세액조회'''
    log.info("화면번호 입력 500874 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("500874")
    pyautogui.press('enter')
    time.sleep(5)
    
    # 먼저 download_combo 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click(pngimg('download_combo'),  region=region, grayscale=True)
    time.sleep(3)
    # 펀드전체 체크
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('fund_all_checkbox'), region=region, grayscale=True)
    i = 0
    while True:
        r = wait_for_image(pngimg('checked_box'), region=region, timeout=3, confidence=0.9)
        if r is not None:
            log.info("외국 납수세액조회: 펀드전체 체크 완료")
            break
        log.info("펀드전체 체크 재시도")
        pyautogui.click()
        # find_and_click(pngimg('fund_all_checkbox'), region=region, grayscale=True)
        i += 1
        if i > 5:
            log.error("외국 납수세액조회: 펀드전체 체크 실패")
            break

    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=5)
    # wait_for_image(pngimg('query_finish_chong'), region=region)
    region = get_region(RegionName.RIGHT_BOTTOM)
    wait_for_image(pngimg('query_finish_gun'), region=(1818,955,100,30))
    time.sleep(3)
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True, ignoreNotFound=True, timeout=60)    
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','down', 'enter'], wait_seconds=5)    
    
    # Save As 파일명 입력
    region = get_region(RegionName.LEFT)
    file_name = wait_for_image(pngimg('file_name'), grayscale=True, region=region)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500874"
    if is_pm:
        screen_no = "500874N"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}" | P:enter')
    time.sleep(1)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, grayscale=True, ignoreNotFound=True, timeout=60)        
    
    log.info(f"파일 저장 경로(8): {saved_file_path}")    
    warning_and_alert_check()
    time.sleep(1)
    return saved_file_path 


def warning_and_alert_check():
    '''저장enter이후 경고창 또는 alert가 나오면 이를 제거한다'''
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('warning_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
    
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('error_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
                    
   
def deleteTodayFiles(ymd, mode:str = "am"):
    """폴더 안에서 특정 날짜 패턴(YYYYMMDD_*)에 맞는 파일 삭제"""
    pattern = os.path.join(Config.SAVE_AS_PATH1, f"{ymd}_*.*")
    files = glob.glob(pattern)  # 패턴에 맞는 파일 찾기

    for file in files:
        try:
            # 오전 모드이고 파일명에 T1N이나 T2N이 포함되어 삭제하지 않는다.
            if mode == "am" and ("T1N" in file or "T2N" in file):
                continue
            if mode == "pm" and ("T1N" not in file and "T2N" not in file):
                continue
            os.remove(file)
            log.info(f" 기존 파일 삭제 완료: {file}")
        except Exception as e:
            log.error(f"기존 파일 삭제 실패: {file} -> {e}")
    
    
def pre_check():
    # auto_esafe를 실행할 수 있는 상태인지 체크, 할 수 없는 상태라면 메세지와 함께 exit
    env_file = env_path()
    if not os.path.exists(env_file):
        print("❌ .env 파일이 존재하지 않습니다.")
        exit(1)
    esafe_exe = Config.PROGRAM_PATH
    if not os.path.exists(esafe_exe):
        print("❌ eSafe 프로그램이  경로에 존재하지 않습니다. (.env 체크요망)")
        exit(1)    
    try:    
        # Config.LOG_DIR 가 존재하는지 체크
        if not os.path.exists(Config.LOG_DIR):
            os.makedirs(Config.LOG_DIR, exist_ok=True)
        # Config.SAVE_AS_PATH1 가 존재하는지 체크
        if not os.path.exists(Config.SAVE_AS_PATH1):
            os.makedirs(Config.SAVE_AS_PATH1, exist_ok=True)
    except Exception as e:
        print(f"❌ 경로 생성 실패: {e}")
        exit(1)
    # 모니터 해상도가 FHD(1920x1080)인지 확인
    if pyautogui.size() != (1920, 1080):
        print("❌ 모니터 해상도가 1920x1080이 아닙니다.")
        exit(1)
    # DPI 100%가 아니면
    if (get_scale_factor() != 1.0):
        print("❌ 화면 배율이 100%가 아닙니다.")
        exit(1)
        

def create_user_name_imge():
    # 사용자 이름을 이미지로 저장
    user_name = Config.USERNAME
    user_name_img = os.path.join(image_path(), "user.png")

    # 이미지 크기 및 배경 설정
    width, height = 34, 13
    img = Image.new("L", (width, height), color=255)  # "L" 모드는 그레이스케일

    # 텍스트 추가
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype("malgun.ttf", 10)  # 'malgun.ttf'는 Windows 기본 한글 폰트
    font = ImageFont.truetype("gulim.ttc", 12)  # 'malgun.ttf'는 Windows 기본 한글 폰트

    # 텍스트 크기 계산 (textbbox 사용)
    bbox = draw.textbbox((0, 0), user_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # 중앙 정렬
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), user_name, fill=0, font=font)  # 검은색 글자 (0)

    # 이미지 저장
    img.save(user_name_img)
    log.info(f"사용자 이름 이미지 저장: {user_name_img}")    

def esafe_auto_work():
    global hts_process  # finally에서 접근하기 위해 전역 변수 사용
    hts_process = None  # 실행한 프로세스 핸들러
    saved_files = []  # 저장된 파일 경로 리스트
    
    process_name = Config.PROCESS_NAME
    if is_process_running(process_name):
        kill_process(process_name)
        log.info(f"{process_name} 가 이미 실행중이라서 프로세스 종료시킴")

    log.info(">>> 프로그램 실행 및 인증서 선택 및 메인으로 진입 시작")
    work_start_main()
    log.info(">>> 프로그램 실행 및 인증서 선택 및 메인으로 진입 완료")
    
    #-------------------------기준가
    log.info(">>> 500068 기준가1 시작")
    filename = work_500068_tab1()
    saved_files.append(filename)
    log.info(">>> 500068 기준가1 종료")
    #-------------------------기준가2
    log.info(">>> 500068 기준가2 작업 시작")
    files = work_500068_tab2()
    saved_files.extend(files)
    log.info(">>> 500068 기준가2 작업 종료")
    # -------------------------500038 분배금 내역통보
    log.info(">>> 500038 분배금 내역통보 작업 시작")
    tabClose = close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    if not tabClose:
        mouse_move_and_click(493, 89, wait_seconds=2)
    #-1전영업일            
    prev_working_day = get_prev_working_day(*get_today())
    #-3전영업일
    
    log.info("-1 영업일전: " + prev_working_day)
    filename = work_500038(prev_working_day)
    saved_files.append(filename)
    log.info(">>> 500038 분배금 내역통보 작업 종료")
    #-------------------------800008종목발행현황
    log.info(">>> 800008 종목발행현황 작업 시작")
    prev_working_3day = get_prev_working_3day(*get_today())
    prev_2month_day =  get_prev_2month_day(*get_today())
    close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    filename = work_800008(prev_working_3day, prev_2month_day)
    saved_files.append(filename)
    log.info(">>> 800008 분배금 내역통보 작업 종료")
    #-------------------------800100 일자별 일정현황
    log.info(">>> 800100 일자별 일정현황 시작")
    close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    filename = work_800100()
    saved_files.append(filename)
    log.info(">>> 800100 일자별 일정현황 종료")
    #-------------------------500086 등록잔량서비스
    log.info(">>> 500086 등록잔량서비스 시작")
    close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    filename = work_500086()
    saved_files.append(filename)
    log.info(">>> 500086 등록잔량서비스 종료")
    #-------------------------500087(외국 납수세액조회) 2025.11.13 추가
    log.info(">>> 500874 외국 납수세액조회 시작")
    close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    filename = work_500874()
    saved_files.append(filename)
    log.info(">>> 500874 외국 납수세액조회 종료")

    # 프로그램 종료
    mouse_move_and_click(1901, 16, wait_seconds=1)
    time.sleep(2)
    pyautogui.press('space')
    return saved_files

def work_500068_tab1_pm():
    # 화면번호 입력
    log.info("화면번호 입력 500068 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.write("500068")
    pyautogui.press('enter')

    time.sleep(5)
    log.info("기준가1 작업시작")
    # 펀드 전체 체크박스 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('fund_all_checkbox'), region=region, grayscale=True)

    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True, wait_seconds=2)

    # 신규등록
    mouse_move_and_click(1045,236, wait_seconds=1)
    mouse_move_and_click(1045,236, wait_seconds=1)
    mouse_move_and_click(1045,236, wait_seconds=1)


    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=3)

    # 조회 완료 확인
    query_finish_check = wait_for_image(pngimg('query_finish_gun'), region=(1818,955,84,30), timeout=(60*10))
    time.sleep(10)
    move_and_press(800, 10, 'space', wait_seconds=1)
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM) 
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','enter'], wait_seconds=2)
    
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500068_T1N"
    saved_file_path = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path}"')
    time.sleep(1)    
    #--------------------------------
    pyautogui.press('enter')
    # time.sleep(10)
    log.info(f"파일 저장 경로(신규등록): {saved_file_path}")
    # warning과 alert체크
    #find_and_press_key(pngimg('alert_icon'), 'space', grayscale=True, region=region, ignoreNotFound=True,  timeout=120)
    # warning_and_alert_check()
    time.sleep(5)

    #안전장치 alert에 대한
    log.info('안전장치 alert_icon.을 못 발견했었을 때를 위해서')
    move_and_press(800, 10, 'space', wait_seconds=1)
    #-------------------------------------------------------
    #------------- 기준가2
    #-------------------------------------------------------
    mouse_move_and_click(440, 276, wait_seconds=3)
    # 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM) 
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    press_keys(['down','down','down', 'enter'], wait_seconds=2)
    
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    mouse_move_and_click(x, y, wait_seconds=1)

    # 저장 경로 입력
    #-------- Rename file------------
    default_filename = get_text_from_input_field()
    screen_no = "500068_T2N"
    saved_file_path1 = os.path.join(Config.SAVE_AS_PATH1, f"{todayYmd()}_{screen_no}.{default_filename.rsplit('.', 1)[-1]}")
    put_keys(f'H:ctrl+a | P:delete | W:"{saved_file_path1}"')
    time.sleep(1)    
    #--------------------------------
    pyautogui.press('enter')
    # time.sleep(10)
    log.info(f"파일 저장 경로(기준가1): {saved_file_path1}")
    # warning과 alert체크
    find_and_press_key(pngimg('alert_icon'), 'space', grayscale=True, region=region, ignoreNotFound=True,  timeout=120)
    # warning_and_alert_check()
    time.sleep(5)
    #안전장치 alert에 대한
    log.info('안전장치 alert_icon.을 못 발견했었을 때를 위해서')
    move_and_press(800, 10, 'space', wait_seconds=1)
    
    return [saved_file_path, saved_file_path1]

def esafe_auto_work_pm():
    ''' 오후작업 '''
    global hts_process  # finally에서 접근하기 위해 전역 변수 사용
    hts_process = None  # 실행한 프로세스 핸들러
    saved_files = []  # 저장된 파일 경로 리스트
    
    process_name = Config.PROCESS_NAME
    if is_process_running(process_name):
        kill_process(process_name)
        log.info(f"{process_name} 가 이미 실행중이라서 프로세스 종료시킴")

    log.info(">>> 프로그램 실행 및 인증서 선택 및 메인으로 진입 시작")
    work_start_main()
    log.info(">>> 프로그램 실행 및 인증서 선택 및 메인으로 진입 완료")
    
    #-------------------------기준가
    log.info(">>> 500068 기준가 신규등록 시작")
    filenames = work_500068_tab1_pm()
    saved_files.extend(filenames)
    log.info(">>> 500068 기준가 신규등록 종료")
    #-------------------------500086 등록잔량서비스
    log.info(">>> 500086 오후작업 등록잔량서비스 시작")
    close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    filename = work_500086(is_pm=True)
    saved_files.append(filename)
    log.info(">>> 500086 오후작업 등록잔량서비스 종료")


    # 프로그램 종료
    mouse_move_and_click(1901, 16, wait_seconds=1)
    time.sleep(2)
    pyautogui.press('space')
    return saved_files


if __name__ == "__main__":
    mode = "am"
    if "pm" in sys.argv:
        mode = "pm"

    version = Config.VERSION
    log.info("------------------------------------------------------")
    log.info(f"auto_esafe 프로그램 시작 ver : {version} mode: {mode}")
    log.info("------------------------------------------------------")

    # exit(1)
    pre_check()
    # 이름문자를 이미지로 만들어서 저장한다.
    create_user_name_imge()
    time.sleep(3)
    
    try:
        # 오늘이 휴일이면 그냥 종료한다.
        today_ymd = datetime.now().strftime("%Y%m%d")
        if isHoliday(today_ymd):
            raise HolidayError(f"오늘({today_ymd})은 공휴일입니다.")
        
        # 이미 오늘의 파일이 존재하면 삭제한다
        deleteTodayFiles(today_ymd, mode)

        # esafe화면작업
        if mode == "am":
            filenames = esafe_auto_work()
        else:
            filenames = esafe_auto_work_pm()
    
        log.info(">>> CSV 변환 시작")
        for idx, filename in enumerate(filenames, start=1):
            # 확장자가 xls인 파일을 csv로 변환
            if filename.endswith('.xls') or filename.endswith('.xlsx'):
                csv_file = filename + ".csv"
                excel_to_csv(filename, csv_file)
                filenames[idx-1] = csv_file
                log.info(f"{idx}. CSV 변환 완료: {csv_file}")
            else:
                log.info(f"{idx}. 저장된 파일 경로: {filename}")
        log.info(">>> CSV 변환 시작") 
        # FTP 업로드
        log.info(">>> SFTP 업로드 시작")
        sftp_upload_files(filenames)
        log.info(">>> SFTP 업로드 종료")
    except HolidayError as e:
        log.info(f"에러메세지: {e}")    
    except Exception as e:
        exception_handler(str(e))
        process_name = Config.PROCESS_NAME
        if is_process_running(process_name):
            kill_process(process_name)
            log.info(f"{process_name} 프로세스 강제 종료시킴")        
    finally:
        # 프로그램이 실행 중이라면 종료
        if 'hts_process' in globals() and hts_process:
            log.info("프로그램 종료 중...")
            hts_process.terminate()
    
    log.info("------------------------------------------------------")
    log.info("auto_esafe  프로그램 종료")
    log.info("------------------------------------------------------")
