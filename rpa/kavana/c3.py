from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser


script = """
main
    SET a = 2
    SET c = "hello"

    FOR i = 1 TO 10 STEP 2
        PRINT "i = {i}"
    END_FOR

    FOR i = a TO LENGTH(c) STEP 1+2
        PRINT "i = {i}"
    END_FOR

    FOR i = 5*2 TO 20
        PRINT "i = {i}"
    END_FOR
end_main
"""
script_lines = script.split("\n")
parser = CommandParser(script_lines)
parsed_commands = parser.parse()

for command in parsed_commands:
    print(command)
# exit(0)

# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)