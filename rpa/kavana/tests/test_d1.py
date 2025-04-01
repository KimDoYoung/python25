import pytest
import builtins  # ✅ `builtins` 모듈을 명확하게 가져옴
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_script_execution():
    script = """
    main

        SET d1 = YmdTime(2025, 3, 5)
        Set d2 = YmdTime(2025, 3, 4, 10, 20, 30)
        Set d3 = d1 + 3
        set diff = d3 - d2
        print f"{d1}, {d2}, {d3}, {diff}"

    end_main
    """
    
    expected_output = "2025-03-05 00:00:00, 2025-03-04 10:20:30, 2025-03-08 00:00:00, 308370"
    
    script_lines = script.split("\n")
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)

    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocessed_lines)

    commandExecutor = CommandExecutor()

    # 실행 결과를 저장할 리스트
    actual_output = []

    # `print` 명령어의 출력을 가로채기 위한 함수
    def mock_print(*args):
        actual_output.append(" ".join(map(str, args)))

    # ✅ `builtins.print`을 백업하고 `mock_print`로 변경
    original_print = builtins.print
    builtins.print = mock_print

    try:
        for command in parsed_commands:
            commandExecutor.execute(command)

        # ✅ 마지막 출력값이 예상 결과와 일치하는지 검증
        assert actual_output[-1] == expected_output, f"Expected: {expected_output}, Got: {actual_output[-1]}"
    finally:
        # ✅ 테스트 종료 후 `print` 복구
        builtins.print = original_print
