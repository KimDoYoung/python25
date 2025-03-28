from abc import ABC, abstractmethod

class DbCommander(ABC):
    @abstractmethod
    def connect(self, **kwargs): pass

    @abstractmethod
    def query(self, sql: str): pass

    @abstractmethod
    def execute(self, sql: str): pass

    @abstractmethod
    def begin_transaction(self): pass

    @abstractmethod
    def commit(self): pass

    @abstractmethod
    def rollback(self): pass

    @abstractmethod
    def close(self): pass
