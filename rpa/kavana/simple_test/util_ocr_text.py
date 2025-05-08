from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
function save_file_name()
    SET save_folder = f"{IMAGE_PATH}\\capture"
    if dir_exists(save_folder) == False
        just DIR_CREATE(save_folder)
    end_if
    SET time_stamp = YMD_FORMAT(now(), "%Y-%m-%d_%H%M%S")
    return f"{save_folder}\\efriend_{time_stamp}.png"
end_function
MAIN
    SET IMAGE_PATH = r"C:\\Users\\PC\\Pictures\\efreind_uhd_175"
    //SET dict1 = {"key1": "value1", "key2": "value2"}
    print save_file_name()
    LOG_INFO "=========================================================="
    LOG_INFO "OCR_TEXT"
    LOG_INFO "=========================================================="
    set base_path = r"C:\\Users\\PC\\Pictures\\efreind_uhd_175"
    
    set img=f"{base_path}\\팝업2.png"
    OCR get_all from_file=img  to_var="text_info_list" preprocess=False
    for text1 in text_info_list
        SET x = text1["x"]
        SET y = text1["y"]
        SET w = text1["w"]
        SET h = text1["h"]
        SET region1 = Region(x, y, w, h)
        print "["+ text1["text"] + "]" , region1
    
        //LOG_INFO "["+ text1["text"] + "]"
        //SET info = DUMP_ATTRS(text1)
        //SET s = info["text"]
        //print s //, info["x"], info["y"], info["w"], info["h"]
    end_for
    LOG_INFO "=========================================================="
    LOG_INFO ">>> OCR_TEXT 종료"
    LOG_INFO "=========================================================="

    ON_EXCEPTION
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
