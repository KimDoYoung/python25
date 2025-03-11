from typing import List


# class ExceptionRegistry:
#     _exception_handler = None  # 현재 등록된 예외 핸들러

#     @classmethod
#     def register_handler(cls, exception_commands: List[dict]):
#         """ON_EXCEPTION 블록을 등록"""
#         if cls._exception_handler is not None:
#             raise Exception("ON_EXCEPTION 블록은 하나만 등록할 수 있습니다.")
#         cls._exception_handler =exception_commands

#     @classmethod
#     def get_handler(cls):
#         """등록된 예외 핸들러 가져오기"""
#         return cls._exception_handler

class ExceptionRegistry:
    _exception_handler = None  # 현재 등록된 예외 핸들러
    _error_message = None  # 예외 메시지 저장

    @classmethod
    def register_handler(cls, exception_commands: list[dict]):
        """ON_EXCEPTION 블록을 등록"""
        if cls._exception_handler is not None:
            raise Exception("ON_EXCEPTION 블록은 하나만 등록할 수 있습니다.")
        cls._exception_handler = exception_commands

    @classmethod
    def get_handler(cls):
        """등록된 예외 핸들러 가져오기"""
        return cls._exception_handler

    @classmethod
    def set_error_message(cls, message: str):
        """RAISE에서 발생한 메시지를 저장"""
        cls._error_message = message

    @classmethod
    def get_error_message(cls):
        """저장된 에러 메시지를 가져오기"""
        return cls._error_message
