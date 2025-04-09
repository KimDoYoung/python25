# kavana에서의 List

## 설계

```

1. 다음과 같은 문법을 지원한다, List안에 List 2중배열를 지원 a[1,2]와 같은 문법을 사용
```

set a = [1,2,3] -> SET, a , =, ListExtoken
set a[1] = 3 -> SET, ListIndexToken, =, 3
set a = [1,olist[3],4] -> SET, a, =, ListExToken(element_expres=[[1],[ListIndexToken],[4]])
set a = [[1,2,3],[4,5]] -> SET, a, = ListExToken(element_expres=[[ListExToken],[ListExToken]])
set a = [[a,b,c+1],[4,5]] -> SET, a, = ListExToken(element_expres=[[ListExToken],[ListExToken]])
set a = [e1,2,3,(2+3*4)]
set a[1,2,list[3]] = 3 -> set, ListIndexToken, =, 3
set a[1,2] = 10

```
2. token단위로 parsing한 것을 post_process_tokens에서 ListExToken과 ListIndexToken으로 만든다.
```

@dataclass
class ListExToken(Token):
    data: ListType  # ✅ `data`는 ListType 타입
    type: TokenType = field(default=TokenType.LIST, init=False)  # ✅ `type`을 LIST로 고정
    element_type: TokenType = field(default=TokenType.UNKNOWN)  # 요소의 토큰 타입
    element_expresses: List[List[Token]] = field(default_factory=list)  # 각 요소의 표현 리스트
    status: Literal["Parsed", "Evaled"] = "Parsed"

    def __post_init__(self):
        if not isinstance(self.data, ListType):
            raise TypeError("ListExToken must contain a ListType")

@dataclass
class ListIndexToken(Token):
    """✅ 리스트에 접근하기 위한 인덱스 토큰"""
    express: List[Token] = field(default_factory=list)  
    row_express: List[Token] = field(default_factory=list)  
    column_express: List[Token] = field(default_factory=list)
    data: String  # ✅ `data`는 String 타입 (생성 시 반드시 입력해야 함)
    type: TokenType = field(default=TokenType.LIST_INDEX, init=False)  # ✅ `type`을 LIST_INDEX 고정

    def __post_init__(self):
        """추가적인 유효성 검사"""
        if not isinstance(self.data, String):
            raise TypeError(f"data 필드는 String 타입이어야 합니다. (현재 타입: {type(self.data)})")

    def __repr__(self) -> str:
        express_str = ", ".join(repr(e) for e in self.express)  # express 리스트의 요소를 문자열로 변환
        return f"ListIndexToken(express=[{express_str}], data={repr(self.data)}, type={self.type})"

```
3. post_process_tokens로직은 다음과 같다.

3.1 in_list 라는 flag를 둔다. 초기값false
3.1 '['를 만나면 이전 Token이 IDENTIFIER인지 확인한다
3.2 IDENTIFIER라면 ListIndexToken으로 판단하고 바로 전 identifiler의 value 를 var_name으로 설정한다.
3.3 list 안이라면 ('['의 count를 체크해서 확인, 즉[]이라면 ) post_process_tokens를 재귀적으로 호출한다. 이때 시작idx와 flag를 false로해서 보낸다.
3.4 ']'를 만나면 flag를 true로 한다.
3.5 '['일때 바로 전 token이 identifiler가 아니면 ListExToken으로 판단한다. 
3.6 ListExToken으로 판단히 전전token의 value를 var_name으로 한다.

set a = [1,2,3] -> SET, a , =, ListExtoken
set a[1] = 3 -> SET, ListIndexToken, =, 3
set a = [1,olist[3],4] -> SET, a, =, ListExToken(element_expres=[[1],[ListIndexToken],[4]])
set a = [[1,2,3],[4,5]] -> SET, a, = ListExToken(element_expres=[[ListExToken],[ListExToken]]
set a = [[a,b,c+1],[4,5]] -> SET, a, = ListExToken(element_expres=[[ListExToken],[ListExToken]]
set a = [e1,2,3,(2+3*4)]
set a[1,2,list[3]] = 3 -> set, ListIndexToken, =, 3
set a[1,2] = 10

```

## 문법

```
set a = [1,2,3] -> SET, a , =, ListExtoken
set a[1] = 3 -> SET, ListIndexToken, =, 3
set a = [1,olist[3],4] -> SET, a, =, ListExToken(element_expres=[[1],[ListIndexToken],[4]])
set a = [[1,2,3],[4,5]] -> SET, a, = ListExToken(element_expres=[[ListExToken],[ListExToken]]
set a = [[a,b,c+1],[4,5]] -> SET, a, = ListExToken(element_expres=[[ListExToken],[ListExToken]]
set a = [e1,2,3,(2+3*4)]
set a[1,2] = 3 -> set, ListIndexToken, =, 3

```

## 특징

1. 같은 데이터 타입만을 지원.
2. SET a = [1,2,3]과 같은 구문으로 지원
3. 2중배열은 없는 것으로 하자

## List 생성

SET myList = LIST() // 빈 리스트 생성
SET myList = LIST(1, 2, 3) // 초기값 포함 리스트 생성
List 요소 접근

SET val = myList[0] // 인덱싱 지원
SET last = myList[-1] // 음수 인덱스 지원 여부?

## List 수정 및 추가

APPEND myList, 4 // 리스트에 요소 추가
INSERT myList, 1, 100 // 특정 인덱스에 삽입
REMOVE myList, 2 // 특정 인덱스 요소 제거

## List 연산 지원 여부

SET newList = myList + LIST(4, 5, 6) // 리스트 병합
SET size = LENGTH(myList) // 리스트 길이 반환

## List 내부 구현 방식

Python의 list를 기반으로 할지?
ListObject 클래스를 따로 만들어 Kavana 전용 List 타입을 제공할지?
