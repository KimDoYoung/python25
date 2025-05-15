from lib.core.managers.base_manager import BaseManager
from bs4 import BeautifulSoup

from lib.core.token_util import TokenUtil


class HtmlManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs
        

        if not self.command:
            self.raise_error("HTML 명령어에 command는 필수입니다.")

    def execute(self):
        command_map = {
            "SELECT": self.select,
            "SELECT_ONE": self.select_one,
        }

        func = command_map.get(self.command.upper())
        if not func:
            self.raise_error(f"OCR 지원하지 않는 명령어: {self.command}")
        return func()

    def select(self):
        
        css = self.options.get("css")
        to_var = self.options.get("to_var")
        html = self.options.get("html")
        self.soup = BeautifulSoup(html, "html.parser")

        if not css:
            self.raise_error("CSS 선택자는 필수입니다.")
        if not to_var:
            self.raise_error("to_var는 필수입니다.")
        # "table.brdComList > tbody > tr"
        rows = self.soup.select(css)
        if not rows:
            # self.raise_error(f"CSS 선택자에 해당하는 요소를 찾을 수 없습니다: {css}")
            self.log("WARN", f"CSS 선택자에 해당하는 요소를 찾을 수 없습니다: {css}")
            return TokenUtil.array_to_array_token([])
        # 각 tr의 HTML 문자열 추출
        tr_html_list = [TokenUtil.string_to_string_token(str(tr)) for tr in rows]
        result_token =  TokenUtil.array_to_array_token(tr_html_list)
        self.executor.set_variable(to_var, result_token)
        self.log("INFO", f"CSS 선택자에 해당하는 요소를 찾았습니다: {css}")
        return result_token
    
    def select_one(self):
        css = self.options.get("css")
        to_var = self.options.get("to_var")
        html = self.options.get("html")
        otype = self.options.get("otype", "html")  # 기본은 HTML 전체
        self.soup = BeautifulSoup(html, "html.parser")

        if not css:
            self.raise_error("CSS 선택자는 필수입니다.")
        if not to_var:
            self.raise_error("to_var는 필수입니다.")

        element = self.soup.select_one(css)
        if not element:
            self.log("WARN", f"CSS 선택자에 해당하는 요소를 찾을 수 없습니다: {css}")
            return TokenUtil.string_to_string_token("")

        if otype == "text":
            value = element.get_text(strip=True)
        elif otype == "html":
            value = element.decode_contents()
        elif otype == "outer":
            value = str(element)
        elif otype.startswith("attr:"):
            attr_name = otype.split(":", 1)[1]
            value = element.get(attr_name, "")
        else:
            self.raise_error(f"지원하지 않는 otype: {otype}")

        result_token = TokenUtil.string_to_string_token(value)
        self.executor.set_variable(to_var, result_token)
        self.log("INFO", f"선택자 '{css}'로 {otype} 추출 완료 → '{to_var}'")
        return result_token