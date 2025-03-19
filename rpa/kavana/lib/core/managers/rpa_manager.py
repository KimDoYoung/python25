import time
import pyautogui

from lib.core.managers.base_manager import BaseManager

class RPAManager(BaseManager):
    """RPA 기능을 담당하는 매니저"""
    
    def wait(self, seconds: int):
        """✅ WAIT 명령어 실행 (일반 대기)"""
        super().log("INFO", f"[RPA] {seconds}초 동안 대기...")
        time.sleep(seconds)

    def wait_for_image(self, image_path: str, timeout: int = 10):
        """✅ 특정 이미지가 화면에 나타날 때까지 대기"""
        super().log("INFO", f"[RPA] {timeout}초 동안 이미지 {image_path} 대기 중...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                super().log("INFO", f"[RPA] 이미지 {image_path} 발견됨.")
                return location
            time.sleep(0.5)

        super().log("WARNING", f"[RPA] 이미지 {image_path}를 {timeout}초 동안 찾을 수 없음.")
        return None

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
