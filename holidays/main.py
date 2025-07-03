import sys
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

def get_holiday_data(year, month):
    """GODATA API에서 휴일 정보를 가져옵니다."""
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    
    params = {
        'serviceKey': os.getenv('GODATA_API_KEY'),
        'solYear': year,
        'solMonth': f"{month:02d}"  # 월을 2자리로 포맷
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None

def parse_xml_response(xml_data):
    """XML 응답을 파싱하여 휴일 정보를 추출합니다."""
    holidays = []
    
    try:
        root = ET.fromstring(xml_data)
        
        # 먼저 OpenAPI 서비스 에러 확인
        err_msg = root.find('.//errMsg')
        if err_msg is not None:
            return_auth_msg = root.find('.//returnAuthMsg')
            return_reason_code = root.find('.//returnReasonCode')
            
            error_details = f"API 서비스 오류: {err_msg.text}"
            if return_auth_msg is not None:
                error_details += f" - {return_auth_msg.text}"
            if return_reason_code is not None:
                error_details += f" (코드: {return_reason_code.text})"
            
            print(error_details)
            return holidays
        
        # resultCode 확인
        result_code = root.find('.//resultCode')
        if result_code is not None and result_code.text != '00':
            result_msg = root.find('.//resultMsg')
            print(f"API 오류: {result_msg.text if result_msg is not None else 'Unknown error'}")
            return holidays
        
        # items에서 휴일 정보 추출
        items = root.findall('.//item')
        for item in items:
            locdate = item.find('locdate')
            date_name = item.find('dateName')
            is_holiday = item.find('isHoliday')
            
            if (locdate is not None and date_name is not None and 
                is_holiday is not None and is_holiday.text == 'Y'):
                holidays.append((locdate.text, date_name.text))
                
    except ET.ParseError as e:
        print(f"XML 파싱 오류: {e}")
    
    return holidays

def get_year_holidays(year):
    """연도별 모든 휴일 정보를 가져옵니다."""
    all_holidays = []
    
    for month in range(1, 13):
        xml_data = get_holiday_data(year, month)
        if xml_data:
            holidays = parse_xml_response(xml_data)
            all_holidays.extend(holidays)
    
    return all_holidays

def get_month_holidays(year, month):
    """특정 년월의 휴일 정보를 가져옵니다."""
    xml_data = get_holiday_data(year, month)
    if xml_data:
        return parse_xml_response(xml_data)
    return []

def print_holidays_csv(holidays):
    """휴일 정보를 CSV 형태로 출력합니다."""
    for locdate, date_name in holidays:
        print(f"{locdate}, {date_name}")

def main():
    if len(sys.argv) < 2:
        print("사용법:")
        print("  holidays yyyy      - 해당 연도의 모든 휴일")
        print("  holidays yyyy mm   - 해당 연월의 휴일")
        sys.exit(1)
    
    try:
        year = int(sys.argv[1])
        
        if len(sys.argv) == 2:
            # 연도만 입력된 경우: 해당 연도의 모든 휴일
            holidays = get_year_holidays(year)
        elif len(sys.argv) == 3:
            # 연도와 월이 입력된 경우: 해당 연월의 휴일
            month = int(sys.argv[2])
            if month < 1 or month > 12:
                print("월은 1-12 사이의 값이어야 합니다.")
                sys.exit(1)
            holidays = get_month_holidays(year, month)
        else:
            print("인자가 너무 많습니다.")
            sys.exit(1)
        
        print_holidays_csv(holidays)
        
    except ValueError:
        print("연도와 월은 숫자여야 합니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
