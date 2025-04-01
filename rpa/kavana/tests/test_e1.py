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
        SET b = list[a-2]
        SET list2 = [ [1,2,3], [4,5,6], [7,8,9] ]
        SET c = list2[0][0]
        SET a1 = 2
        SET list3 = [1, a1, 3, list[3], (2*2)+1]
        print f"{list}  {list2} {c} {list[1]} {a} {b} {list3}"
    END_MAIN
    """

    script_lines = script.split("\n")
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)
    parsed_commands = CommandParser().parse(command_preprocessed_lines)
    commandExecutor = CommandExecutor()

    for command in parsed_commands:
        commandExecutor.execute(command)

    # 캡처된 출력 가져오기
    captured = capfd.readouterr()

    # 예상 출력값
    expected_output = "[10, 2, 3, 4, 5]  [[1, 2, 3], [4, 5, 6], [7, 8, 9]] 1 2 5 4 [1, 2, 3, 4, 5]\n"

    assert captured.out == expected_output
