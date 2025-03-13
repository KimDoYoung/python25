from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# EXIT, ON_EXCEPTION, RAISE
script = """
MAIN
    SET content="우리는 빛이 되어야 한다. ABC!@#"
    SET result = FILE_WRITE("test.txt", content)
    if result == True
        PRINT "파일 쓰기 성공"
    else
        PRINT "파일 쓰기 실패"
    END_IF
    ON_EXCEPTION
        print ">>> {$exception_message} exit code: {$exit_code}"
    END_EXCEPTION
END_MAIN

"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parsed_commands = CommandParser().parse(command_preprocssed_lines)
commandExecutor = CommandExecutor()
for command in parsed_commands:
    commandExecutor.execute(command)
