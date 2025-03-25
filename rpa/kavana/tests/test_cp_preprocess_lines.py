import pytest
from lib.core.command_preprocessor import CommandPreprocessor, PreprocessedLine  # 실제 모듈 경로로 수정해야 함

# (✅ 수정된 예제)
@pytest.mark.parametrize(
    "script, expected",
    [
        (
            """MAIN
    SET a = 10
    PRINT "Hello"
END_MAIN
            """,
            [
                PreprocessedLine("MAIN", 1, 1),  # ✅ 1번째 칸에서 시작
                PreprocessedLine("SET a = 10", 2, 5),
                PreprocessedLine('PRINT "Hello"', 3, 5),
                PreprocessedLine("END_MAIN", 4, 1),
            ],
        ),
#         (
#             """MAIN
#     SET text = "This is a \ 
#  long text spanning \
#   multiple lines"
#     PRINT text
# END_MAIN
#             """,
#             [
#                 PreprocessedLine("MAIN", 1, 1),
#                 PreprocessedLine('SET text = "This is a  long text spanning   multiple lines"', 2, 5),  # ✅ a와 long 사이 공백 2개
#                 PreprocessedLine("PRINT text", 4, 5),
#                 PreprocessedLine("END_MAIN", 5, 1),
#             ],
#         ),
    ],
)

def test_command_preprocessor(script, expected):
    """CommandPreprocessor가 정확하게 작동하는지 확인"""
    script_lines = script.split("\n")
    preprocessor = CommandPreprocessor(script_lines)
    result = preprocessor.preprocess()

    assert len(result) == len(expected), f"출력된 줄 수가 예상과 다릅니다. (Got {len(result)}, Expected {len(expected)})"
    for res, exp in zip(result, expected):
        assert res.text == exp.text, f"잘못된 변환 결과: {res.text} (예상: {exp.text})"
        assert res.original_line == exp.original_line, f"잘못된 줄 번호: {res.original_line} (예상: {exp.original_line})"
        assert res.original_column == exp.original_column, f"잘못된 컬럼 위치: {res.original_column} (예상: {exp.original_column})"
