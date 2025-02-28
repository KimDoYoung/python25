from lib.core.command_parser import CommandParser


script = """
MAIN
    SET a = 10
    FOR i = 1 TO a STEP 2
        PRINT "{i}"
    END_FOR
END_MAIN
"""
script_lines = script.split("\n")
parser = CommandParser(script_lines)
parsed_commands = parser.parse()

for command in parsed_commands:
    print("----------------------")
    print(command)
    print("----------------------")
exit(0)

# 명령어 실행
# executor = CommandExecutor()
# for command in parsed_commands:
#     executor.execute(command)