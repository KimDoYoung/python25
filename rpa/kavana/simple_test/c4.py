from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    set sum = 0
    for i in range(1,10+1)
        set sum = sum + i
    end_for
    //print sum 55
    for i in [1,2,3]
        set sum = sum + i
    end_for
    print sum //61
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
ppLines = CommandPreprocessor(script_lines).preprocess()
parser = CommandParser(ppLines)
parsed_commands = parser.parse()

# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)
