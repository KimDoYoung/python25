from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
ENV_LOAD ".env"
MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 프로그램 시작"
    LOG_INFO "=========================================================="
    SET pt_login = Point(2329, 1105)
    SET pt_user = Point(1640, 1062)
    SET pt_pass = Point(2060, 1335)


    // 애플리케이션 실행
    SET app_path = "C:\\eFriend Plus\\efriendplus\\efriendplus.exe"
    SET process_name = "efplusmain.exe"
    SET image_base_path = "C:\\Users\\PC\\Pictures\\SophiaCap1ture\\efriend"
    SET efriend = Application(app_path)
    RPA app_open from_var="efriend", process_name=process_name, focus=True
    RPA wait seconds=5
    //로그인->사용자->비밀번호 <enter>
    RPA click_point location=pt_login, after="wait:10s"
    RPA click_point location=pt_user, after="wait:2s"
    RPA click_point location=pt_pass, after="wait:2s"
    RPA put_text text=$HTS_PASSWORD
    RPA key_in keys=["enter"], after="wait:2s" 

    RPA wait seconds=(60)
    RPA re_connect from_var="efriend", focus=True
    RPA wait seconds=(30)
    RPA close_all_children from_var="efriend"
    //
    RPA app_close from_var="efriend"
    
    //LOG_INFO "=========================================================="
    //LOG_INFO ">>> eFriend HTS 종료"
    //LOG_INFO "=========================================================="
    
    ON_EXCEPTION
        RPA app_close from_var="efriend" 
        PRINT "예외 발생"
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
