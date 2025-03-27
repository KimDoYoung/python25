from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET list1 = [1, 2, 3]
    SET list2 = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 9
    ]
    SET list3 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    SET list4 = [ 
        "abc", 
        "d[f" ]
    PRINT "{list1}"
    PRINT "{list2}"
    PRINT "{list3}"
    PRINT "{list4}"
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
