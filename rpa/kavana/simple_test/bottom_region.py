from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
function bottom_region(rg, height)
    SET rg_info = DUMP_ATTRS(rg)        
    SET new_height = rg_info["y"] + rg_info["height"] - height
    SET new_region = Region(rg_info["x"], new_height, rg_info["width"], height)
    return new_region
end_function
MAIN
    SET r = Region(0, 0, 100, 100)
    print f"원본영역: {r}"
    SET bottom_region = bottom_region(r, 10)
    print f"변경된영역: {bottom_region}"
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
