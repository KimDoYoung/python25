from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET var1 = 100
    SET var2 = 50

    LOG_INFO "시스템 정상 실행 중. var1 = {var1}"
    LOG_WARN "경고 발생! var1 + var2 = {var1 + var2}"
    LOG_ERROR "에러 발생! var1이 50보다 큰가? {var1 > 50}"
    LOG_DEBUG "디버깅: 현재 값은 var1={var1}, var2={var2}"

    LOG_CONFIG dir="logs", prefix="kdy", level="DEBUG"
    LOG_INFO "새로운 로그 설정 적용됨. 현재 경로: {log_dir}"

    LOG_CONFIG dir="my_logs", prefix="kavana"
    LOG_WARN "기본 설정으로 복원됨. var1={var1}"
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

