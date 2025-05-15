import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from io import StringIO
import sys

def test_script_execution_print_sum(monkeypatch):
    # given
    script = """
MAIN
    for i in [1,2,3]
        set a = [i+1, i+2]
    end_for
    set i = 1
    while i < 3
        set array = [i, i+1]
        set i = i + 1
    end_while
    set b =  a + array
    set sum = 0
    for n in b
        set sum = sum + n
    end_for
    print sum
END_MAIN
"""
    script_lines = script.strip().split("\n")
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocessed_lines)
    command_executor = CommandExecutor()

    # when: stdout 가로채기
    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)

    for command in parsed_commands:
        command_executor.execute(command)

    # then: 출력값 확인
    output = captured_output.getvalue().strip()
    assert output == "14"
