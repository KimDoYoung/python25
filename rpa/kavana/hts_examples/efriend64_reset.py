from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
include "simple_test/efriend64_data.kvs"
  
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
    RPA click_point location=Point(1657, 1417) after="wait:3s" //취소버튼
    //RPA click_point location=Point(1925, 1342) after="wait:3s" //확인
    SET btn = f"{IMAGE_PATH}\\인증서확인.png"
    RPA click_image area=인증서영역, from_file=btn after="wait:5s"
    RPA click_point location= Point(2184, 493)//종료
    
    LOG_INFO "=========================================================="
    LOG_INFO ">>> eFriend HTS 종료"
    LOG_INFO "=========================================================="
    
    ON_EXCEPTION
        //JUST Close_efriend_hts()
        LOG_ERROR "예외 발생"
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
