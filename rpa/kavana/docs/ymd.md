# Ymd 타입 기본 개념

## YYYY-MM-DD 형식의 날짜를 저장하는 데이터 타입

Date 타입과 달리 시간 정보는 포함하지 않음
Ymd 타입을 사용할 때의 문법
✅ SET ymd1 = 2025-03-05 → YYYY-MM-DD 형식을 Ymd 타입으로 자동 변환
✅ SET ymd2 = YMD("2025-03-05") → 명확하게 Ymd 타입을 지정

## Ymd 타입 관련 연산 및 내장 함수

ADD_DAYS(Ymd, N): N일을 더한 새로운 Ymd 반환
DIFF_DAYS(Ymd1, Ymd2): 두 Ymd 간 일(day) 단위 차이 반환
TO_DATE(Ymd): Date 타입으로 변환
FROM_DATE(Date): Date → Ymd 변환
FORMAT(Ymd, "YYYY/MM/DD"): 지정된 형식으로 변환

## Ymd 타입과 다른 타입의 관계

Ymd + Integer (날짜 연산 가능)
Ymd - Ymd (일(day) 단위 차이 반환)
Ymd를 String으로 변환 시 "2025-03-05" 형태 유지