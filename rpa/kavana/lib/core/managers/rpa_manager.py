import time
import pyautogui

from lib.core.builtins.builtin_consts import PointName
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.managers.base_manager import BaseManager

class RPAManager(BaseManager):
    """RPA 기능을 담당하는 매니저"""
    
    def wait(self, seconds: int):
        """✅ WAIT 명령어 실행 (일반 대기)"""
        super().log("INFO", f"[RPA] {seconds}초 동안 대기...")
        time.sleep(seconds)

    def wait_for_image(self, image_path: str, timeout: int = 10, confidence: float = 0.8, grayscale: bool = False, region=None):
        """✅ 특정 이미지가 화면에 나타날 때까지 대기"""
        super().log("INFO", f"[RPA] {timeout}초 동안 이미지 {image_path} 대기 중...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, grayscale=grayscale, region=region)
            if location:
                super().log("INFO", f"[RPA] 이미지 {image_path} 발견됨.")
                return location
            time.sleep(0.5)

        super().log("WARN", f"[RPA] 이미지 {image_path}를 {timeout}초 동안 찾을 수 없음.")
        return None


    def click(self, click_type:str, x:int, y:int, click_count:int=1, duration:float=0.2):
            """ 클릭 유형에 따라 적절한 pyautogui 동작을 실행 """
            if click_type == "single":
                for _ in range(click_count):
                    pyautogui.click(x, y)
            elif click_type == "double":
                pyautogui.doubleClick(x, y)
            elif click_type == "right":
                pyautogui.rightClick(x, y)
            elif click_type == "middle":
                pyautogui.middleClick(x, y)
            elif click_type == "triple":
                pyautogui.tripleClick(x, y)
            elif click_type == "drag":
                pyautogui.mouseDown(x, y)
            elif click_type == "drop":
                pyautogui.mouseUp(x, y)
            elif click_type == "hold":
                pyautogui.mouseDown(x, y)
                time.sleep(duration)
            elif click_type == "release":
                pyautogui.mouseUp(x, y)
            else:
                super().log("ERROR", f"CLICK 명령어의 type 옵션 '{click_type}'은 올바르지 않습니다.")


    def mouse_move(self, x: int, y: int, duration: float = 0.5):
        """✅ 마우스를 특정 위치로 이동"""
        super().log("INFO", f"[RPA] 마우스 이동: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=duration)

    def mouse_click(self, x: int = None, y: int = None, button="left"):
        """✅ 마우스 클릭"""
        if x is not None and y is not None:
            super().log("INFO", f"[RPA] 마우스 클릭: ({x}, {y}) 버튼={button}")
            pyautogui.click(x, y, button=button)
        else:
            super().log("INFO", f"[RPA] 마우스 클릭 (현재 위치) 버튼={button}")
            pyautogui.click(button=button)

    def key_press(self, key: str):
        """✅ 특정 키 입력"""
        super().log("INFO", f"[RPA] 키 입력: {key}")
        pyautogui.press(key)

    def get_point_with_name(self, region, point_name: str):
        """✅ Region 객체에서 point_name에 해당하는 좌표를 반환"""
        x,y,w,h = region
        point_enum = PointName(point_name.lower())
        if point_enum == PointName.CENTER:
            return x + w // 2, y + h // 2
        elif point_enum == PointName.LEFT_TOP:
            return x, y
        elif point_enum == PointName.LEFT_MIDDLE:
            return x, y + h // 2
        elif point_enum == PointName.LEFT_BOTTOM:
            return x, y + h
        elif point_enum == PointName.MIDDLE_TOP:
            return x + w // 2, y
        elif point_enum == PointName.MIDDLE_BOTTOM:
            return x + w // 2, y + h
        elif point_enum == PointName.RIGHT_TOP:
            return x + w, y
        elif point_enum == PointName.RIGHT_MIDDLE:
            return x + w, y + h // 2
        elif point_enum == PointName.RIGHT_BOTTOM:
            return x + w, y + h
        else:
            raise KavanaSyntaxError(f"Region에서 지원하지 않는 PointName: {point_name}")

    def find_image(self, image_path: str, search_region=None,confidence=0.8, grayscale=False):
        try:
            super().log("INFO", f"[RPA] 이미지 {image_path} 찾기 시도...")
            found_region =  pyautogui.locateOnScreen(image_path, confidence=confidence, region=search_region, grayscale=grayscale)
            return found_region
        except pyautogui.ImageNotFoundException:
            return None