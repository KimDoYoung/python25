from typing import Any, List

from lib.core.datatypes.kavana_datatype import Boolean, Integer, String
from lib.core.datatypes.list_type import ListType
from lib.core.exceptions.kavana_exception import KavanaTypeError, KavanaValueError
from lib.core.token import  ListExToken, Token
from lib.core.token_type import TokenType


class StringFunctions:
    @staticmethod
    def LENGTH(s: Any) -> int:
        if isinstance(s, str):
            i = len(s)
            return Token(data=Integer(i), type=TokenType.INTEGER)
        elif isinstance(s, List):
            i = len(s)
            return Token(data=Integer(len(s)), type=TokenType.INTEGER)
        raise KavanaTypeError("LENGTH()는 문자열과 리스트 타입에만 적용됩니다")

    @staticmethod
    def SUBSTR(s: str, start: int, length: int) -> str:
        if isinstance(s, str) and isinstance(start, int) and isinstance(length, int):
            result = s[start:start + length]
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("형식은 SUBSTR(문자열, 시작인덱스, 길이)로 되어 있습니다")
    
    @staticmethod
    def UPPER(s: str) -> str:
        if isinstance(s, str):
            result = s.upper()
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("UPPER()는 문자열에만 적용됩니다")
    
    @staticmethod
    def LOWER(s: str) -> str:
        if isinstance(s, str):
            result = s.lower()
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("LOWER()는 문자열에만 적용됩니다")
    
    @staticmethod
    def TRIM(s: str) -> str:
        if isinstance(s, str):
            result = s.strip()
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("TRIM()는 문자열에만 적용됩니다")
    
    @staticmethod
    def LTRIM(s: str) -> str:
        if isinstance(s, str):
            result = s.lstrip()
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("LTRIM()는 문자열에만 적용됩니다")
    
    @staticmethod
    def RTRIM(s: str) -> str:
        if isinstance(s, str):
            result = s.rstrip()
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("RTRIM()는 문자열에만 적용됩니다")
    
    @staticmethod
    def REPLACE(s: str, old: str, new: str) -> str:
        if isinstance(s, str) and isinstance(old, str) and isinstance(new, str):
            result = s.replace(old, new)
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("사용형식 : REPLACE(문자열, 바꿀문자열 , 새로운문자열)")
    
    @staticmethod
    def SPLIT(s: str, sep: str) -> List[str]:
        if isinstance(s, str) and isinstance(sep, str):
            result = s.split(sep)
            list_type = ListType(result)
            return ListExToken(data=list_type, type=TokenType.LIST_EX)
        raise KavanaTypeError("사용형식 : SPLIT(문자열, 구분자)")
    
    @staticmethod
    def JOIN(s: List[str], sep: str) -> str:
        if isinstance(s, List) and isinstance(sep, str):
            result = sep.join(s)
            return Token(data=String(result), type=TokenType.STRING)
        raise KavanaTypeError("사용형식 : JOIN(리스트, 구분자)")
    
    @staticmethod
    def STARTSWITH(s: str, prefix: str) -> bool:
        if isinstance(s, str) and isinstance(prefix, str):
            return Token(data=Integer(s.startswith(prefix)),type=TokenType.INTEGER)
        raise KavanaTypeError("사용형식 : STARTSWITH(문자열, 접두사)")
    
    @staticmethod
    def ENDSWITH(s: str, suffix: str) -> bool:
        if isinstance(s, str) and isinstance(suffix, str):
            return Token(data=Integer(s.endswith(suffix)), type=TokenType.INTEGER)
        raise KavanaTypeError("사용형식 : ENDSWITH(문자열, 접미사)")
    
    @staticmethod
    def CONTAINS(s: str, sub: str) -> bool:
        if isinstance(s, str) and isinstance(sub, str):
            return Token(data=Boolean(sub in s), type=TokenType.BOOLEAN)
        raise KavanaTypeError("사용형식 : CONTAINS(문자열, 포함문자열)")
    
    @staticmethod
    def INDEX_OF(s: str, sub: str) -> int:
        if isinstance(s, str) and isinstance(sub, str):
            return Token(data=Integer(s.find(sub)), type=TokenType.INTEGER)
        raise KavanaTypeError("사용형식 : INDEX_OF(문자열, 찾을문자열), 못찾았을 때 -1 반환")

    @staticmethod
    def TO_INT(s: str) -> int:
        '''
        문자열을 정수로 변환합니다.
        
        예:
        TO_INT("42") → 42
        TO_INT("-10") → -10
        
        잘못된 입력 예:
        TO_INT("abc") → 오류 발생
        '''
        if not isinstance(s, str):
            raise KavanaTypeError("TO_INT() 함수는 문자열 인자만 받을 수 있습니다")
        try:
            return Token(data=Integer(int(s)), type="INTEGER")
        except ValueError:
            raise KavanaValueError("TO_INT() 함수는 정수형 문자열만 받을 수 있습니다")
        
    @staticmethod
    def TO_FLOAT(s: str) -> float:
        '''
        문자열을 실수(float)로 변환합니다.
        
        예:
        TO_FLOAT("3.14") → 3.14
        TO_FLOAT("-2.5") → -2.5
        
        잘못된 입력 예:
        TO_FLOAT("hello") → 오류 발생
        '''
        if not isinstance(s, str):
            raise KavanaTypeError("TO_FLOAT() 함수는 문자열 인자만 받을 수 있습니다")
        try:
            return Token(data=Integer(float(s)), type="FLOAT")
        except ValueError:
            raise KavanaValueError("TO_FLOAT() 함수는 실수형 문자열만 받을 수 있습니다")
    