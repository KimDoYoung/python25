import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_hashmap_indexing_and_concat_output(capsys):
    script = """
    MAIN
        SET map1 = {1: "one", 2: "two", 3: "three"}
        SET map2 = {"a": 1, "b": 2, "c": 3}
        SET map3 = {
            "aaa": 1+1,
            "bbb": 2+2,
            "ccc": 3+(1+2)
        }
        SET map4 = {
            "a": [1,2,3],
            "b": [4,5,6],
            "c": "홍길동"
        }
        SET a = "a"
        SET list = map4[a]
        SET s = map1[1] + "111" + map4["c"]
        PRINT f"{s}"
    END_MAIN
    """

    # 실행 준비
    script_lines = script.strip().split("\n")
    preprocessed = CommandPreprocessor().preprocess(script_lines)
    parsed = CommandParser().parse(preprocessed)

    # 실행 및 출력 캡처
    executor = CommandExecutor()
    for command in parsed:
        executor.execute(command)

    # 표준 출력 확인
    captured = capsys.readouterr()
    assert "one111홍길동" in captured.out
