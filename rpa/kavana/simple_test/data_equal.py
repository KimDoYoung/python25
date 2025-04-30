from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

script = """
MAIN
    LOG_CONFIG level="ERROR"
    SET b1 =  Point(10,20)==Point(11,22)
    SET b2 =  Region(1,2,10,20) == Region(1,2,10,20)
    SET b3 =  1.23 == 1.23
    RPA capture area=Region(0,0,500,400) to_var="img1" to_file=r"c:\\tmp\\img1.png"
    RPA capture area=Region(0,0,500,400) to_var="img2" to_file=r"c:\\tmp\\img2.png"
    SET b4 = img1 == img2
    SET w1 = Window("제목",1, "1")
    SET w2 = Window("제목",1, "2")
    SET b5 = w1 == w2
    SET app1 = Application("path1", "process_name1")
    SET app2 = Application("path1", "process_name2")
    SET b6 = app1 == app2
    PRINT b1,b2,b3,b4,b5,b6
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
