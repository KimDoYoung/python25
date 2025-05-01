from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET date = YMDTIME(2025, 5, 1, 12, 30, 45)
    print date
    SET ymd1 = YMD(2025, 5, 1)
    print ymd1
    print NOW(),now
    print Today(),today
    print "월요일~일요일(0~6):", weekday(ymd1)
    print f"{ymd1} 은 주말인가?", is_weekend(ymd1)
    print f"{ymd1} 은 {week_name(ymd1)} 입니다"
    SET ymd2 = ymd1 + 30
    print ymd2
    SET start_time = now()
    RPA wait seconds=5
    SET end_time = now()
    SET elapsed_time = end_time - start_time
    print "경과 시간:", elapsed_time
    print YMD_FORMAT(now, "%Y%m%d %H:%M:%S")
    print YMD_FORMAT(today, "%Y%m%d")
    print YMD_FORMAT(ymd1, "%Y%m%d")
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
