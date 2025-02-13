from datetime import datetime, timedelta
import time
import requests
import xml.etree.ElementTree as ET
from config import Config

GODATA_URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'

def get_holiday_list(year: int, month: int):
    """특정 연도와 월의 공휴일 목록을 OpenAPI에서 가져와 리스트로 반환"""
    time.sleep(1)  # OpenAPI 요청 제한 방지를 위한 대기 시간
    API_KEY = Config.GODATA_API_KEY
    params = {'serviceKey': API_KEY, 'solYear': year, 'solMonth': f"{month:02d}"}

    response = requests.get(GODATA_URL, params=params, verify=False)

    if response.status_code != 200:
        print(f"❌ OpenAPI 요청 실패: {response.status_code}")
        return []

    # XML 파싱
    root = ET.fromstring(response.text)
    holidays = [item.find("locdate").text for item in root.findall(".//item") if item.find("isHoliday").text == "Y"]

    return holidays

def get_prev_year_month(year: int, month: int):
    """주어진 연도와 월의 이전 달을 반환 (예: 2024, 12)"""
    first_day_of_this_month = datetime(year, month, 1)
    prev_month = first_day_of_this_month - timedelta(days=1)
    return prev_month.year, prev_month.month

def get_prev_working_day(year: int, month: int, day: int):
    """
    특정 날짜(year, month, day) 이전의 가장 가까운 영업일을 찾음.
    """
    target_date = datetime(year, month, day)  # 지정된 날짜
    prev_day = target_date - timedelta(days=1)  # 하루 전부터 검사 시작

    # 현재 & 이전 달의 공휴일 정보 가져오기
    listHoliday = get_holiday_list(year, month) + get_holiday_list(*get_prev_year_month(year, month))

    while True:
        prev_str = prev_day.strftime("%Y%m%d")  # yyyymmdd 형식 변환
        if prev_day.weekday() in [5, 6] or prev_str in listHoliday:  # 토요일, 일요일, 공휴일 체크
            prev_day -= timedelta(days=1)  # 하루 전으로 이동
        else:
            return prev_str  # 영업일이면 해당 날짜 반환

def get_today():
    """현재 연도, 월, 일을 반환"""
    now = datetime.now()
    return now.year, now.month, now.day

def prev_day():
    """어제 날짜를 반환"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.year, yesterday.month, yesterday.day

def todayYmd():
    """오늘 날짜를 yyyymmdd 형식으로 반환"""
    today = datetime.now()
    return today.strftime("%Y%m%d")