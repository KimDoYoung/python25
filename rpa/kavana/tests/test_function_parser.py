import pytest
from lib.core.function_parser import FunctionParser, FunctionRegistry  # your_module은 FunctionParser가 정의된 모듈입니다.

# 테스트 케이스
test_cases = [
    # 경우1: 일반적인 함수 호출
    (["my_func", "(", "3", "4", ")"], ["my_func(3,4)"]),
    # 경우2: 괄호가 없는 함수 호출
    (["my_func", "3", "4"], ["my_func(3,4)"]),
    # 경우3: 중첩된 괄호가 있는 함수 호출
    (["my_func", "(", "(", "3", ")", "(", "4", ")", ")"], ["my_func((3),(4))"]),
    # 경우4: 중첩된 함수 호출
    (["my_func", "(", "length", "(", '"abc"', ")", "4", ")"], ["my_func(length(\"abc\"),4)"]),
    # 경우5: 중첩된 함수 호출과 복잡한 토큰 형식
    (["my_func", "substr", "(", '"123"', "1", "2", ")", "4"], ["my_func(substr(\"123\",1,2),4)"]),
    # 경우6: 빈 인자
    (["my_func", "(", ")"], ["my_func()"]),
    # 경우7: 단일 인자
    (["my_func", "(", "42", ")"], ["my_func(42)"]),
    # 경우8: 중첩된 함수 호출이 없는 경우
    (["my_func", "(", "1", "2", "3", ")"], ["my_func(1,2,3)"]),
    # 경우9: 함수 이름만 있는 경우
    (["my_func"], ["my_func"]),
    # 경우10: 중첩된 함수 호출이 여러 개 있는 경우
    (["my_func", "(", "length", "(", '"abc"', ")", "substr", "(", '"123"', "1", "2", ")", ")"], ["my_func(length(\"abc\"),substr(\"123\",1,2))"]),
]

# pytest 파라미터화
@pytest.mark.parametrize("tokens, expected", test_cases)
def test_function_parser(tokens, expected):
    # FunctionParser를 사용하여 토큰 파싱
    result = FunctionParser.parse(tokens)
    # 결과 검증
    assert result == expected, f"Expected {expected}, but got {result}"

# 오류 케이스 테스트
def test_function_parser_error():
    # 인자 개수가 맞지 않는 경우
    tokens = ["my_func", "(", "1", ")"]
    func, arg_count = FunctionRegistry.get_function("my_func")
    if func:
        with pytest.raises(ValueError) as exc_info:
            FunctionParser.parse(tokens)
        assert "expects" in str(exc_info.value), "Expected ValueError for incorrect argument count"