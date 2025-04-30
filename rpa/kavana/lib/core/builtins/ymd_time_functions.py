from datetime import date, datetime
from typing import Optional
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import YmdTimeToken, YmdToken


class YmdTimeFunctions:
    
    executor = None  # ✅ 클래스 변수로 executor 저장
    
    @staticmethod
    def set_executor(executor_instance):
        YmdTimeFunctions.executor = executor_instance

    @staticmethod
    def YMDTIME(
        y: Optional[int] = 0, 
        m: Optional[int] = 0, 
        d: Optional[int] = 0, 
        hh: Optional[int] = 0, 
        mm: Optional[int] = 0, 
        ss: Optional[int] = 0
    ) -> YmdTimeToken:
        try:
            # 모든 인자가 0이면 현재 시간 사용
            if (y, m, d, hh, mm, ss) == (0, 0, 0, 0, 0, 0):
                now = datetime.now()
                y, m, d, hh, mm, ss = now.year, now.month, now.day, now.hour, now.minute, now.second
            
            # 유효한 날짜인지 검증
            ymd = datetime(y, m, d, hh, mm, ss)  
        except ValueError as e:
            raise KavanaValueError(f"YMDTIME: 잘못된 날짜 형식입니다: {e}")

        args = [y, m, d, hh, mm, ss]
        return YmdTimeToken(arguments=args)

    @staticmethod
    def YMD(
        y: Optional[int] = 0, 
        m: Optional[int] = 0, 
        d: Optional[int] = 0
    ) -> YmdToken:
        try:
            # 모든 인자가 0이면 현재 날짜 사용
            if (y, m, d) == (0, 0, 0):
                today = date.today()
                y, m, d = today.year, today.month, today.day
            
            # 유효한 날짜인지 검증
            ymd = date(y, m, d)
        except ValueError as e:
            raise KavanaValueError(f"YMD:잘못된 날짜 형식입니다: {e}")

        args = [y, m, d]
        return YmdToken(arguments=args)

    @staticmethod
    def NOW() -> YmdTimeToken:
        return YmdTimeFunctions.YMDTIME()
    
    @staticmethod
    def TODAY() -> YmdToken:
        return YmdTimeFunctions.YMD()