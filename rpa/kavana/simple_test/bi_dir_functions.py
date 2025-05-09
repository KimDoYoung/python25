from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET home_dir = DIR("사용자홈")
    SET pictures_dir = DIR("사진")
    pRINT f"HOME: {home_dir}, 사진: {pictures_dir}"
    SET dirs = DIR_LIST("C:/tmp")
    for file in dirs:
        print file["name"], file["is_directory"], file["size"], file["modified_time"]
    END_FOR
    PRINT "-----------------"
    SET exists = DIR_EXISTS("C:/tmp")
    PRINT exists
    SET created = DIR_CREATE("C:/tmp/new_dir")
    PRINT created
    SET renamed = DIR_RENAME("C:/tmp/new_dir", "C:/tmp/renamed_dir")
    PRINT renamed
    SET deleted = DIR_DELETE("C:/tmp/renamed_dir")
    PRINT deleted
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
