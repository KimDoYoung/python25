
import pyautogui
import imagehash
from lib.core.datatypes.array import Array
from screeninfo import get_monitors
from lib.core.datatypes.region import Region
from lib.core.datatypes.window import Window
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.managers.process_manager import ProcessManager
from lib.core.token import ArrayToken, NoneToken, Token, TokenStatus
from lib.core.token_custom import RegionToken, WindowToken
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil
from datetime import datetime
from lib.core.utils.rpa_image_util import RpaImageUtil  # RpaImageUtil 모듈 import 추가


class RpaFunctions:
    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        RpaFunctions.executor = executor_instance
    
    @staticmethod
    def WINDOW_LIST(process_name:str=None) -> Token:
        """특정 디렉토리의 파일 목록 반환"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            if process_name:
                window_info_list = pm.get_window_info_list(process_name)
            else:
                window_info_list = pm.get_window_info_list()

            array = []
            for window_info in window_info_list:
                window = Window(title=window_info.title, hwnd=window_info.hwnd, class_name=window_info.class_name)
                window_token = WindowToken(data=window)
                window_token.status = TokenStatus.EVALUATED 
                array.append(window_token)

            token =  ArrayToken(data=Array(array))
            token.status = TokenStatus.EVALUATED
            return token
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"WINDOW_LIST ERROR: {e}")
            return Token(data=Array([]), type=TokenType.ARRAY)  # 오류 시 빈 리스트 반환
        
    @staticmethod
    def WINDOW_FIND_BY_TITLE(title:str) -> Token:
        """특정 제목을 가진 창 반환"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            window_info = pm.find_window_by_title(title)
            if window_info:
                window = Window(title=window_info.title, hwnd=window_info.hwnd, class_name=window_info.class_name)
                token = WindowToken(data=window)
                token.status = TokenStatus.EVALUATED
                return token
            else:
                return NoneToken()  # 창이 없을 경우 None 반환
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"WINDOW_FIND_BY_TITLE ERROR: {e}")
            return NoneToken()
        
    @staticmethod    
    def WINDOW_TOP(process_name:str=None) -> Token:
        """특정 프로세스의 최상위 창 반환"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            top_window = pm.find_top_modal_window(process_name)
            if top_window:
                window = Window(title=top_window.title, hwnd=top_window.hwnd, class_name=top_window.class_name)
                token =  WindowToken(data=window)
                token.status = TokenStatus.EVALUATED
                return token
            else:
                return NoneToken()  # 창이 없을 경우 None 반환
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"WINDOW_TOP ERROR: {e}")
            return NoneToken()
    
    @staticmethod
    def WINDOW_REGION(hwnd: int) -> RegionToken:
        """특정 창의 위치 및 크기를 Region 객체로 반환"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            x,y,w,h = pm.get_window_region(hwnd)
            token = RegionToken(data=Region(x, y, w, h))
            token.status = TokenStatus.EVALUATED
            return token
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"WINDOW_REGION ERROR: {e}")
            return NoneToken()
    

    @staticmethod
    def MONITOR_LIST() -> Token:
        """모니터 리스트 반환"""
        try:
            monitors = get_monitors()
            array = []
            for i, m in enumerate(monitors):
                p = False
                if m.is_primary:
                    p = True
                info = {
                    "name": m.name,
                    "width": m.width,
                    "height": m.height,
                    "x": m.x,
                    "y": m.y,
                    "is_primary": p
                }
                info_token = TokenUtil.dict_to_hashmap_token(info)
                array.append(info_token)
            token = TokenUtil.array_to_array_token(array)
            return token
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"MONITOR_LIST ERROR: {e}")
            return NoneToken()

    @staticmethod
    def SNAP_SCREEN_HASH(region:tuple, grid_shape:str) -> Token:
        """Region 영역을 grid 단위로 나누고 각 조각의 해시값 계산 : grid_shape 10x5"""
        info_list = RpaImageUtil.screen_image_split_and_hash(region, grid_shape)
        array = []
        for info in info_list:
            token = TokenUtil.dict_to_hashmap_token(info)
            array.append(token)
        token = TokenUtil.array_to_array_token(array)
        token.status = TokenStatus.EVALUATED
        return token
    
    @staticmethod
    def SNAP_CHANGED_REGION(before:list[dict], region:tuple, grid_shape:str) -> Token:
        """변경된 영역을 찾아서 Region 객체로 반환"""

        after = RpaImageUtil.screen_image_split_and_hash(region, grid_shape)
        if len(before) != len(after):
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", "비교할 타일 개수가 같지 않습니다.")
            raise KavanaValueError("비교할 타일 개수가 달라요.")

        changed_blocks = []
        before_array =[]
        for b in before:
            hash = b.data.get("hash").data.value
            x = b.data.get("x").data.value
            y = b.data.get("y").data.value
            w = b.data.get("w").data.value
            h = b.data.get("h").data.value
            dict = {
                "hash": hash,
                "x": x,
                "y": y,
                "w": w,
                "h": h
            }
            before_array.append(dict)
        r_dict = RpaImageUtil.changed_region_by_hash(before_array, after)
        x = r_dict.get("x")
        y = r_dict.get("y")
        w = r_dict.get("w")
        h = r_dict.get("h")

        return TokenUtil.region_to_token((x,y,w,h))
    
    def PROCESS_LIST() -> Token:
        """현재 실행 중인 프로세스 리스트 반환"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            process_list = pm.get_process_list()
            array = []
            for process in process_list:
                token = TokenUtil.dict_to_hashmap_token(process)
                array.append(token)
            token = TokenUtil.array_to_array_token(array)
            return token
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"PROCESS_LIST ERROR: {e}")
            return NoneToken()
    
    def PROCESS_IS_RUNNING(process_name:str) -> Token:
        """특정 프로세스가 실행 중인지 확인"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            is_running = pm.is_running(process_name)
            return TokenUtil.boolean_to_boolean_token(is_running)
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"PROCESS_IS_RUNNING ERROR: {e}")
            return NoneToken()
    
    def PROCESS_KILL(process_name:str) -> Token:
        """특정 프로세스 종료, 리턴 boolean token"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            pm.kill_process_by_name(process_name)
            return TokenUtil.boolean_to_boolean_token(True)
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"PROCESS_KILL ERROR: {e}")
            return TokenUtil.boolean_to_boolean_token(False)
        
    def PROCESS_FOCUS(process_name:str) -> Token:
        """특정 프로세스 포커스"""
        try:
            pm = ProcessManager(executor=RpaFunctions.executor)
            b = pm.bring_process_to_foreground(process_name)
            return TokenUtil.boolean_to_boolean_token(b)
        except Exception as e:
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", f"PROCESS_FOCUS ERROR: {e}")
            return TokenUtil.boolean_to_boolean_token(False)