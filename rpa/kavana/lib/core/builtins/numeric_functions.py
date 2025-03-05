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