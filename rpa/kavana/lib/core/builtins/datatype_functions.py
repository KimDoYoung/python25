from typing import Any

from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Boolean, KavanaDataType, String
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import HashMapToken, StringToken, Token
from lib.core.token_util import TokenUtil

class DatatypeFunctions:
    """데이터타입관련 내장 함수"""

    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        DatatypeFunctions.executor = executor_instance

    @staticmethod
    def DUMP_ATTRS(obj: KavanaDataType) -> HashMapToken:
        """객체의 속성값을 반환"""
        if not isinstance(obj, KavanaDataType):
            raise KavanaValueError("DUMP_ATTRS 함수는 KavanaDataType 객체만 지원합니다.")

        attr_dict = {}
        for attr in dir(obj):
            if not attr.startswith("_") and not callable(getattr(obj, attr)):
                value = getattr(obj, attr)
                attr_dict[attr] =  value #TokenUtil.primitive_to_token(value)
        return TokenUtil.dict_to_hashmap_token(attr_dict)

    @staticmethod
    def GET_ATTR(obj: KavanaDataType, attr_name:str) -> Token:
        """객체의 속성값을 반환"""
        if not isinstance(obj, KavanaDataType):
            raise KavanaValueError("GET_ATTR 함수는 KavanaDataType 객체만 지원합니다.")
        if not isinstance(attr_name, String):
            raise KavanaValueError("GET_ATTR 함수는 문자열 속성 이름만 지원합니다.")
        name = attr_name.value
        if hasattr(obj, name):
            attr_value = getattr(obj, name)
            return TokenUtil.primitive_to_token(attr_value)
        else:
            raise KavanaValueError(f"'{name}' 속성이 존재하지 않습니다.")

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
    def JSON_STR_PARSE(json_str: String) -> Token:
        """JSON 문자열을 HashMap으로 변환"""
        from lib.core.token_util import TokenUtil
        import json

        try:
            # 문자열을 Python dict/list 등으로 파싱
            json_str = json_str.replace("'", '"')
            parsed = json.loads(json_str)
            if isinstance(parsed, dict):
                return TokenUtil.dict_to_hashmap_token(parsed)
            elif isinstance(parsed, list):
                return TokenUtil.list_to_array_token(parsed)
            else:
                raise KavanaValueError("지원하지 않는 JSON 최상위 구조입니다.")            
            
        except json.JSONDecodeError as e:
            raise KavanaValueError(f"json_str_to_hashmap 함수 내, JSON 파싱 오류: {e}")

