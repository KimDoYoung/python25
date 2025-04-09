
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
    main
        SET p = Point(10,20)
        SET rt = Rectangle(0,0,10,20)
        SET rg = Region(1,1,100,200)
        SET win1 = Window("title1")
        SET img1 = Image("C:/Users/PC/Pictures/1.png")
        SET app1 = Application("notepad.exe")
        print f"{p}, {rt}, {rg}, {win1}, {img1}"
    end_main
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
    print(command)
    commandExecutor.execute(command)
