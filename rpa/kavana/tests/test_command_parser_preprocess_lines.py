import pytest
from lib.core.command_parser import CommandParser

@pytest.mark.parametrize("script_lines, remove_comments, expected_lines", [
    # ✅ 1. 주석이 삭제되는지 확인
    (["SET a = 11 // 주석입니다"], True, ["SET a = 11"]),  

    # ✅ 2. `--pretty` 옵션일 때 주석이 유지되는지 확인
    (["SET a = 12 // 주석입니다"], False, ["SET a = 12 // 주석입니다"]),  

    # ✅ 3. `\t`가 스페이스 4개로 변환되는지 확인 (들여쓰기 부분만)
    (["\tSET a = 13"], True, ["    SET a = 13"]),  

    # ✅ 4. 문자열 내부의 `\t`는 변환되지 않는지 확인
    (['PRINT "Hello\tWorld"'], True, ['PRINT "Hello\tWorld"']),  

    # ✅ 5. 멀티라인(`\`)이 올바르게 연결되는지 확인
    (["SET a = 14 \\", "    + 5"], True, ["SET a = 14 + 5"]),  
])
def test_preprocess_lines(script_lines, remove_comments, expected_lines):
    """✅ `preprocess_lines()`가 올바르게 동작하는지 검증"""
    parser = CommandParser(script_lines)
    processed_lines = parser.preprocess_lines(remove_comments=remove_comments)
    
    assert processed_lines == expected_lines, f"Expected {expected_lines}, but got {processed_lines}"
