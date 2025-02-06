# auto_esafe

## 개요

1. eSAFE2019을 실행
2. 공인인증서로 로그인(하드에 존재)
3. 화면번호를 입력
4. 파일 다운로드
5. 종료

## 제약조건

1. 화면 크기 FHD에서 동작
2. 공인인증서는 하드에 존재.

## 기능 

1. .env를 사용함. password저장
2. config에 상수 보관
3. log폴더에 auto_esafe_yyyy_mm_dd.log 생성
4. 매일 특정시간에 동작하는 것을 기본으로 함(window자체 scheduler사용)