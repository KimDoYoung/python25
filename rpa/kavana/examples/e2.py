from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# Array and Map multiple lines
script = """
MAIN
    SET list1 = [
        1, 2, 
        3, 4, 5
    ]
    SET list2 = [1, 2, 
    3, 4, 5]
    SET map1 = {
        "a": 1,
        "b": 2,
        "c": 3
    }
    set s = map1["a"]
    print "{list1}  {list2} {s}"
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
