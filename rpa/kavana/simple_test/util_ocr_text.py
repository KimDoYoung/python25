from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
  
MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "OCR_TEXT"
    LOG_INFO "=========================================================="
    set base_path = r"C:\\Users\\PC\\Pictures\\efreind_uhd_175\\source"
    
    set img=f"{base_path}\\초기팝업2.png"
    LOG_INFO "=========================================================="
    LOG_INFO ">>> OCR_TEXT 종료"
    LOG_INFO "=========================================================="
    //SET img = r"C:\\Users\\PC\\Pictures\\SophiaCapture\\초기팝업2\\image_0.png"
    //OCR get_all from_file=img area=Region(1361, 1337, 1121, 53) to_var="text_info_list" resize=1.5
    OCR get_all from_file=img area=Region(1480, 1463, 890, 48) to_var="text_info_list" preprocess=False
    for text1 in text_info_list
        print text1["text"]
        //SET info = DUMP_ATTRS(text1)
        //SET s = info["text"]
        //print s //, info["x"], info["y"], info["w"], info["h"]
    end_for

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
