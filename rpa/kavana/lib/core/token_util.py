
from datetime import date, datetime
import re
from typing import Any, List
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Boolean, Float, Integer, KavanaDataType, NoneType, String
from lib.core.datatypes.array import Array
from lib.core.datatypes.point import Point
from lib.core.datatypes.region import Region
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.exceptions.kavana_exception import DataTypeError, KavanaSyntaxError
from lib.core.token import ArrayToken, HashMapToken, StringToken, Token, TokenStatus
from lib.core.token_custom import PointToken, RegionToken
from lib.core.token_type import TokenType


class TokenUtil:
    @staticmethod
    def tokens_to_string(tokens: list[Token]) -> str:
        """토큰 리스트를 문자열로 변환"""
        strs = []
        for token in tokens:
            if isinstance(token, list):
                TokenUtil.tokens_to_string(token)
            elif token.type == TokenType.ACCESS_INDEX:
                string_array = []
                for express in token.element_expresses:
                    s = TokenUtil.tokens_to_string(express)
                    string_array.append(f"[{s}]")
                var_name = token.data.value
                index_express = string_array.join(",")
                strs.append(f"name={var_name}, index express={index_express}")
            elif token.type == TokenType.ARRAY:
                expresses = []
                for express in token.element_expresses:
                    expresses.append(TokenUtil.tokens_to_string(express))
                strs.append(f"length:{len(token.element_expresses)}, els:[{', '.join(expresses)}]")
            else:
                strs.append(str(token.data.value))
        return ', '.join(strs)
    
    
    '''kavana에서 사용하는 토큰 유틸리티 클래스'''
    @staticmethod
    def primitive_to_kavana(primitive: Any) -> KavanaDataType | None:
        """
        파이썬 기본값을 KavanaDataType으로 변환
        """
        if isinstance(primitive, list):
            return Array([TokenUtil.primitive_to_kavana(p) for p in primitive])

        elif isinstance(primitive, dict):
            return HashMap({
                k: TokenUtil.primitive_to_kavana(v)
                for k, v in primitive.items()
            })

        elif isinstance(primitive, int):
            return Integer(primitive)
        elif isinstance(primitive, float):
            return Float(primitive)
        elif isinstance(primitive, bool):
            return Boolean(primitive)
        elif isinstance(primitive, str):
            return String(primitive)
        elif primitive is None:
            return NoneType()
        elif isinstance(primitive, datetime):
            return YmdTime(primitive)
        elif isinstance(primitive, date):
            return Ymd(primitive)
        elif isinstance(primitive, KavanaDataType):
            return primitive  # ✅ 그대로 반환

        return None

    
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

            elif token_type == TokenType.ARRAY:
                if isinstance(value, list):  # ✅ 이미 리스트인 경우
                    return Array(*value)
                if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                    elements = [int(v.strip()) for v in value.strip("[]").split(",")]
                    return Array(*elements)
            else:
                return String(str(value))
        except DataTypeError as e:
            raise e  # 이미 처리된 예외 그대로 전달
        except Exception as e:
            raise DataTypeError(f"primitive_to_kavanatype에서 알려지지 않은 예외발생: {str(e)}", value)    
        

    @staticmethod
    def get_element_token_type(value: Any) -> TokenType:
        """주어진 값의 타입을 확인하여 TokenType 반환"""
        if isinstance(value, int):
            return TokenType.INTEGER
        elif isinstance(value, float):
            return TokenType.FLOAT
        elif isinstance(value, bool):
            return TokenType.BOOLEAN
        elif value is None:
            return TokenType.NONE
        elif isinstance(value, str):
            return TokenType.STRING
        elif isinstance(value, list):
            return TokenType.ARRAY
        else:
            return type(value)
        
    @staticmethod
    def find_key_value(tokens: list[Token], start_index: int) -> tuple[Token, List[Token], int]:
        """
        주어진 토큰 리스트에서 key에 해당하는 토큰1개와 express에 해당하는 토큰 리스트 
        express는 TokenType.COMMA나 tokens의 끝까지로 한다.
        그리고 next_index를 리턴한다
        """
        if start_index >= len(tokens):
            return None, None, start_index
        expresses = []
        key_token = tokens[start_index]
        i = start_index +1
        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.COMMA:
                i += 1
                break
            expresses.append(token)
            i += 1
        return key_token, expresses, i    

    @staticmethod
    def decode_escaped_string(s: str) -> str:
        ESCAPE_MAP = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "b": "\b",
            "f": "\f",
            "v": "\v",
            "\\": "\\",
            '"': '"',
        }        
        result = []
        i = 0
        while i < len(s):
            if s[i] == "\\":
                if i + 1 >= len(s):
                    raise ValueError("잘못된 문자열: 단독 백슬래시(`\\`)가 포함될 수 없습니다.")

                escape_seq = s[i + 1]
                result.append(ESCAPE_MAP.get(escape_seq, "\\" + escape_seq))
                i += 2
            else:
                result.append(s[i])
                i += 1
        return "".join(result)
    
    @staticmethod
    def dict_to_hashmap_token(data: dict) -> HashMapToken:
        """dict → HashMapToken 변환"""
        hash_map = HashMap({
            k: TokenUtil.primitive_to_kavana(v)
            for k, v in data.items()
        })
        result_token = HashMapToken(data=hash_map)
        result_token.status = "Evaled"
        return result_token    
    
    @staticmethod
    def list_to_array_token(data: list) -> ArrayToken:
        """list → ArrayToken 변환"""
        from lib.core.datatypes.kavana_datatype import KavanaDataType
        from lib.core.exceptions.kavana_exception import KavanaTypeError

        if not isinstance(data, list):
            raise KavanaTypeError("list_to_array_token은 리스트만 허용됩니다.")

        kavana_items = [TokenUtil.primitive_to_kavana(item) for item in data]

        array_obj = Array(kavana_items)

        # 토큰 타입 추정 (전부 동일하다는 전제)
        if kavana_items:
            element_token_type = TokenUtil.get_element_token_type(kavana_items[0])
        else:
            element_token_type = TokenType.UNKNOWN

        return ArrayToken(
            data=array_obj,
            element_type=element_token_type,
            element_expresses=[],
            status="Evaled"
        )

    @staticmethod
    def string_to_string_token(data: str) -> Token:
        """문자열을 StringToken으로 변환"""
        from lib.core.datatypes.kavana_datatype import KavanaDataType
        from lib.core.exceptions.kavana_exception import KavanaTypeError

        str_token = StringToken(data=String(data), type=TokenType.STRING)
        return str_token
    
    @staticmethod
    def region_to_token(region: tuple[int, int, int, int]) -> RegionToken:
        """Region을 RegionToken으로 변환"""
        from lib.core.datatypes.kavana_datatype import KavanaDataType
        from lib.core.exceptions.kavana_exception import KavanaTypeError

        if not isinstance(region, tuple) or len(region) != 4:
            raise KavanaTypeError("region_to_token은 (x, y, width, height) 형태의 튜플만 허용됩니다.")

        x, y, width, height = region
        region_obj = Region(x, y, width, height)
        result = RegionToken(data=region_obj)
        result.status = TokenStatus.EVALUATED
        return result
    
    @staticmethod
    def xy_to_point_token(x,y) -> PointToken:
        """x,y를 PointToken으로 변환"""
        from lib.core.datatypes.kavana_datatype import KavanaDataType
        from lib.core.exceptions.kavana_exception import KavanaTypeError

        p = Point(x,y)

        result =  PointToken(data=p)
        result.status = TokenStatus.EVALUATED
        return result
    
    @staticmethod
    def boolean_to_boolean_token(data: bool) -> Token:
        """Boolean을 BooleanToken으로 변환"""
        from lib.core.datatypes.kavana_datatype import KavanaDataType
        from lib.core.exceptions.kavana_exception import KavanaTypeError

        if not isinstance(data, bool):
            raise KavanaTypeError("boolean_to_boolean_token은 bool 타입만 허용됩니다.")

        boolean_obj = Boolean(data)
        result = Token(data=boolean_obj, type=TokenType.BOOLEAN)
        return result