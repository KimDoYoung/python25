from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


script = """
main
    SET a = 2
    SET c = "hello"

    FOR i = 1 TO 10 STEP 2
        PRINT "i = {i}"
    END_FOR

    FOR j = a TO LENGTH(c) STEP 1+2
        PRINT "j = {j}"
    END_FOR

    FOR k = 5*2 TO 20
        PRINT "k = {k}"
    END_FOR
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