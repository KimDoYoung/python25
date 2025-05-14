from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env_law"
INCLUDE "http_kvs/kofia_menu_4_common.kvs"
MAIN
    LOG_INFO "============[ KOFIA-MENU-4 : 규정,제개정예고]============"
    CALL create_db()
    SET URL="https://law.kofia.or.kr//service/revisionNotice/revisionNoticeListframe.do"
    BROWSER OPEN url=URL
    BROWSER WAIT seconds=5
    BROWSER EXTRACT select="tr"  within=".brdComList tbody"  to_var="tr_list"

    for item in tr_list:
        LOG_INFO "{item}"
    end_for
    BROWSER CLOSE

    
    ON_EXCEPTION //예외처리
        LOG_ERROR "에러 발생"
        BROWSER CLOSE
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
