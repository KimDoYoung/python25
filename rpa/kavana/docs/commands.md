# kavana-script 명령어들

Kavana Script에서 사용 가능한 명령어와 그 사용법을 정리한 문서입니다.

## **기본 명령어**

### 🔶SET

- 변수를 설정합니다.
- **문법**

> SET = <표현식>

- **사용 예**

```kvs
SET a = "123"
SET a = 1 + 2 
```

### 🔶PRINT

- 문자열을 인쇄합니다.
- 문자열은 python과 유사하게 첨자 r(raw), f(format)을 지원합니다.
- 여러 인자를 콤마로 분리할 수 있습니다
- **문법**

> PRINT <문자열>, <문자열>, ...

- **사용예**

```kvs
SET name = "Hong"
PRINT name 
PRINT "abc", f"{name}"
```

### 🔶LOG

- 로그파일은 일자별로 생성되는 것으로 확정했습니다.
- LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR 명령어로 구성됩니다.
> LOG_DEBUG <문자열> ...

- LOG_CONFIG 명령어로 설정을 변경할 수 있습니다.
  
> LOG_CONFIG dir=<문자열>, prefix=<문자열>, level=문자열

- dir의 디폴트는 ./logs 입니다. 로그파일이 저장될 폴더입니다.
- prefix는 로그파일의 시작문자열입니다. 즉 my_app 일 경우 파일명은 my_app-yyyy-mm-dd.log 가 됩니다.
- prefix는 디폴트값이 'kavana'입니다.
- 로그파일이 존재하면 그 파일에 추가됩니다.
- level 은 로그를 인쇄할 때의 level입니다. (DEBUG < INFO < WARN < ERROR)
- level이 INFO이면 LOG_DEBUG는 인쇄하지 않습니다.

```kvs
MAIN
    LOG_INFO "--------------------------------------------------"
    LOG_INFO "프로그램 시작"
    LOG_INFO "--------------------------------------------------"
    SET var1 = 100
    SET var2 = 50
    LOG_CONFIG dir="./logs/my_app", prefix="my_app", level="DEBUG"
    LOG_INFO f"시스템 정상 실행 중. var1 = {var1}"
    LOG_WARN f"경고 발생! var1 + var2 = { var1 + var2 }"
    LOG_ERROR f"에러 발생! var1이 50보다 큰가? {var1 > 50}"
    LOG_DEBUG f"디버깅: 현재 값은 var1={var1}, var2={var2}"
    LOG_INFO "--------------------------------------------------"
    LOG_INFO "프로그램 종료"
    LOG_INFO "--------------------------------------------------"
END_MAIN
```
- 위 프로그램을 실행하면 .kvs가 존재하는 폴더 하위에  logs/kavana-yyyy-mm-dd.log에 LOG_INFO 3라인이 인쇄됩니다.
- 그 후 LOG_CONFIG가 실행되어 log파일의 위치가 logs/my_app/my_app-yyyy-mm-dd.log로 변경됩니다.
- 그 후의 로그명령어는 변경된 파일에 인쇄됩니다.
  
### 🔶INCLUDE

- 외부파일 kvs를 읽어 들여서 명령어를 확장한다.
- 외부파일 kvs에는 상수와 사용자함수만이 정의되어야 한다.
- **문법**

> INCLUDE <문자열:파일패스>

- **사용예**

```kvs
 INCLUDE "./lib/global.kvs"
 INCLUDE "./common.kvs"
```

### 🔶ENV_LOAD

- dot-env파일을 읽어들여서 상수로 처리한다.
- 각 key는 $key 변수로 설정됩니다.
  
- **문법**

> LOAD <문자열:ENV파일패스>

- **사용예**

```kvs
ENV_LOAD ".env.test"
MAIN
    PRINT "{$MY_KEY}"
END_MAIN
```

### 🔶RAISE
- Exception을 발생시킵니다.
- **문법**

> RAISE <문자열:에러메세지>, <정수:Exit코드>

> 묵시적으로 $EXCEPTION_MESSAGE, $EXIT_CODE 변수가 설정됩니다.

- **사용예**

```kvs  
RAISE // 인자없이 사용, $EXCEPTION_MESSAGE에 `에러가 발생했습니다`저장, $EXIT_CODE에 0 저장
RAISE "에러가 발생했습니다" // 문자열은 $EXCEPTION_MESSAGE에 저장저장됩니다.
RAISE "에러발생", 1       // 1 은 $EXIT_CODE에 저장됩니다.
ON_EXCEPTION
    PRINT $EXCEPTION_MESSAGE, $EXIT_CODE
END_EXCEPTION

```

## **RPA 명령어**

## **Database 명령어**

- 데이터베이스는 sqlite, mariadb, postgresql을 지원합니다.
> DB sub-commmand option, ...
- sub-commands
    *  connect : database 연결합니다
    *  execute : insert,update,delete 등 sql수행합니다
    *  query   : select sql수행 결과를 변수에 넣습니다
    *  close   : database의 연결을 종료합니다.
    *  begin_transaction : transaction을 시작합니다
    *  commit : commit하고 transaction을 종료합니다.
    *  rollback : rollback하고 transaction을 종료합니다.

- 모든 db 명령어는 name 옵션과 type옵션을 가지고 있습니다.
- 옵션 **name**은 연결된 Database에 대한 alias입니다. 디폴트는 'default'입니다.
- 옵션 **type**은 Database의 종류를 의미하는 문자열입니다.
- **type**은 'sqlite', 'mairiadb', 'postgresql' 중 하나입니다. 디폴트는 'sqlite'입니다.

### 🔶DB CONNECT
  
- **문법**

> DB CONNECT path=<문자열>

- **사용예**
```kvs
DB CONNECT path="test1.db"  // sqlite의 경우
```

### 🔶DB QUERY

- select문을 수행하고 그 결과를 to_var옵션의 값에 해당하는 변수에 저장합니다
- 변수는 **해쉬맵의 배열형태**입니다. 즉 [ { }, ...]과 같은 형태입니다.

- **문법**
> DB QUERY [name=<문자열>, type=문자열], sql=<문자열>, to_var=<변수명>

- **사용예**
```kvs
DB QUERY sql="select * from tasks order by id desc", to_var="tasks"
```

### 🔶DB EXECUTE
- update, delete, insert문을 수행합니다.
- to_var옵션이  없습니다.
  
- **문법**
> DB EXECUTE [name=<문자열>, type=문자열], sql=<문자열>

- **사용예**
```kvs
 DB EXECUTE sql="insert into tasks (title) values ('task1')"
```

### 🔶DB CLOSE
- 데이터베이스 연결을 종료합니다.
  
- **문법**
> DB CLOSE [name=<문자열>, type=문자열]
- **사용예**
```kvs
DB CLOSE
```

- **DB 명령어 사용 예**

```kvs
MAIN
    DB CONNECT path="test1.db" 
    DB EXECUTE sql="""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        done INTEGER DEFAULT 0
    )
    """    
    DB EXECUTE sql="insert into tasks (title) values ('task1')"
    DB EXECUTE sql="insert into tasks (title) values ('task2')"
    DB EXECUTE sql="insert into tasks (title) values ('task3')"
    DB QUERY sql="select * from tasks order by id desc", to_var="tasks"
    PRINT "길이:", Length(tasks)
    PRINT tasks[0] 
    DB QUERY sql="select count(*) as count from tasks", to_var="result"
    PRINT  result[0]["count"]
    DB CLOSE name="default"
END_MAIN
```

### 🔶DB BEGIN_TRANSACTION
- transaction을 시작합니다.
- **문법**
> DB TRANSACTION  [name=<문자열>, type=문자열]
- **사용예**
```kvs
DB BEGIN_TRANSACTION name="default"
```


### 🔶DB COMMIT
- transaction commit 합니다.
- **문법**
> DB COMMIT [name=<문자열>, type=문자열]
- **사용예**
```kvs
 DB COMMIT 
```

### 🔶DB ROLLBACK
- transaction을 rollback 합니다
- **문법**
> DB ROLLBACK [name=<문자열>, type=문자열]
- **사용예**
```kvs
DB ROLLBACK
```

### 전체적인 사용예

```kvs
MAIN
    DB CONNECT path="test1.db" 
    DB BEGIN_TRANSACTION name="default"
    DB EXECUTE sql="insert into tasks (title) values ('task1')"
    DB EXECUTE sql="insert into tasks1 (title) values ('task2')"
    DB COMMIT name="default"

    ON_EXCEPTION
        PRINT f"예외 발생: {$exception_message} (exit code: {$exit_code})"
        DB ROLLBACK name="default"
        DB CLOSE name="default"
    END_EXCEPTION
END_MAIN
```