from datetime import date, datetime
from typing import Optional, Union
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import StringToken, Token, YmdTimeToken, YmdToken
from lib.core.token_util import TokenUtil


class YmdTimeFunctions:
    ''' YmdTimeFunctions 클래스는 날짜 및 시간 관련 기능을 제공합니다. '''
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
            datetime(y, m, d, hh, mm, ss)  
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
            date(y, m, d)
        except ValueError as e:
            raise KavanaValueError(f"YMD:잘못된 날짜 형식입니다: {e}")

        args = [y, m, d]
        return YmdToken(arguments=args)

    @staticmethod
    def NOW() -> YmdTimeToken:
        ''' 현재 시간을 yyyy-mm-dd hh:mm:ss 형식으로 반환 '''
        return YmdTimeFunctions.YMDTIME()
    
    @staticmethod
    def TODAY() -> YmdToken:
        ''' 오늘을 yyyy-mm-dd 형식으로 반환 '''
        return YmdTimeFunctions.YMD()
    
    @staticmethod
    def WEEKDAY(date: Union[Ymd, YmdTime]) -> Token:
        ''' 요일을 0(월요일)부터 6(일요일)까지의 정수로 반환 '''
        d = date.weekday()
        # 월요일: 0, 화요일: 1, 수요일: 2, 목요일: 3, 금요일: 4, 토요일: 5, 일요일: 6
        return TokenUtil.integer_to_integer_token(d)

    @staticmethod
    def IS_WEEKEND(date: Union[Ymd, YmdTime]) -> Token:
        d = date.weekday()
        # 토요일: 5, 일요일: 6
        if d in (5, 6):
            return TokenUtil.boolean_to_boolean_token(True)
        return TokenUtil.boolean_to_boolean_token(False)
    
    @staticmethod
    def WEEK_NAME(date: Union[Ymd, YmdTime], type:str="korea-short") -> StringToken:
        d = date.weekday()
        # 월요일: 0, 화요일: 1, 수요일: 2, 목요일: 3, 금요일: 4, 토요일: 5, 일요일: 6
        korea_short = ["월", "화", "수", "목", "금", "토", "일"]
        korea_long = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        english_short = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        english_long = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        week_names = {
            "korea-short": korea_short, 
            "korea-long": korea_long,
            "english-short": english_short,
            "english-long": english_long
        }
        if type not in week_names:
            raise KavanaValueError(f"WEEK_NAME : 지원하지 않는 요일 형식입니다: {type}")
        name = week_names[type]
        
        return TokenUtil.string_to_string_token(name[d])

    @staticmethod
    def YMD_FORMAT(date: Union[Ymd, YmdTime], format: str) -> StringToken:
        """
        주어진 날짜를 지정된 형식(format)으로 문자열로 변환합니다.

        예:
        YMD_FORMAT(Ymd(2025, 5, 1), "%Y-%m-%d") → "2025-05-01"
        YMD_FORMAT(YmdTime(2025, 5, 1, 12, 30, 45), "%Y-%m-%d %H:%M:%S") → "2025-05-01 12:30:45"
        """
        try:
            # 지정된 형식으로 변환
            formatted_date = date.strftime(format)
            return TokenUtil.string_to_string_token(formatted_date)
        except Exception as e:
            YmdTimeFunctions.executor.log_command("ERROR", f"YMD_FORMAT: 날짜 형식 변환 중 오류 발생: {e}")
            raise KavanaValueError(f"YMD_FORMAT: 날짜 형식 변환 중 오류가 발생했습니다: {e}")    