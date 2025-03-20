
from datetime import date, datetime
import re
from typing import Any, List
from lib.core.datatypes.kavana_datatype import Boolean, Float, Integer, KavanaDataType, NoneType, String
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.exceptions.kavana_exception import DataTypeError, KavanaSyntaxError
from lib.core.token import Token
from lib.core.token_type import TokenType


class TokenUtil:
    @staticmethod
    def tokens_to_string(tokens: list[Token]) -> str:
        """토큰 리스트를 문자열로 변환"""
        strs = []
        for token in tokens:
            if isinstance(token, list):
                TokenUtil.tokens_to_string(token)
            elif token.type == TokenType.LIST_INDEX:
                row_express = TokenUtil.tokens_to_string(token.row_express)
                col_express = TokenUtil.tokens_to_string(token.column_express)
                var_name = token.data.value
                strs.append(f"name={var_name}, row_express:{row_express}, col_express:{col_express}")
            elif token.type == TokenType.LIST_EX:
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
        주어진 value 값으로 해당하는 KavanaDataType을 반환한다.
        """
        if isinstance(primitive, list):  # 리스트 타입이면 내부 요소 확인
            return ListType(*[TokenUtil.primitive_to_kavana(p) for p in primitive])

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

            elif token_type == TokenType.LIST_EX:
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
            return TokenType.LIST_EX
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
    def extract_command_option(tokens: list[Token], start_index: int) -> tuple[Token, List[Token], int]:
        """
        주어진 토큰 리스트에서 key=<express> 구조를 파싱하는 함수
        - key는 IDENTIFIER 토큰으로 시작해야 함
        - '=' 연산자가 반드시 있어야 함
        - express는 TokenType.COMMA 또는 tokens의 끝까지
        - next_index 반환 (다음 key-express 파싱을 위한 인덱스)
        """
        if start_index >= len(tokens):
            return None, None, start_index
        
        key_token = tokens[start_index]
        if key_token.type != TokenType.IDENTIFIER:
            raise KavanaSyntaxError("명령어의 옵션 키는 IDENTIFIER 타입이어야 합니다.")
        
        if start_index + 1 >= len(tokens) or tokens[start_index + 1].type != TokenType.ASSIGN:
            raise KavanaSyntaxError(f"옵션 '{key_token.data.string}' 뒤에 '=' 연산자가 필요합니다.")
        
        expresses = []
        i = start_index + 2  # '=' 다음 토큰부터 시작
        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.COMMA:
                i += 1  # 다음 key-value로 이동하기 위해 인덱스 증가
                break
            expresses.append(token)
            i += 1
        
        if not expresses:
            raise KavanaSyntaxError(f"옵션 '{key_token.data.string}'의 값이 없습니다.")
        
        return key_token, expresses, i    