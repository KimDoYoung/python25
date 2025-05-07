from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
include "simple_test/efriend64_data.kvs"
function close_popups()
    //팝업제거 현재 최상단 윈도우를 찾아서
    LOG_INFO "=====================[ 팝업제거 시작]===================================="
    while True
        SET top_window = WINDOW_TOP(process_name=PROCESS_NAME)
        SET info = DUMP_ATTRS(top_window)
        SET 팝업윈도우영역 = WINDOW_REGION(info["hwnd"])
        LOG_INFO f"팝업윈도우영역: {팝업윈도우영역}"
        SET 찾기영역  = REGION_OF_REGION(팝업윈도우영역, "bottom_one_third")
        LOG_INFO f"찾기영역: {찾기영역}"
        if info["title"] == "유의사항" or info["title"] == "안내" 
            SET tmp_file = FILE_TEMP_NAME(".png")
            RPA capture to_file=tmp_file 
            for text in ["일주일", "닫기", "확인"]
                OCR FIND text=text from_file=tmp_file area=찾기영역 to_var="found" resize=1.5
                if found != None
                    LOG_INFO f"'{text}'를 찾았습니다."
                    SET p = POINT_OF_REGION(found, "center")
                    RPA click_point location=p, after="wait:2s"
                else
                    LOG_INFO f"'{text}'를 찾을 수 없습니다."
                end_if
            end_for
        else
            break
        end_if
        RPA wait seconds=3
    end_while

    LOG_INFO "=====================[ 팝업제거 종료]===================================="
end_function

function virtual_screen_close()
    LOG_INFO "=====================[ 가상화면 종료 시작]===================================="
    //RPA click_point location=Point(3523, 1956) after="wait:1s"
    //RPA click_point location=Point(1854, 1083) after="wait:1s"
    SET 설정메뉴=Point(35, 57) // 설정메뉴 
    SET points= [  Point(96, 162), Point(595, 159), Point(609, 493) ]
    SET 닫기버튼위치 =  Point(1848, 1078) // 닫기 확인
    RPA click_point location=설정메뉴, after="wait:1s"
    RPA move_mouse locations=points, after="wait:1s"
    RPA click_point location=points[2], after="wait:1s"
    RPA click_point location=닫기버튼위치
    LOG_INFO "=====================[ 가상화면 종료]===================================="
end_function 

function close_efriend_hts()
    LOG_INFO "=====================[ eFriend HTS 종료 시작]===================================="
    SET 설정=Point(35, 57) // 설정메뉴
    SET 종료=Point(84, 1202) // 종료메뉴
    SET 종료확인=Point(1764, 1219) //종료확인
    RPA click_point location=설정, after="wait:1s"
    RPA click_point location=종료, after="wait:1s"
    RPA click_point location=종료확인, after="wait:1s"
    LOG_INFO "=====================[ eFriend HTS 종료 ]===================================="
end_function   

function work_0808()
    LOG_INFO "=====================[ 0808 화면 호출 시작]===================================="
    SET 화면번호위치= Point(117, 103) //화면위치
    RPA click_point location=화면번호위치, after="wait:1s"
    put_text text="0808" clipboard=True //0808입력

end_function

MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 프로그램 시작"
    LOG_INFO "=========================================================="
    LOG_INFO "------------------변수확인-------------------"
    LOG_INFO f"HTS_PROGRAM: {HTS_PROGRAM}"
    LOG_INFO f"PROCESS_NAME: {PROCESS_NAME}"
    LOG_INFO f"IMAGE_PATH: {IMAGE_PATH}"
    LOG_INFO "--------------------------------------------"
    RPA open_app from_var="efriend", process_name=process_name, focus=True
    RPA wait seconds=10
    RPA wait_image area=인증서영역 , from_file=인증서창_확인 after="wait:5s"
    LOG_INFO "인증서창 확인됨..."
    RPA click_point location=하드디스크_위치, after="wait:2s"
    SET tmp_file = FILE_TEMP_NAME(".png")
    LOG_INFO f"현재화면 저장 파일명: {tmp_file}"
    RPA capture to_file=tmp_file
    //IMAGE clip from_file=tmp_file area=인증서영역 to_var="image1"
    OCR FIND text=사용자명 from_file=tmp_file area=인증서영역 to_var="found_user_name_area"
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
    LOG_INFO "HTS 메인이 뜰때까지 기다린다...."
    RPA wait seconds=(60)
    RPA focus_app from_var="efriend"

    LOG_INFO "HTS 메인화면이 뜸"
    //팝업제거 
    RPA wait seconds=(3)
    JUST close_popups()
    //가상화면 모두 닫기
    RPA wait seconds=(3)
    JUST virtual_screen_close()
    //0808화면 호출
    just work_0808()
    
    //대기 
    RPA wait seconds=(60*3)
    
    //종료
    JUST close_efriend_hts()
    
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
