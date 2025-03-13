from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


script = """
main
    for i in [3,5,10]
        if i == 3
            set r = "if"
            print "i is 3 {r}"
        elif i == 5 
            set r = "elif"
            print "i is 5 {r}"
        else
            set r = "else"
            print "i is not 3 or 5 {r}"
        end_if
    end_for
end_main
"""
script_lines = script.split("\n")
ppLines = CommandPreprocessor(script_lines).preprocess()
parser = CommandParser(ppLines)
parsed_commands = parser.parse()

# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)