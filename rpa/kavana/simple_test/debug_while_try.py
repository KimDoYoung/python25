from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN   
    set count = 0
    while True
        try
            print "try"
        catch
            print "catch"
        finally
            PRINT "try-catch-finally"
        end_try
        PRINT "while"
        rpa wait seconds=3
        set count = count + 1
        if count > 3
            break
        end_if
    end_while
    try
        for i = 0 to 10
            print i
        end_for
    catch
        print "catch"
    finally
        PRINT "try-catch-finally"
    end_try

ON_EXCEPTION
    PRINT "on_exception handler"
END_EXCEPTION
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
