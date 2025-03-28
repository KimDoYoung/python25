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

'//' 이후는 주석으로 처리됩니다.
멀티라인 주석은 없습니다. 

## 데이터 타입 (Data Types)

    숫자 (Number)

    문자열 (String)

    불리언 (Boolean)

    배열 / 리스트 (Array/List)

    객체 / 딕셔너리 (Object/Dictionary)

    널 / 없음 (Null/None)

## 변수와 상수 (Variables and Constants)

    변수 선언 방법

    상수 선언


## 연산자 (Operators)

    산술 연산자

    비교 연산자

    논리 연산자

    할당 연산자

    기타 연산자 (삼항, 비트 연산자 등)

## 제어 흐름 (Control Flow)

    조건문 (if, else, elif)

    반복문 (for, while)

    루프 제어 (break, continue)

## 함수 (Functions)

    함수 정의와 호출

    매개변수와 반환값


## 에러 처리 (Error Handling)

- raise문으로 예외를 발생시킵니다.
- on_exception .. end_exception블럭으로 

