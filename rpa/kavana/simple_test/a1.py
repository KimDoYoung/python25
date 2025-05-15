from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    CONST pi = 3.14
    CONST age = 10
    SET d = [{
        "pid": age
    }]
    SET i = (10 + 20) * 30
    SET f = 12.34
    SET s = "Hello"
    SET b = not True
    PRINT f"{i} {f} {s} {b}, {pi}"
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
