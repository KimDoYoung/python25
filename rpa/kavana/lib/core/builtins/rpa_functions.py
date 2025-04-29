
from lib.core.datatypes.array import Array
from lib.core.datatypes.window import Window
from lib.core.managers.process_manager import ProcessManager
from lib.core.token import ArrayToken, NoneToken, Token, TokenStatus
from lib.core.token_custom import RegionToken, WindowToken
from lib.core.token_type import TokenType


class RpaFunctions:
    @staticmethod
    def WINDOW_LIST(process_name:str=None) -> Token:
        """특정 디렉토리의 파일 목록 반환"""
        from lib.core.command_executor import CommandExecutor
        try:
            executor = CommandExecutor()
            pm = ProcessManager(executor=executor)
            if process_name:
                window_info_list = pm.get_window_info_list(process_name)
            else:
                window_info_list = pm.get_window_info_list()

            array = []
            for window_info in window_info_list:
                window = Window(title=window_info.title)
                window.hwnd = window_info.hwnd
                window.class_name = window_info.class_name
                window_token = WindowToken(data=window, status=TokenStatus.EVALUATED)
                array.append(window_token)

            token =  ArrayToken(data=Array(array))
            token.status = TokenStatus.EVALUATED
            return token
        except Exception as e:
            # print(f"[WINDOW_LIST ERROR] {e}")
            return Token(data=Array([]), type=TokenType.ARRAY)  # 오류 시 빈 리스트 반환

    @staticmethod    
    def WINDOW_TOP(process_name:str=None) -> Token:
        """특정 프로세스의 최상위 창 반환"""
        from lib.core.command_executor import CommandExecutor
        try:
            executor = CommandExecutor()
            pm = ProcessManager(executor=executor)
            top_window = pm.find_top_modal_window(process_name)
            if top_window:
                window = Window(title=top_window.title)
                window.hwnd = top_window.hwnd
                window.class_name = top_window.class_name
                token =  WindowToken(data=window)
                token.status = TokenStatus.EVALUATED
                return token
            else:
                return NoneToken()  # 창이 없을 경우 None 반환
        except Exception as e:
            # print(f"[WINDOW_TOPIC ERROR] {e}")
            return NoneToken()
    
    @staticmethod
    def WINDOW_REGION(hwnd: int) -> RegionToken:
        """특정 창의 위치 및 크기를 Region 객체로 반환"""
        from lib.core.command_executor import CommandExecutor
        try:
            executor = CommandExecutor()
            pm = ProcessManager(executor=executor)
            x,y,w,h = pm.get_window_region(hwnd)
            token = RegionToken(data=(x, y, w, h))
            token.status = TokenStatus.EVALUATED
            return token
        except Exception as e:
            # print(f"[WINDOW_REGION ERROR] {e}")
            return NoneToken()
    
