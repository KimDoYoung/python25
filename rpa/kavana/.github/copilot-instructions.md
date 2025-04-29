# kavana

## 기술스택

- python 3.12

## 프로젝트 개요

- command base script language written in python
- pyinstaller로 실행파일을 작성함.
- kavana.exe my-script.kvs와 같은 형태로 사용

## 폴더설명

- designs_docs : 설계문서
- docs : 사용자용 문서, mkdocs를 사용함
- examples : kavana script(확장자 kvs)의 예제로 docs에서 사용하기 위해 만듬
- lib : 실제 소스
  - builtins : 내장함수의 구현
  - commands : 기본명령어
    - browser : browser 관련 명령어
    - database : database 관련 명령어
    - image : image 관련 명령어
    - network : sftp, ftp, http 관련 명령어
    - ocr : ocr관련 명령어
    - rpa : rpa관련 명령어
- scripts : kavana scripts
- simple_test : 디버깅하기 위한 짧은 python소스들
- tests : pytest용 테스트 프로그램들

## script 프로그램의 실행과정

1. 소스파일을 CommandPreprocessor가 라인단위로 잘라냄
2. CommandParser가 각 라인을 token으로 잘라냄
3. CommandExecutor가 각 라인을 해석하고 수행함.

```python
script = """
MAIN
    SET i = (10 + 20) * 30
    SET f = 12.34
    SET s = "Hello"
    SET b = not True
    PRINT f"{i} {f} {s} {b}"
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
for line in command_preprocssed_lines:
    print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    print("----------------------")
    print(command)
    commandExecutor.execute(command)
    print("----------------------")

```

## 명령어의 구성

- 명령어 분류 : 기본명령어,  RPA,
- 기본명령어 : SET, INCLUDE, LOAD_ENV, PRINT 등

## 주의사항

- 주로 한글로 대답 요망
- 주로 간결하게 대답 요망, 특별히 자세한 대답을 희망할 때 자세히 대답
