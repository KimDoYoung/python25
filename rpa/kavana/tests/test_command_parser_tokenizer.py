import pytest
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.token import Token
from lib.core.datatypes.token_type import TokenType


@pytest.mark.parametrize("line, expected_tokens", [
    # ✅ String
    ("\"ABC\"", [Token(value="ABC", type=TokenType.STRING, line=1, column=1)]),
    ("\"Hello World\"", [Token(value="Hello World", type=TokenType.STRING, line=1, column=1)]),
    ("\"12345\"", [Token(value="12345", type=TokenType.STRING, line=1, column=1)]),
    ("\"한글 테스트\"", [Token(value="한글 테스트", type=TokenType.STRING, line=1, column=1)]),
    ("\"escaped \\\"quote\\\"\"", [Token(value="escaped \"quote\"", type=TokenType.STRING, line=1, column=1)]),
    ("\"newline\\n\"", [Token(value="newline\n", type=TokenType.STRING, line=1, column=1)]),
    ("\"tab\\tspace\"", [Token(value="tab\tspace", type=TokenType.STRING, line=1, column=1)]),
    ("\"\"", [Token(value="", type=TokenType.STRING, line=1, column=1)]),  # ✅ 빈 문자열

    # ✅ Boolean 값 테스트
    ("True", [Token(value="True", type=TokenType.BOOLEAN, line=1, column=1)]),
    ("False", [Token(value="False", type=TokenType.BOOLEAN, line=1, column=1)]),
    ("None", [Token(value="None", type=TokenType.NONE, line=1, column=1)]),

    # ✅ 제어문 키워드 테스트
    ("IF", [Token(value="IF", type=TokenType.IF, line=1, column=1)]),
    ("ELSE", [Token(value="ELSE", type=TokenType.ELSE, line=1, column=1)]),
    ("ELIF", [Token(value="ELIF", type=TokenType.ELIF, line=1, column=1)]),
    ("WHILE", [Token(value="WHILE", type=TokenType.WHILE, line=1, column=1)]),
    ("FOR", [Token(value="FOR", type=TokenType.FOR, line=1, column=1)]),
    ("TO", [Token(value="TO", type=TokenType.TO, line=1, column=1)]),
    ("STEP", [Token(value="STEP", type=TokenType.STEP, line=1, column=1)]),
    ("END_IF", [Token(value="END_IF", type=TokenType.END_IF, line=1, column=1)]),
    ("END_WHILE", [Token(value="END_WHILE", type=TokenType.END_WHILE, line=1, column=1)]),
    ("END_FOR", [Token(value="END_FOR", type=TokenType.END_FOR, line=1, column=1)]),
    
    # ✅ 함수 관련 키워드 테스트
    ("FUNCTION", [Token(value="FUNCTION", type=TokenType.FUNCTION, line=1, column=1)]),
    ("END_FUNCTION", [Token(value="END_FUNCTION", type=TokenType.END_FUNCTION, line=1, column=1)]),
    ("RETURN", [Token(value="RETURN", type=TokenType.RETURN, line=1, column=1)]),
    ("return", [Token(value="return", type=TokenType.RETURN, line=1, column=1)]),

    # ✅ 스크립트 실행 관련 키워드 테스트
    ("INCLUDE", [Token(value="INCLUDE", type=TokenType.INCLUDE, line=1, column=1)]),
    ("LOAD", [Token(value="LOAD", type=TokenType.LOAD, line=1, column=1)]),
    ("MAIN", [Token(value="MAIN", type=TokenType.MAIN, line=1, column=1)]),
    ("END_MAIN", [Token(value="END_MAIN", type=TokenType.END_MAIN, line=1, column=1)]),

    # ✅ 논리 연산자 테스트
    ("AND", [Token(value="AND", type=TokenType.LOGICAL_OPERATOR, line=1, column=1)]),
    ("OR", [Token(value="OR", type=TokenType.LOGICAL_OPERATOR, line=1, column=1)]),
    ("NOT", [Token(value="NOT", type=TokenType.LOGICAL_OPERATOR, line=1, column=1)]),
    ("and", [Token(value="and", type=TokenType.LOGICAL_OPERATOR, line=1, column=1)]),
    ("or", [Token(value="or", type=TokenType.LOGICAL_OPERATOR, line=1, column=1)]),
    ("not", [Token(value="not", type=TokenType.LOGICAL_OPERATOR, line=1, column=1)]),

    # ✅ 루프 제어 키워드 테스트
    ("BREAK", [Token(value="BREAK", type=TokenType.BREAK, line=1, column=1)]),
    ("CONTINUe", [Token(value="CONTINUe", type=TokenType.CONTINUE, line=1, column=1)]),

    # ✅ 데이터 타입 키워드 테스트
    ("POINT", [Token(value="POINT", type=TokenType.POINT, line=1, column=1)]),
    ("REGION", [Token(value="REGION", type=TokenType.REGION, line=1, column=1)]),
    ("RECTANGLE", [Token(value="RECTANGLE", type=TokenType.RECTANGLE, line=1, column=1)]),
    ("IMAGE", [Token(value="IMAGE", type=TokenType.IMAGE, line=1, column=1)]),
    ("WINDOW", [Token(value="WINDOW", type=TokenType.WINDOW, line=1, column=1)]),
    ("APPLICATION", [Token(value="APPLICATION", type=TokenType.APPLICATION, line=1, column=1)]),

    # ✅ 정수 테스트
    ("42", [Token(value="42", type=TokenType.INTEGER, line=1, column=1)]),
    ("1000", [Token(value="1000", type=TokenType.INTEGER, line=1, column=1)]),

    # ✅ 실수 테스트
    ("3.14", [Token(value="3.14", type=TokenType.FLOAT, line=1, column=1)]),
    ("0.99", [Token(value="0.99", type=TokenType.FLOAT, line=1, column=1)]),
    ("100.5", [Token(value="100.5", type=TokenType.FLOAT, line=1, column=1)]),

    # ✅ 식별자 테스트
    ("myVar", [Token(value="myVar", type=TokenType.IDENTIFIER, line=1, column=1)]),
    ("_var123", [Token(value="_var123", type=TokenType.IDENTIFIER, line=1, column=1)]),
    ("$T_1", [Token(value="$T_1", type=TokenType.IDENTIFIER, line=1, column=1)]),

    # ✅ 연산자 테스트
    ("+", [Token(value="+", type=TokenType.OPERATOR, line=1, column=1)]),
    ("-", [Token(value="-", type=TokenType.OPERATOR, line=1, column=1)]),
    ("*", [Token(value="*", type=TokenType.OPERATOR, line=1, column=1)]),
    ("/", [Token(value="/", type=TokenType.OPERATOR, line=1, column=1)]),
    ("=", [Token(value="=", type=TokenType.OPERATOR, line=1, column=1)]),
    ("%", [Token(value="%", type=TokenType.OPERATOR, line=1, column=1)]),

    # ✅ 괄호 및 구두점 테스트
    ("(", [Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=1)]),
    (")", [Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=1)]),
    ("[", [Token(value="[", type=TokenType.LEFT_BRACKET, line=1, column=1)]),
    ("]", [Token(value="]", type=TokenType.RIGHT_BRACKET, line=1, column=1)]),
    (",", [Token(value=",", type=TokenType.COMMA, line=1, column=1)]),

    # ✅ 변수 할당 테스트
    ("SET x = 10", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=1),
        Token(value="x", type=TokenType.IDENTIFIER, line=1, column=5),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=7),
        Token(value="10", type=TokenType.INTEGER, line=1, column=9),
    ]),


    # ✅ 연산자 테스트
    ("a + b", [
        Token(value="a", type=TokenType.IDENTIFIER, line=1, column=1),
        Token(value="+", type=TokenType.OPERATOR, line=1, column=3),
        Token(value="b", type=TokenType.IDENTIFIER, line=1, column=5),
    ]),

    # ✅ 괄호 테스트
    ("( x )", [
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=1),
        Token(value="x", type=TokenType.IDENTIFIER, line=1, column=3),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=5),
    ]),

    # ✅ 데이터 타입 테스트 (객체 생성)
    ("SET p1 = Point(10,20)", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=1),
        Token(value="p1", type=TokenType.IDENTIFIER, line=1, column=5),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=8),
        Token(value="Point", type=TokenType.POINT, line=1, column=10),
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=15),
        Token(value="10", type=TokenType.INTEGER, line=1, column=16),
        Token(value=",", type=TokenType.COMMA, line=1, column=18),
        Token(value="20", type=TokenType.INTEGER, line=1, column=19),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=21),
    ]),

    ("SET region1 = Region(0,0,100,100)", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=1),
        Token(value="region1", type=TokenType.IDENTIFIER, line=1, column=5),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=13),
        Token(value="Region", type=TokenType.REGION, line=1, column=15),
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=21),
        Token(value="0", type=TokenType.INTEGER, line=1, column=22),
        Token(value=",", type=TokenType.COMMA, line=1, column=23),
        Token(value="0", type=TokenType.INTEGER, line=1, column=24),
        Token(value=",", type=TokenType.COMMA, line=1, column=25),
        Token(value="100", type=TokenType.INTEGER, line=1, column=26),
        Token(value=",", type=TokenType.COMMA, line=1, column=29),  
        Token(value="100", type=TokenType.INTEGER, line=1, column=30),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=33),
    ]),


    # ✅ 리스트 표현식 테스트
    ("SET numbers = [1, 2, 3]", [
        Token(value="SET", type=TokenType.IDENTIFIER, line=1, column=1),
        Token(value="numbers", type=TokenType.IDENTIFIER, line=1, column=5),
        Token(value="=", type=TokenType.OPERATOR, line=1, column=13),
        Token(value="[", type=TokenType.LEFT_BRACKET, line=1, column=15),
        Token(value="1", type=TokenType.INTEGER, line=1, column=16),
        Token(value=",", type=TokenType.COMMA, line=1, column=17),
        Token(value="2", type=TokenType.INTEGER, line=1, column=19),
        Token(value=",", type=TokenType.COMMA, line=1, column=20),
        Token(value="3", type=TokenType.INTEGER, line=1, column=22),
        Token(value="]", type=TokenType.RIGHT_BRACKET, line=1, column=23),
    ]),

    # ✅ 함수 호출 테스트
    ("my_function(10, 20)", [
        Token(value="my_function", type=TokenType.IDENTIFIER, line=1, column=1),
        Token(value="(", type=TokenType.LEFT_PAREN, line=1, column=12),
        Token(value="10", type=TokenType.INTEGER, line=1, column=13),
        Token(value=",", type=TokenType.COMMA, line=1, column=15),
        Token(value="20", type=TokenType.INTEGER, line=1, column=17),
        Token(value=")", type=TokenType.RIGHT_PAREN, line=1, column=19),
    ]),


])
def test_tokenize(line, expected_tokens):
    """✅ `tokenize()` 함수가 올바르게 동작하는지 검증"""

    preProcesor = CommandPreprocessor([line])
    ppLines = preProcesor.preprocess()
    tokens = CommandParser.tokenize(ppLines[0])
    
    assert len(tokens) == len(expected_tokens), f"Expected {len(expected_tokens)} tokens, but got {len(tokens)}"

    for i in range(len(tokens)):
        assert tokens[i].value == expected_tokens[i].value, f"Mismatch at index {i}: expected '{expected_tokens[i].value}', got '{tokens[i].value}'"
        assert tokens[i].type == expected_tokens[i].type, f"Type mismatch at index {i}: expected '{expected_tokens[i].type}', got '{tokens[i].type}'"
        assert tokens[i].line == expected_tokens[i].line, f"Line number mismatch at index {i}: expected '{expected_tokens[i].line}', got '{tokens[i].line}'"
        assert tokens[i].column == expected_tokens[i].column, f"Column mismatch at index {i}: expected '{expected_tokens[i].column}', got '{tokens[i].column}'"
