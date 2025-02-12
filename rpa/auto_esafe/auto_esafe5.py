import os
import subprocess
import time
import pyautogui
from logger import Logger
from config import Config
from datetime import datetime, timedelta
from path_utils import env_path, pngimg
from rpa_misc import get_text_from_input_field
from rpa_utils import *
from rpa_process import is_process_running, kill_process
from ftplib import FTP

from working_days import get_prev_working_day, get_today
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

    
def close_all_tabs_via_context_menu(tab_head_point, context_menu_image, close_all_image):
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
    time.sleep(1)  # 컨텍스트 메뉴가 뜰 시간을 줌

    # 🔹 2. 컨텍스트 메뉴 확인
    context_menu = None
    try:
        context_menu = pyautogui.locateOnScreen(context_menu_image, confidence=0.8, grayscale=True)
    except Exception as e:
        log.warning(f"🚨 탭은 Home밖에 없음: {e}")

    if context_menu is None:
        log.info("🚫 컨텍스트 메뉴가 나타나지 않았습니다. (탭이 없는 상태)")
        return  # 탭이 없으므로 종료

    log.info("✅ 컨텍스트 메뉴 감지 완료.")

    # 🔹 3. '전체 닫기' 버튼 찾기
    close_all_button = pyautogui.locateCenterOnScreen(close_all_image, confidence=0.8)
    
    if close_all_button:
        pyautogui.moveTo(close_all_button, duration=0.3)
        pyautogui.click()
        log.info("✅ '전체 닫기' 버튼 클릭 완료.")
        time.sleep(1)  # 탭이 닫힐 시간을 줌
    else:
        log.warning("❌ '전체 닫기' 버튼을 찾을 수 없습니다.")
            
            
def work_start_main():
    global hts_process  # finally에서 접근하기 위해 전역 변수 사용
    program_path = Config.PROGRAM_PATH
    hts_process = subprocess.Popen(program_path)
    time.sleep(5)

    region = get_region(RegionName.CENTER)

    # 로그인 버튼 클릭
    find_and_click(pngimg('login_button'), region=region, wait_seconds=2)
    
    # 사용자 선택
    find_and_click(pngimg('user'), region=region)

    # 비밀번호 입력
    pyautogui.write(Config.PASSWORD)

    # 인증서 선택 버튼 클릭
    find_and_click(pngimg('certi_select_button'), grayscale=True, wait_seconds=3)


    log.info("업무구분 선택")
    find_and_click(pngimg('work_type'), grayscale=True)
    find_and_click(pngimg('work_type_confirm'), grayscale=True)

    log.info("메인화면 로딩중...")
    time.sleep(5)
    # 메인 화면 체크
    region = get_region(RegionName.LEFT_TOP)
    #find_and_click(pngimg('main_logo'), region=region)
    wait_for_image(pngimg('main_logo'), region=region)
    log.info("메인화면 로딩 완료")

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
    query_finish_check = wait_for_image(pngimg('query_finish_check'), region=region)
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

    # 저장 경로 입력
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    pyautogui.press('enter')
    log.info(f"파일 저장 경로(기준가1): {saved_file_path}")
    time.sleep(5)
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region)
    return saved_file_path

def work_500068_tab2() -> list:
    filenames = []
    # move 493,89 close 기준가조회화면닫기
    mouse_move_and_click(493, 89, wait_seconds=2)
    # move 1793,53 click and enter
    mouse_move_and_click(1793, 53, wait_seconds=2)
    pyautogui.press('enter')
    # 443, 275기준가조회2 클릭
    mouse_move_and_click(443, 275, 5)
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
    query_finish_check = wait_for_image(pngimg('query_finish_check'), region=region, timeout=120)
    time.sleep(3)
    found_image = find_and_press_key(pngimg('error_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
    if found_image:
        log.error("기준가 tab2 조회 오류 발생")
        return []
    # 파일 다운로드 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    move_and_click(pngimg('download_combo'), region=region, grayscale=True)
    # 다운로드 옵션 클릭
    press_keys(['down','down','enter'], wait_seconds=2)
    found_image = find_and_press_key(pngimg('error_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
    if found_image:
        log.error("기준가 tab2 저장시 오류")
        return []    
    # 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
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
    filenames.append(saved_file_path)
    
    time.sleep(5)
    # 종료 확인 버튼 클릭
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region)
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

    # 저장 경로 입력
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    filenames.append(saved_file_path)
    time.sleep(1)
    pyautogui.press('enter')
    log.info(f"Excel 파일 저장 경로(기준가2) : {saved_file_path}")

    time.sleep(5)
        
    # 종료 확인 버튼 클릭
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region)
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
    find_and_press_key(pngimg('alert_icon'), 'space', region=region)
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
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    pyautogui.press('enter')
    log.info(f"파일 저장 경로(기준가1): {saved_file_path}")
    time.sleep(5)
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region)
    return saved_file_path

def work_800008(prev_working_day: str) -> str:
    '''800008 종목발행현황'''
    today_ymd = datetime.now().strftime("%Y%m%d")
    
    log.info("화면번호 입력 800008 입력 후 엔터")
    mouse_move_and_click(1760, 50, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("800008")
    pyautogui.press('enter')
    time.sleep(5)

    mouse_move_and_click(459, 136, wait_seconds=1)
    for _ in range(10):
        pyautogui.press('up')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    mouse_move_and_click(951, 190, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    pyautogui.write(prev_working_day)         
    mouse_move_and_click(1065, 190, wait_seconds=1)
    pyautogui.hotkey('ctrl', 'a') # 전체 선택
    pyautogui.write(today_ymd)         
    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True, wait_seconds=2)

    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    find_and_click(pngimg('query'), region=region, wait_seconds=3)    

    # 조회 완료 확인
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region)
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
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    pyautogui.press('enter')
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('warning_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
    log.info(f"파일 저장 경로(8): {saved_file_path}")
    time.sleep(5)
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, ignoreNotFound=True, timeout=10)
    return saved_file_path

def work_800100() -> str:
    '''800100 일자별 일정현황 시작'''
    log.info("화면번호 입력 800100 입력 후 엔터")
    log.info('1')
    mouse_move_and_click(1760, 50, wait_seconds=1)
    log.info('2')
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    pyautogui.write("800100")
    pyautogui.press('enter')
    time.sleep(5)    
    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    log.info('3')
    find_and_click(pngimg('query'), region=region, wait_seconds=5)
    log.info('4')
    region = get_region(RegionName.RIGHT_BOTTOM)
    log.info('5')
    wait_for_image(pngimg('query_finish_chong'), region=region)
    log.info('6')
    
# 다운로드 옵션 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    find_and_click(pngimg('download_combo'), region=region, grayscale=True)
    log.info('7')
    press_keys(['down','down','enter'], wait_seconds=2)    
    log.info('8')
    # Save As 파일명 입력
    file_name = wait_for_image(pngimg('file_name'), grayscale=True)
    log.info('9')
    if not file_name:
        raise Exception("파일 이름 입력창을 찾을 수 없습니다.")
    
    log.info('10')
    x, y = get_point_with_location(file_name, Direction.RIGHT, 100)
    log.info('11')
    mouse_move_and_click(x, y, wait_seconds=1)
    log.info('12')

    # 저장 경로 입력
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1 + "\\")
    saved_file_path = get_text_from_input_field()
    time.sleep(1)
    log.info('13')
    pyautogui.press('enter')
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('warning_icon'), 'space', region=region, ignoreNotFound=True, timeout=5)
    log.info('14')
    log.info(f"파일 저장 경로(8): {saved_file_path}")
    region = get_region(RegionName.CENTER)
    find_and_press_key(pngimg('alert_icon'), 'space', region=region, ignoreNotFound=True)
    log.info('15')
    time.sleep(3)
    return saved_file_path    
                
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
    # #-------------------------기준가2
    # log.info(">>> 500068 기준가2 작업 시작")
    # files = work_500068_tab2()
    # saved_files.extend(files)
    # log.info(">>> 500068 기준가2 작업 종료")
    
    # #-------------------------500038 분배금 내역통보
    # log.info(">>> 500038 분배금 내역통보 작업 시작")
    # log.info("탭닫기 시작")
    # close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    # log.info("탭닫기 종료")
    # prev_working_day = get_prev_working_day(*get_today())
    # log.info("이전 영업일: " + prev_working_day)
    # filename = work_500038(prev_working_day)
    # saved_files.append(filename)
    # log.info(">>> 500038 분배금 내역통보 작업 종료")
    # #-------------------------800008종목발행현황
    # log.info(">>> 800008 종목발행현황 작업 시작")
    # close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    # filename = work_800008(prev_working_day)
    # saved_files.append(filename)
    # log.info(">>> 800008 분배금 내역통보 작업 종료")
    # #-------------------------800100 일자별 일정현황
    # log.info(">>> 800100 일자별 일정현황 시작")
    # log.info("탭닫기 시작")
    # close_all_tabs_via_context_menu((460,85), pngimg('context_menu'), pngimg('all_tab_close'))
    # log.info("탭닫기 종료")
    # filename = work_800100()
    # saved_files.append(filename)
    # log.info(">>> 800100 일자별 일정현황 종료")
    
    # 프로그램 종료
    mouse_move_and_click(1901, 16, wait_seconds=1)
    time.sleep(2)
    pyautogui.press('space')
    return saved_files

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

if __name__ == "__main__":
    pre_check()
    version = Config.VERSION
    log.info("------------------------------------------------------")
    log.info(f"auto_esafe 프로그램 시작 ver : {version}, Debug Mode = {Config.DEBUG}")
    log.info("------------------------------------------------------")
    if Config.DEBUG:
        log.info(">>> 디버그 모드로 실행합니다.")
        exit(1)
    try:
        # esafe화면작업
        filenames = esafe_auto_work()
        
        # filenames의 항목중 space가 있으면 제거
        for idx, filename in enumerate(filenames, start=1):
            # 확장자가 xls인 파일을 csv로 변환
            if filename.endswith('.xls') or filename.endswith('.xlsx'):
                csv_file = filename + ".csv"
                excel_to_csv(filename, csv_file)
                filenames[idx-1] = csv_file
                log.info(f"{idx}. CSV 변환 완료: {csv_file}")
            else:
                log.info(f"{idx}. 저장된 파일 경로: {filename}")
        # FTP 업로드
        log.info(">>> FTP 업로드 시작")
        ftp_upload_files(filenames)
        log.info(">>> FTP 업로드 종료")
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
