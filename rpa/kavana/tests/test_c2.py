import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


def test_script_execution(capfd):
    script = """
    main
        for i in [3,5,10]
            if i == 3
                set r = "if"
                print "i is 3 {r}"
            elif i == 5 
                set r = "elif"
                print "i is 5 {r}"
            else
                set r = "else"
                print "i is not 3 or 5 {r}"
            end_if
        end_for
        for s in ["갑돌이", "이몽룡", "홍길동"]
            print "{s}"
        end_for
    end_main
    """

    script_lines = script.split("\n")

    # 전처리
    ppLines = CommandPreprocessor(script_lines).preprocess()

    # 파싱
    parser = CommandParser()
    parsed_commands = parser.parse(ppLines)

    # 실행
    executor = CommandExecutor()
    for command in parsed_commands:
        executor.execute(command)

    # 표준 출력 캡처
    captured = capfd.readouterr()

    # 기대값
    expected_output = """\
i is 3 if
i is 5 elif
i is not 3 or 5 else
갑돌이
이몽룡
홍길동"""

    # 출력 비교
    assert captured.out.strip() == expected_output
