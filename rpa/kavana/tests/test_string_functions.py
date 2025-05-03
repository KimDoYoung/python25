import pytest
from lib.core.builtins.string_functions import StringFunctions
from lib.core.token import TokenType
from lib.core.datatypes.kavana_datatype import Integer, String, Boolean
from lib.core.token import ArrayToken
from lib.core.datatypes.array import Array

def test_length():
    """LENGTH() 함수 테스트"""
    assert StringFunctions.LENGTH("hello").data.value == 5
    assert StringFunctions.LENGTH(["a", "b", "c"]).data.value == 3
    assert StringFunctions.LENGTH({"a": 1, "b": 2}).data.value == 2
    with pytest.raises(Exception):
        StringFunctions.LENGTH(123)

def test_substr():
    """SUBSTR() 함수 테스트"""
    assert StringFunctions.SUBSTR("hello", 1, 3).data.value == "ell"
    assert StringFunctions.SUBSTR("hello", 0, 5).data.value == "hello"
    assert StringFunctions.SUBSTR("hello", 1, 5).data.value == "ello"
    assert StringFunctions.SUBSTR("hello", 1, 0).data.value == ""
    with pytest.raises(Exception):
        StringFunctions.SUBSTR("hello", 1, 'a')

def test_upper_lower():
    """UPPER(), LOWER() 함수 테스트"""
    assert StringFunctions.UPPER("hello").data.value == "HELLO"
    assert StringFunctions.LOWER("HELLO").data.value == "hello"
    with pytest.raises(Exception):
        StringFunctions.UPPER(123)
    with pytest.raises(Exception):
        StringFunctions.LOWER(123)

def test_trim():
    """TRIM(), LTRIM(), RTRIM() 함수 테스트"""
    assert StringFunctions.TRIM("  hello  ").data.value == "hello"
    assert StringFunctions.LTRIM("  hello  ").data.value == "hello  "
    assert StringFunctions.RTRIM("  hello  ").data.value == "  hello"
    with pytest.raises(Exception):
        StringFunctions.TRIM(123)
    with pytest.raises(Exception):
        StringFunctions.LTRIM(123)
    with pytest.raises(Exception):
        StringFunctions.RTRIM(123)

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
    assert StringFunctions.CONTAINS([1, 2, 3], 2).data.value is True
    assert StringFunctions.CONTAINS([1, 2, 3], 4).data.value is False
    assert StringFunctions.CONTAINS({"a": 1, "b": 2}, "b").data.value is True
    assert StringFunctions.CONTAINS({"a": 1, "b": 2}, "c").data.value is False
    with pytest.raises(Exception):
        StringFunctions.CONTAINS("hello world", 1)

def test_index_of():
    """INDEX_OF() 함수 테스트"""
    assert StringFunctions.INDEX_OF("hello world", "world").data.value == 6
    assert StringFunctions.INDEX_OF("hello world", "Python").data.value == -1
    assert StringFunctions.INDEX_OF([1, 2, 3], 2).data.value == 1
    assert StringFunctions.INDEX_OF([1, 2, 3], 4).data.value == -1
    assert StringFunctions.INDEX_OF({"a": 1, "b": 2}, "b").data.value == 1
    assert StringFunctions.INDEX_OF({"a": 1, "b": 2}, "c").data.value == -1

    with pytest.raises(Exception):
        StringFunctions.INDEX_OF("hello world", 1)

def test_to_int():
    """TO_INT() 함수 테스트"""
    assert StringFunctions.TO_INT("42").data.value == 42
    assert StringFunctions.TO_INT("-10").data.value == -10
    assert StringFunctions.TO_INT(3.14).data.value == 3
    with pytest.raises(Exception):
        StringFunctions.TO_INT("hello")

def test_to_float():
    """TO_FLOAT() 함수 테스트"""
    assert StringFunctions.TO_FLOAT("3.14").data.value == 3.14
    assert StringFunctions.TO_FLOAT("-2.5").data.value == -2.5
    assert StringFunctions.TO_FLOAT(5).data.value == 5.0
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT("hello")

def test_to_str():
    """TO_STR() 함수 테스트"""
    assert StringFunctions.TO_STR(42).data.value == "42"
    assert StringFunctions.TO_STR(3.14).data.value == "3.14"
    assert StringFunctions.TO_STR(True).data.value == "True"
    assert StringFunctions.TO_STR(False).data.value == "False"
    assert StringFunctions.TO_STR([1, 2, 3]).data.value == "[1, 2, 3]"
    assert StringFunctions.TO_STR({"a": 1, "b": 2}).data.value == "{'a': 1, 'b': 2}"
    with pytest.raises(Exception):
        StringFunctions.TO_STR(Array)

def test_to_float_edge_cases():
    """TO_FLOAT() 함수의 엣지 케이스 테스트"""
    # 정수 입력 테스트
    assert StringFunctions.TO_FLOAT(0).data.value == 0.0
    assert StringFunctions.TO_FLOAT(-100).data.value == -100.0
    assert StringFunctions.TO_FLOAT(123456789).data.value == 123456789.0

    # 문자열 입력 테스트
    assert StringFunctions.TO_FLOAT("0").data.value == 0.0
    assert StringFunctions.TO_FLOAT("-0.0").data.value == -0.0
    assert StringFunctions.TO_FLOAT("1e3").data.value == 1000.0
    assert StringFunctions.TO_FLOAT("-1e-3").data.value == -0.001

    # 잘못된 문자열 입력 테스트
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT("abc")
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT("3.14.15")
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT("")

    # 기타 타입 입력 테스트
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT(None)
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT([1, 2, 3])
    with pytest.raises(Exception):
        StringFunctions.TO_FLOAT({"key": "value"})
        
def test_to_str_edge_cases():
    """TO_STR() 함수의 엣지 케이스 테스트"""
    # None 입력 테스트
    assert StringFunctions.TO_STR(None).data.value == ""

    # 빈 문자열 입력 테스트
    assert StringFunctions.TO_STR("").data.value == ""

    # 복잡한 리스트 입력 테스트
    assert StringFunctions.TO_STR([1, "a", True, None]).data.value == "[1, 'a', True, None]"

    # 복잡한 딕셔너리 입력 테스트
    assert StringFunctions.TO_STR({"key1": 1, "key2": [1, 2], "key3": {"nested": "value"}}).data.value == "{'key1': 1, 'key2': [1, 2], 'key3': {'nested': 'value'}}"

    # 잘못된 타입 입력 테스트
    with pytest.raises(Exception):
        StringFunctions.TO_STR(set([1, 2, 3]))