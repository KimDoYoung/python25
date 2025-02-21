import pytest
from lib.core.function_parser import FunctionParser

@pytest.mark.parametrize("expression, expected_pos_args, expected_kw_args", [
    # ✅ 위치 기반 인자 + 키워드 인자 처리 테스트
    ("example_func(a_region, threshold=128, gray=TRUE)", 
     ["a_region"], {"threshold": 128, "gray": True}),  # ✅ "TRUE" → True 변환

    # ✅ 문자열 리터럴 처리 테스트
    ("SUBSTR(\"hello\", 1, 3)", 
     ["hello", 1, 3], {}),  # ✅ 문자열 따옴표 제거

    # ✅ 키워드 인자 포함 테스트
    ("process_data(region1, region2, mode='fast', debug=True)", 
     ["region1", "region2"], {"mode": "'fast'", "debug": True}),  # ✅ "True" → True 변환

    # ✅ NULL 처리 테스트
    ("set_value(name=NULL, age=30)", 
     [], {"name": None, "age": 30}),  # ✅ "NULL" → None 변환

    # ✅ 숫자만 포함된 위치 기반 인자 테스트
    ("my_func(10, 20, 30)", 
     [10, 20, 30], {}),

    # ✅ 빈 함수 호출 테스트
    ("empty_func()", 
     [], {}),  # ✅ 빈 인자 처리
])
def test_function_parser(expression, expected_pos_args, expected_kw_args):
    """
    FunctionParser가 올바르게 위치 기반 인자와 키워드 인자를 구분하는지 테스트.
    """
    parser = FunctionParser(expression)
    pos_args, kw_args = parser.parse_arguments()
    
    assert pos_args == expected_pos_args, f"Expected {expected_pos_args}, but got {pos_args}"
    assert kw_args == expected_kw_args, f"Expected {expected_kw_args}, but got {kw_args}"

def test_invalid_function_syntax():
    """
    괄호가 없는 잘못된 함수 호출을 처리하는지 확인.
    """
    with pytest.raises(ValueError, match="잘못된 함수 호출 형식"):
        FunctionParser("invalid_function").parse_arguments()
    
    with pytest.raises(ValueError, match="잘못된 함수 호출 형식"):
        FunctionParser("missing_paren(").parse_arguments()
    
    with pytest.raises(ValueError, match="잘못된 함수 호출 형식"):
        FunctionParser("no_closing_paren(arg1, arg2").parse_arguments()
