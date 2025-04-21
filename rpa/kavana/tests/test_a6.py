import pytest
from io import StringIO
import sys

from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_script_execution_result(monkeypatch):
    # 주어진 스크립트
    script = """
    MAIN
        SET map1 = {1: {"a":{"1":3,"2":[1,2,3]},"b":3}, 2: "two", 3: [1,2,3]}
        SET a = map1[1]["a"]["1"] + 10 + (map1[3][1] + 10) + map1[1]["a"]["1"] + 10 
        SET json_str = "{'response': {'header': {'resultCode': '00'}}}"
        SET hm = json_str_parse(json_str)
        set s = hm["response"]["header"]["resultCode"] + "test"
        SET json_str = "{'response': {'header': {'resultCode': '00', 'resultMsg': 'NORMAL SERVICE.'}, 'body': {'items': {'item': [{'dateKind': '02', 'dateName': '4·3희생자 추념일', 'isHoliday': 'N', 'locdate': '20250403', 'seq': '1'}, {'dateKind': '02', 'dateName': '예비군의 날', 'isHoliday': 'N', 'locdate': '20250404', 'seq': '2'}, {'dateKind': '02', 'dateName': '식목일', 'isHoliday': 'N', 'locdate': '20250405', 'seq': '1'}, {'dateKind': '02', 'dateName': '보건의 날', 'isHoliday': 'N', 'locdate': '20250407', 'seq': '1'}, {'dateKind': '02', 'dateName': '대한민국임시정부 수립기념일', 'isHoliday': 'N', 'locdate': '20250411', 'seq': '1'}, {'dateKind': '02', 'dateName': '도시농업의 날', 'isHoliday': 'N', 'locdate': '20250411', 'seq': '2'}, {'dateKind': '02', 'dateName': '4·19혁명 기념일', 'isHoliday': 'N', 'locdate': '20250419', 'seq': '1'}, {'dateKind': '02', 'dateName': '장애인의 날', 'isHoliday': 'N', 'locdate': '20250420', 'seq': '2'}, {'dateKind': '02', 'dateName': '과학의 날', 'isHoliday': 'N', 'locdate': '20250421', 'seq': '1'}, {'dateKind': '02', 'dateName': '정보통신의 날', 'isHoliday': 'N', 'locdate': '20250422', 'seq': '1'}]}, 'numOfRows': '10', 'pageNo': '1', 'totalCount': '13'}}}"
        SET hm1 = json_str_parse(json_str)
        set array1 = hm1["response"]["body"]["items"]["item"]
        set y = array1[0]["seq"]
        print a, y, s
    END_MAIN
    """

    # 표준 출력 리디렉션 (출력 결과 캡처)
    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)

    # 실행
    script_lines = script.strip().split("\n")
    command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocssed_lines)

    executor = CommandExecutor()
    for command in parsed_commands:
        executor.execute(command)

    # 출력 결과 가져오기
    result = captured_output.getvalue().strip()
    assert result == "38 1 00test"
