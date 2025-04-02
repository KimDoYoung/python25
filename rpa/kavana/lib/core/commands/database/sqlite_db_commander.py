import sqlite3

from lib.core.commands.database.db_commander import DbCommander

class SqliteDbCommander(DbCommander):
    def __init__(self):
        self.conn = None
        self.path = None
        self.in_transaction = False

    def connect(self, **kwargs):
        """sqlite3.connect(path)"""
        if self.conn:
            self.conn.close()
        self.path = kwargs.get("path")
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

    def query(self, sql):            
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return [dict(row) for row in rows]  


    def execute(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        if not self.in_transaction:
            self.conn.commit()

    def begin_transaction(self):
        self.conn.execute("BEGIN")
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
