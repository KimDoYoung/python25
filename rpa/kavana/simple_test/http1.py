from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
LOAD_ENV ".env"
MAIN
    // http_info
    set http_info = {
        "url": $GODATA_URL,
        "params" : {
            "ServiceKey": $GODATA_KEY,
            "pageNo": 1,
            "numOfRows": 10,
            "solYear": 2025,
            "solMonth": "04"
        },
        "verify_ssl": True,
    }
    print http_info
    HTTP get with=http_info to_var="http_response"
    print "--------------------------------------"
    print http_response
    print "--------------------------------------"

END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
# for line in command_preprocssed_lines:
#     print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    # print("----------------------")
    # print(command)
    commandExecutor.execute(command)
    # print("----------------------")
