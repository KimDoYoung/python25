from typing import Any

from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Boolean, String
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import HashMapToken, StringToken, Token
from lib.core.token_util import TokenUtil


class DatatypeFunctions:
    """데이터타입관련 내장 함수"""
    @staticmethod
    def TYPE_OF(obj: Any) -> StringToken:
        """특정 디렉토리의 파일 목록 반환"""
        name = obj.type_name()
        return TokenUtil.string_to_string_token(name)

    @staticmethod
    def IS_TYPE(obj: Any, type_name_obj: String) -> Token:
        """특정 타입인지 확인"""
        tname = obj.type_name().upper() 
        type_name = type_name_obj.value.upper()
        b = tname == type_name
        token = TokenUtil.boolean_to_boolean_token(b)
        return token

    @staticmethod
    def IS_NULL (obj: Any) -> Token:
        """null 체크"""
        b = obj is None
        token = TokenUtil.boolean_to_boolean_token(b)
        return token
    
    @staticmethod
    def JSON_STR_TO_(json_str: String) -> HashMapToken:
        """JSON 문자열을 HashMap으로 변환"""
        from lib.core.token_util import TokenUtil
        import json

        try:
            # 문자열을 Python dict/list 등으로 파싱
            parsed = json.loads(json_str)
            if isinstance(parsed, dict):
                return TokenUtil.dict_to_hashmap(parsed)
            elif isinstance(parsed, list):
                return TokenUtil.list_to_array(parsed)
            else:
                raise ValueError("지원하지 않는 JSON 최상위 구조입니다.")            
            
        except json.JSONDecodeError as e:
            raise KavanaValueError(f"json_str_to_hashmap 함수 내, JSON 파싱 오류: {e}")

