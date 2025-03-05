from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# Builtin
script = """
MAIN
    print "------ 문자열함수들 ------"
    SET i = length("hello")
    SET j = length([1, 2, 3])
    SET k = length("안녕하세요")
    SET sub = substr("hello", 1, 3)
    PRINT "{i}{j}{k}{sub}"
    print "------ 숫자함수들 ------"
    SET r = random(1, 10)
    PRINT "random number: {r}"
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
for line in command_preprocssed_lines:
    print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    print("----------------------")
    print(command)
    commandExecutor.execute(command)
    print("----------------------")
