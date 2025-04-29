import sys
from io import StringIO
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_point_and_region_dump_attrs(monkeypatch):
    # Kavana 스크립트
    script = """ 
    MAIN
        SET p = point(10,20)
        SET x = GET_ATTR(p, "x")
        SET d = dump_attrs(p)
        SET rg = region(1,1,100,200)
        SET x1 = GET_ATTR(rg, "x")
        SET d1 = dump_attrs(rg)
        print x == d["x"], x1 + (d1["x"]+1) + (d1["y"]+1)
    END_MAIN
    """

    # 출력 캡처
    captured_output = StringIO()
    monkeypatch.setattr(sys, "stdout", captured_output)

    # 파싱 및 실행
    script_lines = script.strip().split("\n")
    preprocessed = CommandPreprocessor().preprocess(script_lines)
    parsed = CommandParser().parse(preprocessed)
    executor = CommandExecutor()
    for command in parsed:
        executor.execute(command)

    # 출력값 검증
    output = captured_output.getvalue().strip().splitlines()
    assert output[-1] == "True 5"
