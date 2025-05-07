from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
INCLUDE "simple_test/qhd_120.kvs"
MAIN`

    LOG_INFO "=========================================================="
    LOG_INFO "OCR TEST"
    LOG_INFO "=========================================================="
    LOG_INFO "image_base_dir_source: {image_base_dir_source}"
    SET area1 = Region(923, 906, 716, 45)
    SET src_file = f"{image_base_dir_source}\\팝업들.png"
    OCR find text="일주일동안"  area=area1 to_var="r1" resize=1.5 gray=True, similarity=60
    LOG_INFO f"OCR FIND RESULT: {r1}"
    CONST ocr_info = {
        "gray": True,
        "threshold": "none",
        "blur": False,
        "resize": 1.5,
        "invert": False  // 배경 어두운 경우
    }
    //
    OCR get_all with=ocr_info preprocess=True from_file=src_file area=area1 to_var="texts"
    for text in texts
        print text
    END_FOR

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
