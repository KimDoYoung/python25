from typing import Any

from lib.core.datatypes.kavana_datatype import Boolean, String
from lib.core.token import StringToken, Token
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

