# 내장함수(Built-In functions)

- kavana script는 명령어를 보조하는 다양한 built-in 함수를 작성해 두었습니다.
- 내장

## 내장함수의 분류

- 문자열(String) 함수
- 숫자형(Numeric) 함수
- 디렉토리(Directory, Folder) 함수
- 파일(File) 함수
- 패스(Path) 함수
- YmdTime 함수

## 🔴문자열 함수

### 요약

| 함수 | 설명 | 반환 타입 |
|------|------|-----------|
| `LENGTH(S)` | 문자열 `S` 또는 리스트의 길이를 반환 | `int` |
| `SUBSTR(S, start, length)` | 문자열 `S`에서 `start`부터 `length` 길이의 부분 문자열 반환 | `str` |
| `UPPER(S)` | 문자열 `S`를 대문자로 변환 | `str` |
| `LOWER(S)` | 문자열 `S`를 소문자로 변환 | `str` |
| `TRIM(S)` | 문자열 `S`의 앞뒤 공백 제거 | `str` |
| `LTRIM(S)` | 문자열 `S`의 앞쪽 공백 제거 | `str` |
| `RTRIM(S)` | 문자열 `S`의 뒤쪽 공백 제거 | `str` |
| `REPLACE(S, old, new)` | 문자열 `S`에서 `old`를 찾아 `new`로 변경 | `str` |
| `SPLIT(S, sep)` | 문자열 `S`를 `sep` 구분자로 분리한 문자열 리스트 반환 | `List[str]` |
| `JOIN(S_list, sep)` | 문자열 리스트를 `sep`로 연결한 하나의 문자열 반환 | `str` |
| `STARTSWITH(S, prefix)` | 문자열 `S`가 `prefix`로 시작하는지 여부 반환 | `bool` |
| `ENDSWITH(S, suffix)` | 문자열 `S`가 `suffix`로 끝나는지 여부 반환 | `bool` |
| `CONTAINS(S, sub)` | 문자열 `S`에 `sub`가 포함되어 있는지 여부 반환 | `bool` |
| `INDEX_OF(S, sub)` | 문자열 `S`에서 `sub`의 첫 번째 인덱스를 반환. 없으면 -1 | `int` |
| `TO_INT(S)` | 문자열 `S`를 정수로 변환 | `int` |
| `TO_FLOAT(S)` | 문자열 `S`를 실수(float)로 변환 | `float` |


### 코딩 예

```kvs
MAIN
	SET s = "we are the world"
	PRINT LENGTH(s)               // 문자열 길이: 17
	PRINT SUBSTR(s, 3, 5)         // " are "
	PRINT UPPER(s)                // "WE ARE THE WORLD"
	PRINT LOWER(s)                // "we are the world"
	PRINT TRIM("   hello   ")     // "hello"
	PRINT LTRIM("   left")        // "left"
	PRINT RTRIM("right   ")       // "right"
	PRINT REPLACE(s, "world", "universe")  // "we are the universe"
	PRINT SPLIT(s, " ")           // ["we", "are", "the", "world"]
	SET list = ["A", "B", "C"]
	PRINT JOIN(list, "-")         // "A-B-C"
	PRINT STARTSWITH(s, "we")     // True
	PRINT ENDSWITH(s, "world")    // True
	PRINT CONTAINS(s, "the")      // True
	PRINT INDEX_OF(s, "are")      // 3
	PRINT TO_INT("42")            // 42
	PRINT TO_FLOAT("3.14")        // 3.14
END_MAIN
```

## 🔴숫자형 함수

### 요약

| 함수 | 설명 | 반환 타입 |
|------|------|-----------|
| `RANDOM(min, max)` | `min`부터 `max` 사이의 랜덤 정수를 반환 | `int` |
| `ABS(i)` | 정수 `i`의 절대값을 반환 | `int` |
| `MAX(i, j)` | 두 정수 중 큰 값을 반환 | `int` |
| `MIN(i, j)` | 두 정수 중 작은 값을 반환 | `int` |
| `ROUND(i)` | 정수를 반올림하여 반환 (이미 정수라 효과 없음) | `int` |
| `FLOOR(i)` | 정수를 내림 처리 (소수점 제거) | `int` |
| `CEIL(i)` | 정수를 올림 처리 (정수 +1로 표현) | `int` |
| `TRUNC(i)` | 정수 `i`의 소수점 제거 (이미 정수이므로 변화 없음) | `int` |
| `IS_EVEN(i)` | `i`가 짝수이면 `True` 반환 | `bool` |
| `IS_ODD(i)` | `i`가 홀수이면 `True` 반환 | `bool` |
| `RANGE(stop)` | `0`부터 `stop` 미만까지 정수 리스트 생성 | `List[int]` |
| `RANGE(start, stop)` | `start`부터 `stop` 미만까지 정수 리스트 생성 | `List[int]` |
| `RANGE(start, stop, step)` | `start`부터 `stop`까지 `step` 간격의 리스트 생성 | `List[int]` |

### 코딩 예
```kvs
MAIN
	// RANDOM(min, max)
	SET r = RANDOM(1, 10)
	PRINT r

	// ABS(i)
	PRINT ABS(-5)         // 5

	// MAX(i, j)
	PRINT MAX(10, 3)      // 10

	// MIN(i, j)
	PRINT MIN(10, 3)      // 3

	// ROUND(i) - 실질적 효과는 없음 (입력도 정수이므로)
	PRINT ROUND(7)        // 7

	// FLOOR(i)
	PRINT FLOOR(9)        // 9

	// CEIL(i)
	PRINT CEIL(4)         // 5 (정수 입력 기준으로 구현되어 있어서 +1 로 동작)

	// TRUNC(i)
	PRINT TRUNC(123)      // 123

	// IS_EVEN(i)
	PRINT IS_EVEN(8)      // True

	// IS_ODD(i)
	PRINT IS_ODD(7)       // True

	// RANGE(stop)
	SET r1 = RANGE(5)
	PRINT r1              // [0, 1, 2, 3, 4]

	// RANGE(start, stop)
	SET r2 = RANGE(2, 6)
	PRINT r2              // [2, 3, 4, 5]

	// RANGE(start, stop, step)
	SET r3 = RANGE(1, 10, 2)
	PRINT r3              // [1, 3, 5, 7, 9]
END_MAIN
```

## 🔴디렉토리 함수
### 요약

| 함수 | 설명 | 반환 타입 |
|------|------|-----------|
| `DIR_LIST(path)` | `path`에 있는 파일/디렉토리 목록을 리스트로 반환 | `List[str]` |
| `DIR_EXISTS(path)` | `path`가 존재하는 디렉토리인지 여부 반환 | `bool` |
| `DIR_CREATE(path)` | 주어진 경로에 디렉토리 생성 (이미 존재해도 예외 없음) | `bool` |
| `DIR_DELETE(path)` | 디렉토리 삭제 (비어 있어야 함) | `bool` |

### 코딩 예

```kvs
MAIN
	// 디렉토리 생성
	SET path = "test_folder"
	PRINT DIR_CREATE(path)      // True

	// 디렉토리 존재 확인
	PRINT DIR_EXISTS(path)      // True

	// 디렉토리 안의 파일 목록 보기
	PRINT DIR_LIST(path)        // [] (비어 있음)

	// 디렉토리 삭제
	PRINT DIR_DELETE(path)      // True

	// 삭제 후 존재 확인
	PRINT DIR_EXISTS(path)      // False
END_MAIN
```

## 🔴파일(File) 함수

### 요약

| 함수 | 설명 | 반환 타입 |
|------|------|-----------|
| `FILE_READ(path)` | 파일 내용을 문자열로 읽어옴 | `str` |
| `FILE_WRITE(path, content)` | 파일에 문자열 내용을 씀 (덮어쓰기) | `bool` |
| `FILE_APPEND(path, content)` | 파일 끝에 문자열을 추가 | `bool` |
| `FILE_EXISTS(path)` | 파일 존재 여부 반환 | `bool` |
| `FILE_DELETE(path)` | 파일 삭제 | `bool` |
| `FILE_SIZE(path)` | 파일 크기 반환 (바이트) | `int` |
| `FILE_MODIFIED_TIME(path)` | 파일의 마지막 수정 시간 반환 (`YYYY-MM-DD HH:MM:SS`) | `YmdTime` |
| `FILE_TYPE(path)` | 파일 유형 반환 (`file`, `directory`, `none`) | `str` |
| `FILE_COPY(src, dest)` | 파일 복사 | `bool` |
| `FILE_MOVE(src, dest)` | 파일 이동 또는 이름 변경 | `bool` |
| `FILE_HASH(path, algorithm)` | 파일 해시값 반환 (`md5`, `sha256`) | `str` |
| `FILE_LINES(path)` | 파일 내용을 줄 단위 리스트로 반환 | `List[str]` |
| `FILE_FIND(dir, pattern)` | 디렉토리 내 패턴에 맞는 파일 목록 반환 | `List[str]` |


### 코딩 예

```kvs
MAIN
	// 파일 경로 설정
	SET path = "test.txt"

	// 파일 작성
	PRINT FILE_WRITE(path, "Hello, Kavana!\nThis is a file.")

	// 파일에 내용 추가
	PRINT FILE_APPEND(path, "\nAppended line.")

	// 파일 존재 여부
	PRINT FILE_EXISTS(path)           // True

	// 파일 내용 출력
	PRINT FILE_READ(path)

	// 줄 단위 읽기
	PRINT FILE_LINES(path)            // ["Hello, Kavana!", "This is a file.", "Appended line."]

	// 파일 크기
	PRINT FILE_SIZE(path)             // e.g. 42

	// 파일 최종 수정 시간
	PRINT FILE_MODIFIED_TIME(path)

	// 파일 타입 확인
	PRINT FILE_TYPE(path)             // "file"

	// 해시값 출력
	PRINT FILE_HASH(path, "md5")
	PRINT FILE_HASH(path, "sha256")

	// 파일 복사
	PRINT FILE_COPY(path, "copy.txt")

	// 파일 이름 변경
	PRINT FILE_MOVE("copy.txt", "renamed.txt")

	// 특정 디렉토리에서 .txt 파일 찾기
	PRINT FILE_FIND(".", "*.txt")

	// 파일 삭제
	PRINT FILE_DELETE(path)
	PRINT FILE_DELETE("renamed.txt")
END_MAIN
```

## 🔴패스(Path) 함수
### 요약

| 함수 | 설명 | 반환 타입 |
|------|------|-----------|
| `PATH_JOIN(p1, p2, ...)` | 여러 경로 요소를 결합하여 하나의 경로 문자열로 반환 | `str` |
| `PATH_BASENAME(path)` | 경로에서 파일명만 추출 | `str` |
| `PATH_DIRNAME(path)` | 경로에서 디렉토리 부분만 추출 | `str` |

### 코딩 예

```kvs
MAIN
	// 경로 합치기
	PRINT PATH_JOIN("folder", "subfolder", "file.txt") 
	// 출력: folder/subfolder/file.txt (OS에 따라 \ 또는 /)

	// 파일명만 추출
	PRINT PATH_BASENAME("/home/user/data.csv")     
	// 출력: data.csv

	// 디렉토리명만 추출
	PRINT PATH_DIRNAME("/home/user/data.csv")      
	// 출력: /home/user
END_MAIN
```

## 🔴YmdTime 함수
### 요약

| 함수 | 설명 | 반환 타입 |
|------|------|-----------|
| `YMDTIME(y, m, d, hh, mm, ss)` | 지정한 날짜와 시간 객체 생성. 생략 시 현재 시각 사용 | `YmdTime` |
| `YMD(y, m, d)` | 지정한 날짜 객체 생성. 생략 시 오늘 날짜 사용 | `Ymd` |
| `NOW()` | 현재 날짜 및 시간 객체 반환 (YMDTIME와 같음) | `YmdTime` |
| `TODAY()` | 오늘 날짜 객체 반환 (YMD와 같음) | `Ymd` |

### 코딩 예

```kvs
MAIN
	// 현재 날짜/시간
	PRINT NOW()           // 예: 2025-04-03 10:24:55
	PRINT TODAY()         // 예: 2025-04-03

	// 특정 날짜 생성
	PRINT YMD(2024, 12, 25)     // 2024-12-25

	// 특정 날짜/시간 생성
	PRINT YMDTIME(2024, 12, 25, 14, 30, 0)   // 2024-12-25 14:30:00

	// 생략하면 현재 시각 반환
	PRINT YMDTIME()           // NOW() 와 동일
END_MAIN
```
