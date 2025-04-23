from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
main
    print "----------------------"
    SET ymd1 = Ymd(2025, 3, 5)
    SET ymdtime1 = YmdTime(2025, 3, 5, 10, 20, 30)
    print "ymd:", ymd1, "ymdtime:", ymdtime1
	print "ymd:", ymd
    SET now1 = Now()
    print now1
    SET today1 = Today()
    print today1

	SET d1 = YmdTime(2025, 3, 5)
    Set d2 = YmdTime(2025, 3, 4, 10, 20, 30)
    print d1+1, d2
    Set d3 = d1 + 3
    set diff = d3 - d2
	print f"{d1}, {d2}, {d3}, {diff}"
	
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
    commandExecutor.execute(command)
