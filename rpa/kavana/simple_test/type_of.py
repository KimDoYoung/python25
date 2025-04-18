from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET i = 1
    SET s = "hello"
    SET b = True
    SET a = [1, 2, 3]
    SET f = 3.14
    SET d = {"key": "value"}
    SET n = None
    if is_type(i, "integer")
        SET result = "Integer"
    else
        SET result = "Not Integer"
    END_IF
    print type_of(i),type_of(s),type_of(b),type_of(a),type_of(f),type_of(d),type_of(n), result, is_null(n), is_none(f) 
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
