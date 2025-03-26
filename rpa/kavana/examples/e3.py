from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# LIST
script = """
MAIN
    SET map1 = {1: "one", 2: "two", 3: "three"}
    SET map2 = {"a": 1, "b": 2, "c": 3}
    SET map3 = {
        "aaa": 1,
        "bbb": 2,
        "ccc": 3
    }
    print "{map1} {map2} {map3}"
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
