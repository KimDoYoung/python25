from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET p = point(10,20)
    SET x = GET_ATTR(p, "x")
    SET d = dump_attrs(p)
    //print x == d["x"]
    SET rg = region(1,1,100,200)
    SET x1 = GET_ATTR(rg, "x")
    SET d1 = dump_attrs(rg)
    print x == d["x"], x1 + (d1["x"]+1) + (d1["y"]+1)
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
