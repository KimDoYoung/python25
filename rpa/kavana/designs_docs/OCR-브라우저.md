# OCR & 브라우저 명령어

## 개요

- EasyOCR을 선택 : 설치 간단 및 한국어 지원
- Selenium 을 선택

## 📘 OCR 명령어 목록 (Kavana)

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
    - region 
    - retangle
    - image_path
    - image
    - to_var : 저장할 좌표
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
SCROLL_TO	요소로 스크롤 이동
SWITCH_IFRAME	iframe 전환
ASSERT_TEXT	특정 텍스트 존재 여부 검증
WAIT_FOR_TEXT	특정 텍스트가 나올 때까지 대기
### 옵션들
url	접속할 URL	"https://example.com"
selector	CSS, XPath 등 요소 선택자	"#login", "//button[text()='확인']"
selector_type	선택자 방식 (css, xpath, id)	"css" (기본값), "xpath"
text	입력할 텍스트	"admin123"
until	요소 상태 조건 (visible, clickable)	"visible"
timeout	대기 시간 (초)	10
clear_before	입력 전 내용 비우기 여부	True, False
to_var	결과 저장할 변수명 (executor.set_var 대상)	"resultText", "isVisible"
path	이미지 저장 경로	"screen.png"
script	실행할 JS 코드	"return document.title"
headless	브라우저 headless 모드 여부	True, False
window_size	브라우저 창 크기	"1920x1080"
user_agent	브라우저 User-Agent 문자열	"Mozilla/5.0 ...", "custom-bot"
full_page	전체 페이지 스크린샷 여부	True, False

