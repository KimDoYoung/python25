from dataclasses import dataclass, field
from typing import List, Literal, Optional
from lib.core.datatypes.kavana_datatype import KavanaDataType, String
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.token_type import TokenType

@dataclass
class Token:
    ''' 토큰 클래스 '''
    data: KavanaDataType
    type: TokenType  # ✅ 토큰 유형
    line: Optional[int] = None  # ✅ 기본값을 None으로 설정
    column: Optional[int] = None  # ✅ 기본값을 None으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        return f"Token(data={self.data}, type={self.type}, line={self.line}, column={self.column})"

@dataclass
class FunctionToken(Token):
    """✅ 함수 호출을 표현하는 토큰"""
    function_name: str =""  # ✅ 함수 이름
    arguments: List[List[Token]] = field(default_factory=list) # 함수 인자 목록
    data: KavanaDataType = field(init=False)  # ✅ `data`는 function_name을 저장
    type: TokenType = field(default=TokenType.FUNCTION, init=False)  # ✅ `type`을 FUNCTION으로 고정

    def __post_init__(self):
        object.__setattr__(self, "data", String(self.function_name))  # ✅ `data`를 function_name으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        arg_str = ", ".join([repr(arg) for arg in self.arguments])
        return f"FunctionToken(function_name={self.function_name}, arguments=[{arg_str}], line={self.line}, column={self.column})"


@dataclass
class CustomToken(Token):
    """✅ 'Point', 'Rectangle', 'Region', 'Image' 등의 객체를 표현하는 커스텀 토큰"""
    data: KavanaDataType = field(init=False)
    type: TokenType = field(default=TokenType.CUSTOM_TYPE, init=False)  # ✅ `type`을 FUNCTION으로 고정
    object_type: TokenType = TokenType.UNKNOWN  # ✅ 'POINT', 'RECTANGLE', 'REGION', 'IMAGE' 등의 타입
    arguments: List[List[Token]] = field(default_factory=list)  # ✅ 인자 리스트
    
    def __post_init__(self):
        object.__setattr__(self, "data", String(str(self.type)))  # ✅ `data`를 function_name으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        arg_str = ", ".join([repr(arg) for arg in self.arguments])
        return f"CustomToken(type={self.object_type}, arguments=[{arg_str}], line={self.line}, column={self.column})"


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
class ListExToken(Token):
    ''' 리스트 표현식을 표현하는 토큰 '''
    data: ListType  # ✅ `data`는 ListType 타입
    type: TokenType = field(default=TokenType.LIST_EX, init=False)  # ✅ `type`을 LIST로 고정
    element_type: TokenType = field(default=TokenType.UNKNOWN)  # 요소의 토큰 타입
    element_expresses: List[List[Token]] = field(default_factory=list)  # 각 요소의 표현 리스트
    status: Literal["Parsed", "Evaled"] = "Parsed"

    def __post_init__(self):
        if not isinstance(self.data, ListType):
            raise TypeError("ListExToken must contain a ListType")

@dataclass
class ListIndexToken(Token):
    """✅ 리스트에 접근하기 위한 인덱스 토큰"""
    # express: List[Token] = field(default_factory=list)  
    row_express: List[Token] = field(default_factory=list)  
    column_express: List[Token] = field(default_factory=list)
    data: String  # ✅ `data`는 String 타입 (생성 시 반드시 입력해야 함)
    type: TokenType = field(default=TokenType.LIST_INDEX, init=False)  # ✅ `type`을 LIST_INDEX 고정

    def __post_init__(self):
        """추가적인 유효성 검사"""
        if not isinstance(self.data, String):
            raise TypeError(f"data 필드는 String 타입이어야 합니다. (현재 타입: {type(self.data)})")

    def __repr__(self) -> str:
        row_expr_str = ", ".join(repr(e) for e in self.row_express) if self.row_express else "None"
        col_expr_str = ", ".join(repr(e) for e in self.column_express) if self.column_express else "None"
        
        return (f"ListIndexToken("
                f"row_express=[{row_expr_str}], "
                f"column_express=[{col_expr_str}], "
                f"data={repr(self.data)}, "
                f"type={self.type})")
