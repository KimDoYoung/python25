from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# EXIT, ON_EXCEPTION, RAISE
script = """
MAIN
    for i = 1 to 10 
        print "{i}"
        if i == 3
            exit
        end_if
    end_for
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
