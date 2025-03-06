import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_script_execution(capfd):
    script = """
    MAIN
        SET list = [1, 2, 3, 4, 5]
        SET list[2-(1+1)] = 10
        SET a = list[1] + list[2]
        SET b = list[a-1]
        PRINT "{a} {b} {list}"
    END_MAIN
    """
    
    script_lines = script.split("\n")
    command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
    parsed_commands = CommandParser().parse(command_preprocssed_lines)
    commandExecutor = CommandExecutor()
    
    for command in parsed_commands:
        commandExecutor.execute(command)

    # 표준 출력 결과 캡처
    captured = capfd.readouterr()
    
    # 기대하는 출력값과 비교
    assert captured.out.strip() == "5 5 [10, 2, 3, 4, 5]"
