
from lib.core.datatypes.array import Array
from lib.core.datatypes.window import Window
from lib.core.managers.process_manager import ProcessManager
from lib.core.token import Token, TokenStatus
from lib.core.token_custom import WindowToken
from lib.core.token_type import TokenType


class RpaFunctions:
    @staticmethod
    def WINDOW_LIST(process_name:str=None) -> Token:
        """특정 디렉토리의 파일 목록 반환"""
        from lib.core.command_executor import CommandExecutor
        try:
            executor = CommandExecutor
            pm = ProcessManager(executor=executor)
            if process_name:
                window_info_list = pm.get_window_info_list(process_name)
            else:
                window_info_list = pm.get_window_info_list()

            array = []
            for window_info in window_info_list:
                window = Window(title=window_info.title)
                window.hwnd = window_info.hwnd
                window_token = WindowToken(data=window, status=TokenStatus.EVALUATED)
                array.append(window_token)

            return Token(data=Array(array), type=TokenType.ARRAY)
        except Exception:
            return Token(data=Array([]), type=TokenType.ARRAY)  # 오류 시 빈 리스트 반환