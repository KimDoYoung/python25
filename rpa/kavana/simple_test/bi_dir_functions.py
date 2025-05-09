from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET home_dir = DIR("사용자홈")
    SET pictures_dir = DIR("사진")
    SET temp_dir = DIR("임시")
    SET desktop_dir = DIR("바탕화면")
    SET documents_dir = DIR("문서")
    SET downloads_dir = DIR("다운로드")
    SET appdata_dir = DIR("앱데이터")
    SET cwd_dir = DIR("현재")   
    PRINT "사용자홈:", home_dir
    PRINT "사진:", pictures_dir
    PRINT "임시:", temp_dir
    PRINT "바탕화면:", desktop_dir
    PRINT "문서:", documents_dir
    PRINT "다운로드:", downloads_dir
    PRINT "앱데이터:", appdata_dir
    PRINT "현재:", cwd_dir
    PRINT "-----------------"

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
