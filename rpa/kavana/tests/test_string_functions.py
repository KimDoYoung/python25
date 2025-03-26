import pytest
from lib.core.builtins.string_functions import StringFunctions
from lib.core.token import TokenType
from lib.core.datatypes.kavana_datatype import Integer, String, Boolean
from lib.core.token import ArrayToken
from lib.core.datatypes.list_type import Array

def test_length():
    """LENGTH() 함수 테스트"""
    assert StringFunctions.LENGTH("hello").data.value == 5
    assert StringFunctions.LENGTH(["a", "b", "c"]).data.value == 3

def test_substr():
    """SUBSTR() 함수 테스트"""
    assert StringFunctions.SUBSTR("hello", 1, 3).data.value == "ell"

def test_upper_lower():
    """UPPER(), LOWER() 함수 테스트"""
    assert StringFunctions.UPPER("hello").data.value == "HELLO"
    assert StringFunctions.LOWER("HELLO").data.value == "hello"

def test_trim():
    """TRIM(), LTRIM(), RTRIM() 함수 테스트"""
    assert StringFunctions.TRIM("  hello  ").data.value == "hello"
    assert StringFunctions.LTRIM("  hello  ").data.value == "hello  "
    assert StringFunctions.RTRIM("  hello  ").data.value == "  hello"

def test_replace():
    """REPLACE() 함수 테스트"""
    assert StringFunctions.REPLACE("hello world", "world", "Python").data.value == "hello Python"

def test_split():
    """SPLIT() 함수 테스트"""
    result = StringFunctions.SPLIT("hello,world", ",")
    assert isinstance(result, ArrayToken)
    assert result.type == TokenType.ARRAY

def test_join():
    """JOIN() 함수 테스트"""
    result = StringFunctions.JOIN(["hello", "world"], ",")
    assert result.type == TokenType.STRING
    assert result.data.value == "hello,world"

def test_startswith():
    """STARTSWITH() 함수 테스트"""
    assert StringFunctions.STARTSWITH("hello", "he").data.value == 1
    assert StringFunctions.STARTSWITH("hello", "wo").data.value == 0

def test_endswith():
    """ENDSWITH() 함수 테스트"""
    assert StringFunctions.ENDSWITH("hello", "lo").data.value == 1
    assert StringFunctions.ENDSWITH("hello", "he").data.value == 0

def test_contains():
    """CONTAINS() 함수 테스트"""
    assert StringFunctions.CONTAINS("hello world", "world").data.value is True
    assert StringFunctions.CONTAINS("hello world", "Python").data.value is False

def test_index_of():
    """INDEX_OF() 함수 테스트"""
    assert StringFunctions.INDEX_OF("hello world", "world").data.value == 6
    assert StringFunctions.INDEX_OF("hello world", "Python").data.value == -1

def test_to_int():
    """TO_INT() 함수 테스트"""
    assert StringFunctions.TO_INT("42").data.value == 42
    assert StringFunctions.TO_INT("-10").data.value == -10
    with pytest.raises(Exception):
        StringFunctions.TO_INT("hello")

def test_to_float():
    """TO_FLOAT() 함수 테스트"""
    assert StringFunctions.TO_FLOAT("3.14").data.value == 3.14
    assert StringFunctions.TO_FLOAT("-2.5").data.value == -2.5
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT("hello")
