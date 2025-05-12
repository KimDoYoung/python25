from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    set window_list = WINDOW_LIST()
    for window1 in window_list
        set info = DUMP_ATTRS(window1)
        print info["hwnd"], info["title"], info["class_name"]
    end_for
    print "----------------------"
    set cert_over = WINDOW_FIND_BY_TITLE("인증서 만료공지")
    if cert_over != None
        set info = DUMP_ATTRS(cert_over)
        print info["hwnd"], info["title"], info["class_name"]
    end_if
    print window_list[0]
    set top_window = WINDOW_TOP("efplusmain.exe")
    if top_window != None
        PRINT top_window    
    end_if
ON_EXCEPTION
    PRINT $EXCEPTION_MESSAGE, $EXIT_CODE
END_EXCEPTION
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
