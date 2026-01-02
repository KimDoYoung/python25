from datetime import datetime, timedelta
import os
import time
import requests
import xml.etree.ElementTree as ET
from config import Config
from logger import Logger
log = Logger()
GODATA_URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'

def get_holiday_list(year: int, month: int):
    """특정 연도와 월의 공휴일 목록을 OpenAPI에서 가져와 리스트로 반환"""
    time.sleep(1)  # OpenAPI 요청 제한 방지를 위한 대기 시간
    API_KEY = Config.GODATA_API_KEY
    params = {'serviceKey': API_KEY, 'solYear': year, 'solMonth': f"{month:02d}"}

    response = requests.get(GODATA_URL, params=params, verify=False)

    if response.status_code != 200:
        print(f"❌ OpenAPI 요청 실패: {response.status_code}, {response.text}")
        log.error(f"OpenAPI 요청 실패: {response.status_code}, {response.text}")
        holiday_file = Config.HOLIDAY_FILE
        if holiday_file and os.path.exists(holiday_file):
            with open(holiday_file, 'r', encoding='utf-8') as f:
                holidays = [line.strip() for line in f if line.strip()]
            log.info(f"로컬 공휴일 파일에서 공휴일 목록 로드: {holiday_file}")    
            return holidays
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
        
def get_prev_working_3day(year: int, month: int, day: int):
    """
    특정 날짜(year, month, day) 이전의 영업일3일 전 날짜를 찾음.
    """
    target_date = datetime(year, month, day)  # 지정된 날짜
    prev_day = target_date - timedelta(days=1)  # 하루 전부터 검사 시작

    # 현재 & 이전 달의 공휴일 정보 가져오기
    listHoliday = get_holiday_list(year, month) + get_holiday_list(*get_prev_year_month(year, month))

    working_day_count = 0  # 영업일 카운트
    while True:
        prev_str = prev_day.strftime("%Y%m%d")  # yyyymmdd 형식 변환
        if prev_day.weekday() in [5, 6] or prev_str in listHoliday:  # 토요일, 일요일, 공휴일 체크
            prev_day -= timedelta(days=1)  # 하루 전으로 이동
        else:
            working_day_count += 1  # 영업일 카운트 증가
            if working_day_count == 3:  # 영업일 3개를 찾으면
                return prev_str  # 3영업일 전 날짜 반환
            prev_day -= timedelta(days=1)  # 하루 전으로 이동        

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

def isTodayAHoliday() -> bool:
    """오늘 날짜가 공휴일인지 여부를 반환"""
    today = datetime.now()
    # today 가 토요일이거나 일요일이면 공휴일
    if today.weekday() in [5, 6]:
        return True
    # 오늘이 공휴일 목록에 있는지 확인
    listHoliday = get_holiday_list(today.year, today.month)
    return today.strftime("%Y%m%d") in listHoliday

def isHoliday(ymd: str) -> bool:
    """주어진 날짜(YYYYMMDD 형식)가 공휴일인지 여부를 반환"""
    try:
        date_obj = datetime.strptime(ymd, "%Y%m%d")
    except ValueError:
        raise ValueError("날짜 형식이 잘못되었습니다. YYYYMMDD 형식으로 입력하세요.")

    # 해당 날짜가 주말(토요일 or 일요일)인지 확인
    if date_obj.weekday() in [5, 6]:  # 5: 토요일, 6: 일요일
        return True

    # 해당 날짜가 공휴일 목록에 있는지 확인
    listHoliday = get_holiday_list(date_obj.year, date_obj.month)
    return ymd in listHoliday