from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    DB CONNECT path="test1.db" 
    DB BEGIN_TRANSACTION name="default"
    DB EXECUTE sql="insert into tasks (title) values ('task1')"
    DB EXECUTE sql="insert into tasks1 (title) values ('task2')"
    DB COMMIT name="default"

    ON_EXCEPTION
        PRINT f"예외 발생: {$exception_message} (exit code: {$exit_code})"
        DB ROLLBACK name="default"
        DB CLOSE name="default"
    END_EXCEPTION
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
    print("----------------------")
    commandExecutor.execute(command)
