from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
MAIN

    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 64bit 프로그램 시작 (OCR)"
    LOG_INFO "=========================================================="
    LOG_INFO ">>> efplusmain.exe 프로그램실행"
    SET program_path = "C:\\eFriend Plus x64\\efriendplus\\efplusmain.exe"
    SET efriend64 = Application(program_path)
    RPA focus_app from_var="efriend64"
    SET top_window = WINDOW_TOP("efplusmain.exe")
    SET hwnd = GET_ATTR(top_window, "hwnd")
    
    SET top_window_region = WINDOW_REGION(hwnd)
    LOG_INFO ">>> 최상위 창: {top_window_region}"
    RPA click_point location=Point(38, 56) //설정
    RPA move_mouse locations=[Point(115, 171),Point(621, 162)] after="wait:3s"
    RPA click_point location=Point(610, 498) //모든창닫기
    RPA wait seconds=3
    RPA click_point location=Point(1855, 1081)//확인
    RPA wait seconds=60

    LOG_INFO ">>> 끝내기"
    RPA key_in keys=["alt+f4", "enter"]
    //LOG_INFO ">>> 인증서 패스워드 넣기"
    //RPA wait seconds=5
    //RPA wait_image area=Region(775, 232, 624, 754) 

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
