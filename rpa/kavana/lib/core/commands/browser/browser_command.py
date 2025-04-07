from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaBrowserError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.browser_manager import BrowserManager


class BrowserCommand(BaseCommand):
    ''' BROWSER 명령어 해석 및 실행 '''

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaBrowserError("BROWSER 명령어는 최소 하나 이상의 인자가 필요합니다.")
        
        sub_command = args[0].data.value.upper()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)

        try:
            browser = BrowserManager.get_instance(executor)

            match sub_command:
                case "OPEN":
                    browser.open(**option_values)
                case "CLICK":
                    browser.click(**option_values)
                case "TYPE" | "PUT_TEXT":
                    browser.type(**option_values)
                case "WAIT":
                    browser.wait(**option_values)
                case "GET_TEXT":
                    result = browser.get_text(**option_values)
                    if "to_var" in option_values:
                        executor.set_variable(option_values["to_var"], result)
                case "CAPTURE" | "SCREEN_SHOT":
                    browser.capture(**option_values)
                case "SCROLL_TO":
                    browser.scroll_to(**option_values)
                case "SWITCH_IFRAME":
                    browser.switch_iframe(**option_values)
                case "EXISTS":
                    exists = browser.exists(**option_values)
                    if "to_var" in option_values:
                        executor.set_variable(option_values["to_var"], exists)
                case "ASSERT_TEXT":
                    browser.assert_text(**option_values)
                case "WAIT_FOR_TEXT":
                    browser.wait_for_text(**option_values)
                case "CLOSE":
                    browser.close()
                case _:
                    raise KavanaBrowserError(f"지원하지 않는 BROWSER sub_command: {sub_command}")
        except KavanaBrowserError as e:
            raise KavanaBrowserError(f"`{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

    OPTION_DEFINITIONS = {
        "url": {"required": False, "allowed_types": [TokenType.STRING]},
        "selector": {"required": False, "allowed_types": [TokenType.STRING]},
        "selector_type": {"default": "css", "allowed_types": [TokenType.STRING]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "until": {"default": "visible", "allowed_types": [TokenType.STRING]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "clear_before": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "path": {"required": False, "allowed_types": [TokenType.STRING]},
        "script": {"required": False, "allowed_types": [TokenType.STRING]},
        "headless": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "window_size": {"required": False, "allowed_types": [TokenType.STRING]},
        "user_agent": {"required": False, "allowed_types": [TokenType.STRING]},
        "full_page": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
    }

    def option_map_define(self, *keys):
        required_keys = {"selector_type", "timeout"}  # 기본 공통 필수
        keys = set(keys) | required_keys

        return {k: self.OPTION_DEFINITIONS[k] for k in keys if k in self.OPTION_DEFINITIONS}

    def get_option_map(self, sub_command: str) -> dict:
        match sub_command:
            case "OPEN":
                return self.option_map_define("url", "headless", "window_size", "user_agent")
            case "CLICK":
                return self.option_map_define("selector")
            case "TYPE" | "PUT_TEXT":
                return self.option_map_define("selector", "text", "clear_before")
            case "WAIT":
                return self.option_map_define("selector", "until", "timeout")
            case "GET_TEXT":
                return self.option_map_define("selector", "to_var")
            case "CAPTURE" | "SCREEN_SHOT":
                return self.option_map_define("path", "full_page")
            case "SCROLL_TO":
                return self.option_map_define("selector")
            case "SWITCH_IFRAME":
                return self.option_map_define("selector")
            case "EXISTS":
                return self.option_map_define("selector", "to_var")
            case "ASSERT_TEXT":
                return self.option_map_define("text")
            case "WAIT_FOR_TEXT":
                return self.option_map_define("text", "timeout")
            case "CLOSE":
                return {}
            case _:
                raise KavanaBrowserError(f"지원하지 않는 browser sub_command: {sub_command}")
