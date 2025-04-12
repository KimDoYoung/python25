# OCR & 브라우저 명령어

## 개요

- EasyOCR을 선택 : 설치 간단 및 한국어 지원
- Selenium 을 선택

## 📘 OCR 명령어 목록 (Kavana)

### FIX

```kvs
OCR READ from_file="screen.png", to_var="text1"
OCR READ from_var=img1, area=(100, 200, 300, 100), to_var="text1"

OCR FIND text="계좌번호", from_file="screen.png", area=area1, to_var="found_point"
OCR GET_ALL from_var=img1, to_var="ocr_results"
```

### ✅ READ

- 영역 또는 이미지에서 문자열을 읽어들인다.
- 옵션들
  - `region`: 텍스트를 추출할 REGION 객체
  - `rectangle`: 텍스트를 추출할 RECTANGLE 객체
  - `image_path`: 이미지 파일 경로 (`"path/to/image.png"`)
  - `image`: IMAGE 객체
  - `to_var`: 추출된 텍스트를 저장할 변수명

```kvs
OCR READ region=r1, to_var=text1
OCR READ rectangle=rect1, to_var=text1
OCR READ image_path="name.png", to_var=text1
OCR READ image=image1, to_var=text1
```

### FIND

- 특정 단어를 영역이나 이미지에서 찾는다. 찾은 좌표를 리턴
- 옵션들
  - text: 찾고자 하는 문자열
  - area
  - from_file
  - from_var
  - to_var : 저장할 좌표
  - to_file

```kvs
OCR FIND text="로그인" region=r1, to_var="found_point"
OCR FIND text="계좌번호" image_path="screen.png", to_var="p1"
```

### GET_ALL

- 영역이나 이미지에서 모든 text를 추출해서 배열로 리턴
- 옵션들
  - region, rectangle, image_path, image
  - to_var: 결과 리스트(Array)를 저장할 변수

```kvs
OCR GET_ALL image_path="report.png", to_var="ocr_results"
OCR GET_ALL region=r1, to_var="text_infos"
```

- 결과

```json
[
  { "text": "로그인", "point": {x:100, y:200}, "confidence": 0.92 },
  { "text": "비밀번호", "point": {x:150, y:250}, "confidence": 0.88 }
]
```

## BROWSER command

- 명령어 : BROWSER
- sub 명령어들
  - OPEN
  - CLOSE
  - FIND
  - CLICK
  - PUT_TEXT
  - GET_TEXT
  - EXISTS
  - CLOSE
  - WAIT
  - SCREEN_SHOT

```kvs
BROWSER OPEN url="https://naver.com" headless=True
BROWSER TYPE selector="#query" text="kavana" clear_before=True
BROWSER CLICK selector=".btn_search"
BROWSER WAIT selector=".result" until="visible" timeout=5
BROWSER GET_TEXT selector=".result-title" to_var="firstTitle"
BROWSER CAPTURE path="search_result.png"
BROWSER CLOSE
```

SCROLL_TO 요소로 스크롤 이동
SWITCH_IFRAME iframe 전환
ASSERT_TEXT 특정 텍스트 존재 여부 검증
WAIT_FOR_TEXT 특정 텍스트가 나올 때까지 대기

## Extract

- select 추출할 요소 선택자
- select_by 선택자 방식: css(기본), xpath, id
- within 탐색 범위를 제한할 상위 요소 셀렉터
- attr 추출할 속성: src, href, text 등
- to_var 결과 저장 변수 이름

## click

- select 클릭할 대상 요소 셀렉터
- select_by 셀렉터 방식 (css, xpath, id)
- timeout 요소 대기 시간 (초)
- scroll_first 클릭 전 스크롤 여부 (기본값 True)
- click_js .click() 대신 JS 방식 클릭 (기본값 False)
- within select를 할 대상

```kvs
BROWSER click select=".buy-btn" within=".product" select_by="css" scroll_first=True click_js=False
```

## put_text

- select 입력할 input/select 요소
- select_by css, xpath, id
- within 상위 요소 범위 제한
- text 입력할 문자열
- clear_before 기존 텍스트 지우고 입력할지 여부
- scroll_first 입력 전 스크롤할지 여부 (기본 True)

## get_text

- select 어떤 요소에서 텍스트를 추출할지 ✅ 있음
- within 특정 요소 내부 범위에서만 탐색 ✅ 있음
- select_by 선택자 방식 (기본값 css) ✅ 있음
- scroll_first 스크롤 후 추출 안정성 확보 ✅ 있음
- to_var 추출한 값을 변수로 저장 ✅ 있음
- timeout default 10
- attr : 'text','value'

```kvs
BROWSER GET_TEXT select="#product-name" within=".product" scroll_first=True to_var="product_name"
```

## catpure

- to_file

BROWSER CAPTURE select=".item" to_file="item_#.png" multi=True
BROWSER to_file="full-screen.png"

## execute_js

- script 실행할 JS 코드
- select (선택) 대상 요소 지정
- select_by css, xpath, id
- within (선택) 검색 범위
- scroll_first (선택) 요소에 대해 실행할 경우 스크롤 이동
- to_var (선택) 실행 결과 저장할 변수명

```kvs
BROWSER EXECUTE_JS script="return document.title" to_var="title"
BROWSER EXECUTE_JS select=".price" script="return arguments[0].innerText" to_var="price"
BROWSER EXECUTE_JS select="#button" script="arguments[0].click();"
```

## find_elements

- 현재 구현이 의미 없음

```python
@dataclass
class ElementPointerToken(KavanaDataType):
    selector: str
    index: int
```

- extract에 attr 옵션을 넣다.

```
BROWSER EXTRACT select=".product" attr="data-id" to_var="ids"

for id in ids:
    BROWSER EXECUTE_JS script="console.log(arguments[0])" select=f".product[data-id='{id}']"
```

## switch_frame

- select iframe 요소 셀렉터
- select_by 셀렉터 타입 (css, xpath, id)
- within (선택) 상위 영역 안에서 검색
- to_default True일 경우 기본 페이지로 복귀
- scroll_first (선택) 진입 전 iframe 뷰포트 이동 (기본: True)

```kvs
BROWSER SWITCH_TO_FRAME select="iframe[name='preview']"
BROWSER SWITCH_TO_FRAME to_default=True
```
