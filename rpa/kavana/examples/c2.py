from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


script = """
main
    PRINT "Before loop"

    FOR i = 1 TO 5 STEP 1
        IF i == 3
            PRINT "Skipping 3"
            CONTINUE
        END_IF
        IF i == 4
            PRINT "Breaking at 4"
            BREAK
        END_IF
        PRINT "Loop iteration {i}"
    END_FOR

    PRINT "After loop"
end_main
"""
script_lines = script.split("\n")
ppLines = CommandPreprocessor(script_lines).preprocess()
parser = CommandParser(ppLines)
parsed_commands = parser.parse()

for command in parsed_commands:
    print(command)
# exit(0)

# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)