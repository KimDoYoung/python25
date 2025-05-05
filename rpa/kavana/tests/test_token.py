import pytest
from typing import Dict, List

from lib.core.datatypes.array import Array
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Integer, NoneType, String
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.token import (
    AccessIndexToken,
    ArrayToken,
    FunctionToken,
    HashMapToken,
    NoneToken,
    StringToken,
    Token,
    TokenStatus,
    YmdTimeToken,
    YmdToken,
)
from lib.core.token_type import TokenType


class TestToken:
    def test_token_basic(self):
        """기본 토큰 생성 테스트"""
        token = Token(data=String("test"), type=TokenType.STRING, line=1, column=5)
        
        assert token.data.value == "test"
        assert token.type == TokenType.STRING
        assert token.line == 1
        assert token.column == 5
        
        # 문자열 표현 테스트
        assert repr(token) == "Token(data=test, type=TokenType.STRING, line=1, column=5)"
    
    def test_token_without_position(self):
        """위치 정보 없는 토큰 생성 테스트"""
        token = Token(data=Integer(10), type=TokenType.INTEGER)
        
        assert token.data.value == 10
        assert token.type == TokenType.INTEGER
        assert token.line is None
        assert token.column is None


class TestNoneToken:
    def test_none_token(self):
        """NoneToken 생성 테스트"""
        token = NoneToken()
        
        assert isinstance(token.data, NoneType)
        assert token.type == TokenType.NONE
        assert token.line is None
        assert token.column is None


class TestStringToken:
    def test_string_token_basic(self):
        """기본 StringToken 생성 테스트"""
        token = StringToken(data=String("hello"), type=TokenType.STRING, line=1, column=5)
        
        assert token.data.value == "hello"
        assert token.type == TokenType.STRING
        assert token.line == 1
        assert token.column == 5
        assert token.is_raw is False
        assert token.is_formatted is False
        assert token.expressions is None
    
    def test_string_token_raw(self):
        """raw 문자열 StringToken 테스트"""
        token = StringToken(data=String(r"line\n"), type=TokenType.STRING, is_raw=True)
        
        assert token.data.value == r"line\n"
        assert token.is_raw is True
    
    def test_string_token_formatted(self):
        """f-string StringToken 테스트"""
        # 표현식 리스트 생성
        expr_token = Token(data=Integer(10), type=TokenType.INTEGER)
        expressions = [[expr_token]]
        
        token = StringToken(
            data=String("Value: {0}"), 
            type=TokenType.STRING,
            is_formatted=True,
            expressions=expressions
        )
        
        assert token.data.value == "Value: {0}"
        assert token.is_formatted is True
        assert len(token.expressions) == 1
        assert token.expressions[0][0].data.value == 10


class TestFunctionToken:
    def test_function_token_basic(self):
        """기본 FunctionToken 생성 테스트"""
        # 함수 인자 생성
        arg1 = [Token(data=Integer(10), type=TokenType.INTEGER)]
        arg2 = [Token(data=String("test"), type=TokenType.STRING)]
        
        token = FunctionToken(
            function_name="my_func",
            arguments=[arg1, arg2],
            line=5,
            column=10
        )
        
        assert token.function_name == "my_func"
        assert token.data.value == "my_func"  # data는 function_name을 저장
        assert token.type == TokenType.FUNCTION
        assert token.line == 5
        assert token.column == 10
        assert len(token.arguments) == 2
        assert token.arguments[0][0].data.value == 10
        assert token.arguments[1][0].data.value == "test"
    
    def test_function_token_repr(self):
        """FunctionToken 문자열 표현 테스트"""
        arg = [Token(data=Integer(5), type=TokenType.INTEGER)]
        token = FunctionToken(function_name="test_func", arguments=[arg])
        
        expected = "FunctionToken(function_name=test_func, arguments=[" \
                   "[Token(data=5, type=TokenType.INTEGER, line=None, column=None)]], " \
                   "line=None, column=None)"
        assert repr(token) == expected


class TestYmdTimeToken:
    def test_ymdtime_token_with_six_args(self):
        """YmdTimeToken 6개 인자 생성 테스트"""
        token = YmdTimeToken(
            arguments=[2023, 5, 15, 14, 30, 45],
            line=1,
            column=5
        )
        
        assert token.type == TokenType.YMDTIME
        assert token.line == 1
        assert token.column == 5
        assert isinstance(token.data, YmdTime)
        assert token.data.year == 2023
        assert token.data.month == 5
        assert token.data.day == 15
        assert token.data.hour == 14
        assert token.data.minute == 30
        assert token.data.second == 45
    
    def test_ymdtime_token_with_three_args(self):
        """YmdTimeToken 3개 인자 생성 테스트 (시간 00:00:00 자동 추가)"""
        token = YmdTimeToken(arguments=[2023, 5, 15])
        
        assert isinstance(token.data, YmdTime)
        assert token.data.year == 2023
        assert token.data.month == 5
        assert token.data.day == 15
        assert token.data.hour == 0
        assert token.data.minute == 0
        assert token.data.second == 0
    
    def test_ymdtime_token_invalid_args(self):
        """YmdTimeToken 잘못된 인자 개수 테스트"""
        with pytest.raises(ValueError, match="YmdTime 인자 개수 오류"):
            YmdTimeToken(arguments=[2023, 5])
        
        with pytest.raises(ValueError, match="YmdTime 인자 개수 오류"):
            YmdTimeToken(arguments=[2023, 5, 15, 14, 30])


class TestYmdToken:
    def test_ymd_token_basic(self):
        """YmdToken 기본 생성 테스트"""
        token = YmdToken(arguments=[2023, 5, 15], line=1, column=5)
        
        assert token.type == TokenType.YMD
        assert token.line == 1
        assert token.column == 5
        assert isinstance(token.data, Ymd)
        assert token.data.year == 2023
        assert token.data.month == 5
        assert token.data.day == 15
    
    def test_ymd_token_invalid_args(self):
        """YmdToken 잘못된 인자 개수 테스트"""
        with pytest.raises(ValueError, match="Ymd 인자 개수 오류"):
            YmdToken(arguments=[2023, 5])
        
        with pytest.raises(ValueError, match="Ymd 인자 개수 오류"):
            YmdToken(arguments=[2023, 5, 15, 14])


class TestArrayToken:
    def test_array_token_basic(self):
        """ArrayToken 기본 생성 테스트"""
        array_data = Array([Integer(1), Integer(2), Integer(3)])
        token = ArrayToken(
            data=array_data,
            element_type=TokenType.INTEGER,
            line=1,
            column=5
        )
        
        assert token.type == TokenType.ARRAY
        assert token.line == 1
        assert token.column == 5
        assert token.element_type == TokenType.INTEGER
        assert token.status == TokenStatus.PARSED
        assert len(token.data.value) == 3
        assert token.data.value[0].value == 1
        assert token.data.value[1].value == 2
        assert token.data.value[2].value == 3
    
    def test_array_token_with_expressions(self):
        """ArrayToken 표현식 포함 테스트"""
        array_data = Array([Integer(1), Integer(2)])
        
        expr1 = [Token(data=Integer(1), type=TokenType.INTEGER)]
        expr2 = [Token(data=Integer(2), type=TokenType.INTEGER)]
        
        token = ArrayToken(
            data=array_data,
            element_type=TokenType.INTEGER,
            element_expresses=[expr1, expr2]
        )
        
        assert token.element_expresses[0][0].data.value == 1
        assert token.element_expresses[1][0].data.value == 2
    
    def test_array_token_invalid_data(self):
        """ArrayToken 잘못된 데이터 타입 테스트"""
        with pytest.raises(TypeError, match="ListExToken must contain a ListType"):
            ArrayToken(
                data=String("not an array"),  # 잘못된 데이터 타입
                element_type=TokenType.STRING
            )


class TestHashMapToken:
    def test_hashmap_token_basic(self):
        """HashMapToken 기본 생성 테스트"""
        hash_data = HashMap({
            "key1": String("value1"),
            "key2": Integer(2)
        })
        token = HashMapToken(
            data=hash_data,
            line=1,
            column=5
        )
        
        assert token.type == TokenType.HASH_MAP
        assert token.line == 1
        assert token.column == 5
        assert token.status == TokenStatus.PARSED
        assert len(token.data.value) == 2
        assert token.data.value["key1"].value == "value1"
        assert token.data.value["key2"].value == 2
    
    def test_hashmap_token_with_expressions(self):
        """HashMapToken 표현식 포함 테스트"""
        hash_data = HashMap({
            "key1": String("value1"),
            "key2": Integer(2)
        })
        
        expr1 = [Token(data=String("value1"), type=TokenType.STRING)]
        expr2 = [Token(data=Integer(2), type=TokenType.INTEGER)]
        
        token = HashMapToken(
            data=hash_data,
            key_express_map={
                "key1": expr1,
                "key2": expr2
            }
        )
        
        assert token.key_express_map["key1"][0].data.value == "value1"
        assert token.key_express_map["key2"][0].data.value == 2
    
    def test_hashmap_token_invalid_data(self):
        """HashMapToken 잘못된 데이터 타입 테스트"""
        with pytest.raises(TypeError, match="HashMapToken must contain a HashMap instance"):
            HashMapToken(
                data=String("not a hashmap")  # 잘못된 데이터 타입
            )


class TestAccessIndexToken:
    def test_access_index_token_basic(self):
        """AccessIndexToken 기본 생성 테스트"""
        # 인덱스 표현식 생성
        idx_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        
        token = AccessIndexToken(
            data=String("arr"),
            index_expresses=[idx_expr],
            line=1,
            column=5
        )
        
        assert token.type == TokenType.ACCESS_INDEX
        assert token.line == 1
        assert token.column == 5
        assert token.data.value == "arr"
        assert len(token.index_expresses) == 1
        assert token.index_expresses[0][0].data.value == 0
    
    def test_access_index_token_multiple_indices(self):
        """AccessIndexToken 다중 인덱스 테스트"""
        # 다중 인덱스 표현식 생성
        idx1 = [Token(data=Integer(0), type=TokenType.INTEGER)]
        idx2 = [Token(data=String("key"), type=TokenType.STRING)]
        
        token = AccessIndexToken(
            data=String("arr"),
            index_expresses=[idx1, idx2]
        )
        
        assert len(token.index_expresses) == 2
        assert token.index_expresses[0][0].data.value == 0
        assert token.index_expresses[1][0].data.value == "key"
        
    
    def test_access_index_token_invalid_data(self):
        """AccessIndexToken 잘못된 데이터 타입 테스트"""
        with pytest.raises(TypeError, match="data 필드는 String 타입이어야 합니다"):
            AccessIndexToken(
                data=Integer(10),  # 잘못된 데이터 타입
                index_expresses=[]
            )
    
