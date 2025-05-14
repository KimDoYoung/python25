from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env_law"
INCLUDE "http_kvs/kofia_menu_4_common.kvs"
MAIN
    LOG_INFO "============[ KOFIA-MENU-4 : 규정,제개정예고]============"
    //CALL create_db()
    SET URL="https://law.kofia.or.kr/service/revisionNotice/revisionNoticeListframe.do"
    SET DETAIL_URL = "https://law.kofia.or.kr/service/revisionNotice/revisionNoticeViewframe.do"
    SET i = 1
    while True:
        SET param = {"page":i}
        HTTP post url=URL params=param  to_var="http_response"
        HTML select css="table.brdComList > tbody > tr" html=http_response to_var="tr_list" 
        
        FOR tr in tr_list:
            HTML select_one css="td:nth-child(1)" html=tr to_var="ui_seq" otype="text"
            HTML select_one css="td:nth-child(2) a" html=tr to_var="title" otype="text"
            HTML select_one css="td:nth-child(3)" html=tr to_var="gubun" otype="text"
            HTML select_one css="td:nth-child(4)" html=tr to_var="start_date" otype="text"
            HTML select_one css="td:nth-child(5)" html=tr to_var="end_date" otype="text"
            HTML select_one css="td:nth-child(2) a" html=tr to_var="seq" otype="attr:href"
            SET real_seq = REG_EX(seq, "(\\d+)")
            LOG_INFO "real_seq: {real_seq}"
            SET param = {"revisionSeq":real_seq}
            HTTP post url=DETAIL_URL params=param to_var="detail_response"
            LOG_INFO "detail_response: {detail_response}"

            HTML select_one css="div.storyIn" html=detail_response to_var="summary" otype="text"
            HTML select_one css="tr:has(th:contains('관련파일')) td a" html=detail_response otype="attr:href" to_var="download_url"
            HTML select_one css="tr:has(th:contains('관련파일')) td a" html=detail_response otype="text" to_var="download_filename"

            HTTP get url="https://law.kofia.or.kr/" + download_url to_var="download_response"
            
            LOG_INFO "--------------------------------------"
            LOG_INFO "ui_seq: {ui_seq}, real_seq:{real_seq}, title: {title}, gubun: {gubun}, start_date: {start_date}, end_date: {end_date}, summary: {summary}"
            LOG_INFO "download_url: {download_url}, download_filename: {download_filename}"
            LOG_INFO "--------------------------------------"
            RPA WAIT seconds=3
        END_FOR

        SET i = i + 1
        IF i > 1:
            break
        END_IF
        RPA WAIT seconds=5
    END_WHILE

    ON_EXCEPTION //예외처리
        LOG_ERROR "XXXX 에러 발생"
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
