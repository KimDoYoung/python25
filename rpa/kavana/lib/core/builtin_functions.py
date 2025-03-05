import random
from datetime import date, datetime
from typing import Optional

from lib.core.token import YmdTimeToken, YmdToken

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

    @staticmethod
    def YMDTIME(y: Optional[int] = None, m: Optional[int] = None, d: Optional[int] = None, 
                hh: Optional[int] = None, mm: Optional[int] = None, ss: Optional[int] = None) -> "YmdTimeToken":
        """현재 시간 또는 지정된 날짜를 YmdTimeToken으로 변환"""

        try:
            if y is None or m is None or d is None:
                now = datetime.now()
                y, m, d = now.year, now.month, now.day  # 현재 날짜로 설정
                hh = now.hour if hh is None else hh  # 현재 시 가져오기 (없으면 기본값 사용)
                mm = now.minute if mm is None else mm  # 현재 분 가져오기
                ss = now.second if ss is None else ss  # 현재 초 가져오기
            else:
                hh = 0 if hh is None else hh
                mm = 0 if mm is None else mm
                ss = 0 if ss is None else ss

            ymd = datetime(y, m, d, hh, mm, ss)  # 유효한 날짜인지 검증
        except ValueError as e:
            raise ValueError(f"잘못된 날짜 형식입니다: {e}")

        args = [y, m, d, hh, mm, ss]
        return YmdTimeToken(arguments=args)

    @staticmethod
    def YMD(y: Optional[int] = None, m: Optional[int] = None, d: Optional[int] = None) -> "YmdToken":
        """✅ 현재 날짜 또는 지정된 날짜를 YmdToken으로 변환"""

        try:
            if y is None or m is None or d is None:
                today = date.today()
                y, m, d = today.year, today.month, today.day  # ✅ 현재 날짜로 설정

            # ✅ 유효한 날짜인지 검증 (date 객체 생성)
            ymd = date(y, m, d)

        except ValueError as e:
            raise ValueError(f"잘못된 날짜 형식입니다: {e}")

        args = [y, m, d]
        return YmdToken(arguments=args)



# 내장 함수의 인자 개수 정보
BuiltinFunctions.arg_counts = {
    "LENGTH": 1,  # LENGTH 함수는 1개의 인자를 받음
    "SUBSTR": 3,  # SUBSTR 함수는 3개의 인자를 받음
    "CURRENT_DATETIME": 0,  # CURRENT_DATETIME 함수는 인자를 받지 않음
    "RANDOM": 2,  # RANDOM 함수는 2개의 인자를 받음
    "DATE_FORMAT": 2,  # DATE_FORMAT 함수는 2개의 인자를 받음
    "YMDTIME": 6,  # YMDTIME 함수는 6개의 인자를 받음
    "YMD": 3,  # YMD 함수는 3개의 인자를 받음
}

# 테스트 코드
# if __name__ == "__main__":
#     print("LENGTH('hello'):", BuiltinFunctions.LENGTH("hello"))
#     print("SUBSTR('hello', 1, 3):", BuiltinFunctions.SUBSTR("hello", 1, 3))
#     print("CURRENT_DATETIME():", BuiltinFunctions.CURRENT_DATETIME())
#     print("RANDOM(1, 10):", BuiltinFunctions.RANDOM(1, 10))
#     print("DATE_FORMAT(CURRENT_DATETIME(), '%Y-%m-%d'):", 
#           BuiltinFunctions.DATE_FORMAT(BuiltinFunctions.CURRENT_DATETIME(), '%Y-%m-%d'))
