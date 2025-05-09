from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List,  Optional
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import  KavanaDataType, NoneType, String
from lib.core.datatypes.array import Array
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.token_type import TokenType

class TokenStatus(str, Enum):
    PARSED = "Parsed"
    EVALUATED = "Evaluated"

@dataclass
class Token:
    ''' 토큰 클래스 '''
    data: KavanaDataType
    type: TokenType  # ✅ 토큰 유형
    line: Optional[int] = None  # ✅ 기본값을 None으로 설정
    column: Optional[int] = None  # ✅ 기본값을 None으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        return f"Token(data={self.data.value}, type={self.type}, line={self.line}, column={self.column})"

# 타입 정의
Express = List[Token]

@dataclass
class NoneToken(Token):
    def __init__(self):
        super().__init__(data=NoneType(), type=TokenType.NONE)

@dataclass
class StringToken(Token):
    is_raw: bool = False
    is_formatted: bool = False
    expressions: Optional[List[List[Token]]] = None  # f-string인 경우

@dataclass
class FunctionToken(Token):
    """✅ 함수 호출을 표현하는 토큰"""
    function_name: str =""  # ✅ 함수 이름
    # arguments: List[List[Token]] = field(default_factory=list) # 함수 인자 목록
    arguments: List[Express] = field(default_factory=list) # 함수 인자 목록
    data: KavanaDataType = field(init=False)  # ✅ `data`는 function_name을 저장
    type: TokenType = field(default=TokenType.FUNCTION, init=False)  # ✅ `type`을 FUNCTION으로 고정

    def __post_init__(self):
        object.__setattr__(self, "data", String(self.function_name))  # ✅ `data`를 function_name으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        arg_str = ", ".join([repr(arg) for arg in self.arguments])
        return f"FunctionToken(function_name={self.function_name}, arguments=[{arg_str}], line={self.line}, column={self.column})"

@dataclass
class YmdTimeToken(Token):
    """✅ YmdTime 함수 호출을 표현하는 토큰"""
    arguments: List[int] = field(default_factory=list)  # ✅ `init=True`로 변경하여 생성자에서 받음
    data: YmdTime = field(init=False)  # ✅ `data`는 `YmdTime` 객체
    type: TokenType = field(default=TokenType.YMDTIME, init=False)  # ✅ 고정된 타입

    def __post_init__(self):
        values = self.arguments[:]  # 리스트 복사하여 불변성 유지

        # ✅ 인자가 3개일 경우 기본 시간(00:00:00) 추가
        if len(values) == 3:
            values = values + [0, 0, 0]
        elif len(values) != 6:
            raise ValueError(f"YmdTime 인자 개수 오류: {values}")

        object.__setattr__(self, "data", YmdTime(*values))  # ✅ `data`를 YmdTime 객체로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        arg_str = ", ".join(map(str, self.arguments))
        return f"YmdTimeToken(arguments=[{arg_str}], data={self.data}, line={self.line}, column={self.column})"

@dataclass
class YmdToken(Token):
    """✅ Ymd 함수 호출을 표현하는 토큰"""
    arguments: List[int] = field(default_factory=list)  # ✅ 생성자에서 리스트 형태로 받음
    data: Ymd = field(init=False)  # ✅ `data`는 `Ymd` 객체
    type: TokenType = field(default=TokenType.YMD, init=False)  # ✅ `type`을 YMD로 고정

    def __post_init__(self):
        values = self.arguments[:]  # 리스트 복사하여 불변성 유지

        # ✅ `Ymd`는 3개의 인자만 허용
        if len(values) != 3:
            raise ValueError(f"Ymd 인자 개수 오류: {values} (필수: 3개)")

        object.__setattr__(self, "data", Ymd(*values))  # ✅ `data`를 Ymd 객체로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        arg_str = ", ".join(map(str, self.arguments))
        return f"YmdToken(arguments=[{arg_str}], data={self.data}, line={self.line}, column={self.column})"


@dataclass
class ArrayToken(Token):
    ''' 리스트 표현식을 표현하는 토큰 '''
    data: Array  # ✅ `data`는 ListType 타입
    type: TokenType = field(default=TokenType.ARRAY, init=False)  # ✅ `type`을 LIST로 고정
    element_type: TokenType = field(default=TokenType.UNKNOWN)  # 요소의 토큰 타입
    element_expresses: List[List[Token]] = field(default_factory=list)  # 각 요소의 표현 리스트
    status : TokenStatus = TokenStatus.PARSED  # ✅ 기본값을 "Parsed"로 설정

    def __post_init__(self):
        if not isinstance(self.data, Array):
            raise TypeError("ListExToken must contain a ListType")

@dataclass
class HashMapToken(Token):
    """HashMap 표현식을 나타내는 토큰"""
    data: HashMap  # ✅ 실제 HashMap 데이터
    type: TokenType = field(default=TokenType.HASH_MAP, init=False)  # ✅ 고정 타입
    key_express_map: Dict[str|int, List[Token]] = field(default_factory=dict)  # 각 key에 대응하는 value 표현식
    status : TokenStatus = TokenStatus.PARSED  # ✅ 기본값을 "Parsed"로 설정

    def __post_init__(self):
        if not isinstance(self.data, HashMap):
            raise TypeError("HashMapToken must contain a HashMap instance")


@dataclass
class AccessIndexToken(Token):
    """✅ 리스트나 해시맵에 접근하기 위한 인덱스 토큰"""
    index_expresses: List[Express] = field(default_factory=list)  # ✅ 중첩 인덱스 표현
    data: String  # ✅ `data`는 String 타입 (필수)
    type: TokenType = TokenType.ACCESS_INDEX  # ✅ 기본값 설정

    def __post_init__(self):
        if not isinstance(self.data, String):
            raise TypeError(f"data 필드는 String 타입이어야 합니다. (현재 타입: {type(self.data)})")

    def __repr__(self) -> str:
        express_str = " -> ".join(
            "[" + ", ".join(repr(tok) for tok in expr) + "]"
            for expr in self.index_expresses
        ) if self.index_expresses else "None"

        return (f"AccessIndexToken("
                f"index_expresses={express_str}, "
                f"data={repr(self.data)}, "
                f"type={self.type})")
    
