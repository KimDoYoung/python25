from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    set i = 0
    while i < 10
        try
            print i
            set i = i + 1
            if i == 5
                break
            end_if
        catch
            print "예외 발생"
        finally
            print "finally 블록 실행"
        end_try
    end_while
    print "루프 종료"
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
