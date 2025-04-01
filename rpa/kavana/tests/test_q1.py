import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor


def test_script_exception_handling(capfd):
    script = """
    MAIN
        for i = 1 to 10
            if i == 3
                raise f"예외 발생: i는 {i}입니다."
            end_if
        end_for
        ON_EXCEPTION
            print f">>> {$exception_message} exit code: {$exit_code}"
        END_EXCEPTION
    END_MAIN
    """

    script_lines = script.split("\n")

    # 전처리
    command_preprocessed_lines = CommandPreprocessor().preprocess(script_lines)

    # 파싱
    parsed_commands = CommandParser().parse(command_preprocessed_lines)

    # 실행
    executor = CommandExecutor()

    with pytest.raises(SystemExit) as excinfo:  # SystemExit 예외를 예상된 동작으로 처리
        for command in parsed_commands:
            executor.execute(command)

    # 표준 출력 캡처
    captured = capfd.readouterr()

    # 기대값과 비교
    assert captured.out.strip() == ">>> 예외 발생: i는 3입니다. exit code: 1"
    assert excinfo.value.code == 1  # exit 코드가 1인지 확인
