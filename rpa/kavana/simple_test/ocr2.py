from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
INCLUDE "simple_test/qhd_120.kvs"
MAIN

    LOG_INFO "=========================================================="
    LOG_INFO "eFriend HTS 64bit 프로그램 시작 (OCR)"
    LOG_INFO "=========================================================="
    LOG_INFO ">>> efplusmain.exe 프로그램실행"
    print image_base_dir, program_path, process_name
    SET efriend64 = Application(program_path)
    RPA app_open from_var="efriend64", process_name=process_name, focus=True
    RPA wait_image from_file=cert_mark  area=center_area timeout=(5*10) 
    RPA wait seconds=5
    RPA click_image from_file=name_image area=center_area, after="wait:3s" to_var="result"
    if result == None
        raise "사용자명을 찾을 수 없습니다"
    end_if
    RPA click_point location=password_point after="wait:3s" 
    RPA put_text text=$HTS_PASSWORD clipboard=False after="wait:3s"
    RPA key_in keys=["enter"]

    RPA wait_image from_file=logo area=area_right_bottom timeout=3*60
    
    RPA wait seconds=5*60

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
