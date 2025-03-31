from typing import List

from lib.core.exceptions.kavana_exception import KavanaException, KavanaSyntaxError

class ExceptionRegistry:
    _exception_handler = None  # 현재 등록된 예외 핸들러

    @classmethod
    def register_exception(cls, exception_commands: list[dict]):
        """ON_EXCEPTION 블록을 등록"""
        if cls._exception_handler is not None:
            raise KavanaSyntaxError("ON_EXCEPTION 블록은 하나만 등록할 수 있습니다.")
        cls._exception_handler = exception_commands

    @classmethod
    def get_exception_commands(cls):
        """등록된 예외 핸들러 가져오기"""
        return cls._exception_handler

