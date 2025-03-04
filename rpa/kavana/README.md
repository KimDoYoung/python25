# kavana

## 개요

- RPA관련 라이브러리 작성
- 그것을 이용해서 kfs-rpa-script 생성
- 최종적으로는 kfs-auto.exe, a.kas, .env  제공한다.

## TODO

- literal이 keyword이면 안된다.
- SET a = [a,b,c,1+2]와 같이 되는가?
- myList[<express>] 해석
- RETURN에 인자가 없어도 된다. 처리가 되는가?
- LOAD, INCLUDE 구현
- CLICK, MOVE, WAIT_IMAGE, SLEEP 등 RPA 명령어 구현
- builtin함수 추가.
- DATE :
SET d = Date(2025,10,12,10,00,00)
SET today = date_format( current_day(), "%y-%m-%d")
SET time = current_time()
