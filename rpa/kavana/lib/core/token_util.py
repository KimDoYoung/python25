
from datetime import date, datetime
import re
from typing import Any
from lib.core.datatypes.kavana_datatype import Boolean, Float, Integer, KavanaDataType, NoneType, String
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.exceptions.kavana_exception import DataTypeError
from lib.core.token_type import TokenType


class TokenUtil:
    '''kavana에서 사용하는 토큰 유틸리티 클래스'''
    @staticmethod
    def primitive_to_kavana(primitive: Any) -> KavanaDataType | None:
        """
        주어진 value 값으로 해당하는 KavanaDataType을 반환한다.
        """
        if isinstance(primitive, list):  # 리스트 타입이면 내부 요소 확인
            if len(primitive) == 0:
                return None  # 빈 리스트이면 타입 미정

            first_type = TokenUtil.primitive_to_kavana(primitive[0])  # 첫 번째 요소 타입 결정
            return first_type

        # 개별 값에 대한 타입 결정
        if isinstance(primitive, int):
            return Integer(primitive)
        elif isinstance(primitive, float):
            return Float(primitive)
        elif isinstance(primitive, bool):
            return Boolean(primitive)
        elif primitive is None:
            return NoneType
        elif isinstance(primitive, str):
            return String(primitive)
        elif isinstance(primitive, datetime):
            return YmdTime(primitive)
        elif isinstance(primitive, date):
            return Ymd(primitive)
        elif isinstance(primitive, KavanaDataType):
            return type(primitive)
        return None  # 알 수 없는 타입
    
    @staticmethod        
    def primitive_to_kavana_by_tokentype(value: Any, token_type: TokenType) -> KavanaDataType:
        """토큰 값을 해당 TokenType에 맞게 변환 (잘못된 값이면 Custom Exception 발생)"""
        try:
            if token_type == TokenType.INTEGER:
                # if not isinstance(value, int) and not str(value).isdigit():
                #     raise DataTypeError("Invalid integer format", value)
                return Integer(int(value))

            elif token_type == TokenType.FLOAT:
                # if not isinstance(value, float) and not re.match(r'^-?\d+\.\d+$', str(value)):
                #     raise DataTypeError("Invalid float format", value)
                return Float(float(value))

            elif token_type == TokenType.BOOLEAN:
                # if value not in {"True", "False", True, False}:
                #     raise DataTypeError("Invalid boolean value, expected 'True' or 'False'", value)
                return Boolean(value == "True" or value is True)

            elif token_type == TokenType.NONE:
                # if value not in {"None", None}:
                #     raise DataTypeError("Invalid None value, expected 'None'", value)
                return NoneType(None)

            elif token_type == TokenType.STRING:
                return String(str(value))

            elif token_type == TokenType.LIST:
                if isinstance(value, list):  # ✅ 이미 리스트인 경우
                    return ListType(*value)
                if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                    elements = [int(v.strip()) for v in value.strip("[]").split(",")]
                    return ListType(*elements)
            else:
                return String(str(value))
        except DataTypeError as e:
            raise e  # 이미 처리된 예외 그대로 전달
        except Exception as e:
            raise DataTypeError(f"primitive_to_kavanatype에서 알려지지 않은 예외발생: {str(e)}", value)    