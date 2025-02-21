from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """
    모든 명령어 클래스가 상속해야 하는 기본 인터페이스
    """
    @abstractmethod
    def execute(self, args, executor):
        pass
