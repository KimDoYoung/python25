from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
INCLUDE "./examples/common.kvs"
LOAD_ENV "./examples/env.test"
MAIN
    print "{global_name}"
    print "PASSWORD: {$PASSWORD}, USERNAME: {$USERNAME}"
    SET c = plus(1, 2)
    print "c = {c}"
    print "1 + 2 = {plus(1, 2)}"
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
    print("----------------------")
    commandExecutor.execute(command)
