
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
                window = Window(title=window_info.title, hwnd=window_info.hwnd, class_name=window)
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
                p = ""
                if m.is_primary:
                    p = "Primary"
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
    def screen_image_split_and_hash(region: tuple, grid_shape: str) -> list[dict]:
        """Region 영역을 grid 단위로 나누고 각 조각의 해시값 계산"""
        x, y, w, h = region
        cols, rows = map(int, grid_shape.lower().split("x"))  # 예: "10x5"
        tile_w, tile_h = w // cols, h // rows

        full_image = pyautogui.screenshot(region=(x, y, w, h))
        blocks = []

        for row in range(rows):
            for col in range(cols):
                cx = col * tile_w
                cy = row * tile_h
                tile = full_image.crop((cx, cy, cx + tile_w, cy + tile_h))
                tile_hash = str(imagehash.average_hash(tile))
                blocks.append({
                    "hash": tile_hash,
                    "x": x + cx,
                    "y": y + cy,
                    "w": tile_w,
                    "h": tile_h
                })
        
        return blocks

    @staticmethod
    def SNAP_SCREEN_INFO(region:tuple, grid_shape:str) -> Token:
        """Region 영역을 grid 단위로 나누고 각 조각의 해시값 계산"""
        info_list = RpaFunctions.screen_image_split_and_hash(region, grid_shape)
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

        after = RpaFunctions.screen_image_split_and_hash(region, grid_shape)
        if len(before) != len(after):
            if RpaFunctions.executor:
                RpaFunctions.executor.log_command("ERROR", "비교할 타일 개수가 같지 않습니다.")
            raise KavanaValueError("비교할 타일 개수가 달라요.")

        changed_blocks = []
        before_array =[]
        for b in before:
            before_array.append(b.data.primitive)

        for b, a in zip(before_array, after):
            if b["hash"] != a["hash"]:
                changed_blocks.append(a)

        if not changed_blocks:
            return TokenUtil.region_to_token((0,0,0,0))

        # 변화된 블록들을 포함하는 최소 bounding box 계산
        min_x = min(block["x"] for block in changed_blocks)
        min_y = min(block["y"] for block in changed_blocks)
        max_x = max(block["x"] + block["w"] for block in changed_blocks)
        max_y = max(block["y"] + block["h"] for block in changed_blocks)

        return TokenUtil.region_to_token((min_x, min_y, max_x - min_x, max_y - min_y))