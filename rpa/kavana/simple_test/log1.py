from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    LOG_INFO "--------------------------------------------------"
    LOG_INFO "프로그램 시작"
    LOG_INFO "--------------------------------------------------"
    SET var1 = 100
    SET var2 = 50
    LOG_CONFIG dir="./logs/my_app", prefix="my_app", level="DEBUG"
    LOG_INFO f"시스템 정상 실행 중. var1 = {var1}"
    LOG_WARN f"경고 발생! var1 + var2 = { var1 + var2 }"
    LOG_ERROR f"에러 발생! var1이 50보다 큰가? {var1 > 50}"
    LOG_DEBUG f"디버깅: 현재 값은 var1={var1}, var2={var2}"
    LOG_INFO "--------------------------------------------------"
    LOG_INFO "프로그램 종료"
    LOG_INFO "--------------------------------------------------"
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

