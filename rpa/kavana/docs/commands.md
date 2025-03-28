# kavana-script 명령어들
Kavana Script에서 사용 가능한 명령어와 그 사용법을 정리한 문서입니다.

## 기본 명령어

### SET
- 변수를 설정합니다.
- **문법**
> SET = <표현식>
- **사용 예**
```kvs
SET a = "123"
SET a = 1 + 2 
```
### PRINT
- 문자열을 인쇄합니다.
- 문자열은 python과 유사하게 첨자 r(raw), f(format)을 지원합니다.
- 표현식(변수명 포함)을 직접 인쇄하지 않습니다.
- **문법**
> PRINT <문자열>, <문자열>, ...
- **사용예**
```kvs
SET name = "Hong"
PRINT "abc", f"{name}"
PRINT name // ❌Error
```
### INCLUDE
- 외부파일 kvs를 읽어 들여서 명령어를 확장한다.
- 외부파일 kvs에는 상수와 사용자함수만이 정의되어야 한다.
- **문법**
> INCLUDE <문자열:파일패스>
- **사용예**
```kvs
 INCLUDE "./lib/global.kvs"
 INCLUDE "./common.kvs"
```

### ENV_LOAD
- dot-env파일을 읽어들여서 상수로 처리한다.
- **문법**
> LOAD <문자열:ENV파일패스>
- **사용예**
```kvs
ENV_LOAD ".env.test"
MAIN
    PRINT "{$MY_KEY}"
END_MAIN
```

## RPA 명령어
