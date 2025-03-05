import random

from lib.core.datatypes.kavana_datatype import Integer
from lib.core.token import Token


class NumericFunctions:
    @staticmethod
    def RANDOM(min_val: int, max_val: int) -> int:
        if not isinstance(min_val, int) or not isinstance(max_val, int):
            raise TypeError("RANDOM() 함수는 정수형 인자만 받을 수 있습니다")
        if min_val > max_val:
            raise ValueError("최소값은 최대값보다 작아야 합니다")
        i = random.randint(min_val, max_val)
        return Token(data=Integer(i), type="INTEGER")
    
    @staticmethod
    def ABS(i: int) -> int:
        if not isinstance(i, int):
            raise TypeError("ABS() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(abs(i)), type="INTEGER")
    
    @staticmethod
    def MAX(i: int, j: int) -> int:
        if not isinstance(i, int) or not isinstance(j, int):
            raise TypeError("MAX() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(max(i, j)), type="INTEGER")
    @staticmethod
    def MIN(i: int, j: int) -> int:
        if not isinstance(i, int) or not isinstance(j, int):
            raise TypeError("MIN() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(min(i, j)), type="INTEGER")
    @staticmethod
    def ROUND(i: int) -> int:
        if not isinstance(i, int):
            raise TypeError("ROUND() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(round(i)), type="INTEGER")
    @staticmethod
    def FLOOR(i: int) -> int:
        if not isinstance(i, int):
            raise TypeError("FLOOR() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i // 1), type="INTEGER")
    @staticmethod
    def CEIL(i: int) -> int:
        if not isinstance(i, int):
            raise TypeError("CEIL() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i // 1 + 1), type="INTEGER")
    @staticmethod
    def TRUNC(i: int) -> int:
        if not isinstance(i, int):
            raise TypeError("TRUNC() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i), type="INTEGER")