import pytest
from lib.core.function_parser import FunctionParser, FunctionRegistry

# 테스트 전에 my_func를 등록하는 fixture
@pytest.fixture(autouse=True)
def register_my_func():
    FunctionRegistry.register_function('my_func', ['a', 'b'], 'print a')

# 테스트 케이스
test_cases = [
    # 경우1: 일반적인 함수 호출
    (["my_func", "(", "3", "4", ")"], ["MY_FUNC(3,4)"]),
    # 경우2: 괄호가 없는 함수 호출
    (["my_func", "3", "4"], ["MY_FUNC(3,4)"]),
    # 경우3: 중첩된 괄호가 있는 함수 호출
    (["my_func", "(", "(", "3", ")", "(", "4", ")", ")"], ["MY_FUNC((3),(4))"]),
    # 경우4: 중첩된 함수 호출
    (["my_func", "(", "length", "(", '"abc"', ")", "4", ")"], ["MY_FUNC(LENGTH(\"abc\"),4)"]),
    # 경우5: 중첩된 함수 호출과 복잡한 토큰 형식
    (["my_func", "substr", "(", '"123"', "1", "2", ")", "4"], ["MY_FUNC(SUBSTR(\"123\",1,2),4)"]),
    # 경우6: 빈 인자
    (["my_func", "(", ")"], ["MY_FUNC()"]),
    # 경우7: 단일 인자
    (["my_func", "(", "42", ")"], ["MY_FUNC(42)"]),
    # 경우8: 중첩된 함수 호출이 없는 경우
    (["my_func", "(", "1", "2", "3", ")"], ["MY_FUNC(1,2,3)"]),
    # 경우9: 함수 이름만 있는 경우
    (["my_func"], ["MY_FUNC()"]),
    # 경우10: 중첩된 함수 호출이 여러 개 있는 경우
    (["my_func", "(", "length", "(", '"abc"', ")", "substr", "(", '"123"', "1", "2", ")", ")"], ["MY_FUNC(LENGTH(\"abc\"),SUBSTR(\"123\",1,2))"]),
]

# pytest 파라미터화
@pytest.mark.parametrize("tokens, expected", test_cases)
def test_function_parser(tokens, expected):
    # FunctionRegistry에서 함수 정보 가져오기
    func_name = tokens[0].upper()
    func, arg_count = FunctionRegistry.get_function(func_name)
    
    # FunctionParser를 사용하여 토큰 파싱
    if func is not None:
        result, _ = FunctionParser._parse_function_call(tokens, 0, None, arg_count)
        assert [result] == expected, f"Expected {expected}, but got {[result]}"
    else:
        # 함수가 등록되지 않은 경우
        assert tokens == expected, f"Expected {expected}, but got {tokens}"

