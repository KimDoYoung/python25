from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "KSD SAFE 프로그램 시작"
    LOG_INFO "=========================================================="
    SET image_base_path = "C:\\Users\\PC\\Pictures\\SophiaCapture\\esafe"
    RPA find_image to_var="found_point" area=Region(0,0,100,100), from_file=f"{image_base_path}\\탭닫기.png", grayscale=True, confidence=0.8    

    if found_point != None
        LOG_INFO f"탭닫기 이미지 발견 {found_point}"
    else
        LOG_INFO "탭닫기 이미지 발견 못함"
    end_if
    SET save_folder = r"c:\\tmp"
    SET ymd = YMD(2024, 4, 17)
    SET save_file_name = f"{save_folder}\\{ymd}_500068.csv"
    if file_exists(save_file_name) == True
        just file_delete(save_file_name)
        print f"기존 파일 삭제 {save_file_name}"
    else
        print f"기존 파일 없음 {save_file_name}"
    end_if


    ON_EXCEPTION
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
    print("----------------------")
    print(command)
    commandExecutor.execute(command)
    print("----------------------")
