import time
from typing import List
import pyautogui
import pyperclip

from lib.core.builtins.builtin_consts import PointName
from lib.core.datatypes.application import Application
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.managers.base_manager import BaseManager
from lib.core.token_type import TokenType

class RpaManager(BaseManager):
    """RPA 기능을 담당하는 매니저"""
    
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs

        if not self.command:
            self.raise_error("command는 필수입니다.")

    def execute(self):
        method_map = {
            "app_open": self.app_open,
            "app_close": self.app_close,
            "wait": self.wait,
            "wait_image_and_click": self.wait_image_and_click,
            "click_point": self.click_point,
            "click_image": self.click_image,
            "mouse_move": self.mouse_move,
            "key_in": self.key_in,
            "put_text": self.put_text,
            "get_text": self.get_text,
            "capture": self.capture,
        }

        func = method_map.get(self.command.lower())
        if not func:
            self.raise_error(f"RPA 명령어에서 지원하지 않는 sub명령어: {self.command}")

        result = func()  # 실제 실행

        return result

    def app_open(self):
        ''' 애플리케이션 실행 '''
        from_var = self.options.get("from_var")
        maximize = self.options.get("maximize", False)
        process_name = self.options.get("process_name")

        if not from_var:
            self.raise_error("app_open 명령에는 'from_var' 옵션이 필요합니다.")

        app_token = self.executor.get_variable(from_var)

        if app_token.type != TokenType.APPLICATION:
            self.raise_error(f"'{from_var}'는 Application 인스턴스가 아닙니다.")

        app = app_token.data
        self.log("INFO", f"Application 실행: {app.path}")
        try:
            app.launch(
                executor=self.executor,
                maximize=maximize,
                process_name=process_name
            )
        except Exception as e:
            self.raise_error(f"Application 실행 실패: {e}")

    def app_close(self):
        ''' 애플리케이션 종료 '''
        from_var = self.options.get("from_var")

        if not from_var:
            self.raise_error("app_close 명령에는 'from_var' 옵션이 필요합니다.")

        app_token = self.executor.get_variable(from_var)

        if app_token.type != TokenType.APPLICATION:
            self.raise_error(f"'{from_var}'는 Application 인스턴스가 아닙니다.")
        app = app_token.data
        self.log("INFO", f"Application 종료 요청: {app.path}")
        try:
            app.close()
            self.log("INFO", f"Application 종료 완료: {app.path}")
        except Exception as e:
            self.raise_error(f"Application 종료 실패: {e}")



    def wait(self):
        """ WAIT 명령어 실행 (일반 대기)"""
        seconds = self.options.get("seconds")

        if not isinstance(seconds, int) or seconds < 0:
            self.raise_error("seconds는 0 이상의 정수여야 합니다.")

        self.log("INFO", f"[RPA] {seconds}초 동안 대기 시작...")

        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            super().log("WARNING", "[RPA] 대기 중단됨 (사용자 인터럽트)")
            raise

        self.log("INFO", "[RPA] 대기 완료")

    def wait_image_and_click(self):
        """RPA 명령어: find_image_and_click - 특정 이미지가 화면에 나타날 때까지 대기 그리고 click"""
        region = self.options.get("area")
        timeout = int(self.options.get("timeout", 10))
        grayscale = self.options.get("grayscale", False)
        confidence = float(self.options.get("confidence", 0.8))

        target_image = self._load_pilimage()

        # Region 객체를 pyautogui 호환 튜플로 변환
        if region and hasattr(region, "left"):
            region = (region.left, region.top, region.width, region.height)

        self.log("INFO", f"[RPA] {timeout}초 동안 대기 중...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(
                    target_image,
                    confidence=confidence,
                    grayscale=grayscale,
                    region=region
                )
                if location:
                    center = pyautogui.center(location)
                    pyautogui.moveTo(center)
                    pyautogui.click(center)
                    self.log("INFO", f"[RPA] 이미지  발견됨: {location}")

                    return location
            except Exception as e:
                self.log("ERROR", f"[RPA] 이미지 검색 중 오류 발생: {e}")

            time.sleep(0.5)

        self.log("WARN", f"[RPA] 이미지  {timeout}초 내에 찾을 수 없음.")
        return None

    def click_point(self):
        """RPA 명령어: click_point - 주어진 좌표에서 마우스 클릭 수행"""

        x = self.options.get("x")
        y = self.options.get("y")
        click_count = int(self.options.get("click_count", 1))
        click_type = self.options.get("click_type", "left").lower()
        duration = float(self.options.get("duration", 0.2))  # duration은 기본 0초 (즉시 클릭)

        if x is None or y is None:
            self.raise_error("click_point 명령에는 'x'와 'y' 값이 필요합니다.")

        # 좌표 로그
        self.log("INFO", f"[RPA] 위치 ({x}, {y}) 클릭 - 타입: {click_type}, 횟수: {click_count}, duration: {duration}")

        # 유효한 클릭 타입 확인
        if click_type not in ("left", "right", "double"):
            self.raise_error(f"지원되지 않는 click_type: {click_type} (left|right|double만 가능)")

        # 클릭 수행
        pyautogui.moveTo(x, y, duration=duration if click_count == 1 else 0)

        if click_type == "double":
            pyautogui.doubleClick(x, y)
        elif click_type == "right":
            for _ in range(click_count):
                pyautogui.rightClick(x, y)
                if click_count > 1 and duration > 0:
                    time.sleep(duration)
        else:  # 기본 left click
            for _ in range(click_count):
                pyautogui.click(x, y)
                if click_count > 1 and duration > 0:
                    time.sleep(duration)

        self.log("INFO", f"[RPA] CLICK_POINT  완료")


    # def click(self, click_type:str, x:int, y:int, click_count:int=1, duration:float=0.2):
    #         """ 클릭 유형에 따라 적절한 pyautogui 동작을 실행 """
    #         if click_type == "single":
    #             for _ in range(click_count):
    #                 pyautogui.click(x, y)
    #         elif click_type == "double":
    #             pyautogui.doubleClick(x, y)
    #         elif click_type == "right":
    #             pyautogui.rightClick(x, y)
    #         elif click_type == "middle":
    #             pyautogui.middleClick(x, y)
    #         elif click_type == "triple":
    #             pyautogui.tripleClick(x, y)
    #         elif click_type == "drag":
    #             pyautogui.mouseDown(x, y)
    #         elif click_type == "drop":
    #             pyautogui.mouseUp(x, y)
    #         elif click_type == "hold":
    #             pyautogui.mouseDown(x, y)
    #             time.sleep(duration)
    #         elif click_type == "release":
    #             pyautogui.mouseUp(x, y)
    #         else:
    #             super().log("ERROR", f"CLICK 명령어의 type 옵션 '{click_type}'은 올바르지 않습니다.")


    def click_image(self):
        """RPA 명령어: click_image - 화면에서 이미지 찾아 클릭"""
        region = self.options.get("area")
        timeout = int(self.options.get("timeout", 10))
        grayscale = self.options.get("grayscale", False)
        confidence = float(self.options.get("confidence", 0.8))

        target_img = self._load_pilimage()

        # region 객체 변환
        if region and hasattr(region, 'left'):
            region = (region.left, region.top, region.width, region.height)

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(
                    target_img,
                    region=region,
                    grayscale=grayscale,
                    confidence=confidence
                )
                if location:
                    center = pyautogui.center(location)
                    pyautogui.moveTo(center)
                    pyautogui.click()
                    self.log("INFO", f"[RPA] 이미지 클릭 완료: {center}")
                    return center
            except Exception as e:
                self.log("ERROR", f"[RPA] 이미지 검색 중 오류 발생: {e}")

            time.sleep(0.5)

        self.log("WARN", f"[RPA] click_image  이미지를 {timeout}초 내에 찾지 못했습니다.")
        return None


    def mouse_move(self):
        """RPA 명령어: mouse_move - 마우스를 지정 좌표로 이동 (절대/상대)"""

        x = self.options.get("x")
        y = self.options.get("y")
        duration = float(self.options.get("duration", 0))
        relative = self.options.get("relative", False)

        if x is None or y is None:
            self.raise_error("mouse_move 명령에는 'x'와 'y' 옵션이 필요합니다.")

        if relative:
            current_x, current_y = pyautogui.position()
            x += current_x
            y += current_y
            self.log("DEBUG", f"[RPA] 상대 이동 → 기준: ({current_x}, {current_y}) → 목적지: ({x}, {y})")

        self.log("INFO", f"[RPA] 마우스 이동 → ({x}, {y}), duration={duration}s")
        pyautogui.moveTo(x, y, duration=duration)


    def key_press(self, key: str):
        """ 특정 키 입력"""
        super().log("INFO", f"[RPA] 키 입력: {key}")
        pyautogui.press(key)

    def _get_point_with_name(self, region, point_name: str):
        """ Region 객체에서 point_name에 해당하는 좌표를 반환"""
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
        """ 이미지를 찾아서 이미지의 영역을 리턴,실패시 None 리턴 """
        try:
            super().log("INFO", f"[RPA] 이미지 {image_path} 찾기 시도...")
            found_region =  pyautogui.locateOnScreen(image_path, confidence=confidence, region=search_region, grayscale=grayscale)
            return found_region
        except pyautogui.ImageNotFoundException:
            return None
    

    def key_in(self):
        """RPA 명령어: key_in - Enter, Ctrl, Alt 등 특수 키 입력"""

        keys = self.options.get("keys")
        speed = float(self.options.get("speed", 0.5))

        if not keys:
            self.raise_error("key_in 명령에는 'keys' 옵션이 필요합니다.")

        # 문자열 하나만 들어온 경우 리스트로 처리
        if isinstance(keys, str):
            keys = [keys]

        self.log("INFO", f"[RPA] 특수 키 입력 시작: {keys}, 간격: {speed}s")

        for key in keys:
            key = key.strip().lower()

            # 허용된 특수 키만 처리
            if '+' in key:
                parts = key.split('+')
                self.log("DEBUG", f"[RPA] 조합 키 입력: {parts}")
                pyautogui.hotkey(*parts)
            else:
                self.log("DEBUG", f"[RPA] 단일 키 입력: {key}")
                pyautogui.press(key)

            time.sleep(speed)

        self.log("INFO", "[RPA] 특수 키 입력 완료")


    def put_text(self):
        """RPA 명령어: put_text - 텍스트를 클립보드로 복사해 붙여넣기"""

        text = self.options.get("text")
        if not text:
            self.raise_error("put_text 명령에는 'text' 옵션이 필요합니다.")

        self.log("INFO", f"[RPA] 텍스트 입력 시작: {text}")

        try:
            # 클립보드에 텍스트 복사
            pyperclip.copy(text)
            time.sleep(0.2)  # 클립보드 안정화 대기

            # 붙여넣기
            pyautogui.hotkey("ctrl", "v")
            self.log("INFO", "[RPA] 텍스트 입력 완료 (Ctrl+V)")
        except Exception as e:
            self.raise_error(f"[RPA] 텍스트 입력 중 오류 발생: {e}")


    def get_text(self):
        """RPA 명령어: get_text - 현재 위치에서 텍스트 복사 후 변수에 저장"""

        to_var = self.options.get("to_var")
        strip = self.options.get("strip", True)
        wait_before = float(self.options.get("wait_before", 0.5))

        if not to_var:
            self.raise_error("get_text 명령에는 'to_var' 옵션이 필요합니다.")

        self.log("INFO", f"[RPA] 텍스트 복사 시작 (to_var: {to_var}, strip={strip}, wait_before={wait_before}s)")

        try:
            if wait_before > 0:
                time.sleep(wait_before)

            # 전체 선택 후 복사
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.2)  # 클립보드 복사 대기

            # 클립보드에서 읽어오기
            copied_text = pyperclip.paste()

            if strip and isinstance(copied_text, str):
                copied_text = copied_text.strip()

            if not copied_text:
                self.log("WARN", "[RPA] 복사된 텍스트가 비어 있습니다.")

            # 변수 저장
            self.set_variable(to_var, copied_text)
            self.log("INFO", f"[RPA] 텍스트 복사 완료 → 변수 '{to_var}'에 저장됨")

        except Exception as e:
            self.raise_error(f"[RPA] 텍스트 복사 중 오류 발생: {e}")


    def capture(self):
        """RPA 명령어: capture - 화면 또는 특정 영역을 이미지로 캡처 (파일 저장 또는 변수 저장)"""

        area = self.options.get("area")  # Region 객체
        to_file = self.options.get("to_file")
        to_var = self.options.get("to_var")

        if not to_file and not to_var:
            self.raise_error("capture 명령에는 'to_file' 또는 'to_var' 중 하나는 필요합니다.")

        # 영역 지정이 있다면 pyautogui용 튜플로 변환
        region = None
        if area and hasattr(area, "left"):
            region = (area.left, area.top, area.width, area.height)

        try:
            self.log("INFO", f"[RPA] 화면 캡처 시작 (영역: {region if region else '전체 화면'})")

            # 스크린샷 찍기
            screenshot = pyautogui.screenshot(region=region)

            # to_file로 저장
            if to_file:
                screenshot.save(to_file)
                self.log("INFO", f"[RPA] 이미지 저장 완료: {to_file}")

            # to_var에 저장
            if to_var:
                self.set_variable(to_var, screenshot)
                self.log("INFO", f"[RPA] 이미지 객체 변수 저장 완료: {to_var}")

        except Exception as e:
            self.raise_error(f"[RPA] 화면 캡처 실패: {e}")

    
    def _load_pilimage(self):
        ''' from_file 또는 from_var에서 이미지를 로드 (PIL.Image 객체 반환) '''
        from PIL import Image as PILImage
        import numpy as np

        from_var = self.options.get("from_var")
        from_file = self.options.get("from_file")

        if from_var:
            img_token = self.executor.get_variable(from_var)
            if not img_token:
                self.raise_error(f"'{from_var}' 변수에서 이미지를 찾을 수 없습니다.")
            if img_token.type != TokenType.IMAGE:
                self.raise_error(f"'{from_var}'는 이미지 객체가 아닙니다.")

            # numpy 배열 → PIL 이미지로 변환
            img_np = img_token.data
            if not isinstance(img_np.data, np.ndarray):
                self.raise_error(f"'{from_var}'는 유효한 numpy 이미지가 아닙니다.")
            try:
                return PILImage.fromarray(img_np.data)
            except Exception as e:
                self.raise_error(f"이미지 변환 실패: {str(e)}")

        elif from_file:
            if not isinstance(from_file, str):
                self.raise_error(f"'{from_file}'는 문자열 경로여야 합니다.")
            try:
                return PILImage.open(from_file)
            except Exception as e:
                self.raise_error(f"이미지 파일 열기 실패: {from_file} -> {e}")
        else:
            self.raise_error("'from_file' 또는 'from_var' 중 하나는 반드시 필요합니다.")

            
