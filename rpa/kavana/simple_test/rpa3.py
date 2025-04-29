from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
function Remove_popups()
    LOG_INFO "=====================[ 팝업제거 시작]===================================="
    RPA wait seconds=(5)
    while True
        //RPA find_image area=Region(828, 373, 2138, 1399), from_file=close_button, to_var="found_close" multi=True
        RPA find_image area=Region(828, 373, 2138, 1399), from_file=confirm_button, to_var="found_confirm" multi=True
        //SET points = found_close + found_confirm
        SET points = found_confirm
        if length(points) > 0
            for p in points
                RPA click_point location=p, after="wait:1s", click_type="left", click_count=1, duration=0.5
            end_for
        else
            break
        end_if
        RPA wait seconds=(3)
    end_while
    LOG_INFO "=====================[ 팝업제거 종료]===================================="
end_function
function Close_efriend_hts()
    LOG_INFO "=====================[ eFriend HTS 종료 시작]===================================="
    RPA key_in keys=["alt+f4"], after="wait:2s"
    RPA click_point location=Point(1475, 1241)
    LOG_INFO "=====================[ eFriend HTS 종료]===================================="
end_function
function Close_all_virtual_screens()
    LOG_INFO "=====================[ 가상화면 종료 시작]===================================="
    RPA click_point location=Point(3523, 1956) after="wait:1s"
    RPA click_point location=Point(1854, 1083) after="wait:1s"

    LOG_INFO "=====================[ 가상화면 종료]===================================="
end_function    
MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 프로그램 시작"
    LOG_INFO "=========================================================="
    
    SET pt_login = Point(2329, 1105)
    SET pt_user = Point(1640, 1062)
    SET pt_pass = Point(2060, 1335)
    SET image_base_path = "C:\\Users\\PC\\Pictures\\kavana"
    SET close_button = f"{image_base_path}\\닫기버튼.png"
    SET confirm_button = f"{image_base_path}\\확인버튼.png"
    //efplusmain.exe

    // 애플리케이션 실행
    SET app_path = "C:\\eFriend Plus\\efriendplus\\efriendplus.exe"
    SET process_name = "efplusmain.exe"
    SET image_base_path = "C:\\Users\\PC\\Pictures\\SophiaCapture\\efriend"
    SET efriend = Application(app_path)
    RPA app_open from_var="efriend", process_name=process_name, focus=True
    RPA wait seconds=10
    //로그인->사용자->비밀번호 <enter>
    RPA click_point location=pt_login, after="wait:10s"
    RPA click_point location=pt_user, after="wait:2s"
    RPA click_point location=pt_pass, after="wait:2s"
    RPA put_text text=$HTS_PASSWORD
    RPA key_in keys=["enter"], after="wait:2s" 

    RPA wait seconds=(20)
    RPA re_connect from_var="efriend", focus=True

    //팝업제거 
    JUST Remove_popups()
    //가상화면 닫기
    JUST close_all_virtual_screens()

    LOG_INFO "==================[ 0808 화면] ===================================="
    RPA wait seconds=(10)
    RPA click_point location=Point(104, 107)
    RPA key_in keys=["ctrl+a", "delete"], after="wait:2s"
    RPA put_text text="0808" clipboard=False
    JUST remove_popups()

    RPA wait seconds=(5)
    RPA put_text text="4114" clipboard=False
    RPA key_in keys=["enter"], after="wait:2s"
    RPA wait seconds=(30)
    //HTS의 종료를 수행해 줘야 안전하게 종료됨    
    JUST Close_efriend_hts()
    
    LOG_INFO "=========================================================="
    LOG_INFO ">>> eFriend HTS 종료"
    LOG_INFO "=========================================================="
    
    ON_EXCEPTION
        PRINT "예외 발생"
        JUST Close_efriend_hts()
        LOG_ERROR f">>> {$exception_message} exit code: {$exit_code}"
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
