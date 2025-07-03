# holidays

## 개요
GODATA 의 휴일 정보를 이용하여 휴일정보를 가져온다.

## EXE로 빌드

- make.sh을 사용하여 1개의 exe로 빌드해서 사용한다.

## 사용법
- 인자로 yyyy, mm을 받으면 년도, 월의 휴일 정보를 csv 형태로 출력
- 인자로 yyyy을 받으면 그 년도의 모든 휴일정보를 csv 형태로 출력
```bash
- holidays yyyy mm
- holidays yyyy
```

## 기능
1. url : http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo에 
2. params :  serviceKey,solYear, solMonth 를 붙여서 호출
3. serviceKey는 .env에 GODATA_API_KEY에 기록되어 있음
4. response는 xml로 아래와 같은 형태임.
```xml
<response>
<header>
<resultCode>00</resultCode>
<resultMsg>NORMAL SERVICE.</resultMsg>
</header>
<body>
<items>
<item>
<dateKind>01</dateKind>
<dateName>1월1일</dateName>
<isHoliday>Y</isHoliday>
<locdate>20220101</locdate>
<seq>1</seq>
</item>
<item>
<dateKind>01</dateKind>
<dateName>설날</dateName>
<isHoliday>Y</isHoliday>
<locdate>20220131</locdate>
<seq>1</seq>
</item>
</items>
<numOfRows>10</numOfRows>
<pageNo>1</pageNo>
<totalCount>2</totalCount>
</body>
</response>
```
5. 인자로 yyyy를 받으면 yyyy 01 ~ 12 까지 호출, csv형태로 출력
```text
202220101, 1월1일
202220101, 설날
```
6. 인자로 yyyy mm 2개를 받으면 해당하는 yyyy,mm의 결과를 csv형태로 출력
7. logging없음
8. dotenv사용
