# kavana script 문법

## 특징 기본 문법 (Basic Syntax)

kavana script는 명령어 베이스로 동작합니다.
기본적으로 1줄 단위(배열, 맵 자료구조 정의 제외)로 동작합니다.
python언어로 작성되어으므로 python언어의 특징에 C언어, plsql형태등의 문법을 차용하였습니다.

### 특징

- 대소문자를  구분하지 않습니다.
- 문자열은 쌍따옴표로 표현합니다. (따옴표는 사용하지 않습니다)
- 사용자 함수를 작성할 수 있습니다.
- dot-env를 사용가능합니다.
- include문장으로 여러개의 파일로 분할하여 관리 할 수 있습니다.
- log를 내장하고 있습니다.
- 다양한 built-in함수를 가지고 있습니다.

## 코드 구조

- 전형적인 스크립트의 구조

```kvs
INCLUDE "./examples/common.kvs" // 사용자정의함수 및  상수 설정
ENV_LOAD "./examples/env.test"  // .env 파일을 읽어서 변수로 설정

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

## 주석 작성법

- '//' 이후는 주석으로 처리됩니다.
- 멀티라인 주석은 없습니다.

## 데이터 타입 (Data Types)

    - Integer
    - Float
    - String
    - Boolean
    - None
    - Array
    - HashMap

## 변수와 상수 (Variables and Constants)

    - 변수 선언 방법 : SET 명령어로 설정
    - 상수 선언 : CONST 명령어로 설정
    ```kvs
        SET name = "홍길동"
        CONST PI = 3.14
    ```

## 연산자 (Operators)

    산술 연산자
    비교 연산자
    논리 연산자
    

## 제어 흐름 (Control Flow)

- IF, FOR, WHILE 3개의 문장으로 흐름을 제어하며 각각 END_IF,END_FOR, END_WHILE로 끝납니다

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

## 함수 (Functions)

    - FUNCTION func_name(arg1, arg2) ... RETURN  END_FUNCTION
    - 인자의 타입은 정하지 않습니다. 
    - RETURN <express> 로 리턴값을 정합니다.
    ```kvs
        FUNCTION plus(a,b)
            RETURN a + b
        END_FUNCTION
    ```

## 에러 처리 (Error Handling)

- RAISE문으로 예외를 발생시킵니다.
- ON_EXCEPTION .. END_EXCEPTION 블럭으로 EXCEPTION을 잡아서 처리 후 종료할 수 있습니다.
- TRY ... CATCH ... FINALLY ... END_TRY로
