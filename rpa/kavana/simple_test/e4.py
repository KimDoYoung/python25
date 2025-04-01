from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# HashMap
script = """
MAIN
    set map1 = { "name": "Alice1", "age": 31 }
    set map2 = { "name": "Alice2", "age": 32 }
    set map3 = { "name": "Alice3", "age": 33 }
    set list = [map1, map2, map3]
    PRINT list[0]["name"]
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
