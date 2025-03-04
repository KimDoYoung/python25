from enum import Enum

class TokenType(Enum):
    UNKNOWN = "UNKNOWN"
    GLOBAL = "GLOBAL"
    # 기존 타입
    NONE = "NONE" # None
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN" # True, False
    DATE = "DATE"
    IDENTIFIER = "IDENTIFIER" 
    OPERATOR = "OPERATOR" # +, -, *, /, ==, !=, <, >, <=, >=, AND, OR
    LOGICAL_OPERATOR = "LOGICAL_OPERATOR" # AND, OR, NOT
    COMMA = "COMMA" # ,
    LEFT_PAREN = "LEFT_PAREN" # (
    RIGHT_PAREN = "RIGHT_PAREN" # )
    LEFT_BRACKET = "LEFT_BRACKET"    # [ 
    RIGHT_BRACKET = "RIGHT_BRACKET"  # ]
    LIST = "LIST" # LIST

    # ✅ 사용자 정의 데이터 타입 (POINT, REGION 등)
    POINT = "POINT"
    REGION = "REGION"
    RECTANGLE = "RECTANGLE"
    IMAGE = "IMAGE"
    WINDOW = "WINDOW"
    APPLICATION = "APPLICATION"


    # ✅ 제어문 키워드
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF"
    END_IF = "END_IF"
    FOR = "FOR"
    TO = "TO"
    STEP = "STEP"
    END_FOR = "END_FOR"
    WHILE = "WHILE"
    END_WHILE = "END_WHILE"

    # ✅ 함수 및 시스템 명령어
    FUNCTION = "FUNCTION"
    END_FUNCTION = "END_FUNCTION"
    RETURN = "RETURN"
    INCLUDE = "INCLUDE"
    LOAD = "LOAD"

    # ✅ 루프 제어문
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"

    # ✅ 프로그램 실행 관련
    MAIN = "MAIN"
    END_MAIN = "END_MAIN"
    EOF = "EOF"
