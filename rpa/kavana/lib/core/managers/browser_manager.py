import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from lib.core.managers.base_manager import BaseManager
from lib.core.token_util import TokenUtil

class BrowserManager(BaseManager):
    _driver = None

    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs

        if not self.command:
            self.raise_error("command는 필수입니다.")

    def get_driver(self):
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

    def execute(self):
        method_map = {
            "open": self.open_browser,
            "wait": self.wait,
            "extract": self.extract,
            "click": self.click,
            "put_text": self.type_text,
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

    def open_browser(self):
        url = self.options.get("url")
        if not url:
            self.raise_error("url 옵션이 필요합니다.")
        driver = self.get_driver()
        driver.get(url)
        self.log("INFO", f"브라우저 열기: {url}")

    def click(self):
        selector = self.options.get("selector")
        if not selector:
            self.raise_error("selector 옵션이 필요합니다.")
        element = self.find_element(selector, self.options.get("selector_type", "css"))
        element.click()
        self.log("INFO", f"클릭: {selector}")

    def type_text(self):
        selector = self.options.get("selector")
        text = self.options.get("text")
        if not selector or text is None:
            self.raise_error("TYPE에는 selector와 text가 필요합니다.")
        element = self.find_element(selector, self.options.get("selector_type", "css"))
        if self.options.get("clear_before", False):
            element.clear()
        element.send_keys(text)
        self.log("INFO", f"입력: {text} → {selector}")

    def wait(self): 
        selector = self.options.get("select")
        seconds = self.options.get("seconds")
        until = self.options.get("until", "visible")
        timeout = int(self.options.get("timeout", 10))
        by_type = self.options.get("select_by", "css")
        driver = self.get_driver()

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
        driver = self.get_driver()

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
        for el in elements:
            try:
                if attr == "text":
                    value = el.text
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


    def get_text(self):
        selector = self.options.get("selector")
        to_var = self.options.get("to_var")
        if not selector or not to_var:
            self.raise_error("GET_TEXT에는 selector와 to_var가 필요합니다.")
        element = self.find_element(selector, self.options.get("selector_type", "css"))
        text = element.text
        self.log("INFO", f"GET_TEXT: {text}")
        if self.executor:
            self.executor.set_var(to_var, text)
        return text

    def capture(self):
        path = self.options.get("path")
        if not path:
            self.raise_error("CAPTURE에는 path가 필요합니다.")
        driver = self.get_driver()
        driver.save_screenshot(path)
        self.log("INFO", f"스크린샷 저장: {path}")

    def execute_js(self):
        script = self.options.get("script")
        to_var = self.options.get("to_var")
        if not script:
            self.raise_error("EXECUTE_JS에는 script가 필요합니다.")
        driver = self.get_driver()
        result = driver.execute_script(script)
        self.log("INFO", f"JS 실행 결과: {result}")
        if to_var and self.executor:
            self.executor.set_var(to_var, result)
        return result

    def find_elements(self):
        selector = self.options.get("selector")
        to_var = self.options.get("to_var")
        if not selector or not to_var:
            self.raise_error("FIND_ELEMENTS에는 selector와 to_var가 필요합니다.")
        driver = self.get_driver()
        selector_type = self.options.get("selector_type", "css")
        by = By.CSS_SELECTOR if selector_type == "css" else By.XPATH if selector_type == "xpath" else By.ID
        elements = driver.find_elements(by, selector)
        self.log("INFO", f"{len(elements)}개의 요소 발견")
        if self.executor:
            self.executor.set_var(to_var, elements)
        return elements

    def scroll_to(self):
        selector = self.options.get("selector")
        if not selector:
            self.raise_error("SCROLL_TO에는 selector가 필요합니다.")
        element = self.find_element(selector, self.options.get("selector_type", "css"))
        driver = self.get_driver()
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        self.log("INFO", f"스크롤 이동 완료: {selector}")

    def switch_iframe(self):
        selector = self.options.get("selector")
        if not selector:
            self.raise_error("SWITCH_IFRAME에는 selector가 필요합니다.")
        element = self.find_element(selector, self.options.get("selector_type", "css"))
        self.get_driver().switch_to.frame(element)
        self.log("INFO", f"iframe 전환 완료: {selector}")

    def close_browser(self):
        if BrowserManager._driver:
            try:
                BrowserManager._driver.quit()
            except Exception as e:
                self.log("WARN", f"브라우저 종료 중 오류 발생: {str(e)}")
            finally:
                BrowserManager._driver = None
                self.log("INFO", "브라우저 종료 완료")

                
