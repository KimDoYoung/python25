# 내장함수

## 문자열

### LENGTH(s|list)

문자열의 길이 또는 List의 요소의 갯수를 리턴

### SUBSTR(문자열, 시작인덱스, 길이)

문자열의 시작인덱스에서 길이만큼의 문자열을 잘라서 리턴

### UPPER(S)

문자열 S를 대문자로 변환
예: UPPER("hello") → "HELLO"

### LOWER(S)

문자열 S를 소문자로 변환
예: LOWER("Hello") → "hello"

### TRIM(S)

문자열 S의 앞뒤 공백 제거
예: TRIM(" hello ") → "hello"

### LTRIM(S)

문자열 S의 왼쪽 공백 제거
예: LTRIM(" hello ") → "hello "

### RTRIM(S)

문자열 S의 오른쪽 공백 제거
예: RTRIM(" hello ") → " hello"

### REPLACE(S, target, replacement)

문자열 S에서 target을 replacement로 치환
예: REPLACE("hello world", "world", "Kavana") → "hello Kavana"

### SPLIT(S, delimiter)

문자열 S를 delimiter 기준으로 리스트(ListType)로 분리
예: SPLIT("a,b,c", ",") → ["a", "b", "c"] (ListType 반환)

### JOIN(delimiter, list)

list의 요소를 delimiter로 이어붙인 문자열 반환
예: JOIN("-", ["a", "b", "c"]) → "a-b-c"

### STARTS_WITH(S, prefix)

문자열 S가 prefix로 시작하는지 여부 반환 (Boolean)
예: STARTS_WITH("hello", "he") → True

### ENDS_WITH(S, suffix)

문자열 S가 suffix로 끝나는지 여부 반환 (Boolean)
예: ENDS_WITH("hello", "lo") → True

### CONTAINS(S, substring)

문자열 S에 substring이 포함되어 있는지 여부 반환 (Boolean)
예: CONTAINS("hello world", "world") → True

### INDEX_OF(S, substring)

문자열 S에서 substring의 첫 번째 등장 위치 반환 (0-based, 없으면 -1)
예: INDEX_OF("hello world", "world") → 6
