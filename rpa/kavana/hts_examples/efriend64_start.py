from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
include "hts_examples/efriend64_data.kvs"
include "hts_examples/common_functions.kvs"

function virtual_screen_close2()
    CONST 가상화면호출버튼_위치= Point(3522, 1956)
    CONST 가상화면닫기팝업이미지=f"{IMAGE_PATH}\\가상화면닫기확인.png"
    CONST 가상화면_닫기_버튼_위치=Point(1860, 1085)
    LOG_INFO "====> 가상화면 닫기 버튼 클릭"
    RPA click_point location=가상화면호출버튼_위치, after="wait:2s"
    RPA find_image aeea=팝업영역, from_file=가상화면닫기팝업이미지 to_var="found" 
    if found != None
        LOG_INFO "가상화면 닫기 팝업을 찾았습니다."
        RPA click_point location=가상화면_닫기_버튼_위치
    end_if
end_function

//타이틀의 팝업이 있으면 닫기
function close_popup_window()
    LOG_INFO "=====================[ Close Popup Window]===================================="
    SET window_list = WINDOW_LIST(process_name=PROCESS_NAME)
    LOG_INFO "현재 위도우들----->"
    for win in window_list
        SET win_info = DUMP_ATTRS(win)
        SET title1 = win_info["title"]
        LOG_INFO f"윈도우: [{title1}]"
    end_for
    LOG_INFO "<-----"    
    SET 닫기버튼=f"{IMAGE_PATH}\\닫기버튼.png"
    SET 확인버튼=f"{IMAGE_PATH}\\확인버튼.png"
    SET top_window = WINDOW_TOP(process_name=PROCESS_NAME)
    SET info = DUMP_ATTRS(top_window)
    SET 팝업윈도우영역 = WINDOW_REGION(info["hwnd"])
    LOG_INFO f"팝업윈도우영역: {팝업윈도우영역}"
    SET 찾기영역  = bottom_region(팝업윈도우영역, 50)
    SET allow_titles = ["유의사항", "안내"]
    SET title = TRIM(info["title"])
    if title == "유의사항"
        LOG_INFO f"'{title}' 팝업을 찾았습니다."
        RPA click_point location=Point(1916, 1377) after="wait:2s" // 확인버튼 클릭
    end_if
    LOG_INFO "=====================[ Close Popup Window]===================================="
end_function

function close_popups()
    SET success = False
    //팝업제거 현재 최상단 윈도우를 찾아서
    LOG_INFO "=====================[ 팝업제거 시작]===================================="
    RPA capture to_file=r"c:\\tmp\\popup.png"
    SET window_list = WINDOW_LIST(process_name=PROCESS_NAME)
    //LOG_INFO "현재 위도우들----->"
    //for win_info in window_list
    //    LOG_INFO f"윈도우: {win_info}"
    //end_for
    //LOG_INFO "<-----"
    SET count = 0
    while True
        SET top_window = WINDOW_TOP(process_name=PROCESS_NAME)
        SET info = DUMP_ATTRS(top_window)
        SET 팝업윈도우영역 = WINDOW_REGION(info["hwnd"])
        LOG_INFO f"팝업윈도우영역: {팝업윈도우영역}"
        # SET 찾기영역  = REGION_OF_REGION(팝업윈도우영역, "bottom_one_third")
        SET 찾기영역  = bottom_region(팝업윈도우영역, 50)
        LOG_INFO f"찾기영역: {찾기영역}"
        if info["title"] == "유의사항" or info["title"] == "안내" 
            for text in [ "닫기", "확인", "확 인", "확 민", "닫 기"]
                OCR FIND text=text  area=찾기영역 to_var="found" preprocess=False
                if found != None
                    LOG_INFO f"'{text}'를 찾았습니다."
                    SET p = POINT_OF_REGION(found, "center")
                    RPA click_point location=p, after="wait:2s" // 팝업의 닫기 또는 확인 버튼 클릭
                    just virtual_screen_close()
                    set success = True
                else
                    LOG_INFO f"'{text}'를 찾을 수 없습니다."
                    SET count = count + 1
                end_if
            end_for
        else
            LOG_INFO "팝업이 아닙니다."
            break
        end_if
        RPA wait seconds=3
        if count > 5
            LOG_WARN "팝업이 5번 이상 반복되어 종료합니다."
            break
        end_if
    end_while

    LOG_INFO "=====================[ 팝업제거 종료]===================================="
    return success
end_function

function virtual_screen_close()
    LOG_INFO "=====================[ 가상화면 종료 시작]===================================="
    SET 설정메뉴=Point(35, 57) // 설정메뉴 
    SET points= [  Point(96, 162), Point(595, 159), Point(609, 493) ]
    SET 닫기버튼위치 =  Point(1848, 1078) // 닫기 확인
    SET check_region = Region(52, 192, 127, 120)
    // 설정 풀다운의 서브메뉴가 뜨는 곳의 이미지를 저장해서 설정버튼이 동작하는지 체크한다.
    Image clip area=check_region to_var="image1"
    RPA wait seconds=1
    RPA click_point location=설정메뉴, after="wait:1s" speed=0.7
    Image clip area=check_region to_var="image2"
    if image1 != image2
        LOG_INFO "설정메뉴가 열렸습니다."
    else
        LOG_INFO "설정메뉴가 열리지 않았습니다."
        LOG_INFO "팝업이 떠 있다고 가정하고 팝업을 닫습니다"
        just close_popups()
    end_if

    RPA move_mouse locations=points, after="wait:1s" speed=0.7
    RPA click_point location=points[2], after="wait:1s"  speed=0.7
    RPA click_point location=닫기버튼위치 after="wait:1s" speed=0.7
    LOG_INFO "=====================[ 가상화면 종료]===================================="
end_function 

function close_efriend_hts()
    LOG_INFO "=====================[ eFriend HTS 종료 시작]===================================="
    just virtual_screen_close()
    SET 설정=Point(35, 57) // 설정메뉴
    SET 종료=Point(84, 1202) // 종료메뉴
    SET 종료확인=Point(1764, 1219) //종료확인
    RPA click_point location=설정, after="wait:1s"
    RPA click_point location=종료, after="wait:1s"
    RPA click_point location=종료확인, after="wait:1s"
    LOG_INFO "=====================[ eFriend HTS 종료 ]===================================="
end_function   
function save_file_name()
    SET save_folder = f"{IMAGE_PATH}\\capture"
    if dir_exists(save_folder) == False
        just DIR_CREATE(save_folder)
    end_if
    SET time_stamp = YMD_FORMAT(now(), "%Y-%m-%d_%H%M%S")
    return f"{save_folder}\\efriend_{time_stamp}.png"
end_function
function work_0808()
    LOG_INFO "=====================[ 0808 화면 호출 시작]===================================="
    SET 화면번호위치= Point(117, 103) //화면위치
    SET 비밀번호위치= Point(432, 201) //비밀번호위치
    RPA click_point location=화면번호위치, after="wait:1s"
    RPA put_text text="0808" clipboard=False  //0808입력
    just close_popup_window()
    
    RPA click_point location=비밀번호위치 after="wait:1s" //0808화면 클릭
    SET password = TO_STR($HTS_ACCT_PW)
    RPA put_text text=password clipboard=False  //pw입력
    RPA key_in keys=["enter"], after="wait:3s" // 엔터키입력
    
    RPA capture to_file=save_file_name()

    RPA click_point location= Point(451, 915) click_type="right" after="wait:1s" //0808화면 우클릭
    OCR FIND text="파일로 보내기" to_var="found" preprocess=False
    if found != None
        SET p = POINT_OF_REGION(found, "center")
        RPA click_point location=p, after="wait:1s" turtle=True speed=1.0 // 파일로 보내기 클릭
        LOG_INFO "파일로 보내기 클릭"
        OCR FIND text="Csv로 저장" to_var="found" preprocess=False
        if found != None
            SET p = POINT_OF_REGION(found, "center")
            RPA click_point location=p, after="wait:1s" // Csv로 저장 클릭
            LOG_INFO "Csv로 저장 클릭"
            SET file_name = f"{RESULT_PATH}\\0808.csv"
            RPA put_text text=file_name clipboard=True // 파일명입력
            RPA key_in keys=["enter"], after="wait:1s" // 엔터키입력
            LOG_INFO "0808 화면 종료"
        else
            LOG_INFO "Csv로 저장 찾을 수 없습니다."
        end_if
    else
        LOG_INFO "파일로 보내기 찾을 수 없습니다."
    end_if
end_function

function work_0801()
    LOG_INFO "=====================[ 0801 화면 호출 시작]===================================="
    SET 화면번호위치= Point(117, 103) //화면위치
    SET 비밀번호위치= Point(432, 201) //비밀번호위치
    RPA click_point location=화면번호위치, after="wait:1s"
    RPA put_text text="0801" clipboard=False  //0808입력
    just close_popup_window()
    
    OCR FIND text="국내 체결기준잔고" to_var="found" resize=1.5
    if found != None
        RPA click_region name=found after="wait:3s" //국내 체결기준잔고 클릭
    end_if


    //RPA click_point location=비밀번호위치 after="wait:1s" //0808화면 클릭
    SET password = TO_STR($HTS_ACCT_PW)
    RPA put_text text=password clipboard=False  //0808입력
    RPA key_in keys=["enter"], after="wait:3s" // 엔터키입력

    RPA capture to_file=save_file_name()

    RPA click_point location= Point(647, 658) click_type="right" after="wait:1s" //0801화면 우클릭    

    OCR FIND text="파일로 보내기" to_var="found" preprocess=False
    if found != None
        SET p = POINT_OF_REGION(found, "center")
        RPA click_point location=p, after="wait:1s" // 파일로 보내기 클릭
        LOG_INFO "파일로 보내기 클릭"
        OCR FIND text="Csv로 저장" to_var="found" preprocess=False
        if found != None
            SET p = POINT_OF_REGION(found, "center")
            RPA click_point location=p, turtle=True, after="wait:1s" // Csv로 저장 클릭
            LOG_INFO "Csv로 저장 클릭"
            SET file_name = f"{RESULT_PATH}\\0801.csv"
            RPA put_text text=file_name clipboard=True // 파일명입력
            RPA key_in keys=["enter"], after="wait:1s" // 엔터키입력
            LOG_INFO "0801 화면 종료"
        else
            LOG_INFO "Csv로 저장 찾을 수 없습니다."
        end_if
    else
        LOG_INFO "`파일로 보내기` 텍스트를 찾을 수 없습니다."
    end_if
end_function

//인증서 만료 팝업이 뜨면 확인 클릭
function close_cert_popup()
    SET cert_popup = WINDOW_FIND_BY_TITLE("인증서 만료공지")
    if cert_popup != None
        SET info = DUMP_ATTRS(cert_popup)
        LOG_INFO f"인증서 만료 팝업을 찾았습니다. {info}"
        RPA click_point location=Point(2175, 1127) after="wait:2s" // 확인버튼 클릭
        RPA wait seconds=3
        RPA click_point location=Point(2175, 1127) after="wait:2s" // 확인버튼 클릭
    end_if
end_function

function check_already_running_and_quit()
    SET is_running = PROCESS_IS_RUNNING(PROCESS_NAME)
    if is_running == True
        LOG_INFO f"{PROCESS_NAME} 프로세스가 이미 실행중입니다. 종료합니다."
        JUST PROCESS_FOCUS(PROCESS_NAME)
        RPA wait seconds=3
        JUST close_efriend_hts()
        RPA wait seconds=3
    end_if
end_function    
MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 프로그램 시작"
    LOG_INFO "=========================================================="
    LOG_INFO "------------------변수확인-------------------"
    LOG_INFO f"HTS_PROGRAM: {HTS_PROGRAM}"
    LOG_INFO f"PROCESS_NAME: {PROCESS_NAME}"
    LOG_INFO f"IMAGE_PATH: {IMAGE_PATH}"
    LOG_INFO f"RESULT_PATH: {RESULT_PATH}"
    LOG_INFO "--------------------------------------------"
    JUST check_already_running_and_quit()
    RPA open_app from_var="efriend", process_name=process_name, focus=True
    RPA wait seconds=10
    RPA wait_image area=인증서영역 , from_file=인증서창_확인 after="wait:5s" timeout=60*3
    LOG_INFO "인증서창 확인됨..."
    RPA click_point location=하드디스크_위치, after="wait:2s"
    SET tmp_file = FILE_TEMP_NAME(".png")
    LOG_INFO f"현재화면 저장 파일명: {tmp_file}"
    RPA capture to_file=tmp_file
    //IMAGE clip from_file=tmp_file area=인증서영역 to_var="image1"
    OCR FIND text=사용자명 from_file=tmp_file area=인증서영역 to_var="found_user_name_area" preprocess=False
    if found_user_name_area == None
        RAISE_ERROR "사용자명을 찾을 수 없습니다."
    else
        LOG_INFO f"사용자명:{사용자명} 영역을 찾았습니다."
    end_if

    SET p = POINT_OF_REGION(found_user_name_area, "center")
    RPA click_point location=p, after="wait:2s" // 사용자명클릭
    RPA click_point location=패스워드입력위치, after="wait:2s" // 패스워드위치클릭
    RPA put_text text=$HTS_PASSWORD // 패스워드입력
    RPA key_in keys=["enter"], after="wait:5s" // 엔터키입력
    //인증서 만료 팝업이 뜨면 확인 클릭
    just close_cert_popup()

    LOG_INFO "HTS 메인이 뜰때까지 기다린다...."
    RPA wait seconds=(60)
    RPA focus_app from_var="efriend"

    LOG_INFO "HTS 메인화면이 뜸"
    
    LOG_INFO "=========================================================="
    LOG_INFO ">>> eFriend HTS 종료"
    LOG_INFO "=========================================================="
    
    ON_EXCEPTION
        LOG_ERROR "예외 발생"
        LOG_ERROR f">>> {$exception_message} exit code: {$exit_code}"
        JUST Close_efriend_hts()
    END_EXCEPTION
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
# for line in command_preprocssed_lines:
#     print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    commandExecutor.execute(command)
