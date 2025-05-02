import math
import random
from typing import Union
from lib.core.datatypes.kavana_datatype import Float, Integer
from lib.core.datatypes.array import Array
from lib.core.exceptions.kavana_exception import KavanaValueError, KavanaTypeError
from lib.core.token import  ArrayToken, Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

class NumericFunctions:
    ''' 숫자 관련 내장 함수들 '''
    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        NumericFunctions.executor = executor_instance

    @staticmethod
    def RANDOM(min_val: int, max_val: int) -> Token:
        '''
        min_val과 max_val 사이의 랜덤한 정수를 반환합니다.
        
        예:
        RANDOM(1, 10) → 3  (랜덤 값)
        RANDOM(100, 200) → 157  (랜덤 값)
        '''
        if not isinstance(min_val, int) or not isinstance(max_val, int):
            NumericFunctions.executor.log_command("ERROR", "RANDOM() 함수는 정수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("RANDOM() 함수는 정수형 인자만 받을 수 있습니다")
        if min_val > max_val:
            NumericFunctions.executor.log_command("ERROR", "RANDOM() 함수: 최소값은 최대값보다 작아야 합니다")
            raise KavanaTypeError("RANDOM() 함수: 최소값은 최대값보다 작아야 합니다")
        i = random.randint(min_val, max_val)
        return Token(data=Integer(i), type=TokenType.INTEGER)
    
    @staticmethod
    def ABS(i: Union[int,float]) -> Token:
        '''
        주어진 숫자의 절대값을 반환합니다.
        
        예:
        ABS(-5) → 5
        ABS(-10.3) → 10.3
        '''
        if not isinstance(i, int) and not isinstance(i, float):
            NumericFunctions.executor.log_command("ERROR", "ABS() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("ABS() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        if isinstance(i, float):
            return Token(data=Float(abs(i)), type=TokenType.FLOAT)
        else:
            return Token(data=Integer(abs(i)), type=TokenType.INTEGER)
    
    @staticmethod
    def MAX(i: int, j: int) -> Token:
        '''
        두 숫자 중 큰 값을 반환합니다.
        
        예:
        MAX(3, 7) → 7
        MAX(10, -5) → 10
        '''
        if not isinstance(i, int) or not isinstance(j, int):
            NumericFunctions.executor.log_command("ERROR", "MAX() 함수는 정수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("MAX() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(max(i, j)), type=TokenType.INTEGER)
    
    @staticmethod
    def MIN(i: int, j: int) -> Token:
        '''
        두 숫자 중 작은 값을 반환합니다.
        
        예:
        MIN(3, 7) → 3
        MIN(10, -5) → -5
        '''
        if not isinstance(i, int) or not isinstance(j, int):
            NumericFunctions.executor.log_command("ERROR", "MIN() 함수는 정수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("MIN() 함수는 정수형 인자만 받을 수 있습니다")
        return Token(data=Integer(min(i, j)),type=TokenType.INTEGER)
    
    @staticmethod
    def ROUND(i: Union[int, float]) -> Token:
        '''
        주어진 숫자를 반올림합니다.
        
        예:
        ROUND(3.6) → 4
        ROUND(2.3) → 2
        ROUND(5) → 5
        '''
        if not isinstance(i, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "ROUND() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("ROUND() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Integer(round(i)), type=TokenType.INTEGER)
    
    @staticmethod
    def FLOOR(i: Union[int, float]) -> Token:
        '''
        주어진 숫자를 내림 처리합니다 (소수점 이하 제거).
        
        예:
        FLOOR(3.9) → 3
        FLOOR(-1.2) → -2
        '''
        if not isinstance(i, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "FLOOR() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("FLOOR() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Integer(math.floor(i)), type=TokenType.INTEGER)


    @staticmethod
    def CEIL(i: Union[int, float]) -> Token:
        '''
        주어진 숫자를 올림 처리합니다.
        
        예:
        CEIL(3.1) → 4
        CEIL(-1.8) → -1
        '''
        if not isinstance(i, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "CEIL() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("CEIL() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Integer(math.ceil(i)), type=TokenType.INTEGER)


    @staticmethod
    def TRUNC(i: Union[int, float]) -> Token:
        '''
        주어진 숫자의 소수점을 제거하여 정수 부분만 반환합니다.
        
        예:
        TRUNC(3.14159) → 3
        TRUNC(-5.9) → -5
        '''
        if not isinstance(i, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "TRUNC() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("TRUNC() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Integer(math.trunc(i)), type=TokenType.INTEGER)    
    
    @staticmethod
    def IS_EVEN(i: int) -> Token:
        '''
        숫자가 짝수인지 여부를 반환합니다.
        
        예:
        IS_EVEN(4) → True
        IS_EVEN(7) → False
        '''
        if not isinstance(i, int):
            NumericFunctions.executor.log_command("ERROR", "IS_EVEN() 함수는 정수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("IS_EVEN() 함수는 정수형 인자만 받을 수 있습니다")
        if ((i % 2) == 0):
            return TokenUtil.boolean_to_boolean_token(True)
        else:
            return TokenUtil.boolean_to_boolean_token(False)
    
    @staticmethod
    def IS_ODD(i: int) -> Token:
        '''
        숫자가 홀수인지 여부를 반환합니다.
        
        예:
        IS_ODD(3) → True
        IS_ODD(8) → False
        '''
        if not isinstance(i, int):
            NumericFunctions.executor.log_command("ERROR", "IS_ODD() 함수는 정수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("IS_ODD() 함수는 정수형 인자만 받을 수 있습니다")

        if ((i % 2) == 1):
            return TokenUtil.boolean_to_boolean_token(True)
        else:
            return TokenUtil.boolean_to_boolean_token(False)        

    @staticmethod
    def RANGE(*args) -> ArrayToken:
        """RANGE(stop) 또는 RANGE(start, stop, step) 형태로 동작"""
        arg_len = len(args)

        if arg_len not in [1, 2, 3]:
            NumericFunctions.executor.log_command("ERROR", "RANGE()는 1~3개의 정수를 인자로 받아야 합니다.")
            raise KavanaTypeError("RANGE()는 1~3개의 정수를 인자로 받아야 합니다.")

        for arg in args:
            if not isinstance(arg, int):
                NumericFunctions.executor.log_command("ERROR", "RANGE()의 모든 인자는 정수여야 합니다.")
                raise KavanaTypeError("RANGE()의 모든 인자는 정수여야 합니다.")

        if arg_len == 1:
            start, stop, step = 0, args[0], 1
        elif arg_len == 2:
            start, stop, step = args[0], args[1], 1
        else:
            start, stop, step = args

        if step == 0:
            NumericFunctions.executor.log_command("ERROR", "RANGE()의 step 값은 0이 될 수 없습니다.")
            raise KavanaValueError("RANGE()의 step 값은 0이 될 수 없습니다.")

        range_list = list(range(start, stop, step))
        token_list =[]
        for i in range_list:
            token_list.append(Token(data=Integer(i), type=TokenType.INTEGER))
        resultToken = TokenUtil.array_to_array_token(token_list)
        return resultToken

    @staticmethod
    def POWER(base: Union[int, float], exp: Union[int, float]) -> Token:
        '''
        base의 exp 거듭제곱을 반환합니다.
        
        예:
        POWER(2, 3) → 8
        POWER(4, 0.5) → 2
        '''
        if not isinstance(base, (int, float)) or not isinstance(exp, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "POWER() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("POWER() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Float(math.pow(base, exp)), type=TokenType.FLOAT)

    @staticmethod
    def SQRT(i: Union[int, float]) -> Token:
        '''
        숫자의 제곱근을 반환합니다.
        
        예:
        SQRT(16) → 4
        SQRT(2) → 1.414
        '''
        if not isinstance(i, (int, float)) or i < 0:
            NumericFunctions.executor.log_command("ERROR", "SQRT() 함수는 0 이상의 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaValueError("SQRT() 함수는 0 이상의 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Float(math.sqrt(i)), type=TokenType.FLOAT)

    @staticmethod
    def SIN(angle: Union[int, float]) -> Token:
        '''
        주어진 각도의 사인 값을 반환합니다 (라디안 단위).
        
        예:
        SIN(math.pi / 2) → 1
        SIN(0) → 0
        '''
        if not isinstance(angle, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "SIN() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("SIN() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Float(math.sin(angle)), type=TokenType.FLOAT)

    @staticmethod
    def COS(angle: Union[int, float]) -> Token:
        '''
        주어진 각도의 코사인 값을 반환합니다 (라디안 단위).
        
        예:
        COS(0) → 1
        COS(math.pi) → -1
        '''
        if not isinstance(angle, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "COS() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("COS() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Float(math.cos(angle)), type=TokenType.FLOAT)

    @staticmethod
    def TAN(angle: Union[int, float]) -> Token:
        '''
        주어진 각도의 탄젠트 값을 반환합니다 (라디안 단위).
        
        예:
        TAN(0) → 0
        TAN(math.pi / 4) → 1
        '''
        if not isinstance(angle, (int, float)):
            NumericFunctions.executor.log_command("ERROR", "TAN() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("TAN() 함수는 정수형 또는 실수형 인자만 받을 수 있습니다")
        return Token(data=Float(math.tan(angle)), type=TokenType.FLOAT)

    @staticmethod
    def MOD(a: int, b: int) -> Token:
        '''
        a를 b로 나눈 나머지를 반환합니다.
        
        예:
        MOD(10, 3) → 1
        MOD(15, 5) → 0
        '''
        if not isinstance(a, int) or not isinstance(b, int):
            NumericFunctions.executor.log_command("ERROR", "MOD() 함수는 정수형 인자만 받을 수 있습니다")
            raise KavanaTypeError("MOD() 함수는 정수형 인자만 받을 수 있습니다")
        if b == 0:
            NumericFunctions.executor.log_command("ERROR", "MOD() 함수는 0으로 나눌 수 없습니다")
            raise KavanaValueError("MOD() 함수는 0으로 나눌 수 없습니다")
        return Token(data=Integer(a % b), type=TokenType.INTEGER)

