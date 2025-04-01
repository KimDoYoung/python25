import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_script_execution(capfd):
    script = """
    MAIN
        SET name="홍길동"
        SET hello = f"안녕하세요, {name}님!"
        PRINT f"{hello}", "HI", "ABC"
    END_MAIN
    """

    script_lines = script.split("\n")
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)
    
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocessed_lines)

    command_executor = CommandExecutor()

    for command in parsed_commands:
        command_executor.execute(command)

    # 표준 출력 캡처
    captured = capfd.readouterr()
    
    # 기대값과 비교
    assert captured.out.strip() == "안녕하세요, 홍길동님! HI ABC"
