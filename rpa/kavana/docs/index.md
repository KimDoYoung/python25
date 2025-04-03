# Welcome to Kavana script

- kavana script는 처음 RPA 동작을 수행하는 명령어 기반 스크립트언어 입니다.

## ✅특징

- RPA 동작이 필요한 업무를 쉽게 개발하기 위해서 개발됨.
- logger를 자체적으로 내장하였습니다.
- .env파일 편리하게 변수로 만들어 사용할 수 있습니다
- 다양한 내장함수(built-in)를 갖고 있습니다

## ✅활용

- make.sh 를 이용하여 host에 설치 후 사용가능
- make.sh은 pyinstaller를 사용합니다.

```bash
kavana upload.kvs
```

## ✅Example 코드

```kvs

// kavana hello.kvs
MAIN
    SET greeting = "Hello, Kavana!"
    PRINT greeting
END_MAIN

```
