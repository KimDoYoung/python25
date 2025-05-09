from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET p = Point(10,20 )
    SET result = 0
    if p != None
        SET result = result + 1
    else
        print "p is None"
    END_IF
    if None == None
        SET result = result + 1
    else
        print "None is not None"
    END_IF 
    SET p2 = Point(10,20 )
    if p == p2
        SET result = result + 1
    else
        print "p is not p2"
    END_IF
    print result
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
