from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    
    //TRY
    //    PRINT "try"
    //CATCH
    //    PRINT "catch"
    //FINALLY
    //    PRINT "finally"
    //END_TRY
    //raise "first error"
    //TRY
    //    PRINT "try"
    //    RAISE "error"
    //CATCH
    //    PRINT "catch"
    //FINALLY
    //    PRINT "finally"
    //END_TRY

    
    TRY
        for i = 0 to 10
            PRINT i
            IF i == 1 
                RAISE "error"
            END_IF
        END_FOR
    CATCH
        PRINT "catch"
    FINALLY
        PRINT "finally"
    END_TRY

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
