import os
import re
import tempfile
import time
from typing import List, Tuple
import pyautogui
import pyperclip

from lib.core.builtins.builtin_consts import PointName
from lib.core.datatypes.application import Application
from lib.core.datatypes.image import Image
from lib.core.exceptions.kavana_exception import KavanaSyntaxError, KavanaValueError
from lib.core.managers.base_manager import BaseManager
from lib.core.token import NoneToken
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

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
            "open_app": self.open_app,
            "close_app": self.close_app,
            "wait": self.wait,
            "wait_image": self.wait_image,
            "click_point": self.click_point,
            "click_image": self.click_image,
            "click_region": self.click_region,
            "find_image": self.find_image,
            "move_mouse": self.move_mouse,
            "key_in": self.key_in,
            "put_text": self.put_text,
            "get_text": self.get_text,
            "capture": self.capture,
            "close_all_children": self.close_all_children,
            "focus_app": self.focus_app,
        }

        func = method_map.get(self.command.lower())
        if not func:
            self.raise_error(f"RPA 명령어에서 지원하지 않는 sub명령어: {self.command}")
            return None

        result = func()  # 실제 실행

        return result

    def open_app(self):
        ''' 애플리케이션 실행 '''
        from_var = self.options.get("from_var")
        maximize = self.options.get("maximize", False)
        process_name = self.options.get("process_name")
        focus = self.options.get("focus")

        if not from_var:
            self.raise_error("open_app 명령에는 'from_var' 옵션이 필요합니다.")

        app_token = self.executor.get_variable(from_var)

        if app_token.type != TokenType.APPLICATION:
            self.raise_error(f"'{from_var}'는 Application 인스턴스가 아닙니다.")

        app = app_token.data
        self.log("INFO", f"Application 실행: {app.path}")
        try:
            app.launch(
                executor=self.executor,
                maximize=maximize,
                process_name=process_name,
                focus = focus
            )
        except Exception as e:
            self.raise_error(f"Application 실행 실패: {e}")

    def close_app(self):
        ''' 애플리케이션 종료 '''
        from_var = self.options.get("from_var")

        if not from_var:
            self.raise_error("close_app 명령에는 'from_var' 옵션이 필요합니다.")

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

    def close_all_children(self):
        '''' 자식 윈도우 모두 닫기 '''
        from_var = self.options.get("from_var")
        if not from_var:
            self.raise_error("close_all_children 명령에는 'from_var' 옵션이 필요합니다.")

        app_token = self.executor.get_variable(from_var)

        if app_token.type != TokenType.APPLICATION:
            self.raise_error(f"'{from_var}'는 Application 인스턴스가 아닙니다.")
        app = app_token.data
        try:
            app.close_child_windows(executor=self.executor)
            self.log("INFO", f"close all childredn window  완료: {app.path}")
        except Exception as e:
            self.raise_error(f"close all childredn window 실패: {e}")

    def focus_app(self):
        """RPA 명령어: reconnect - 연결된 애플리케이션을 재연결"""
        from_var = self.options.get("from_var")
        if not from_var:
            self.raise_error("reconnect 명령에는 'from_var' 옵션이 필요합니다.")

        app_token = self.executor.get_variable(from_var)
        if app_token.type != TokenType.APPLICATION:
            self.raise_error(f"'{from_var}'는 Application 인스턴스가 아닙니다.")

        app = app_token.data
        try:
            app.reconnect(executor=self.executor, focus=True)
            self.log("INFO", f"Application 재연결 완료: {app.path}")
        except Exception as e:
            self.raise_error(f"Application 재연결 실패: {e}")

    def wait(self):
        """ WAIT 명령어 실행 (일반 대기)"""
        seconds = self.options.get("seconds")
        minutes = self.options.get("minutes")

        if seconds is not None:
            if not isinstance(seconds, int) or seconds < 0:
                self.raise_error("seconds는 0 이상의 정수여야 합니다.")

            self.log("INFO", f"[RPA:wait] {seconds}초 동안 대기 시작...")
        elif minutes is not None:
            if not isinstance(minutes, int) or minutes < 0:
                self.raise_error("minutes는 0 이상의 정수여야 합니다.")
            seconds = minutes * 60
            self.log("INFO", f"[RPA:wait] {minutes}분 동안 대기 시작...")

        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            super().log("WARN", "[RPA:wait] 대기 중단됨 (사용자 인터럽트)")
            raise

        self.log("INFO", f"[RPA:wait] {seconds} 대기 완료")

    def wait_image(self):
        """RPA 명령어: find_image - 특정 이미지가 화면에 나타날 때까지 대기 그리고 click"""
        region = self.options.get("area")
        timeout = int(self.options.get("timeout", 10))
        grayscale = self.options.get("grayscale", False)
        confidence = float(self.options.get("confidence", 0.8))
        after = self.options.get("after", None)
        to_var = self.options.get("to_var", None)

        target_image = self._load_pilimage()

        # Region 객체를 pyautogui 호환 튜플로 변환
        if region and hasattr(region, "left"):
            region = (region.left, region.top, region.width, region.height)

        self.log("INFO", f"[RPA:wait_image] {timeout}초 동안 대기 중...")

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
                    self.log("INFO", f"[RPA:wait_image] 이미지 {target_image.filename}  발견됨: {location}")
                    self._after_action(location, after)
                    if to_var:
                        region_token = TokenUtil.region_to_token(location)
                        self.executor.set_variable(to_var, region_token)
                    return location
                    
            except Exception as e:
                self.log("WARN", f"[RPA:wait_image] 이미지 {target_image.filename} 검색 중... 아직 발견하지 못함:  {type(e).__name__} - {str(e)}")

            time.sleep(3)
        if to_var:
            self.executor.set_variable(to_var, NoneToken())
        self.log("ERROR", f"[RPA:wait_image] 이미지 {target_image.filename} {timeout}초 내에 찾을 수 없음.")
        return None
    
    def click_region(self):
        """RPA 명령어: click_region - 지정된 영역에서 클릭 수행"""
        region = self.options.get("name")
        x,y,w,h =  region
        center = ((x + w) // 2, y + h // 2)
        self.options["location"] = center
        return self.click_point()
    
    def click_point(self):
        """RPA 명령어: click_point - 주어진 좌표에서 마우스 클릭 수행"""

        x = self.options.get("x")
        y = self.options.get("y")
        location = self.options.get("location")
        click_count = int(self.options.get("click_count", 1))
        click_type = self.options.get("click_type", "left").lower()
        duration = float(self.options.get("duration", 0.5))  # duration은 기본 0초 (즉시 클릭)
        speed = float(self.options.get("speed", 0.5))  # speed는 기본 0.5초 (사람처럼 클릭)
        turtle = self.options.get("turtle", False)
        if location:
            x,y = location
        # 좌표 로그
        self.log("INFO", f"[RPA:click_point] 위치 ({x}, {y}) 클릭 - 타입: {click_type}, 횟수: {click_count}, duration: {duration}")

        # 유효한 클릭 타입 확인
        if click_type not in ("left", "right", "double"):
            self.raise_error(f"지원되지 않는 click_type: {click_type} (left|right|double만 가능)")

        # 이동
        now_x, now_y = pyautogui.position()
        if turtle :
            mid_x, mid_y = x, now_y
            # 거북이 모드: 현재 위치에서 클릭 위치까지 이동
            pyautogui.moveTo(mid_x, mid_y, duration=speed)
        pyautogui.moveTo(x, y, duration=speed)
        
        # 클릭 수행
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


        # 클릭 후 추가 작업 수행 (예: 대기, 이동 등)
        after = self.options.get("after")
        if after:
            self._after_action(location, after)

        self.log("INFO", f"[RPA:click_point] CLICK_POINT  완료")


    def click_image(self):
        """RPA 명령어: click_image - 화면에서 이미지 찾아 클릭"""
        region = self.options.get("area")
        grayscale = self.options.get("grayscale", False)
        confidence = float(self.options.get("confidence", 0.8))
        after = self.options.get("after", None)
        to_var = self.options.get("to_var", None)

        target_img = self._load_pilimage()

        # region 객체 변환
        if region and hasattr(region, 'left'):
            region = (region.left, region.top, region.width, region.height)

        try:
            location = pyautogui.locateOnScreen(
                target_img,
                region=region,
                grayscale=grayscale,
                confidence=confidence
            )
            if location:
                center = pyautogui.center(location)
                result_token = TokenUtil.region_to_token(location)
                if to_var:
                    self.executor.set_variable(to_var, result_token)
                pyautogui.click(center.x, center.y)    
                self.log("INFO", f"[RPA:click_image] {target_img.filename} 이미지 클릭 완료: {center}")
                if after:
                    self._after_action(location, after)
                return center
        except Exception as e:
            self.log("ERROR", f"[RPA:click_image] 이미지 {target_img.filename} 검색 중 오류 발생: {e}")
            if to_var:
                self.executor.set_variable(to_var, NoneToken())

        self.log("WARN", f"[RPA:click_image] click_image  이미지를 {target_img.filename}초 내에 찾지 못했습니다.")
        return None

    def find_image(self):
        """ 이미지를 찾아서 center point를 to_var에 넣는다. 못찾았으면 None을 넣는다."""
        search_region = self.options.get("area")
        grayscale = self.options.get("grayscale", True)
        confidence = float(self.options.get("confidence", 0.8))
        after = self.options.get("after", None)
        to_var = self.options.get("to_var", None)
        multi = self.options.get("multi", False)

        target_img = self._load_pilimage()

        try:
            super().log("INFO", f"[RPA:find_image] 이미지 {target_img.filename} 찾기 시도...")
            found_regions = []
            
            if multi:
                found_regions = list(pyautogui.locateAllOnScreen(
                    target_img, region=search_region, confidence=confidence, grayscale=grayscale
                ))
            else:
                found_region = pyautogui.locateOnScreen(
                    target_img, region=search_region, confidence=confidence, grayscale=grayscale
                )
                if found_region:
                    found_regions = [found_region]
            
            result_list = []
            last_center = None
            
            for region in found_regions:
                center = pyautogui.center(region)
                last_center = center  # 마지막 center 저장
                token = TokenUtil.xy_to_point_token(center.x, center.y)
                result_list.append(token)
            
            if result_list:
                if multi:
                    result_token = TokenUtil.array_to_array_token(result_list)
                else:
                    result_token = result_list[0]  # 첫 번째 결과만 사용
            else:
                result_token = NoneToken() #TokenUtil.array_to_array_token([])  # 비어 있는 list
            
            if to_var:
                self.executor.set_variable(to_var, result_token)
            
            if last_center:
                super().log("INFO", f"[RPA:find_image] 이미지 {target_img.filename} 찾기 완료: {last_center.x}, {last_center.y}")
            else:
                super().log("INFO", f"[RPA:find_image] 이미지 {target_img.filename} 찾기 결과 없음")
            
            if after and found_regions:
                self._after_action(found_regions[0], after)
            return found_regions

        except Exception as e:
            super().log("WARN", f"[RPA:find_image] 이미지 {target_img.filename} 찾기 실패: {str(e)}")
            if to_var:
                result_token = NoneToken()
                self.executor.set_variable(to_var, result_token)
            return None


    def move_mouse(self):
        """RPA 명령어: move_mouse - 마우스를 지정 좌표로 이동 (절대/상대)"""

        x = self.options.get("x")
        y = self.options.get("y")
        location = self.options.get("location", None)
        locations = self.options.get("locations", None)
        duration = float(self.options.get("duration", 0.5))
        speed = float(self.options.get("speed", 0.5))
        relative = self.options.get("relative", False)
        after = self.options.get("after", None)

        if location:
            x, y = location            

        if relative and not locations:
            current_x, current_y = pyautogui.position()
            x += current_x
            y += current_y
            self.log("DEBUG", f"[RPA] 상대 이동 → 기준: ({current_x}, {current_y}) → 목적지: ({x}, {y})")

        self.log("INFO", f"[RPA] 마우스 이동 → ({x}, {y}), duration={speed}s")
        if locations:
            for pt in locations:
                x,y = pt
                pyautogui.moveTo(x, y, duration=speed)    
        else:
            pyautogui.moveTo(x, y, duration=speed)
        if after:
            self._after_action(None, after)
        return


    def key_in(self):
        """RPA 명령어: key_in - Enter, Ctrl, Alt 등 특수 키 입력"""

        keys = self.options.get("keys")
        speed = float(self.options.get("speed", 0.5))
        after = self.options.get("after", None)

        if not keys:
            self.raise_error("key_in 명령에는 'keys' 옵션이 필요합니다.")

        # 문자열 하나만 들어온 경우 리스트로 처리
        if isinstance(keys, str):
            keys = [keys]

        self.log("INFO", f"[RPA:key_in] 특수 키 입력 시작: {keys}, 간격: {speed}s")

        for key in keys:
            key = key.strip().lower()

            # 허용된 특수 키만 처리
            if '+' in key:
                parts = key.split('+')
                self.log("DEBUG", f"[RPA:key_in] 조합 키 입력: {parts}")
                pyautogui.hotkey(*parts)
            else:
                self.log("DEBUG", f"[RPA:key_in] 단일 키 입력: {key}")
                pyautogui.press(key)

            time.sleep(speed)

        if after:
            self._after_action(None, after)

        self.log("INFO", "[RPA:key_in] 특수 키 입력 완료")


    def put_text(self):
        """RPA 명령어: put_text - 텍스트를 클립보드로 복사해 붙여넣기"""

        text = self.options.get("text")
        clipboard = self.options.get("clipboard")
        if not text:
            self.raise_error("put_text 명령에는 'text' 옵션이 필요합니다.")

        self.log("INFO", f"[RPA:put_text] 텍스트 입력 시작: {text}")

        try:
            if clipboard:
                # 클립보드에 텍스트 복사
                pyperclip.copy(text)
                # 붙여넣기
                pyautogui.hotkey("ctrl", "v")
            else:
                pyautogui.write(text, interval=0.05)  # 사람처럼 입력 (0.05초 간격)
            time.sleep(0.2)  # 클립보드 안정화 대기

            self.log("INFO", "[RPA:put_text] 텍스트 입력 완료 (Ctrl+V)")
        except Exception as e:
            self.raise_error(f"[RPA:put_text] 텍스트 입력 중 오류 발생: {e}")


    def get_text(self):
        """RPA 명령어: get_text - 현재 위치에서 텍스트 복사 후 변수에 저장"""

        to_var = self.options.get("to_var")
        strip = self.options.get("strip", True)
        wait_before = float(self.options.get("wait_before", 0.5))

        if not to_var:
            self.raise_error("get_text 명령에는 'to_var' 옵션이 필요합니다.")

        self.log("INFO", f"[RPA:get_text] 텍스트 복사 시작 (to_var: {to_var}, strip={strip}, wait_before={wait_before}s)")

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
                self.log("WARN", "[RPA:get_text] 복사된 텍스트가 비어 있습니다.")

            # 변수 저장
            self.executor.set_variable(to_var, copied_text)
            self.log("INFO", f"[RPA:get_text] 텍스트 복사 완료 → 변수 '{to_var}'에 저장됨")

        except Exception as e:
            self.log("ERROR", f"[RPA:get_text] 텍스트 복사 중 오류 발생: {e}")
            self.raise_error(f"[RPA:get_text] 텍스트 복사 중 오류 발생: {e}")
    
    # def _get_temp_file_path(self, suffix=".png", prefix="tmp_", dir=None):
    #     """임시 파일 경로를 생성하고 반환 (파일 생성은 안 함)"""
    #     tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    #     os.close(tmp_fd)  # 파일 디스크립터는 닫아줌 (파일은 그대로 있음)
    #     return tmp_path

    def capture(self):
        """RPA 명령어: capture - 화면 또는 특정 영역을 이미지로 캡처 (파일 저장 또는 변수 저장)"""

        area = self.options.get("area")  # Region 객체
        to_file = self.options.get("to_file")
        to_var = self.options.get("to_var")

        if not to_file and not to_var:
            self.raise_error("capture 명령에는 'to_file' 또는 'to_var' 중 하나는 필요합니다.")

        # 영역 지정이 있다면 pyautogui용 튜플로 변환
        region = None
        if area:
            region = area
            # region = (area.left, area.top, area.width, area.height)
            # region = (area[0], area[1], area[2], area[3])

        try:
            self.log("INFO", f"[RPA] 화면 캡처 시작 (영역: {region if region else '전체 화면'})")

            # 스크린샷 찍기
            screenshot = pyautogui.screenshot(region=region)
            image_path = self._get_temp_file_path(suffix=".png", prefix="screenshot_")
            if to_file:
                image_path = to_file
            screenshot.save(image_path)
            self.log("INFO", f"[RPA:capture] 이미지 저장 완료: {image_path}")

            # to_var에 저장
            if to_var:
                image = Image(image_path)
                image_token = TokenUtil.image_to_image_token(image)
                self.executor.set_variable(to_var, image_token)
                self.log("INFO", f"[RPA:capture] 이미지 객체 변수 저장 완료: {to_var}")

        except Exception as e:
            self.log("ERROR", f"[RPA:capture] 화면 캡처 중 오류 발생: {e}")
            self.raise_error(f"[RPA:capture] 화면 캡처 실패: {e}")

    
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

    def _after_action(self, location: Tuple[int,int,int,int], after):
        """ 추가 작업 수행 """
        if not after:
            return
        action = after.lower()
        if action == "click"  and location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center)
                pyautogui.click(center)
        elif action == "move" and location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center)
        elif action.startswith("wait"): # wait:3ㄴㄴ
            match = re.match(r"wait\s*:\s*(\d+)\s*([sm])", action)
            if not match:
                raise KavanaValueError("올바른 형식 after wait 문자열이 아닙니다. 예: 'wait: 3m' 또는 'wait:3s'")
            number = int(match.group(1))  # 숫자 추출
            unit = match.group(2)         # 단위 추출 ('s' 또는 'm')

            if unit == "s":
                self.log("INFO", f"[RPA:after] {number}초 대기")
                time.sleep(number)  # 초 단위 대기
            elif unit == "m":
                time.sleep(number * 60)  # 분 단위 대기 
        return