import pytest
from lib.core.builtins.numeric_functions import NumericFunctions
from lib.core.token import TokenType
from lib.core.datatypes.kavana_datatype import Integer
from lib.core.token import ArrayToken
from lib.core.datatypes.array import Array

def test_random():
    """RANDOM() 함수 테스트"""
    result = NumericFunctions.RANDOM(1, 10)
    assert result.type == TokenType.INTEGER
    assert 1 <= result.data.value <= 10

def test_abs():
    """ABS() 함수 테스트"""
    assert NumericFunctions.ABS(-5).data.value == 5
    assert NumericFunctions.ABS(10).data.value == 10
    assert NumericFunctions.ABS(-5.3).data.value == 5.3
    assert NumericFunctions.ABS(-10.3).data.value == 10.3

def test_max_min():
    """MAX(), MIN() 함수 테스트"""
    assert NumericFunctions.MAX(3, 7).data.value == 7
    assert NumericFunctions.MAX(10, -5).data.value == 10
    assert NumericFunctions.MIN(3, 7).data.value == 3
    assert NumericFunctions.MIN(10, -5).data.value == -5

def test_round():
    """ROUND() 함수 테스트"""
    assert NumericFunctions.ROUND(3).data.value == 3
    assert NumericFunctions.ROUND(-2).data.value == -2

def test_floor():
    """FLOOR() 함수 테스트"""
    assert NumericFunctions.FLOOR(3).data.value == 3
    assert NumericFunctions.FLOOR(-2).data.value == -2

def test_ceil():
    """CEIL() 함수 테스트"""
    assert NumericFunctions.CEIL(3).data.value == 3  # 올림
    assert NumericFunctions.CEIL(-2).data.value == -2  # 올림

def test_trunc():
    """TRUNC() 함수 테스트"""
    assert NumericFunctions.TRUNC(3).data.value == 3
    assert NumericFunctions.TRUNC(-2).data.value == -2

def test_is_even():
    """IS_EVEN() 함수 테스트"""
    assert NumericFunctions.IS_EVEN(4).data.value is True
    assert NumericFunctions.IS_EVEN(7).data.value is False

def test_is_odd():
    """IS_ODD() 함수 테스트"""
    assert NumericFunctions.IS_ODD(3).data.value is True
    assert NumericFunctions.IS_ODD(8).data.value is False

def test_range():
    """RANGE() 함수 테스트"""
    result = NumericFunctions.RANGE(5)
    assert isinstance(result, ArrayToken)
    array = []
    for t in result.data.value:
        array.append(t.data.value)
    assert array == [0, 1, 2, 3, 4]

    array =[]
    result = NumericFunctions.RANGE(2, 6)
    assert isinstance(result, ArrayToken)
    for t in result.data.value:
        array.append(t.data.value)
    assert array == [2, 3, 4, 5]
    
    result = NumericFunctions.RANGE(1, 10, 2)
    assert isinstance(result, ArrayToken)
    array = []
    for t in result.data.value:
        array.append(t.data.value)
    assert array == [1, 3, 5, 7, 9]
