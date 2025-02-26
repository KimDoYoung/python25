import pytest
from lib.core.command_parser import CommandParser
from lib.core.token import Token
from lib.core.datatypes.token_type import TokenType


@pytest.mark.parametrize("line, expected_tokens", [
    # ✅ Boolean 값 테스트
    ("True", [Token(value="True", type=TokenType.BOOLEAN, line=1, column=0)]),
    ("False", [Token(value="False", type=TokenType.BOOLEAN, line=1, column=0)]),
    ("None", [Token(value="None", type=TokenType.NONE, line=1, column=0)]),

    # # ✅ 제어문 키워드 테스트
    ("IF", [Token(value="IF", type=TokenType.IF, line=1, column=0)]),
    ("ELSE", [Token(value="ELSE", type=TokenType.ELSE, line=1, column=0)]),
    ("ELIF", [Token(value="ELIF", type=TokenType.ELIF, line=1, column=0)]),
    ("WHILE", [Token(value="WHILE", type=TokenType.WHILE, line=1, column=0)]),
    ("FOR", [Token(value="FOR", type=TokenType.FOR, line=1, column=0)]),
    ("TO", [Token(value="TO", type=TokenType.TO, line=1, column=0)]),
    ("STEP", [Token(value="STEP", type=TokenType.STEP, line=1, column=0)]),
    ("END_IF", [Token(value="END_IF", type=TokenType.END_IF, line=1, column=0)]),
    ("END_WHILE", [Token(value="END_WHILE", type=TokenType.END_WHILE, line=1, column=0)]),
    ("END_FOR", [Token(value="END_FOR", type=TokenType.END_FOR, line=1, column=0)]),
    
    # ✅ 함수 관련 키워드 테스트
    ("FUNCTION", [Token(value="FUNCTION", type=TokenType.FUNCTION, line=1, column=0)]),
    ("END_FUNCTION", [Token(value="END_FUNCTION", type=TokenType.END_FUNCTION, line=1, column=0)]),
    ("RETURN", [Token(value="RETURN", type=TokenType.RETURN, line=1, column=0)]),
    ("return", [Token(value="return", type=TokenType.RETURN, line=1, column=0)]),

    # ✅ 스크립트 실행 관련 키워드 테스트
    ("INCLUDE", [Token(value="INCLUDE", type=TokenType.INCLUDE, line=1, column=0)]),
    ("LOAD", [Token(value="LOAD", type=TokenType.LOAD, line=1, column=0)]),
    ("MAIN", [Token(value="MAIN", type=TokenType.MAIN, line=1, column=0)]),
    ("END_MAIN", [Token(value="END_MAIN", type=TokenType.END_MAIN, line=1, column=0)]),

    # ✅ 논리 연산자 테스트
    ("AND", [Token(value="AND", type=TokenType.LOGICAL_OPERATOR, line=1, column=0)]),
    ("OR", [Token(value="OR", type=TokenType.LOGICAL_OPERATOR, line=1, column=0)]),
    ("NOT", [Token(value="NOT", type=TokenType.LOGICAL_OPERATOR, line=1, column=0)]),
    ("and", [Token(value="and", type=TokenType.LOGICAL_OPERATOR, line=1, column=0)]),
    ("or", [Token(value="or", type=TokenType.LOGICAL_OPERATOR, line=1, column=0)]),
    ("not", [Token(value="not", type=TokenType.LOGICAL_OPERATOR, line=1, column=0)]),

    # ✅ 루프 제어 키워드 테스트
    ("BREAK", [Token(value="BREAK", type=TokenType.BREAK, line=1, column=0)]),
    ("CONTINUe", [Token(value="CONTINUe", type=TokenType.CONTINUE, line=1, column=0)]),

    # ✅ 데이터 타입 키워드 테스트
    ("POINT", [Token(value="POINT", type=TokenType.POINT, line=1, column=0)]),
    ("REGION", [Token(value="REGION", type=TokenType.REGION, line=1, column=0)]),
    ("RECTANGLE", [Token(value="RECTANGLE", type=TokenType.RECTANGLE, line=1, column=0)]),
    ("IMAGE", [Token(value="IMAGE", type=TokenType.IMAGE, line=1, column=0)]),
    ("WINDOW", [Token(value="WINDOW", type=TokenType.WINDOW, line=1, column=0)]),
    ("APPLICATION", [Token(value="APPLICATION", type=TokenType.APPLICATION, line=1, column=0)]),

    # ✅ 정수 테스트
    ("42", [Token(value="42", type=TokenType.INTEGER, line=1, column=0)]),
    ("1000", [Token(value="1000", type=TokenType.INTEGER, line=1, column=0)]),

    # ✅ 실수 테스트
    ("3.14", [Token(value="3.14", type=TokenType.FLOAT, line=1, column=0)]),
    ("0.99", [Token(value="0.99", type=TokenType.FLOAT, line=1, column=0)]),
    ("100.5", [Token(value="100.5", type=TokenType.FLOAT, line=1, column=0)]),

    # ✅ 식별자 테스트
    ("myVar", [Token(value="myVar", type=TokenType.IDENTIFIER, line=1, column=0)]),
    ("_var123", [Token(value="_var123", type=TokenType.IDENTIFIER, line=1, column=0)]),
    ("$T_1", [Token(value="$T_1", type=TokenType.IDENTIFIER, line=1, column=0)]),

    # ✅ 연산자 테스트
    ("+", [Token(value="+", type=TokenType.OPERATOR, line=1, column=0)]),
    ("-", [Token(value="-", type=TokenType.OPERATOR, line=1, column=0)]),
    ("*", [Token(value="*", type=TokenType.OPERATOR, line=1, column=0)]),
    ("/", [Token(value="/", type=TokenType.OPERATOR, line=1, column=0)]),
    ("=", [Token(value="=", type=TokenType.OPERATOR, line=1, column=0)]),
    ("%", [Token(value="%", type=TokenType.OPERATOR, line=1, column=0)]),

    # ✅ 괄호 및 구두점 테스트
    ("(", [Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=0)]),
    (")", [Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=0)]),
    ("[", [Token(value="[", type=TokenType.LEFT_BRACKET, line=1, column=0)]),
    ("]", [Token(value="]", type=TokenType.RIGHT_BRACKET, line=1, column=0)]),
    (",", [Token(value=",", type=TokenType.COMMA, line=1, column=0)]),


    # # ✅ 변수 할당 테스트
    ("SET x = 10", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=0),
        Token(value="x", type=TokenType.IDENTIFIER, line=1, column=4),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=6),
        Token(value="10", type=TokenType.INTEGER, line=1, column=8),
    ]),


    # # ✅ 연산자 테스트
    ("a + b", [
        Token(value="a", type=TokenType.IDENTIFIER, line=1, column=0),
        Token(value="+", type=TokenType.OPERATOR, line=1, column=2),
        Token(value="b", type=TokenType.IDENTIFIER, line=1, column=4),
    ]),

    # # ✅ 괄호 테스트
    ("( x )", [
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=0),
        Token(value="x", type=TokenType.IDENTIFIER, line=1, column=2),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=4),
    ]),

    # # ✅ 데이터 타입 테스트 (객체 생성)
    ("SET p1 = Point(10,20)", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=0),
        Token(value="p1", type=TokenType.IDENTIFIER, line=1, column=4),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=7),
        Token(value="Point", type=TokenType.POINT, line=1, column=9),
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=14),
        Token(value="10", type=TokenType.INTEGER, line=1, column=15),
        Token(value=",", type=TokenType.COMMA, line=1, column=17),
        Token(value="20", type=TokenType.INTEGER, line=1, column=18),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=20),
    ]),

    ("SET region1 = Region(0,0,100,100)", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=0),
        Token(value="region1", type=TokenType.IDENTIFIER, line=1, column=4),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=12),
        Token(value="Region", type=TokenType.REGION, line=1, column=14),
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=20),
        Token(value="0", type=TokenType.INTEGER, line=1, column=21),
        Token(value=",", type=TokenType.COMMA, line=1, column=22),
        Token(value="0", type=TokenType.INTEGER, line=1, column=23),
        Token(value=",", type=TokenType.COMMA, line=1, column=24),
        Token(value="100", type=TokenType.INTEGER, line=1, column=25),
        Token(value=",", type=TokenType.COMMA, line=1, column=28),  
        Token(value="100", type=TokenType.INTEGER, line=1, column=29),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=32),
    ]),



    # # ✅ 리스트 표현식 테스트
    ("SET numbers = [1, 2, 3]", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=0),
        Token(value="numbers", type=TokenType.IDENTIFIER, line=1, column=4),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=12),
        Token(value="[", type=TokenType.LEFT_BRACKET, line=1, column=14),
        Token(value="1", type=TokenType.INTEGER, line=1, column=15),
        Token(value=",", type=TokenType.COMMA, line=1, column=16),
        Token(value="2", type=TokenType.INTEGER, line=1, column=18),
        Token(value=",", type=TokenType.COMMA, line=1, column=19),
        Token(value="3", type=TokenType.INTEGER, line=1, column=21),
        Token(value="]", type=TokenType.RIGHT_BRACKET, line=1, column=22),
    ]),

    # # ✅ 함수 호출 테스트
    ("my_function(10, 20)", [
        Token(value="my_function", type=TokenType.IDENTIFIER, line=1, column=0),
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=11),
        Token(value="10", type=TokenType.INTEGER, line=1, column=12),
        Token(value=",", type=TokenType.COMMA, line=1, column=14),
        Token(value="20", type=TokenType.INTEGER, line=1, column=16),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=18),
    ]),

])
def test_tokenize(line, expected_tokens):
    """✅ `tokenize()` 함수가 올바르게 동작하는지 검증"""
    tokens = CommandParser.tokenize(line, line_num=1)
    
    assert len(tokens) == len(expected_tokens), f"Expected {len(expected_tokens)} tokens, but got {len(tokens)}"

    for i in range(len(tokens)):
        assert tokens[i].value == expected_tokens[i].value, f"Mismatch at index {i}: expected '{expected_tokens[i].value}', got '{tokens[i].value}'"
        assert tokens[i].type == expected_tokens[i].type, f"Type mismatch at index {i}: expected '{expected_tokens[i].type}', got '{tokens[i].type}'"
        assert tokens[i].line == expected_tokens[i].line, f"Line number mismatch at index {i}: expected '{expected_tokens[i].line}', got '{tokens[i].line}'"
        assert tokens[i].column == expected_tokens[i].column, f"Column mismatch at index {i}: expected '{expected_tokens[i].column}', got '{tokens[i].column}'"
