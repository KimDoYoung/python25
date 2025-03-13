from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


script = """
function plus(a, b)
    return a + b
end_function

main
    SET a = 5
    SET sum = 0
    IF a > 3
        SET sum = sum + a
    END_IF

    FOR i = 1 TO 3 STEP 1
       SET sum = sum + i
    END_FOR

    SET count_sum = 0
    SET count = 0
    WHILE count < 3
        SET count_sum = count_sum + count + 1
        set count = count + 1
    END_WHILE
    PRINT "{sum} {count_sum} {count}"
end_main
"""
script_lines = script.split("\n")
ppLines = CommandPreprocessor(script_lines).preprocess()
parser = CommandParser(ppLines)
parsed_commands = parser.parse()


# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)