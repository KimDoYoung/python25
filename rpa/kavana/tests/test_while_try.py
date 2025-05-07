import pytest
from io import BytesIO, TextIOWrapper
import sys
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.exception_registry import ExceptionRegistry

@pytest.fixture(autouse=True)
def reset_exception_registry():
    ExceptionRegistry._exception_handler = None

def test_try_finally_output():
    script = """MAIN
        set count = 0
        while True
            try
                print "try"
            catch
                print "catch"
            finally
                PRINT "try-catch-finally"
            end_try
            PRINT "while"
            rpa wait seconds=0
            set count = count + 1
            if count > 3
                break
            end_if
        end_while
        try
            for i = 0 to 10
                print i
            end_for
        catch
            print "catch"
        finally
            PRINT "try-catch-finally"
        end_try
    ON_EXCEPTION
        PRINT "on_exception handler"
    END_EXCEPTION
    END_MAIN"""

    # 👇 표준 출력 가로채기 - buffer 포함
    byte_stream = BytesIO()
    fake_stdout = TextIOWrapper(byte_stream, encoding='utf-8')
    original_stdout = sys.stdout
    sys.stdout = fake_stdout

    try:
        script_lines = script.strip().split("\n")
        pp_lines = CommandPreprocessor().preprocess(script_lines)
        parser = CommandParser()
        parsed = parser.parse(pp_lines)

        executor = CommandExecutor()
        for command in parsed:
            executor.execute(command)

        sys.stdout.flush()  # flush 버퍼
        output = byte_stream.getvalue().decode("utf-8").strip().split("\n")

        # ✅ 마지막 줄 검증
        assert output[-1].strip() == "try-catch-finally"
    finally:
        sys.stdout = original_stdout  # 복원
