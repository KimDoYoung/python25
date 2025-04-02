from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


# 제어문
script = """
MAIN
    SET a = 10
    // for문
    FOR i = 1 TO a STEP 2
        PRINT i
    END_FOR

    // if문
    IF a == 10
        PRINT "a is 10"
    END_IF
    
    // while문
    WHILE a > 0
        PRINT f"{a}"
        SET a = a - 1
    END_WHILE 
    
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

