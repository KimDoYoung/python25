"""
working_days 모듈의 함수들을 테스트하는 스크립트
사용법: python test_holiday.py YYYYMMDD
예: python test_holiday.py 20251226
"""

import sys
import os

# 상위 디렉토리를 경로에 추가하여 모듈 import 가능하도록 설정
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from working_days import get_prev_working_day, isHoliday
from logger import Logger

# Logger 인스턴스 생성
log = Logger()

def main():
    """메인 함수"""
    # 인자 체크
    if len(sys.argv) != 2:
        print("사용법: python test_holiday.py YYYYMMDD")
        print("예: python test_holiday.py 20251226")
        sys.exit(1)
    
    date_str = sys.argv[1]
    
    # 날짜 형식 검증
    if len(date_str) != 8 or not date_str.isdigit():
        print("❌ 잘못된 형식입니다. YYYYMMDD 형식으로 입력하세요.")
        sys.exit(1)
    
    try:
        # 날짜 파싱
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        
        # isHoliday 테스트
        is_holiday = isHoliday(date_str)
        holiday_status = "휴일" if is_holiday else "휴일아님"
        
        # get_prev_working_day 테스트
        prev_working = get_prev_working_day(year, month, day)
        
        # 결과 출력
        print(f"{date_str} -> {holiday_status}")
        print(f"이전 근무일: {prev_working}")
        
        # 로그 기록
        log.info(f"테스트 날짜: {date_str}, 결과: {holiday_status}, 이전 근무일: {prev_working}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        log.error(f"테스트 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
