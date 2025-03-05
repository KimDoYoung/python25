import random
from datetime import datetime

from lib.core.token import YmdTimeToken

class BuiltinFunctions:
    @staticmethod
    def LENGTH(s: str) -> int:
        if isinstance(s, str):
            return len(s)
        raise TypeError("LENGTH() requires a string argument")

    @staticmethod
    def SUBSTR(s: str, start: int, length: int) -> str:
        return s[start:start + length]
    
    @staticmethod
    def CURRENT_DATETIME() -> datetime:
        return datetime.now()
    
    @staticmethod
    def RANDOM(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def DATE_FORMAT(date_obj: datetime, format_str: str) -> str:
        return date_obj.strftime(format_str)

    def YMDTIME(y: int, m: int, d: int, hh: int = 0, mm: int = 0, ss: int = 0) -> "YmdTimeToken":
        try:
            ymd = datetime(y, m, d, hh, mm, ss)  # 유효한 날짜인지 검증
        except ValueError as e:
            raise ValueError(f"잘못된 날짜 형식입니다: {e}")

        args = [y, m, d, hh, mm, ss]
        return YmdTimeToken(arguments=args)


# 내장 함수의 인자 개수 정보
BuiltinFunctions.arg_counts = {
    "LENGTH": 1,  # LENGTH 함수는 1개의 인자를 받음
    "SUBSTR": 3,  # SUBSTR 함수는 3개의 인자를 받음
    "CURRENT_DATETIME": 0,  # CURRENT_DATETIME 함수는 인자를 받지 않음
    "RANDOM": 2,  # RANDOM 함수는 2개의 인자를 받음
    "DATE_FORMAT": 2,  # DATE_FORMAT 함수는 2개의 인자를 받음
    "YMDTIME": 6  # YMDTIME 함수는 6개의 인자를 받음
}

# 테스트 코드
# if __name__ == "__main__":
#     print("LENGTH('hello'):", BuiltinFunctions.LENGTH("hello"))
#     print("SUBSTR('hello', 1, 3):", BuiltinFunctions.SUBSTR("hello", 1, 3))
#     print("CURRENT_DATETIME():", BuiltinFunctions.CURRENT_DATETIME())
#     print("RANDOM(1, 10):", BuiltinFunctions.RANDOM(1, 10))
#     print("DATE_FORMAT(CURRENT_DATETIME(), '%Y-%m-%d'):", 
#           BuiltinFunctions.DATE_FORMAT(BuiltinFunctions.CURRENT_DATETIME(), '%Y-%m-%d'))
