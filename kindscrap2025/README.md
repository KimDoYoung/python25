# kindscrap

## 개요

- [KIND사이트의 상세검색](https://kind.krx.co.kr/disclosure/details.do?method=searchDetailsMain)에서 공시정보를 Scrapping
- 일자범위내에서 검색, 하나씩 scrapping해서 sqlite3 db에 넣음.
- kindscrap.py 1개의 파일로 동작
- 명령어 라인 : python3 main.py <start yyyy-mm-dd> <end yyyy-mm-dd> all | page_index

- data폴더 하위에 sqlite3이 kindscrap_start_endday.sqlite3의 형식으로 생성됨

- 페이지를 scrapping하는 것임 특별한 api_key같은 것은 없슴
- selenium 사용
- 설정값 .env.real이 같은 폴더에 존재해야 함

- 2025.3.17 : linux용으로 개발한 것을,윈도우11 용으로 수정함. exe파일로 만듬



## run.sh

- 오전 1시쯤에 동작하고  start-day와 end-day를 그 전날로 설정한다.

## run_kindscrap.bat

- run.sh에 해당하는 윈도우  batch
- 하루전 날짜를 계산해한다. 
- 만약 실패를 하면 한번 더 수행한다

## 빌드(버젼업)
- venv 사용됨
- setting.py에 버젼정보
- which python
- which pyinstaller
- pyinstaller main.py

## history

| 날짜         | 버전   | 변경 사항                                                                                   |
|--------------|--------|---------------------------------------------------------------------------------------------|
| 2025-05-19   | v1.1   | content를 DB에서 제거함 (용량 문제로 인해)                                                  |
| 2025-05-19   | v1.2   | content와 text_only를 DB에서 제거, stkcode만 추출, 시간 저장 기능 추가                      |
| 2025-08-05   | v1.3   | 7.30, 8.1 스크래핑 실패 → 재시도 가능, `run_kindscrapping.bat`에서 실패 시 10초 후 재실행 추가, <br>로그를 더 세밀하게 기록하도록 개선 |
            