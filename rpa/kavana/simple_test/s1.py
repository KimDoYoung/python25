from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET text = \"\"\"
    Hello, World!
    We are the champions, my friends!
    \"\"\"
    SET name="Kavana"
    SET s1 = f"Hello, {name}"
    SET s2 = r"Hello,\nWorld!"
    SET s3 = f"Hello,\n{name}"
    SET s4 = rf"Hello,\n{name}"
    PRINT "{text}"
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
