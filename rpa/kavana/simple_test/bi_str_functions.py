from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET s1 = "hello" //나는 내가 빛나는 별인 줄 알았어요"
    SET s2 = "홍길동 입니다"
    print "------------------------------"   
    PRINT length(s1) , length(s2)
    PRINT substr(s1, 0, 2) , substr(s2, 0, 2)
    SET array1 = SPLIT("hello,world", ",")
    PRINT array1[0], array1[1]
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    commandExecutor.execute(command)
