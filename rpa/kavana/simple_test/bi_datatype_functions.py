from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET app = Application("notepad.exe","process_name")
    SET app_info = DUMP_ATTRS(app)
    SET app_name = GET_ATTR(app, "process_name")
    PRINT app_info,app_name
    SET p = Point(100, 200)
    PRINT type_of(p)
    IF IS_TYPE(p, "Point") 
        PRINT "p is Point"
    ELSE
        PRINT "p is not Point"
    END_IF
    SET b = None
    if is_null(b)
        PRINT "b is null"
    else
        PRINT "b is not null"
    END_IF
    SET json_str = "{'name':'kavana', 'age': 3}"
    SET json_obj = JSON_STR_PARSE(json_str)
    PRINT json_obj["name"]
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
