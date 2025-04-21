from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    //SET json_str = "{'response': {'header': {'resultCode': '00', 'resultMsg': 'NORMAL SERVICE.'}, 'body': {'items': {'item': [{'dateKind': '02', 'dateName': '4·3희생자 추념일', 'isHoliday': 'N', 'locdate': '20250403', 'seq': '1'}, {'dateKind': '02', 'dateName': '예비군의 날', 'isHoliday': 'N', 'locdate': '20250404', 'seq': '2'}, {'dateKind': '02', 'dateName': '식목일', 'isHoliday': 'N', 'locdate': '20250405', 'seq': '1'}, {'dateKind': '02', 'dateName': '보건의 날', 'isHoliday': 'N', 'locdate': '20250407', 'seq': '1'}, {'dateKind': '02', 'dateName': '대한민국임시정부 수립기념일', 'isHoliday': 'N', 'locdate': '20250411', 'seq': '1'}, {'dateKind': '02', 'dateName': '도시농업의 날', 'isHoliday': 'N', 'locdate': '20250411', 'seq': '2'}, {'dateKind': '02', 'dateName': '4·19혁명 기념일', 'isHoliday': 'N', 'locdate': '20250419', 'seq': '1'}, {'dateKind': '02', 'dateName': '장애인의 날', 'isHoliday': 'N', 'locdate': '20250420', 'seq': '2'}, {'dateKind': '02', 'dateName': '과학의 날', 'isHoliday': 'N', 'locdate': '20250421', 'seq': '1'}, {'dateKind': '02', 'dateName': '정보통신의 날', 'isHoliday': 'N', 'locdate': '20250422', 'seq': '1'}]}, 'numOfRows': '10', 'pageNo': '1', 'totalCount': '13'}}}"
    SET json_str = "{'response': {'header': {'resultCode': '00'}}}"
    SET hm = json_str_parse(json_str)
    print type_of(hm)
    print hashmap1["response"]["header"]["resultCode"]
    set s = hashmap1["response"]["header"]["resultCode"] + "test"
    print s
END_MAIN 
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
for line in command_preprocssed_lines:
    print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    print("----------------------")
    print(command)
    commandExecutor.execute(command)
    print("----------------------")
