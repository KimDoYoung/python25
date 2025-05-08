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
    LOG_INFO "=========================================================="
    LOG_INFO "OCR_TEST"
    LOG_INFO "=========================================================="
    SET IMAGE_PATH = r"C:\\Users\\USER\\Pictures\\efriend_plus_qhd125"
    SET img1 = f"{IMAGE_PATH}\\source\\0801_context_menu.png"
    OCR get_all from_file=img1 area=Region(7, 123, 990, 38) to_var="texts"  resize=1.5
    for txt in texts
        LOG_INFO f"텍스트: {txt}"
        //print txt
    end_for

    OCR get_all from_file=img1 area=Region(7, 123, 990, 38) to_var="texts2"  preprocess=False
    for txt in texts2
        LOG_INFO f"텍스트: {txt}"
        //print txt
    end_for

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
