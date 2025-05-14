import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from lib.core.managers.base_manager import BaseManager
from lib.core.token import Token
from lib.core.token_util import TokenUtil

class BrowserManager(BaseManager):
    _driver = None

    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs

        if not self.command:
            self.raise_error("command는 필수입니다.")

    def execute(self):
        method_map = {
            "open": self.open_browser,
            "wait": self.wait,
            "extract": self.extract,
            "click": self.click,
            "put_text": self.put_text,
            "get_text": self.get_text,
            "capture": self.capture,
            "execute_js": self.execute_js,
            "find_elements": self.find_elements,
            "scroll_to": self.scroll_to,
            "switch_iframe": self.switch_iframe,
            "close": self.close_browser
        }
        
        func = method_map.get(self.command)
        if not func:
            self.log("ERROR", f"BROWSER Manager: 알 수 없는 명령어: {self.command}")
            self.raise_error(f"BROWSER Manager 지원하지 않는 명령어: {self.command}")
        
        # 실행 코드 추가
        return func()


    def _get_driver(self):
        if BrowserManager._driver is None:
            options = webdriver.ChromeOptions()
            if self.options.get("headless", False):
                # 최신 Chrome 버전에서 권장되는 headless 모드 설정
                options.add_argument("--headless=new")
            if self.options.get("user_agent"):
                options.add_argument(f"user-agent={self.options['user_agent']}")
            if self.options.get("window_size"):
                options.add_argument(f"--window-size={self.options['window_size']}")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu") # GPU X
            # options.add_argument("--disable-software-rasterizer") # 고급옵션 X
            # options.add_experimental_option('excludeSwitches', ['enable-logging']) #로그사용X 
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('useAutomationExtension', False)
            
            try:
                BrowserManager._driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=options
                )
            except Exception as e:
                self.log("ERROR", f"브라우저 드라이버 초기화 오류: {str(e)}")
                self.raise_error(f"브라우저 드라이버 초기화 실패: {str(e)}")
                
        return BrowserManager._driver

    def open_browser(self):
        url = self.options.get("url")
        if not url:
            self.raise_error("url 옵션이 필요합니다.")
        driver = self._get_driver()
        driver.get(url)
        self.log("INFO", f"브라우저 열기: {url}")

    def click(self):
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        timeout = int(self.options.get("timeout", 10))
        scroll_first = self.options.get("scroll_first", True)
        click_js = self.options.get("click_js", False)

        if not select:
            self.raise_error("select 옵션이 필요합니다.")

        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }.get(select_by, By.CSS_SELECTOR)

        driver = self._get_driver()

        try:
            search_scope = driver
            if within:
                search_scope = driver.find_element(by, within)
                self.log("INFO", f"within 요소 탐색 성공: {within}")

            self.log("INFO", f"요소 클릭 대기 중: {select}")
            element = WebDriverWait(search_scope, timeout).until(
                EC.element_to_be_clickable((by, select))
            )

            if scroll_first:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.log("INFO", f"스크롤 완료: {select}")

            if click_js:
                driver.execute_script("arguments[0].click();", element)
                self.log("INFO", f"JS로 클릭 완료: {select}")
            else:
                element.click()
                self.log("INFO", f"클릭 완료: {select}")

        except Exception as e:
            self.log("ERROR", f"클릭 실패: {select} - {str(e)}")
            self.raise_error(f"클릭 실패: {str(e)}")

    def wait(self): 
        selector = self.options.get("select")
        seconds = self.options.get("seconds")
        until = self.options.get("until", "visible")
        timeout = int(self.options.get("timeout", 10))
        by_type = self.options.get("select_by", "css")
        driver = self._get_driver()

        # 단순 시간 대기
        if selector is None and seconds:
            time.sleep(float(seconds))
            self.log("INFO", f"{seconds}초간 대기 완료")
            return

        if selector is None:
            self.raise_error("selector 또는 seconds 중 하나는 반드시 필요합니다.")

        # 셀렉터를 사용하는 기존 로직
        by = By.CSS_SELECTOR if by_type == "css" else By.XPATH if by_type == "xpath" else By.ID
        cond = {
            "visible": EC.visibility_of_element_located((by, selector)),
            "clickable": EC.element_to_be_clickable((by, selector)),
            "present": EC.presence_of_element_located((by, selector)),
        }.get(until)
        
        if cond is None:
            self.raise_error(f"지원하지 않는 until 조건: {until}")
        
        WebDriverWait(driver, timeout).until(cond)
        self.log("INFO", f"WAIT 완료: {selector} ({until})")

    def extract(self):
        ''' 웹페이지에서 요소를 추출하는 메서드, ArrayToken을 to_var에 저장'''
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        attr = self.options.get("attr", "text")
        to_var = self.options.get("to_var")
        driver = self._get_driver()

        # 셀렉터 타입 결정
        by_map = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }

        if select_by not in by_map:
            self.log("ERROR", f"BROWSER extract : 지원하지 않는 select_by: {select_by}")
            return TokenUtil.list_to_array_token([])

        by = by_map[select_by]

        # 탐색 범위 설정
        search_scope = driver
        if within:
            try:
                search_scope = driver.find_element(by, within)
            except Exception:
                self.log("WARN", f"BROWSER extract : within 요소를 찾을 수 없습니다: {within}")
                return TokenUtil.list_to_array_token([])
                
        # 대상 요소 찾기
        try:
            elements = search_scope.find_elements(by, select)
        except Exception:
            self.log("WARN", f"select에 해당하는 요소를 찾을 수 없습니다: {select}")
            return TokenUtil.list_to_array_token([])

        # 값 추출
        results = []
        value = None
        for el in elements:
            try:
                if attr == "text":
                    value = el.get_attribute("outerHTML")
                else:
                    value = el.get_attribute(attr)
                if value:
                    results.append(value)
            except Exception as e:
                self.log("WARN", f"추출 중 오류 발생: {e}")
                return TokenUtil.list_to_array_token([])

        # 결과 저장
        if to_var:
            result_token = TokenUtil.list_to_array_token(results)
            self.executor.set_variable(to_var, result_token)
            self.log("INFO", f"{len(results)}개 추출 → 변수 '{to_var}'에 저장 완료")
        else:
            self.log("INFO", f"{len(results)}개 추출됨 (변수 저장 없음)")

        return results

    def put_text(self):
        ''' 웹페이지의 요소에 텍스트를 입력하는 메서드 '''
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        text = self.options.get("text")
        scroll_first = self.options.get("scroll_first", True)
        timeout = int(self.options.get("timeout", 10))

        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }.get(select_by, By.CSS_SELECTOR)

        driver = self._get_driver()

        try:
            search_scope = driver
            if within:
                search_scope = driver.find_element(by, within)
                self.log("INFO", f"within 요소 탐색 성공: {within}")

            self.log("INFO", f"입력할 요소 대기 중: {select}")
            element = WebDriverWait(search_scope, timeout).until(
                EC.visibility_of_element_located((by, select))
            )

            if scroll_first:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.log("INFO", f"스크롤 완료: {select}")

            if self.options.get("clear_before", False):
                element.clear()

            element.send_keys(text)
            self.log("INFO", f"입력 완료: '{text}' → {select}")

        except Exception as e:
            self.log("ERROR", f"텍스트 입력 실패: {select} - {str(e)}")
            self.raise_error(f"PUT_TEXT 실패: {str(e)}")

    def get_text(self):
        ''' 웹페이지의 요소에서 텍스트를 추출하는 메서드 '''
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        scroll_first = self.options.get("scroll_first", True)
        to_var = self.options.get("to_var")
        timeout = int(self.options.get("timeout", 10))
        attr = self.options.get("attr", "text")  # 기본은 text

        if not select or not to_var:
            self.raise_error("GET_TEXT에는 select와 to_var가 필요합니다.")

        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }.get(select_by, By.CSS_SELECTOR)

        driver = self._get_driver()

        try:
            search_scope = driver
            if within:
                search_scope = driver.find_element(by, within)

            element = WebDriverWait(search_scope, timeout).until(
                EC.presence_of_element_located((by, select))
            )

            if scroll_first:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # 텍스트 추출 방식
            if attr == "text":
                value = element.text
            else:
                value = element.get_attribute(attr)
            
            str_token = TokenUtil.string_to_string_token(value)

            self.executor.set_variable(to_var, str_token)
            self.log("INFO", f"GET_TEXT 완료: '{value}' → {to_var}")
            return value

        except Exception as e:
            self.log("ERROR", f"GET_TEXT 실패: {select} - {str(e)}")
            self.raise_error(f"GET_TEXT 실패: {str(e)}")


    def capture(self):
        ''' 웹페이지의 스크린샷을 저장하는 메서드 '''
        to_file = self.options.get("to_file")
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        scroll_first = self.options.get("scroll_first", True)
        multi = self.options.get("multi", False)

        if not to_file:
            self.raise_error("CAPTURE에는 to_file 옵션이 필요합니다.")

        driver = self._get_driver()

        if select:
            by = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID
            }.get(select_by, By.CSS_SELECTOR)

            elements = driver.find_elements(by, select)
            if not elements:
                self.raise_error(f"요소를 찾을 수 없습니다: {select}")

            if len(elements) > 1 and not multi:
                self.log("WARN", f"복수 요소 발견. 첫 번째 요소만 캡처됩니다. (multi=False)")

            targets = elements if multi else [elements[0]]
            base, ext = os.path.splitext(to_file)

            for idx, el in enumerate(targets):
                try:
                    if scroll_first:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)

                    # 파일명 결정
                    if multi:
                        file_path = to_file.replace("#", str(idx + 1))
                        if file_path == to_file:
                            file_path = f"{base}_{idx + 1}{ext}"
                    else:
                        file_path = to_file

                    el.screenshot(file_path)
                    self.log("INFO", f"[{idx + 1}] 요소 스크린샷 저장 완료: {file_path}")

                except Exception as e:
                    self.log("WARN", f"[{idx + 1}] 스크린샷 실패: {e}")
        else:
            driver.save_screenshot(to_file)
            self.log("INFO", f"전체 페이지 스크린샷 저장 완료: {to_file}")


    def execute_js(self):
        script = self.options.get("script")
        to_var = self.options.get("to_var")
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        scroll_first = self.options.get("scroll_first", True)

        if not script:
            self.raise_error("EXECUTE_JS에는 script가 필요합니다.")

        driver = self._get_driver()

        arg = None
        if select:
            by = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID
            }.get(select_by, By.CSS_SELECTOR)

            search_scope = driver
            if within:
                search_scope = driver.find_element(by, within)

            element = search_scope.find_element(by, select)

            if scroll_first:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            arg = element

        result = driver.execute_script(script, arg) if arg else driver.execute_script(script)

        self.log("INFO", f"JS 실행 결과: {result}")
        if to_var and self.executor:
            if isinstance(result, list):
                result = TokenUtil.list_to_array_token(result)
            elif isinstance(result, str):
                result = TokenUtil.string_to_string_token(result)
            elif isinstance(result, dict):
                result = TokenUtil.dict_to_dict_token(result)
            else:
                result_data = TokenUtil.primitive_to_kavanatype(result)
                result_type = TokenUtil.get_element_token_type(result)
                result = Token(data=result_data, type=result_type)

            self.executor.set_variable(to_var, result)
        return result

  
    def switch_iframe(self):
        to_default = self.options.get("to_default", False)
        if to_default:
            self._get_driver().switch_to.default_content()
            self.log("INFO", "기본 프레임으로 복귀")
            return

        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        scroll_first = self.options.get("scroll_first", True)

        if not select:
            self.raise_error("SWITCH_TO_FRAME에는 select 또는 to_default 옵션이 필요합니다.")

        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }.get(select_by, By.CSS_SELECTOR)

        driver = self._get_driver()

        search_scope = driver
        if within:
            search_scope = driver.find_element(by, within)

        iframe_element = search_scope.find_element(by, select)

        if scroll_first:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iframe_element)

        driver.switch_to.frame(iframe_element)
        self.log("INFO", f"iframe 전환 완료: {select}")


    def close_browser(self):
        if BrowserManager._driver:
            try:
                BrowserManager._driver.quit()
            except Exception as e:
                self.log("WARN", f"브라우저 종료 중 오류 발생: {str(e)}")
            finally:
                BrowserManager._driver = None
                self.log("INFO", "브라우저 종료 완료")

    #----------------------------------- 
    # TODO: 추가만 해 놓음, 구현 필요
    #----------------------------------- 
    def find_elements(self):
        ''' 웹페이지에서 요소를 찾는 메서드 '''
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        timeout = int(self.options.get("timeout", 10))

        if not select:
            self.raise_error("FIND_ELEMENTS에는 select가 필요합니다.")

        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }.get(select_by, By.CSS_SELECTOR)

        driver = self._get_driver()

        search_scope = driver
        if within:
            search_scope = driver.find_element(by, within)

        try:
            elements = WebDriverWait(search_scope, timeout).until(
                EC.presence_of_all_elements_located((by, select))
            )
            return elements
        except Exception as e:
            self.log("ERROR", f"요소 찾기 실패: {select} - {str(e)}")
            return []

    #----------------------------------- 
    # TODO: 추가만 해 놓음, 구현 필요
    #----------------------------------- 
    def scroll_to(self):
        ''' 웹페이지에서 특정 요소로 스크롤하는 메서드 '''
        select = self.options.get("select")
        select_by = self.options.get("select_by", "css")
        within = self.options.get("within")
        scroll_first = self.options.get("scroll_first", True)
        timeout = int(self.options.get("timeout", 10))

        if not select:
            self.raise_error("SCROLL_TO에는 select가 필요합니다.")

        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID
        }.get(select_by, By.CSS_SELECTOR)

        driver = self._get_driver()

        search_scope = driver
        if within:
            search_scope = driver.find_element(by, within)

        try:
            element = WebDriverWait(search_scope, timeout).until(
                EC.presence_of_element_located((by, select))
            )

            if scroll_first:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.log("INFO", f"스크롤 완료: {select}")

        except Exception as e:
            self.log("ERROR", f"스크롤 실패: {select} - {str(e)}")
            self.raise_error(f"SCROLL_TO 실패: {str(e)}")