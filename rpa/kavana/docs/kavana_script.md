# kavana script

## 기본적인 생각

- kavana 스크립트의 확장자 .kvs
- kavana.exe abc.kvs 와 같이 사용
- abc.kva의 내용
    LOAD ".env" # 로 처음에 환경변수등을 load한다 .env에는 LOG_DIR와 같은 꼭필요한 변수를 넣는다. 없으면 에러보여주고 종료

## 전제적인 구조

```sql
// functions
FUCTION plus n, b
    RETURN
END_FUNCTION


EXCEPTION
    SET error_img = CAPTURE_SCREEN
    SAVE error_img TO $EXEUTE_FOLDER+"/error"+$NOW+".png"
    EXIT 1
END_EXCEPTION

MAIN
    LOAD ".env"
    // 프로그램 코드
END_MAIN
```

## System변수
    $EXCEPTION_MSG : exception message 문자열
    $EXCEPTION_TYPE : exception type 문자열
    $NOW : yyyy-mm-dd HH:MM:SS
    $TODAY : yyyyMMdd
    $TIMESTAMP : yy

## 예약어

FUNCTION, RETURN, END_FUNCTION, MAIN, EXIT, END_MAIN, ON_EXCEPTION, END_EXCEPTION
IF, ELSE_IF, ELSE, END_IF, WHILE, END_WHILE, FOR TO STEP END_FOR


## 주석

- '//' 한줄 라인 주석
- /* 멀티라인 주석 */

```sql
 PRINT abc // 이것은 주석입니다
 /*
 ....
 */       
```

## 함수

### 문자열함수

- FORMAT_DATE : SET today  = FORAMT_DATE "20250219" AS "%y-%m-%d"
- SUBSTRING : SET s = SUBSTRING "123", 1, 2 // startIndex, Length 
- LENGTH  : SET len = LENGTH "12345"


## 명령어

CLICK {3} WITH duration=0.2, RIGHT-CLICK, DOUBLE-CLICK : {1}은 생략, {2}는 더블클릭을 의미하지 않음.
WAIT 정수 : 숫자만큼 대기
SET : SET abc =CREATE_IMAGE "홍길동" WITH size=(10,30), font="굴림" ...
REGION : SET r = REGION 0,0,100,20
POINT :  SET p = POINT 100,200
MOUSE_MOVE : MOUSE_MOVE 100, 200, MOUSE_MOVE p
KEYIN : <enter>, "abc", {ctrl+shift+a}, abc 
	- < > : press, "" : 문자열, { }: hot key
	- example : KEY_IN <down>, <down>, <enter>
WAIT_FOR 변수 WITH gray=true, post_wait_seconds=2 
FIND_IMAGE 변수
	SET img = FIND_IMAGE user_img WITH gray=TRUE
	MOVE CENTER(img)
IMAGE_CLICK : image를 찾아가서 click 실패시 return false
PRINT : log.info를 수행
PRINT_INFO : log.info를 수행
PRINT_DEBUG : log.debug
... 유사하게


## 문법

1. 예약어는 모두 대문자, 변수명은 소문자
	(모든 명령어는 대문자가 좋을까? 변수, 옵션 함수명 이런것은 소문자로 하고)
2. 변수 : 알파벳으로 시작 255글자 이하. 특수문자 사용 못함. 알파벳과 숫자로만 
	- .env에 기술된 변수는 모두 sys_FTP_HOST와 같이 sys_를 붙여서 가져오는 사용가능하게끔, 아니면 $FTP_HOST와 같이 특수문자를 앞에 붙이는게 좋을까?
	
3. 데이터 타입
	1. String
	2. Integer
	3. Float
	3. Point
	4. Region
	5. Image
	6. Boolean 
	7. Date
	8. List, Map, NONE 
SET numbers = [1, 2, 3, 4, 5];
PRINT numbers[0];  # 1 출력

FOR i = 0 TO LENGTH(numbers) - 1 STEP 1
    PRINT numbers[i];
ENDFOR;

SET user = { "name": "홍길동", "age": 30 };
PRINT user["name"];  # "홍길동" 출력
SET user["age"] = 31;
PRINT user["age"];  # 31 출력

SET result = NONE;
IF result == NONE
    PRINT "값이 없음";
ENDIF;
	
	
3. 연산자
	==, !=, >, >= , < ,<=
	+, -, /, *, % 
	가능한 산술인지는 추후에 더 논의하기로 함.
	논리 연산자 : OR, AND 2가지만 지원

3. 대입 
	SET abc = "abc"
	SET user_img = CREATE_IMAGE "홍길동" WITH width=100, height=20
	SET b = "1" == "1"
	
4. 한 문장의 끝은 ;으로 끝냄 또는 줄바꿈으로 끝냄
   WAIT 3; MOUSE_MOVE 10,200; CLICK

제어문
5. GOTO abc; 
	Label abc::
		....
	End_Label
6.  IF <조건식> BEGIN ... ENDIF, 

IF EXISTS "confirm.png"
    CLICK "confirm.png";
ELSEIF EXISTS "cancel.png"
    CLICK "cancel.png";
ELSE
    PRINT "어떤 버튼도 없음";
ENDIF;	
	
	WHILE <조건식> ...ENDWHILE
WHILE EXISTS "loading.png"
    WAIT 1;
ENDWHILE;	
    FOR <수식> TO <수식> STEP <수식> BEGIN ... ENDFOR
FOR i = 1 TO 5 STEP 1
    CLICK "button.png";
ENDFOR;

7. FUNCTION 있음. CALL functio_name 
	FUNCTION LOGIN username 
		MOUSE_MOVE 10,10; CLICK; KEY_IN "honggildong"
		MOUSE_MOVE 20,20; WAIT 3, CLICK;
		RETURN # 생략가능
	END_FUNCTION
	FUNCTION plus n,m 
		RETURN n + m
	END_FUNCTION
	
	
8. EXIT {n} : EXIT 0 정상종료, EXIT 1 등 0아닌 숫자 비정상종료
9. ON_EXCEPTION BEGIN ..EXIT 1. END_EXCEPTION
10. SET init_screen = CAPTURE_SCREEN 화면캡쳐해서 이미지변수에 저장

