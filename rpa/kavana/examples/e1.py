from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# LIST
script = """
MAIN
    //SET list = [1, 2, 3, 4, 5]
    //SET list[2-(1+1)] = 10
    //SET a = list[1] + list[2]
    //SET b = list[a-2]
    //SET list2 = [ [1,2,3], [4,5,6], [7,8,9] ]
    //SET c = list2[0,0]
    SET list = [[1,2],[3,4],[5,6]]
    //print "{list} {list[1]} {a} {b} {list2} {c}"
    print "{list[0,1]}"
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parsed_commands = CommandParser().parse(command_preprocssed_lines)
commandExecutor = CommandExecutor()
for command in parsed_commands:
    # print("----------------------")
    # print(command)
    commandExecutor.execute(command)
    # print("----------------------")
