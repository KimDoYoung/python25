# tests/test_function_parser.py
import pytest
from lib.core.function_parser import FunctionParser
from .helper_func import get_raw_tokens
from lib.core.token import FunctionToken
from lib.core.token_type import TokenType

def test_make_function_token_basic_function_call():
    tokens = get_raw_tokens("my_func(1, 2)")

    # 함수 호출 시작 인덱스를 찾음
    start_index = 0
    for i, t in enumerate(tokens):
        if t.type == TokenType.IDENTIFIER:
            start_index = i
            break

    func_token, next_index = FunctionParser.make_function_token(tokens, start_index)

    assert isinstance(func_token, FunctionToken)
    assert func_token.function_name == "MY_FUNC"
    assert len(func_token.arguments) == 2
    assert all(isinstance(arg, list) for arg in func_token.arguments)
    assert next_index > start_index

def test_make_function_token_nested_args():
    tokens = get_raw_tokens("my_func(a, inner_func(1, 2))")

    start_index = 0
    for i, t in enumerate(tokens):
        if t.type == TokenType.IDENTIFIER:
            start_index = i
            break

    func_token, next_index = FunctionParser.make_function_token(tokens, start_index)

    assert func_token.function_name == "MY_FUNC"
    assert len(func_token.arguments) == 2
    # 중첩 함수가 있는 두 번째 인자도 리스트여야 함
    assert any(tok.type == TokenType.IDENTIFIER and tok.data.value.upper() == "INNER_FUNC"
               for tok in func_token.arguments[1])

