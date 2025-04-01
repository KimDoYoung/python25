from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# HashMap
script = """
MAIN
    SET list1 = [1, 2, 3]
    SET list2 = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    SET a = list1[0] + list2[0][1]
    SET map1 = {
        "key1": 1,
        "key2": 2,
        "key3": 3
    }
    SET map2 = {
        "key1": [1, 2, 3],
        "key2": [4, 5, 6], 
        "key3": [7, 8, 9]
    }
    PRINT a, map1["key2"], map2["key2"][1]
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
