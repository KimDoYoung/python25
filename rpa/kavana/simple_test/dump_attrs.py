from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET p = point(10,20)
    SET x = GET_ATTR(p, "x")
    SET d = dump_attrs(p)
    print x == d["x"]
    SET r = region(1,1,100,200)
    SET x = GET_ATTR(r, "x")
    SET d = dump_attrs(r)
    print x, d["x"]+1, d["y"]+1
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
