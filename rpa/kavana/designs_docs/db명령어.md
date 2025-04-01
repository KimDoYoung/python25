# DB 명령어

## 설계

1. VariableManager에 DatabaseRepository객체를 member로
2. DatabaseRepository는 {name: DbCommander,...} dict를 갖고 있음.
3. DbCommander는 추상 class
4. DbCommander에서 상속받아서 SqliteDbCommander, PostgreDbCommander... 작성
5. db connect 명령어에서 DbCommander객체 생성, VariableManager.set_db_commander 호출
6. db query, update, insert, delete, commit...  dbcommander를 찾아서 동작수행

```
class DbCommander:
    def __init__(self):
        self.in_transaction = False

    def begin_transaction(self):
        self.in_transaction = True  dddd
        self.conn.execute("BEGIN")

    def end_transaction(self, commit=True):
        if commit:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.in_transaction = False

    def execute(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        if not self.in_transaction:
            self.conn.commit()

```

- sqlite3을 기본으로 제공합니다.
- DB_CONNECT name="default" type="SQLite3", path=" ",

```
DB CONNECT name="main", path="main.db" 
DB CONNECT name="log", path="log.db"

DB QUERY name="main", sql="SELECT * FROM tasks WHERE done = 0", output="rows"

for row in rows:
    log("처리중: " + row.title)
    db execute name="main", sql="UPDATE tasks SET done = 1 WHERE id = " + row.id
    db insert name="log", table="history", values={"task": row.title, "status": "done"}

db close name="main"
db close name="log"

```

### db connect

- db와 연결한다
- **문법**

> db connect [name="default", path="sqlite",] type="postgres", host="db.company.com", port=5432, user="admin", password="pass", dbname="corp"

- **사용예**

```kvs
db connect path="mydb.sqlite3"
db connect name="mydb" path="mydb.db"
db connect type="postgres", host="db.company.com", port=5432, user="admin", password="pass", dbname="corp"
```

### db query, execute, insert, update

### 트랜잭션

```kvs
db begin name="main"
db execute ...
db execute ...
db rollback name="main"   # 예외 시 롤백
```
