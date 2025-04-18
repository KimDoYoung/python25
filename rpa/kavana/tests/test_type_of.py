import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_typeof_and_is_type(monkeypatch, capsys):
    script = """
    MAIN
        SET i = 1
        SET s = "hello"
        SET b = True
        SET a = [1, 2, 3]
        SET f = 3.14
        SET d = {"key": "value"}
        SET n = None
        if is_type(i, "integer")
            SET result = "Integer"
        else
            SET result = "Not Integer"
        END_IF
        print type_of(i),type_of(s),type_of(b),type_of(a),type_of(f),type_of(d),type_of(n), result,is_null(n), is_none(f) 
    END_MAIN
    """

    # ---------------------------
    # 실행
    # ---------------------------
    script_lines = script.strip().split("\n")
    command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocssed_lines)
    executor = CommandExecutor()

    for command in parsed_commands:
        executor.execute(command)

    # ---------------------------
    # 출력 결과 검증
    # ---------------------------
    captured = capsys.readouterr()
    expected = "Integer String Boolean Array Float HashMap NoneType Integer True False"
    output_line = [line for line in captured.out.strip().split("\n") if expected in line]

    assert output_line, "기대한 출력 라인이 없습니다."
    assert expected in output_line[0]
