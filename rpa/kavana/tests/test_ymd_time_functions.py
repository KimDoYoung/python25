import pytest
from datetime import datetime, date
from lib.core.builtins.ymd_time_functions import YmdTimeFunctions

# 필요한 Mock 클래스 정의
class MockYmd:
    def __init__(self, dt):
        self.data = dt

class MockYmdTime(MockYmd):
    def __init__(self, dt):
        super().__init__(dt)
        self.value = dt
    def weekday(self):
        return self.value.weekday()

    def is_weekend(self):
        return self.weekday() in (5, 6)  # 5: Saturday, 6: Sunday

class MockToken:
    def __init__(self, value):
        self.value = value
class MockTokenUtil:
    @staticmethod
    def integer_to_integer_token(val):
        return MockToken(val)

    @staticmethod
    def boolean_to_boolean_token(val):
        return MockToken(val)

# 실제 TokenUtil을 Mock으로 대체
YmdTimeFunctions.TokenUtil = MockTokenUtil

def test_YMDTIME_now():
    token = YmdTimeFunctions.YMDTIME()
    assert isinstance(token.arguments, list)
    assert len(token.arguments) == 6

def test_YMD_valid():
    token = YmdTimeFunctions.YMD(2024, 4, 30)
    assert token.arguments == [2024, 4, 30]

def test_YMD_invalid():
    with pytest.raises(Exception):
        YmdTimeFunctions.YMD(2024, 2, 30)

def test_WEEKDAY():
    dt = datetime(2024, 4, 29)  # 월요일
    weekday_token = YmdTimeFunctions.WEEKDAY(MockYmdTime(dt))
    assert weekday_token.data.value == 0

def test_IS_WEEKEND_true():
    dt = datetime(2024, 4, 28)  # 일요일
    result = YmdTimeFunctions.IS_WEEKEND(MockYmdTime(dt))
    assert result.data.value is True

def test_IS_WEEKEND_false():
    dt = datetime(2024, 4, 29)  # 월요일
    result = YmdTimeFunctions.IS_WEEKEND(MockYmdTime(dt))
    assert result.data.value is False

def test_WEEK_NAME_korean_short():
    dt = datetime(2024, 4, 29)  # 월요일
    token = YmdTimeFunctions.WEEK_NAME(MockYmdTime(dt), type="korea-short")
    assert token.data.value == "월"

def test_WEEK_NAME_english_long():
    dt = datetime(2024, 5, 1)  # 수요일
    token = YmdTimeFunctions.WEEK_NAME(MockYmdTime(dt), type="english-long")
    assert token.data.value == "Wednesday"