from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    for i in range(1, 5):
        SET all_data = {
            "a": i,
            "b": i + 1
        }
        print all_data
    end_for
    SET item1 = 111
    SET item2 = 222
    SET all_data = {"a": 1, "b": 2}
    SET all_data = {"a": 11, "b": 22}
    SET all_data = {"a": item1, "b": item2}
    print all_data
    SET a = 10
    SET p = {
    "a": 1,
    "b": 2
    }
    SET sql_template = "SELECT * FROM test WHERE ? = ?"
    SET sql = MAKE_SQL(sql_template, p)
    print sql
    SET i = -12
    SET f = -12.34
    SET f2 = 12.34
    SET d = {
        "a": 1
    }
    SET a = ABS(-10 + d["a"])
    SET b = ABS(-10.5)
    print i,f,f2,a,b
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
