
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
    main
        //SET p = Point(10,20)
        //print p
        //SET r = Rectangle(10,20,100,200)
        //print r
        //SET rg = Region(5,10,150,80)
        //print rg
        SET base_dir = "C:/Users/PC/Pictures/"
        SET img1 = Image(base_dir + "1.png")

        SET a = Application("notepad.exe")
        print a
        SET w = Window("Untitled - Notepad")
        print w
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
    # print(command)
    commandExecutor.execute(command)
