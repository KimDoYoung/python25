from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    // CLICK 10, 20
    // CLICK 10, 20, count=2, duration=0.5, type="double"
    // CLICK x=10, y=20
    // SET p1 = Point(30,40)
    // CLICK p1
    // CLICK Point(10,20)
    // SET r = Region(10, 20, 30, 40)
    // CLICK r, point_name="center"
    // CLICK image_path="C:\\Users\\PC\\Pictures\\SophiaCapture\\esafe\\login_button.png", confidence=0.8, search_region=None, grayscale=False, type="single"
    // CLICK rectangle(10,10,100,200), point_name="center"
    MOUSE_MOVE 10, 20
    MOUSE_MOVE x=10, y=20
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
