from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser


script = """
main
IF a >= 10
    PRINT "confirm.png"
ELIF a == 5
    PRINT "cancel.png"
ELSE
    PRINT "어떤 버튼도 없음";
END_IF

WHILE x < 100
    WAIT 1
END_WHILE

FOR i = 1 TO 5 STEP 1
    CLICK "button.png"
END_FOR
end_main
"""
script_lines = script.split("\n")
parser = CommandParser(script_lines)
parsed_commands = parser.parse()

for command in parsed_commands:
    print(command)
exit(0)

# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)