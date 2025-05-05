import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

@pytest.mark.parametrize("script, expected_output", [
    ("""
    MAIN
        SET i = (10 + 20) * 30
        SET f = 12.34
        SET s = "Hello"
        SET b = not True
        CONST pi = 3.14
        PRINT f"{i} {f} {s} {b} {pi}"
    END_MAIN
    """, "900 12.34 Hello False 3.14\n")  # ✅ 예상 출력값
])
def test_script_execution(script, expected_output, capsys):
    """✅ Kavana 스크립트 실행 테스트"""

    # ✅ 사전 처리 및 파싱
    script_lines = script.strip().split("\n")
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocessed_lines)

    # ✅ 실행
    commandExecutor = CommandExecutor()
    for command in parsed_commands:
        commandExecutor.execute(command)

    # ✅ 실행 결과 캡처
    captured = capsys.readouterr()
    assert captured.out == expected_output  # ✅ 기대한 출력과 비교
