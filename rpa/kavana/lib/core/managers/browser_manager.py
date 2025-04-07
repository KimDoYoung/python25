from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from base_manager import BaseManager

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
                options.add_argument("--headless")
            if self.options.get("user_agent"):
                options.add_argument(f"user-agent={self.options['user_agent']}")
            if self.options.get("window_size"):
                options.add_argument(f"--window-size={self.options['window_size']}")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            BrowserManager._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        return BrowserManager._driver

    def find_element(self, selector, selector_type="css"):
        driver = self.get_driver()
        if selector_type == "xpath":
            return driver.find_element(By.XPATH, selector)
        elif selector_type == "id":
            return driver.find_element(By.ID, selector)
        else:
            return driver.find_element(By.CSS_SELECTOR, selector)

    def execute(self):
        method_map = {
            "OPEN": self.open_browser,
            "CLICK": self.click,
            "TYPE": self.type_text,
            "WAIT": self.wait,
            "GET_TEXT": self.get_text,
            "CAPTURE": self.capture,
            "EXECUTE_JS": self.execute_js,
            "FIND_ELEMENTS": self.find_elements,
            "CLOSE": self.close_browser,
            "SCROLL_TO": self.scroll_to,
            "SWITCH_IFRAME": self.switch_iframe,
        }
        func = method_map.get(self.command.upper())
        if not func:
            self.raise_error(f"지원하지 않는 명령어: {self.command}")
        return func()

    def open(self):
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
        selector = self.options.get("selector")
        until = self.options.get("until", "visible")
        timeout = int(self.options.get("timeout", 10))
        by_type = self.options.get("selector_type", "css")
        driver = self.get_driver()

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
            BrowserManager._driver.quit()
            BrowserManager._driver = None
            self.log("INFO", "브라우저 종료 완료")
