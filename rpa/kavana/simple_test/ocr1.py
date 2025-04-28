from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
ENV_LOAD ".env"
MAIN

    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 64bit 프로그램 시작 (OCR)"
    LOG_INFO "=========================================================="
    LOG_INFO ">>> efplusmain.exe 프로그램실행"
    SET base_img_dir = "C:\\Users\\PC\\Pictures\\efreind_uhd_175"
    SET app_path = "C:\\eFriend Plus x64\\efriendplus\\efriendplus.exe"
    SET efriend64 = Application(app_path)
    SET process_name = "efplusmain.exe"
    RPA app_open from_var="efriend64", process_name=process_name, focus=True
    LOG_INFO ">>> 인증서 패스워드 넣기"
    RPA wait seconds=5
    RPA wait_image area=Region(775, 232, 624, 754) 

    //CONST ocr_info = {
    //    "gray": False,
    //    "threshold": "none",
    //    "blur": False,
    //    "resize": 1.5,
    //    "invert": False  // 배경 어두운 경우
    //}
//
    //OCR get_all with=ocr_info preprocess=True from_file=f"{base_dir}{filename}" area=r4 to_var="texts"
    //for text in texts
    //    print text
    //END_FOR
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")

command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    commandExecutor.execute(command)
