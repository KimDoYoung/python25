import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.token_type import TokenType

def test_basic_assignment_and_abs_function():
    script = """
    MAIN
        SET i = -12
        SET f = -12.34
        SET f2 = 12.34
        SET a = ABS(-10)
        SET b = ABS(-10.5)
        print i,f,f2,a,b
    END_MAIN
    """

    expected_values = {
        "i": (-12, TokenType.INTEGER),
        "f": (-12.34, TokenType.FLOAT),
        "f2": (12.34, TokenType.FLOAT),
        "a": (10, TokenType.INTEGER),
        "b": (10.5, TokenType.FLOAT),
    }

    script_lines = script.strip().split("\n")
    command_lines = CommandPreprocessor().preprocess(script_lines)
    parsed_commands = CommandParser().parse(command_lines)
    executor = CommandExecutor()

    for command in parsed_commands:
        executor.execute(command)

    for var_name, (expected_value, expected_type) in expected_values.items():
        token = executor.get_variable(var_name)
        assert token.type == expected_type
        assert token.data.value == expected_value, f"{var_name} 값 오류: 기대값 {expected_value}, 실제값 {token.data.value}"
