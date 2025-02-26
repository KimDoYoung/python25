import pytest
from lib.core.command_parser import CommandParser

@pytest.mark.parametrize("input_line, expected_tokens", [
    # ✅ 기본 명령어 테스트
    ("LENGTH(\"abc\")", ["LENGTH", '"abc"']),
    
    # ✅ 기본 명령어 테스트
    ("PRINT Hello", ["PRINT", "Hello"]),
    ("SET x = 10", ["SET", "x", "=", "10"]),

    # ✅ 따옴표 포함된 문자열 테스트
    ('PRINT "Hello World"', ["PRINT", '"Hello World"']),
    ('SET name = "홍길동"', ["SET", "name", "=", '"홍길동"']),

    # ✅ PRINT("hello {name}") 테스트
    ('PRINT("hello {name}")', ["PRINT", '"hello {name}"']),
    ('PRINT "hello {name}"', ["PRINT", '"hello {name}"']),
    ('PRINT("Age: {age}")', ["PRINT", '"Age: {age}"']),

    # ✅ 여러 개의 인자를 처리하는 경우
    ('PRINT("hello", "world")', ["PRINT", '"hello"', '"world"']),
    ('PRINT("Name:", name, "Age:", age)', ["PRINT", '"Name:"', "name", '"Age:"', "age"]),

    # ✅ 특수 문자 포함
    ('PRINT("Hello\\nWorld")', ["PRINT", '"Hello\\nWorld"']),
    ('PRINT("Tabbed\\tText")', ["PRINT", '"Tabbed\\tText"']),

    # ✅ 함수 형태가 아닌 일반적인 명령어
    ("FUNCTION myFunc", ["FUNCTION", "myFunc"]),
    ("FUNCTION myFunc a, b", ["FUNCTION", "myFunc","a","b"]),
    ("FUNCTION myFunc (a, b)", ["FUNCTION", "myFunc","a","b"]),
    ("END_FUNCTION", ["END_FUNCTION"]),
    ("a > 1", ["a", ">", "1"]),
    ("a < 1", ["a", "<", "1"]),
    ("a <= 1", ["a", "<=", "1"]),
    ("a >= 1", ["a", ">=", "1"]),
    ("a == 1", ["a", "==", "1"]),
    ("a != 1", ["a", "!=", "1"]),
    ("a + 1", ["a", "+", "1"]),
    ("a - 1", ["a", "-", "1"]),
    ("a * 1", ["a", "*", "1"]),
    ("a / 1", ["a", "/", "1"]),
    ("a % 1", ["a", "%", "1"]),
    ("a AND b", ["a", "AND", "b"]),
    ("a OR b", ["a", "OR", "b"]),
    ("a NOT b", ["a", "NOT", "b"]),
    ("a = b", ["a", "=", "b"]),
    ("a > b", ["a", ">", "b"]),
    ("a < b", ["a", "<", "b"]),
    ("a >= b", ["a", ">=", "b"]),
    ("a <= b", ["a", "<=", "b"]),
    
])
def test_tokenize(input_line, expected_tokens):
    """CommandParser의 tokenize()가 올바르게 동작하는지 검증"""
    tokens = CommandParser.tokenize(input_line)
    assert tokens == expected_tokens, f"Expected {expected_tokens}, but got {tokens}"

if __name__ == "__main__":
    pytest.main()
