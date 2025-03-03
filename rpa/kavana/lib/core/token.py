from dataclasses import dataclass, field
from typing import List, Optional
from lib.core.datatypes.kavana_datatype import KavanaDataType, String
from lib.core.datatypes.list_type import ListType
from lib.core.token_type import TokenType

@dataclass(frozen=True)
class Token:
    data: KavanaDataType
    type: TokenType  # ✅ 토큰 유형
    line: Optional[int] = None  # ✅ 기본값을 None으로 설정
    column: Optional[int] = None  # ✅ 기본값을 None으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        return f"Token(data={self.data}, type={self.type}, line={self.line}, column={self.column})"

@dataclass(frozen=True)
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

@dataclass(frozen=True)
class ListToken(Token):

    def __post_init__(self):
        if not isinstance(self.data, ListType):
            raise TypeError("ListToken must contain a ListType")


@dataclass(frozen=True)
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
