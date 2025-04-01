import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_function_execution(capfd):
    """✅ 사용자 정의 함수 호출 및 연산이 정상 동작하는지 검증"""

    script = """
    MAIN
        function plus(a, b)
            set c = 2+3+(4*5)
            return a + b + c - 10
        END_FUNCTION
        SET d = plus(1, 2) + 12
        print f"{d}"
    END_MAIN
    """

    # ✅ 스크립트 처리
    script_lines = script.strip().split("\n")
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocessed_lines)

    # ✅ 실행기 생성 및 실행
    command_executor = CommandExecutor()
    for command in parsed_commands:
        command_executor.execute(command)

    # ✅ 표준 출력 캡처 및 결과 검증
    captured = capfd.readouterr()
    assert captured.out.strip() == "30"  # ✅ 기대 결과 검증

