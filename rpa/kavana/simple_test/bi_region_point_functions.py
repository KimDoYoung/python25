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

    SET p2 = Point(100, 100)
    SET p3 = POINT_MOVE(p2, "N:10, E:10")
    PRINT p3
    SET p4 = POINT_MOVE(p3, "D:10, L:10")
    print p4

    SET rg1 = POINT_TO_REGION(p2, 10, 10)
    print "POINT_TO_REGION", rg1
    SET rg2 = POINTS_TO_REGION(POINT(8,43), POINT(3829,1914))
    print "POINTS_TO_REGION", rg2

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
