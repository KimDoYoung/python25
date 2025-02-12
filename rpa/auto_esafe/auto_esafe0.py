import subprocess
import sys
from logger import Logger
from config import Config
from rpa_utils import *
# Logger 인스턴스 생성
log = Logger()

def main():
    # 실행
    program_path = Config.PROGRAM_PATH
    hts_process = subprocess.Popen(program_path)
    time.sleep(5)
    
    region = get_region(RegionName.CENTER)
    # 로그인 버튼 클릭
    login_button = wait_for_image('./images/login_button.png', region=region)
    if not login_button:
        log.error("로그인 화면이 나타나지 않았습니다.")
        sys.exit(0)
    pyautogui.click(pyautogui.center(login_button))
    # 인증서에서 사용자를 찾아서 클릭
    time.sleep(2)
    user_option = wait_for_image('./images/user.png', region=region, grayscale=True)
    if not user_option:
        log.error("사용자를 찾을 수 없습니다.")
        sys.exit(0)
    user_center = pyautogui.center(user_option)
    pyautogui.moveTo(user_center.x, user_center.y, duration=0.5)
    # pyautogui.click()
    #pyautogui.click(pyautogui.center(user_option))
    # 인증서 비밀번호 입력
    pyautogui.write(Config.PASSWORD)
    certi_select_button = wait_for_image('./images/certi_select_button.png', grayscale=True)
    if not certi_select_button:
        log.error("인증서 선택 버튼을 찾을 수 없습니다.")
        sys.exit(0)
    certify_center = pyautogui.center(certi_select_button)
    pyautogui.moveTo(certify_center.x, certify_center.y, duration=0.5)
    pyautogui.click()
    time.sleep(3)
    # work type 선택
    work_type = wait_for_image('./images/work_type.png', grayscale=True)
    if not work_type:
        log.error("업무구분을 찾을 수 없습니다.")
        sys.exit(0)
    work_type_center = pyautogui.center(work_type)
    pyautogui.moveTo(work_type_center.x, work_type_center.y, duration=0.5)
    pyautogui.click()
    work_type_confirm = wait_for_image('./images/work_type_confirm.png', grayscale=True)
    if not work_type_confirm:
        log.error("업무구분 확인 버튼을 찾을 수 없습니다.")
        sys.exit(0)
    work_type_confirm_center = pyautogui.center(work_type_confirm)
    pyautogui.moveTo(work_type_confirm_center.x, work_type_confirm_center.y, duration=0.5)
    pyautogui.click()
    log.info("메인화면 로딩중...")
    time.sleep(5)
    region = get_region(RegionName.LEFT_TOP)
    main_logo = wait_for_image('./images/main_logo.png', region=region)
    if not main_logo:
        log.error("메인화면 로딩 실패")
        sys.exit(0)
    log.info("메인화면 로딩 완료")
    # 화면번호입력란으로 이동 및 클릭  1760, 50 으로 마우스 이동 후 클릭
    pyautogui.moveTo(1760, 50, duration=0.5)
    pyautogui.click()
    # 화면번호 입력 
    pyautogui.write("500068")
    pyautogui.press('enter')
    time.sleep(5) 
    # 펀드전체 체크 박스 클릭
    region = get_region(RegionName.RIGHT_TOP)
    fund_all_checkbox = wait_for_image('./images/fund_all_checkbox.png', region=region, grayscale=True)
    if not fund_all_checkbox:
        log.error("전체선택 체크박스를 찾을 수 없습니다.")
        sys.exit(0)
    fund_all_checkbox_center = pyautogui.center(fund_all_checkbox)
    pyautogui.moveTo(fund_all_checkbox_center.x, fund_all_checkbox_center.y, duration=0.5)
    pyautogui.click()

    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    download_combo = wait_for_image('./images/download_combo.png', region=region, grayscale=True)
    if not download_combo:
        log.error("파일 다운로드 콤보을 찾을 수 없습니다.")
        sys.exit(0)
    time.sleep(2)
    download_combo_center = pyautogui.center(download_combo)
    pyautogui.moveTo(download_combo_center.x, download_combo_center.y, duration=0.5)
    pyautogui.click()
    
    # 조회 버튼 클릭
    region = get_region(RegionName.RIGHT_TOP)
    search_button = wait_for_image('./images/query.png', region=region)
    if not search_button:
        log.error("조회 버튼을 찾을 수 없습니다.")
        sys.exit(0)
    search_button_center = pyautogui.center(search_button)
    pyautogui.moveTo(search_button_center.x, search_button_center.y, duration=0.5)
    pyautogui.click()
    time.sleep(3)
    # 조회된 데이터가 있는지 확인
    query_finish_check = wait_for_image('./images/query_finish_check.png', region=region)
    time.sleep(3)
    
    # 파일 다운로드 버튼 클릭
    region = get_region(RegionName.LEFT_BOTTOM)
    download_combo = wait_for_image('./images/download_combo.png', region=region, grayscale=True)
    if not download_combo:
        log.error("파일 다운로드 콤보을 찾을 수 없습니다.")
        sys.exit(0)
    time.sleep(2)
    download_combo_center = pyautogui.center(download_combo)
    pyautogui.moveTo(download_combo_center.x, download_combo_center.y, duration=0.5)
    pyautogui.click()
    download_options = wait_for_image('./images/download_options.png', region=region, grayscale=True)
    if not download_options:
        log.error("파일 다운로드 옵션을 찾을 수 없습니다.")
        sys.exit(0)
    # csv 파일 선택
    download_options_center = pyautogui.center(download_options)
    pyautogui.moveTo(download_options_center.x, download_options_center.y, duration=0.5)    
    pyautogui.click()
    time.sleep(2)
    
    # SaveAs에서
    file_name = wait_for_image('./images/file_name.png',  grayscale=True)
    if not file_name:
        log.error("파일 이름 입력창을 찾을 수 없습니다.")
        sys.exit(0)
    p = get_point_with_location(file_name, Direction.RIGHT, 100)
    pyautogui.moveTo(p[0], p[1], duration=0.5)
    pyautogui.click()
    # home key 입력 후 c:\tmp    
    pyautogui.press('home')
    pyautogui.write(Config.SAVE_AS_PATH1+"\\")
    pyautogui.press('enter')
    # 확인 alert 기다림
    time.sleep(5)
    # 확인 버튼 클릭
    region = get_region(RegionName.CENTER)
    # alert_confirm = wait_for_image('./images/alert_icon.png', region=region, grayscale=True)
    alert_confirm = wait_for_image('./images/alert_icon.png')
    if not alert_confirm:
        log.error("alert_icon 이미지을 찾을 수 없습니다.")
        sys.exit(0)
    pyautogui.press('space')
    
    # 1901,16으로 이동 클릭 종료 버튼을 클릭한다.
    pyautogui.moveTo(1901, 16, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    # 확인 버튼 클릭 프로그램 종료
    region = get_region(RegionName.CENTER)
    alert_confirm = wait_for_image('./images/alert_icon.png')
    if not alert_confirm:
        log.error("alert_icon 이미지을 찾을 수 없습니다.")
        sys.exit(0)
    pyautogui.press('space')    
        
    
if __name__ == "__main__":
    log.info("------------------------------------------------------")
    log.info("프로그램 시작")
    log.info("------------------------------------------------------")
    main()
    log.info("------------------------------------------------------")
    log.info("프로그램 종료")
    log.info("------------------------------------------------------")
