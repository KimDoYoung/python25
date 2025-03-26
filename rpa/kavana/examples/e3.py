from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# HashMap
script = """
MAIN
    SET map1 = {1: "one", 2: "two", 3: "three"}
    SET map2 = {"a": 1, "b": 2, "c": 3}
    SET map3 = {
        "aaa": 1+1,
        "bbb": 2+2,
        "ccc": 3+(1+2)
    }
    SET map4 = {
        "a": [1,2,3],
        "b": [4,5,6],
        "c": "홍길동"
    }
    SET a = "a"
    SET list = map4[a]
    SET s= map1[1] + "111"+map4["c"]
    PRINT "{s}"
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
