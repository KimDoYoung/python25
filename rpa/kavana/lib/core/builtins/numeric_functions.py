import random
from lib.core.datatypes.kavana_datatype import Integer
from lib.core.datatypes.array import Array
from lib.core.exceptions.kavana_exception import KavanaValueError, KavanaTypeError
from lib.core.token import  ArrayToken, Token
from lib.core.token_type import TokenType

class NumericFunctions:
    @staticmethod
    def RANDOM(min_val: int, max_val: int) -> Integer:
        '''
        min_val과 max_val 사이의 랜덤한 정수를 반환합니다.
        
        예:
        RANDOM(1, 10) → 3  (랜덤 값)
        RANDOM(100, 200) → 157  (랜덤 값)
        '''
        if not isinstance(min_val, int) or not isinstance(max_val, int):
            raise KavanaTypeError("RANDOM() 함수는 정수형 인자만 받을 수 있습니다")
        if min_val > max_val:
            raise KavanaTypeError("최소값은 최대값보다 작아야 합니다")
        i = random.randint(min_val, max_val)
        return Token(data=Integer(i), type=TokenType.INTEGER)
    
    @staticmethod
    def ABS(i: int) -> int:
        '''
        주어진 숫자의 절대값을 반환합니다.
        
        예:
        ABS(-5) → 5
        ABS(10) → 10
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("ABS() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(abs(i)), type=TokenType.INTEGER)
    
    @staticmethod
    def MAX(i: int, j: int) -> int:
        '''
        두 숫자 중 큰 값을 반환합니다.
        
        예:
        MAX(3, 7) → 7
        MAX(10, -5) → 10
        '''
        if not isinstance(i, int) or not isinstance(j, int):
            raise KavanaTypeError("MAX() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(max(i, j)), type=TokenType.INTEGER)
    
    @staticmethod
    def MIN(i: int, j: int) -> int:
        '''
        두 숫자 중 작은 값을 반환합니다.
        
        예:
        MIN(3, 7) → 3
        MIN(10, -5) → -5
        '''
        if not isinstance(i, int) or not isinstance(j, int):
            raise KavanaTypeError("MIN() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(min(i, j)),type=TokenType.INTEGER)
    
    @staticmethod
    def ROUND(i: int) -> int:
        '''
        주어진 숫자를 반올림합니다.
        
        예:
        ROUND(3.6) → 4
        ROUND(2.3) → 2
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("ROUND() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(round(i)), type=TokenType.INTEGER)
    
    @staticmethod
    def FLOOR(i: int) -> int:
        '''
        주어진 숫자를 내림 처리합니다 (소수점 이하 제거).
        
        예:
        FLOOR(3.9) → 3
        FLOOR(-1.2) → -2
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("FLOOR() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i // 1), type=TokenType.INTEGER)
    
    @staticmethod
    def CEIL(i: int) -> int:
        '''
        주어진 숫자를 올림 처리합니다.
        
        예:
        CEIL(3.1) → 4
        CEIL(-1.8) → -1
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("CEIL() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i // 1 + 1), type=TokenType.INTEGER)
    
    @staticmethod
    def TRUNC(i: int) -> int:
        '''
        주어진 숫자의 소수점을 제거하여 정수 부분만 반환합니다.
        
        예:
        TRUNC(3.14159) → 3
        TRUNC(-5.9) → -5
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("TRUNC() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i), type=TokenType.INTEGER)
    
    @staticmethod
    def IS_EVEN(i: int) -> bool:
        '''
        숫자가 짝수인지 여부를 반환합니다.
        
        예:
        IS_EVEN(4) → True
        IS_EVEN(7) → False
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("IS_EVEN() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i % 2 == 0), type=TokenType.INTEGER)
    
    @staticmethod
    def IS_ODD(i: int) -> bool:
        '''
        숫자가 홀수인지 여부를 반환합니다.
        
        예:
        IS_ODD(3) → True
        IS_ODD(8) → False
        '''
        if not isinstance(i, int):
            raise KavanaTypeError("IS_ODD() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(i % 2 == 1), type=TokenType.INTEGER)

    @staticmethod
    def RANGE(*args) -> ArrayToken:
        """RANGE(stop) 또는 RANGE(start, stop, step) 형태로 동작"""
        arg_len = len(args)

        if arg_len not in [1, 2, 3]:
            raise KavanaTypeError("RANGE()는 1~3개의 정수를 인자로 받아야 합니다.")

        for arg in args:
            if not isinstance(arg, int):
                raise KavanaTypeError("RANGE()의 모든 인자는 정수여야 합니다.")

        if arg_len == 1:
            start, stop, step = 0, args[0], 1
        elif arg_len == 2:
            start, stop, step = args[0], args[1], 1
        else:
            start, stop, step = args

        if step == 0:
            raise KavanaValueError("RANGE()의 step 값은 0이 될 수 없습니다.")

        range_list = list(range(start, stop, step))
        resultToken = ArrayToken(data=Array(range_list), element_type=TokenType.INTEGER)
        return resultToken
