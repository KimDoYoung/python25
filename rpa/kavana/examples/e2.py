from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET olist = [1, 2, 3, 4, 5]
    SET a = 1
    //SET list = [1, a+oList[a], a+2, 2+2, (20+5)/5]
    SET list = [1, a+oList[a],1, 2, 3]
    PRINT "{list}"
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
    print("----------------------")
    print(command["cmd"])
    for arg in command["args"]:
        print(f">>>{arg}")
    # commandExecutor.execute(command)
    print("----------------------")
