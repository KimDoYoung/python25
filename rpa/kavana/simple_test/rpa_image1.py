from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# LIST
script = """
MAIN
    SET region1 = Region(0, 0, 100, 100)
    IMAGE clip area=region1 to_var="img1"
    rpa wait seconds=5
    IMAGE clip area=region1 to_var="img2"
    if img1 != img2
        print "이미지가 다름"
    else
        print "이미지가 같음"
    end_if
    SET process_list = PROCESS_LIST()
    for process in process_list
        print process
    end_for
    if PROCESS_IS_RUNNING("efplusmain.exe")
        print "efplusmain.exe is running"
        rpa wait seconds=5
        JUST PROCESS_FOCUS("efplusmain.exe")
    else
        print "efplusmain.exe is not running"
    end_if
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parsed_commands = CommandParser().parse(command_preprocssed_lines)
commandExecutor = CommandExecutor()
for command in parsed_commands:
    # print("----------------------")
    # print(command)
    commandExecutor.execute(command)
    # print("----------------------")
