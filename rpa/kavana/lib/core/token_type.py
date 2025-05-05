from enum import Enum

class TokenType(Enum):
    # COMMAND
    ACCESS_INDEX = "LIST_INDEX"
    # MAP_KEY = "MAP_KEY"
    # COMMAND = "COMMAND"
    
    UNKNOWN = "UNKNOWN"
    GLOBAL = "GLOBAL"
    # 기존 타입
    NONE = "NONE" # None
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    # RAW_STRING = "RAW_STRING"
    BOOLEAN = "BOOLEAN" # True, False
    YMDTIME = "YMDTIME"
    YMD = "YMD"
    IDENTIFIER = "IDENTIFIER" 
    OPERATOR = "OPERATOR" # +, -, *, /, ==, !=, <, >, <=, >=, AND, OR
    LOGICAL_OPERATOR = "LOGICAL_OPERATOR" # AND, OR, NOT
    COMMA = "," # ,
    ASSIGN = "=" # =
    LEFT_PAREN = "(" # (
    RIGHT_PAREN = ")" # )
    LEFT_BRACKET = "["    # [ 
    RIGHT_BRACKET = "]"  # ]
    LEFT_BRACE = "{" # {
    RIGHT_BRACE = "}" # }
    ARRAY = "ARRAY" # ARRAY
    HASH_MAP = "HASHMAP" # HASHMAP
    COLON = ":" # :

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
    IN = "IN"
    END_FOR = "END_FOR"
    WHILE = "WHILE"
    END_WHILE = "END_WHILE"

    # ✅ 함수 및 시스템 명령어
    FUNCTION = "FUNCTION"
    END_FUNCTION = "END_FUNCTION"
    RETURN = "RETURN"
    INCLUDE = "INCLUDE"
    LOAD_ENV = "LOAD_ENV"

    # ✅ 루프 제어문
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"

    # ✅ 프로그램 실행 관련
    MAIN = "MAIN"
    END_MAIN = "END_MAIN"
    # EOF = "EOF"

    CUSTOM_TYPE = "CUSTOM_TYPE" # 사용자 정의 데이터 타입
    