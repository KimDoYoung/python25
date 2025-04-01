import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

@pytest.mark.parametrize("script, expected_output", [
    ("""
    MAIN
        function plus(a, b)
            set c = 2+3+(4*5)
            return a + b + c - 10
        END_FUNCTION
        SET d = plus(1, 2)
        print f"{d}"
    END_MAIN
    """, "18\n")  # ✅ 예상 출력값
])
def test_script_execution(script, expected_output, capsys):
    """✅ 사용자 정의 함수 실행 테스트"""

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
