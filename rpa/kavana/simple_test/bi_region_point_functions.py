from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET p = Point(100, 200)
    SET r = Region(0,0, 300, 400)
    if IS_POINT_IN_REGION(p, r)
        PRINT "p is in r"
    else
        PRINT "p is not in r"
    END_IF
    print POINT_OF_REGION(r, "center")
    print REGION_OF_REGION(r, "top_left")
    print REGION_OF_REGION(r, "top-left")
    SET p1 = Point(100, 200)
    PRINT POINT_MOVE_NORTH(p1, 10)
    PRINT POINT_MOVE_SOUTH(p1, 10)
    PRINT POINT_MOVE_EAST(p1, 10)
    PRINT POINT_MOVE_WEST(p1, 10)
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
