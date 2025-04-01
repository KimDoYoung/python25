import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

def test_array_and_hashmap_multiline_output(capsys):
    script = """
    MAIN
        SET list1 = [
            1, 2, 
            3, 4, 5
        ]
        SET list2 = [1, 2, 
        3, 4, 5]
        SET map1 = {
            "a": 1,
            "b": 2,
            "c": 3
        }
        SET s = map1["a"]
        PRINT f"{list1}  {list2} {s}"
    END_MAIN
    """

    script_lines = script.strip().split("\n")
    preprocessed = CommandPreprocessor().preprocess(script_lines)
    parsed = CommandParser().parse(preprocessed)

    executor = CommandExecutor()
    for command in parsed:
        executor.execute(command)

    captured = capsys.readouterr()
    expected = "[1, 2, 3, 4, 5]  [1, 2, 3, 4, 5] 1"
    assert expected in captured.out
