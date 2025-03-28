import pymysql
from lib.core.commands.database.db_commander import DbCommander

class MariaDbCommander(DbCommander):
    def __init__(self):
        self.conn = None
        self.in_transaction = False
        self.config = {}

    def connect(self, **kwargs):
        self.config = {
            "host": kwargs.get("host", "localhost"),
            "port": kwargs.get("port", 3306),
            "user": kwargs.get("user"),
            "password": kwargs.get("password"),
            "database": kwargs.get("database"),
            "charset": "utf8mb4"
        }
        self.conn = pymysql.connect(**self.config)

    def query(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def execute(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
        if not self.in_transaction:
            self.conn.commit()

    def begin_transaction(self):
        self.conn.begin()
        self.in_transaction = True

    def commit(self):
        self.conn.commit()
        self.in_transaction = False

    def rollback(self):
        self.conn.rollback()
        self.in_transaction = False

    def close(self):
        if self.conn:
            self.conn.close()
            print(f"[MariaDB 연결 종료] {self.config.get('host')}:{self.config.get('database')}")
