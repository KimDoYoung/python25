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

function get_all_test()
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
end_function
function find_test()
    SET text_list = ["국내 체결기준잔고", "결제기준잔고","예수금현황","미수금현황","외화미수금","반대매매현황","신용/대출잔고현황","국내 대여잔고조회"]
    for text in text_list
        OCR find text=text from_file=img1 area=Region(7, 123, 990, 38) to_var="found_region" resize=1.5
        if found_region == None
            LOG_ERROR f"{text} 텍스트를 찾지 못했습니다."
        else
            LOG_INFO f"찾은 영역: {found_region}"
        end_if
    end_for
end_function
function read_test()
    SET rg_list = [
            Region(11, 193, 262, 103),
            Region(272, 193, 266, 104),
            Region(537, 195, 262, 97),
            Region(798, 193, 265, 103)    
    ]
    for r1 in rg_list
        OCR read from_file=img1 area=r1 to_var="texts3"  resize=1.5
        LOG_INFO f"영역: {r1}"
        LOG_INFO f"텍스트: {texts3}"
    end_for
end_function

MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "OCR_TEST"
    LOG_INFO "=========================================================="
    SET IMAGE_PATH = r"C:\\Users\\USER\\Pictures\\efriend_plus_qhd125"
    SET img1 = f"{IMAGE_PATH}\\source\\0801_context_menu.png"

    LOG_INFO "--------------------------------------------------------"
    //just get_all_test()
    LOG_INFO "--------------------------------------------------------"    
    //just find_test()
    LOG_INFO "--------------------------------------------------------"
    just read_test()
    LOG_INFO "--------------------------------------------------------"
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
