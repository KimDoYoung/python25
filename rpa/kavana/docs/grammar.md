# kavana script 문법

## ✅기본 문법 (Basic Syntax)

- kavana script는 명령어 베이스로 동작합니다.
- 기본적으로 1줄 단위(배열, 맵 자료구조 정의 제외)로 동작합니다.
- python언어로 작성되었습니다.

### 특징

- 대소문자를  구분하지 않습니다.
- 문자열은 쌍따옴표로 표현합니다. (따옴표는 사용하지 않습니다)
- 사용자 함수를 작성할 수 있습니다.
- dot-env를 사용가능합니다.
- include문장으로 여러개의 파일로 분할하여 관리 할 수 있습니다.
- log를 내장하고 있습니다.
- 다양한 built-in함수를 가지고 있습니다.

## ✅ 코드 구조

- 전형적인 스크립트의 구조

```kvs
INCLUDE "./examples/common.kvs" // 사용자정의함수 및  상수 설정
LOAD_ENV "./examples/env.test"  // .env 파일을 읽어서 변수로 설정

//사용자함수
FUNCTION plus(a, b)
    RETURN a + b
END_FUNCTION

//메인함수
MAIN
    SET c = plus(1, 2)
    PRINT "Hi! kavana" 

ON_EXCEPTION //예외처리
    PRINT ">>> {$exception_message} exit code: {$exit_code}"
END_EXCEPTION
END_MAIN
```

## ✅ 주석 작성법

- '//' 이후는 주석으로 처리됩니다.
- 멀티라인 주석은 없습니다.

## ✅ 기본 데이터 타입 (Data Types)

    - Integer
    - Float
    - String
    - Boolean
    - None
    - Array
    - HashMap

```kvs
MAIN
    SET i = 1 // 정수형
    SET f = 12.34 // 실수형
    SET s = "Hello" // 문자열형 ❌ 'Hello'는 안됨
    SET b = not True // 불리언형
    
    PRINT f"i={i} f={f} s={s} b={b}" 

    SET array1 = [1, 2, 3] // 배열형
    SET array2 = [
        [1, 2, 3], 
        [4, 5, 6],
        [7, 8, 9]
    ]  
    SET dict1 = {
        "key1": 1,
        "key2": 2,
        "key3": 3
    } 
    SET dict2 = {
        "key1": [1, 2, 3],
        "key2": [4, 5, 6],
        "key3": [7, 8, 9]
    } 
    PRINT array1[1] // 2
    PRINT array2[1][2] // 6
    PRINT dict1["key2"] // 2
    PRINT dict2["key3"][1] // 8
END_MAIN
```

## ✅ 변수와 상수 (Variables and Constants)

    - 변수 선언 방법 : SET 명령어로 설정
    - 상수 선언 : CONST 명령어로 설정

    ```kvs
        SET name = "홍길동"
        CONST PI = 3.14
    ```

## ✅ 연산자 (Operators)

    - 산술 연산자
        - `+`, `-`, `*`, `/`, `%` 만 지원
        - `++`, `--`, `+=`, `-=` 등의 복합 연산자는 **지원 않음**❌
    - 비교 연산자
        - `==`, `!=`, `>`,`<`,`>=`,`<=` 
    - 논리 연산자
        - not, and, or 

### 연산자 우선순위

| 우선순위 | 연산자 | 설명 |
|----------|------------|------------|
| 1 | `()` | 괄호 (최우선) |
| 2 | `*`, `/`, `%` | 곱셈, 나눗셈, 나머지 |
| 3 | `+`, `-` | 덧셈, 뺄셈 |

### 데이터 타입별 연산자

- `%` 연산자는 정수 % 정수 만 지원합니다.
- 배열 + 배열 연산을 지원합니다.
- YMDTIME `+`,`-` 정수 연산을 지원합니다.
- 결과는 정수만큼의 일수를 +/- 한 YMDTIME 입니다.
- YMDTIME - YMDTIME을 지원하며 결과는 milisecond 입니다.
- YMD `+`, `-` 정수를 지원합니다. 결과는 정수만큼의 일수를 더하거나 뺀 YMD입니다.
- YMD - YMD 를 지원하며 결과는 두 일자의 일수 차이입니다
- 문자열 + 문자열을 지원하면 결과는 두 문자열을 합친 문자열입니다.

## ✅ 제어 흐름 (Control Flow)

- IF, FOR, WHILE 3개의 문장으로 흐름을 제어하며 각각 END_IF,END_FOR, END_WHILE로 끝납니다
- SWITCH, CASE문은 없습니다.

### 조건문(IF)

- IF <조건식> ELIF <조건식> ELSE ... END_IF

```kvs
    SET i = 10
    IF i > 7 
        PRINT "{i} 는 7 보다 큽니다."
    ELIF i > 5 
        PRINT "{i} 는 5 보다 큽니다."
    ELSE
        PRINT "{i} 는 5 이하입니다"
    END_IF 
```

### FOR 반복문

- 두가지 FOR문이 있습니다.
- FOR i = 1 to 10 STEP 2 ... END_FOR
- FOR i in [1,2,3] ... END_FOR

```kvs
    FOR i=1 TO 10 
        PRINT i
    END_FOR
    FOR i IN range(1, 10)
        PRINT i
    END_FOR
```

### WHILE 반복문

- WHILE <조건식> ... END_WHILE

```kvs
    WHILE i < 10
        PRINT i
        SET i = i + 1 // SET i += 1 ❌ `+=` 연산자가 없습니다.
    END_WHILE
```

## ✅ 함수 (Functions)

    - FUNCTION func_name(arg1, arg2) ... RETURN  END_FUNCTION
    - 인자의 타입은 정하지 않습니다. 
    - RETURN <express> 로 리턴값을 정합니다.
    ```kvs
        FUNCTION plus(a,b)
            RETURN a + b
        END_FUNCTION
    ```

## ✅ 에러 처리 (Error Handling)

- RAISE문으로 예외를 발생시킵니다.
- ON_EXCEPTION .. END_EXCEPTION 블럭으로 EXCEPTION을 처리 후 종료할 수 있습니다.
- TRY ... CATCH ... FINALLY ... END_TRY 로 특정 부분에서의 exception발생을 관리할 수 있습니다.
- RAISE문은 2 인자를 갖을 수 있습니다. 첫번째는 에러문자열, 두번째는 프로그램 exit 정수형 인자입니다.

> RAISE <문자열:에러메세지>, <정수:Exit코드>

```kvs
MAIN
    FOR i = 0 to 10
        IF i == 1
            RAISE "i == 1 에러가 발생했습니다", 99
        END_IF
    END_FOR
ON_EXCEPTION
    PRINT $EXCEPTION_MESSAGE, $EXIT_CODE
END_EXCEPTION
END_MAIN
```

- 아래는 try catch 문의 예시입니다.

```kvs
MAIN
    // RAISE 이곳에서는 ON_EXCEPTION으로 빠지고 프로그램 종료합니다
    TRY
        for i = 0 to 10
            PRINT i
            IF i == 1 
                RAISE "error" // catch문으로 빠집니다
            END_IF
        END_FOR
    CATCH
        PRINT "catch"
    FINALLY
        PRINT "finally"
    END_TRY
    // RAISE 이곳에서는 ON_EXCEPTION으로 빠지고 프로그램 종료합니다
ON_EXCEPTION
    PRINT "on_exception handler"
END_EXCEPTION
END_MAIN
```
