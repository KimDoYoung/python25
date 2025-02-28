from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser


script = """
function plus(a, b)
    return a + b
end_function

main
    SET a = 5

    IF a > 3
        PRINT "a is greater than 3"
    END_IF

    FOR i = 1 TO 3 STEP 1
        PRINT "Loop iteration {i}"
    END_FOR

    SET count = 0
    WHILE count < 3
        PRINT "Count is {count}"
        SET count = count + 1
    END_WHILE
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