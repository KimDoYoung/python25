# kavana-script 명령어들

Kavana Script에서 사용 가능한 명령어와 그 사용법을 정리한 문서입니다.

## **기본 명령어**

### 🔶SET

- 변수를 설정합니다.
- **문법**

> SET = <표현식>

- **사용 예**

```kvs
SET a = "123"
SET a = 1 + 2 
```

### 🔶PRINT

- 문자열을 인쇄합니다.
- 문자열은 python과 유사하게 첨자 r(raw), f(format)을 지원합니다.
- 여러 인자를 콤마로 분리할 수 있습니다
- **문법**

> PRINT <문자열>, <문자열>, ...

- **사용예**

```kvs
SET name = "Hong"
PRINT name 
PRINT "abc", f"{name}"
```

### 🔶LOG

- 로그파일은 일자별로 생성되는 것으로 확정했습니다.
- LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR 명령어로 구성됩니다.

> LOG_DEBUG <문자열> ...

- LOG_CONFIG 명령어로 설정을 변경할 수 있습니다.
  
> LOG_CONFIG dir=<문자열>, prefix=<문자열>, level=문자열

- dir의 디폴트는 ./logs 입니다. 로그파일이 저장될 폴더입니다.
- prefix는 로그파일의 시작문자열입니다. 즉 my_app 일 경우 파일명은 my_app-yyyy-mm-dd.log 가 됩니다.
- prefix는 디폴트값이 'kavana'입니다.
- 로그파일이 존재하면 그 파일에 추가됩니다.
- level 은 로그를 인쇄할 때의 level입니다. (DEBUG < INFO < WARN < ERROR)
- level이 INFO이면 LOG_DEBUG는 인쇄하지 않습니다.

```kvs
MAIN
    LOG_INFO "--------------------------------------------------"
    LOG_INFO "프로그램 시작"
    LOG_INFO "--------------------------------------------------"
    SET var1 = 100
    SET var2 = 50
    LOG_CONFIG dir="./logs/my_app", prefix="my_app", level="DEBUG"
    LOG_INFO f"시스템 정상 실행 중. var1 = {var1}"
    LOG_WARN f"경고 발생! var1 + var2 = { var1 + var2 }"
    LOG_ERROR f"에러 발생! var1이 50보다 큰가? {var1 > 50}"
    LOG_DEBUG f"디버깅: 현재 값은 var1={var1}, var2={var2}"
    LOG_INFO "--------------------------------------------------"
    LOG_INFO "프로그램 종료"
    LOG_INFO "--------------------------------------------------"
END_MAIN
```

- 위 프로그램을 실행하면 .kvs가 존재하는 폴더 하위에  logs/kavana-yyyy-mm-dd.log에 LOG_INFO 3라인이 인쇄됩니다.
- 그 후 LOG_CONFIG가 실행되어 log파일의 위치가 logs/my_app/my_app-yyyy-mm-dd.log로 변경됩니다.
- 그 후의 로그명령어는 변경된 파일에 인쇄됩니다.
  
### 🔶INCLUDE

- 외부파일 kvs를 읽어 들여서 명령어를 확장한다.
- 외부파일 kvs에는 상수와 사용자함수만이 정의되어야 한다.
- **문법**

> INCLUDE <문자열:파일패스>

- **사용예**

```kvs
 INCLUDE "./lib/global.kvs"
 INCLUDE "./common.kvs"
```

### 🔶LOAD_ENV

- dot-env파일을 읽어들여서 상수로 처리한다.
- 각 key는 $key 변수로 설정됩니다.
  
- **문법**

> LOAD <문자열:ENV파일패스>

- **사용예**

```kvs
LOAD_ENV ".env.test"
MAIN
    PRINT "{$MY_KEY}"
END_MAIN
```

### 🔶RAISE

- Exception을 발생시킵니다.
- **문법**

> RAISE <문자열:에러메세지>, <정수:Exit코드>

> 묵시적으로 $EXCEPTION_MESSAGE, $EXIT_CODE 변수가 설정됩니다.

- **사용예**

```kvs  
RAISE // 인자없이 사용, $EXCEPTION_MESSAGE에 `에러가 발생했습니다`저장, $EXIT_CODE에 0 저장
RAISE "에러가 발생했습니다" // 문자열은 $EXCEPTION_MESSAGE에 저장저장됩니다.
RAISE "에러발생", 1       // 1 은 $EXIT_CODE에 저장됩니다.
ON_EXCEPTION
    PRINT $EXCEPTION_MESSAGE, $EXIT_CODE
END_EXCEPTION

```

## **RPA 명령어**

### 🔷APP_OPEN

- **설명**

> `APP_OPEN` 명령어는 미리 정의된 애플리케이션 객체를 실행하는 데 사용됩니다.  
> 실행 시 창을 최대화할지, 포커스를 줄지, 또는 특정 프로세스 이름을 사용할지 등의 옵션을 함께 지정할 수 있습니다.  
> 이 명령어는 최소한 하나의 인자(애플리케이션 변수)를 필요로 하며, 선택적으로 여러 옵션을 함께 사용할 수 있습니다.

---

- **문법**

> `APP_OPEN` `app_variable` [`maximize=boolean`, `focus=boolean`, `process_name=string`]

- `app_variable`: 실행할 애플리케이션 객체 변수명 (필수)
- `maximize`: 애플리케이션 실행 시 창을 최대화할지 여부 (기본값: false)
- `focus`: 애플리케이션 실행 후 포커스를 줄지 여부 (기본값: true)
- `process_name`: 실행할 프로세스 이름을 명시적으로 지정할 경우 사용 (기본값: None)

---

- **옵션 설명**

| 옵션명         | 타입     | 설명                                           | 기본값   |
|----------------|----------|------------------------------------------------|----------|
| `maximize`     | BOOLEAN  | 창을 최대화할지 여부                          | `false`  |
| `focus`        | BOOLEAN  | 실행 후 포커스를 줄지 여부                    | `true`   |
| `process_name` | STRING   | 실행할 프로세스의 이름을 명시적으로 지정      | `None`   |

> ⚠️ 옵션은 `key=value` 형식으로 작성하며, 여러 옵션은 `,`(쉼표)로 구분합니다.

---

- **사용 예**

```kvs
APP_OPEN myApp
APP_OPEN myApp maximize=True, focus=False
APP_OPEN myApp process_name="notepad.exe"
```

### 🔷APP CLOSE

- **설명**

> `APP_CLOSE` 명령어는 실행 중인 애플리케이션 객체를 종료하는 데 사용됩니다.  
> 지정된 애플리케이션 변수는 반드시 `Application` 타입이어야 하며, 해당 변수가 올바르게 정의되어 있어야 합니다.  
> 이 명령어는 추가적인 옵션 없이 간단하게 사용됩니다.

---

- **문법**

> `APP_CLOSE <app_variable>`

- `app_variable`: 종료할 애플리케이션 객체 변수명 (필수)

---

- **옵션 설명**

> 해당 명령어는 추가 옵션을 받지 않습니다.

---

- **사용 예**

```kvs
APP_CLOSE myApp
```

### 🔷CAPTURE SCREEN

- **설명**

> `CAPTURE_SCREEN` 명령어는 전체 화면 또는 지정된 영역의 스크린샷을 캡쳐하는 데 사용됩니다.  
> 캡쳐한 이미지는 변수로 저장하거나 파일로 저장할 수 있습니다.  
> 필수적으로 `var_to` 또는 `save_to` 옵션 중 하나 이상을 포함해야 합니다.

---

- **문법**

> `CAPTURE_SCREEN full, var_to=<string>, save_to=<string>`  
> `CAPTURE_SCREEN region|rectangle, var_to=<string>, save_to=<string>`

- `full`: 전체 화면을 캡쳐합니다.  
- `region`: 사전에 정의된 영역 변수를 캡쳐합니다.  
- `rectangle`: 좌표로 구성된 사각형 영역을 캡쳐합니다.  
- `var_to`: 캡쳐된 이미지를 저장할 변수명 (선택, `save_to`와 둘 중 하나는 필수)  
- `save_to`: 캡쳐된 이미지를 저장할 경로 (선택, `var_to`와 둘 중 하나는 필수)

---

- **옵션 설명**

| 옵션명      | 타입    | 설명                                       | 필수 여부 |
|-------------|---------|--------------------------------------------|------------|
| `var_to`    | STRING  | 캡쳐 이미지를 변수에 저장                 | ❌ (save_to가 없을 경우 필수) |
| `save_to`   | STRING  | 캡쳐 이미지를 파일로 저장                 | ❌ (var_to가 없을 경우 필수) |

> ⚠️ `var_to`, `save_to` 중 최소 하나는 반드시 지정해야 합니다.

---

- **사용 예**

```kvs
CAPTURE_SCREEN full, save_to="capture1.png"
CAPTURE_SCREEN full, var_to="img1"
CAPTURE_SCREEN full, var_to="img2", save_to="backup2.jpg"
SET r1 = REGION(x=100, y=100, width=300, height=200)
CAPTURE_SCREEN r1, save_to="region.png"

```

### 🔷CLICK

- **설명**

> `CLICK` 명령어는 화면의 특정 위치를 클릭하는 데 사용됩니다.  
> 정적인 좌표, 이미지 인식, 객체(Point, Region, Rectangle) 또는 명시적 키워드 인자를 사용하여 다양한 방식으로 클릭할 수 있습니다.  
> 옵션으로 클릭 횟수, 클릭 타입(싱글/더블), 클릭 지속 시간 등을 지정할 수 있습니다.

---

- **문법**

> `CLICK <x: int>, <y: int> [count=<int>] [duration=<float>] [type=<string>]`  
> `CLICK x=<int>, y=<int>, [count=<int>] [duration=<float>] [type=<string>]`  
> `CLICK image_path=<string>, confidence=<float>, region=<region>, grayscale=<boolean>, type=<string>`  
> `CLICK <Point|Region|Rectangle>, point_name=<string>, [count=<int>] [duration=<float>] [type=<string>]`

---

- **옵션 설명**

| 옵션명        | 타입     | 설명                                                   | 기본값     |
|---------------|----------|--------------------------------------------------------|------------|
| `x`, `y`      | INTEGER  | 클릭할 절대 좌표                                       | 필수 (x/y 방식) |
| `count`       | INTEGER  | 클릭 횟수                                              | `1`        |
| `duration`    | FLOAT    | 클릭 유지 시간 (초)                                    | `0.2`      |
| `type`        | STRING   | `"single"` 또는 `"double"` 클릭                         | `"single"` |
| `image_path`  | STRING   | 클릭할 이미지를 파일 경로로 지정                        | 필수 (이미지 방식) |
| `confidence`  | FLOAT    | 이미지 인식 신뢰도 (0.0 ~ 1.0)                          | `0.8`      |
| `region`      | REGION   | 이미지 검색을 제한할 영역 (성능 향상)                   | 없음       |
| `grayscale`   | BOOLEAN  | 이미지 비교 시 흑백 비교 여부                           | `false`    |
| `point_name`  | STRING   | 객체 기반 클릭 시 참조 포인트 이름 (`"center"`, `"left"` 등) | `"center"` |

---

- **사용 예**

```kvs
CLICK 100, 200  // 화면의 (100, 200) 좌표를 한 번 클릭합니다.

CLICK 300, 400 count=2 duration=0.1 type="double"  // (300, 400)을 더블 클릭하며, 클릭 간격은 0.1초입니다.

CLICK x=150, y=250  // 키워드 방식으로 좌표를 지정하여 클릭합니다.

CLICK image_path="button.png"  // button.png 이미지가 화면에서 탐지되면 해당 위치를 클릭합니다.

CLICK image_path="icon.png", confidence=0.9, grayscale=true  // 흑백 비교와 신뢰도 0.9로 icon.png 클릭

SET p1 = POINT(x=500, y=600)
CLICK p1  // p1 좌표 객체(Point)를 클릭합니다.

SET r1 = REGION(x=100, y=100, width=300, height=200)
CLICK r1 point_name="top_left"  // r1 영역의 좌측 상단 지점을 클릭합니다.

SET rect1 = RECTANGLE(x=50, y=50, width=100, height=100)
CLICK rect1 point_name="center", count=2  // rect1의 중심을 더블 클릭합니다.
```

### 🔷CLOSE CHILD WINDOWS

- **설명**

> `CLOSE_CHILD_WINDOWS` 명령어는 지정된 애플리케이션의 자식 윈도우(팝업 창 등)를 모두 닫습니다.  
> 예를 들어, 문서 편집기에서 “찾기”, “설정”과 같은 서브 윈도우를 닫을 때 유용합니다.  
> 메인 윈도우는 닫지 않으며, 자식 윈도우만 대상으로 합니다.

---

- **문법**

> `CLOSE_CHILD_WINDOWS <app_variable>`

- `app_variable`: 자식 창을 닫을 대상 애플리케이션 객체 변수 (필수)

---

- **옵션 설명**

> 이 명령어는 옵션 없이 동작합니다.  
> 단, 지정된 변수는 반드시 `Application` 타입이어야 하며, 정의되어 있어야 합니다.

---

- **사용 예**

```kvs
CLOSE_CHILD_WINDOWS myApp  // myApp 애플리케이션의 자식 윈도우를 모두 닫습니다.

APP_OPEN myEditor
WAIT 2
CLOSE_CHILD_WINDOWS myEditor  // 에디터 실행 후 2초 대기 후 자식 창 닫기

APP_OPEN winApp process_name="wordpad.exe"
WAIT 3
CLOSE_CHILD_WINDOWS winApp  // WordPad의 자식 창 (예: “인쇄”, “서식”) 닫기
```

### 🔷GET_TEXT

- **설명**

> `GET_TEXT` 명령어는 현재 포커스된 UI 요소(텍스트 필드 등)의 내용을 복사하여 변수에 저장합니다.  
> 내부적으로 `Ctrl+A`, `Ctrl+C` 키를 자동으로 입력한 후 클립보드 내용을 읽어 변수에 할당합니다.

---

- **문법**

> `GET_TEXT var_to=<변수명>`

- `var_to`: 복사된 텍스트를 저장할 변수 이름 (필수)

---

- **옵션 설명**

| 옵션명     | 타입     | 설명                               | 필수 여부 |
|------------|----------|------------------------------------|------------|
| `var_to`   | STRING   | 복사한 텍스트를 저장할 변수명       | ✅ 필수     |

> ⚠️ 텍스트를 읽을 수 있는 상태(포커스된 텍스트 필드 등)에서 사용해야 합니다.  
> 클립보드에 다른 내용이 있을 경우, 그 내용이 저장될 수 있습니다.

---

- **사용 예**

```kvs
GET_TEXT var_to=text1  // 현재 화면의 텍스트를 복사하여 text1 변수에 저장

CLICK 300, 400
WAIT 0.5
GET_TEXT var_to=resultText  // 특정 위치 클릭 후 텍스트 가져오기

APP_OPEN myApp
WAIT 2
CLICK image_path="output_field.png"
WAIT 0.2
GET_TEXT var_to=fieldValue  // 애플리케이션의 출력 필드를 클릭 후 텍스트 추출
```

### 🔷PUT TEXT

- **설명**

> `PUT_TEXT` 명령어는 문자열을 현재 커서 위치에 입력(타이핑)합니다.  
> 키보드 입력과 동일한 방식으로 동작하며, 단일 문자열만 인자로 받습니다.  
> 여러 번 입력하거나 변수로 관리하고 싶다면 `SET` 명령어와 함께 사용할 수 있습니다.

---

- **문법**

> `PUT_TEXT <string>`

- `<string>`: 입력할 문자열 (필수)

---

- **옵션 설명**

> 별도의 키워드 옵션 없이 문자열 표현식만 받습니다.  
> 복잡한 표현식을 사용할 경우에는 `SET` 명령어로 먼저 변수에 저장한 후 활용할 수 있습니다.

---

- **사용 예**

```kvs
PUT_TEXT "Hello, world!"  // 커서 위치에 "Hello, world!" 입력

PUT_TEXT "사용자 이름을 입력하세요"  // 한글 문자열도 정상 입력됩니다.

SET name = "홍길동"
PUT_TEXT name  // 변수에 저장된 문자열을 입력합니다.

SET content = "Line1\\nLine2\\nLine3"
PUT_TEXT content  // 줄바꿈 문자를 포함한 텍스트 입력

WAIT 1
PUT_TEXT "다음 페이지로 이동 중..."  // 1초 대기 후 텍스트 입력
```

### 🔷KEY_IN

- **설명**

> `KEY_IN` 명령어는 키보드 입력을 자동으로 수행합니다.  
> 문자열 하나 또는 문자열 리스트(배열)를 입력받아 순서대로 타이핑하거나 단축키를 입력할 수 있습니다.  
> 입력 속도도 조절할 수 있습니다.

---

- **문법**

> `KEY_IN <string or array>, speed=<float>`

- `string`: 단일 문자열을 입력합니다.  
- `array`: 여러 문자열(예: 키 입력 조합)을 리스트로 입력합니다.  
- `speed`: 각 키 입력 사이의 대기 시간 (초 단위, 기본값: 0.5초)

---

- **옵션 설명**

| 옵션명     | 타입   | 설명                                      | 기본값   |
|------------|--------|-------------------------------------------|----------|
| `speed`    | FLOAT  | 키 입력 간 딜레이 시간 (초 단위)         | `0.5`    |

> ⚠️ 단일 키 입력은 문자열로, 여러 키 입력은 배열 형태로 입력해야 합니다.

---

- **사용 예**

```kvs
KEY_IN "hello world"  // "hello world"라는 문자열을 입력합니다.

KEY_IN ["ctrl+a", "ctrl+c"]  // Ctrl+A → Ctrl+C 키 조합을 순서대로 입력합니다.

KEY_IN "enter", speed=0.2  // Enter 키를 빠르게 한 번 입력합니다.

KEY_IN ["tab", "tab", "enter"], speed=0.3  // Tab → Tab → Enter 순으로 입력, 0.3초 간격

SET keys = ["ctrl+v", "enter"]
KEY_IN keys  // 미리 정의된 배열 변수로 입력합니다.

KEY_IN ["h", "e", "l", "l", "o"], speed=0.1  // 한 글자씩 입력하며 빠른 속도로 타이핑합니다.
```

### 🔷MOUSE MOVE

- **설명**

> `MOUSE_MOVE` 명령어는 마우스 커서를 특정 위치로 이동시키는 데 사용됩니다.  
> 이동 대상은 좌표, 이미지의 중심, 또는 `Point`, `Region`, `Rectangle` 객체가 될 수 있습니다.  
> 이동 속도는 `duration` 옵션을 통해 조절할 수 있습니다.

---

- **문법**

> `MOUSE_MOVE <x: int>, <y: int> [, duration=<float>]`  
> `MOUSE_MOVE x=<int>, y=<int> [, duration=<float>]`  
> `MOUSE_MOVE image_path=<string>, confidence=<float>, search_region=<region>, grayscale=<boolean>`  
> `MOUSE_MOVE <Point|Region|Rectangle>, point_name=<string>, duration=<float>`

---

- **옵션 설명**

| 옵션명          | 타입     | 설명                                                           | 기본값   |
|------------------|----------|----------------------------------------------------------------|----------|
| `x`, `y`          | INTEGER  | 마우스를 이동시킬 화면 좌표                                    | 필수 (좌표 방식) |
| `duration`        | FLOAT    | 마우스 이동에 걸리는 시간 (초)                                | `0.5`    |
| `image_path`      | STRING   | 기준 이미지 경로                                               | 필수 (이미지 방식) |
| `confidence`      | FLOAT    | 이미지 인식 신뢰도 (0.0 ~ 1.0)                                  | `0.8`    |
| `search_region`   | REGION   | 이미지 탐색 범위 지정                                          | 없음     |
| `grayscale`       | BOOLEAN  | 흑백 모드로 이미지 비교                                        | `false`  |
| `point_name`      | STRING   | `Region`, `Rectangle` 기준 이동 지점 (`"center"` 등)          | `"center"` |

---

- **사용 예**

```kvs
MOUSE_MOVE 200, 300  // (200, 300) 좌표로 마우스를 이동합니다.

MOUSE_MOVE 100, 150, duration=1.0  // (100, 150)으로 1초에 걸쳐 천천히 이동합니다.

MOUSE_MOVE x=500, y=400  // x, y를 명시적으로 지정하여 이동합니다.

MOUSE_MOVE image_path="submit.png"  // submit.png 이미지 중심으로 이동합니다.

MOUSE_MOVE image_path="ok.png", confidence=0.9, grayscale=true  // 신뢰도 0.9, 흑백비교로 OK 버튼 위치 탐색 후 이동

SET p1 = POINT(x=800, y=600)
MOUSE_MOVE p1  // p1 포인트로 마우스를 이동합니다.
```

### 🔷WAIT

- **설명**

> `WAIT` 명령어는 지정된 시간만큼 실행을 일시 정지하거나, 특정 이미지가 화면에 나타날 때까지 대기하는 데 사용됩니다.  
> `WAIT <초>` 방식은 단순 대기용이며,  
> `WAIT until ...` 방식은 이미지 인식 기반의 조건 대기입니다.

---

- **문법**

> `WAIT <seconds>`  
> `WAIT until image_path=<string>, timeout=<int>, confidence=<float>, region=<region>, grayscale=<boolean>`

---

- **옵션 설명 (`WAIT until` 사용 시)**

| 옵션명        | 타입     | 설명                                                      | 기본값     |
|---------------|----------|-----------------------------------------------------------|------------|
| `image_path`  | STRING   | 화면에 나타나기를 기다릴 이미지 경로                     | **필수**   |
| `timeout`     | INTEGER  | 최대 대기 시간 (초 단위)                                  | `60`       |
| `confidence`  | FLOAT    | 이미지 인식 신뢰도 (0.0 ~ 1.0)                             | `0.8`      |
| `region`      | REGION   | 이미지 검색 범위 (전체화면이 기본)                        | `None`     |
| `grayscale`   | BOOLEAN  | 흑백 비교 여부 (성능 향상을 위해 사용 가능)               | `false`    |

---

- **사용 예**

```kvs
WAIT 5  // 5초간 실행을 일시 정지합니다.

WAIT 0  // 대기 없이 바로 다음 명령 실행

WAIT until image_path="login.png"  // login.png가 나타날 때까지 기본 설정으로 대기 (최대 60초)

WAIT until image_path="popup.png", timeout=30  // popup.png가 뜰 때까지 최대 30초간 대기

WAIT until image_path="save_button.png", confidence=0.9, grayscale=true  
// save_button.png를 신뢰도 0.9로 흑백 비교 방식으로 검색하며 대기

SET searchRegion = REGION(x=100, y=100, width=500, height=300)
WAIT until image_path="ok.png", region=searchRegion  

```

## **Database 명령어**

- 데이터베이스는 sqlite, mariadb, postgresql을 지원합니다.

> DB sub-commmand option, ...

- sub-commands
  - connect : database 연결합니다
  - execute : insert,update,delete 등 sql수행합니다
  - query   : select sql수행 결과를 변수에 넣습니다
  - close   : database의 연결을 종료합니다.
  - begin_transaction : transaction을 시작합니다
  - commit : commit하고 transaction을 종료합니다.
  - rollback : rollback하고 transaction을 종료합니다.

- 모든 db 명령어는 name 옵션과 type옵션을 가지고 있습니다.
- 옵션 **name**은 연결된 Database에 대한 alias입니다. 디폴트는 'default'입니다.
- 옵션 **type**은 Database의 종류를 의미하는 문자열입니다.
- **type**은 'sqlite', 'mairiadb', 'postgresql' 중 하나입니다. 디폴트는 'sqlite'입니다.

### 🔶DB CONNECT
  
- **문법**

> DB CONNECT path=<문자열>

- **사용예**

```kvs
DB CONNECT path="test1.db"  // sqlite의 경우
```

### 🔶DB QUERY

- select문을 수행하고 그 결과를 to_var옵션의 값에 해당하는 변수에 저장합니다
- 변수는 **해쉬맵의 배열형태**입니다. 즉 [ { }, ...]과 같은 형태입니다.

- **문법**

> DB QUERY [name=<문자열>, type=문자열], sql=<문자열>, to_var=<변수명>

- **사용예**

```kvs
DB QUERY sql="select * from tasks order by id desc", to_var="tasks"
```

### 🔶DB EXECUTE

- update, delete, insert문을 수행합니다.
- to_var옵션이  없습니다.
  
- **문법**

> DB EXECUTE [name=<문자열>, type=문자열], sql=<문자열>

- **사용예**

```kvs
 DB EXECUTE sql="insert into tasks (title) values ('task1')"
```

### 🔶DB CLOSE

- 데이터베이스 연결을 종료합니다.
  
- **문법**

> DB CLOSE [name=<문자열>, type=문자열]

- **사용예**

```kvs
DB CLOSE
```

- **DB 명령어 사용 예**

```kvs
MAIN
    DB CONNECT path="test1.db" 
    DB EXECUTE sql="""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        done INTEGER DEFAULT 0
    )
    """    
    DB EXECUTE sql="insert into tasks (title) values ('task1')"
    DB EXECUTE sql="insert into tasks (title) values ('task2')"
    DB EXECUTE sql="insert into tasks (title) values ('task3')"
    DB QUERY sql="select * from tasks order by id desc", to_var="tasks"
    PRINT "길이:", Length(tasks)
    PRINT tasks[0] 
    DB QUERY sql="select count(*) as count from tasks", to_var="result"
    PRINT  result[0]["count"]
    DB CLOSE name="default"
END_MAIN
```

### 🔶DB BEGIN_TRANSACTION

- transaction을 시작합니다.
- **문법**

> DB TRANSACTION  [name=<문자열>, type=문자열]

- **사용예**

```kvs
DB BEGIN_TRANSACTION name="default"
```

### 🔶DB COMMIT

- transaction commit 합니다.
- **문법**

> DB COMMIT [name=<문자열>, type=문자열]

- **사용예**

```kvs
 DB COMMIT 
```

### 🔶DB ROLLBACK

- transaction을 rollback 합니다
- **문법**

> DB ROLLBACK [name=<문자열>, type=문자열]

- **사용예**

```kvs
DB ROLLBACK
```

### 전체적인 사용예

```kvs
MAIN
    DB CONNECT path="test1.db" 
    DB BEGIN_TRANSACTION name="default"
    DB EXECUTE sql="insert into tasks (title) values ('task1')"
    DB EXECUTE sql="insert into tasks1 (title) values ('task2')"
    DB COMMIT name="default"

    ON_EXCEPTION
        PRINT f"예외 발생: {$exception_message} (exit code: {$exit_code})"
        DB ROLLBACK name="default"
        DB CLOSE name="default"
    END_EXCEPTION
END_MAIN
```
