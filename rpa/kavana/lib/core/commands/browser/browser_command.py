from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaBrowserError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.browser_manager import BrowserManager


class BrowserCommand(BaseCommand):
    ''' BROWSER 명령어 해석 및 실행 '''

    BROWSER_RULES = {
        "url": {
            "mutually_exclusive": [  # 서로 동시에 존재하면 안 되는 파라미터들
                # ["from_file", "from_var"],
            ],
            "required_together": [  # 함께 있어야만 유효한 조합
                # ["width", "height"]
            ]
        }
    }

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaBrowserError("BROWSER 명령어는 최소 하나 이상의 인자가 필요합니다.")
        
        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_command_rules(self.BROWSER_RULES, sub_command, option_values)
        try:
            browser_manager = BrowserManager(command=sub_command,**option_values, executor=executor)
            browser_manager.execute()
        except KavanaBrowserError as e:
            raise KavanaBrowserError(f"OCR `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
    OPTION_DEFINITIONS = {
        "url": {"required": False, "allowed_types": [TokenType.STRING]},
        "headless": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "window_size": {"default": "1920,1080", "allowed_types": [TokenType.STRING]},
        "user_agent": {"required": False, "allowed_types": [TokenType.STRING]},
        #-----
        "selector": {"required": False, "allowed_types": [TokenType.STRING]},
        "selector_type": {"default": "css", "allowed_types": [TokenType.STRING]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "until": {"default": "visible", "allowed_types": [TokenType.STRING]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "clear_before": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "path": {"required": False, "allowed_types": [TokenType.STRING]},
        "script": {"required": False, "allowed_types": [TokenType.STRING]},
        "full_page": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
    }

    def option_map_define(self, *keys):
        required_keys = {"selector_type", "timeout"}  # 기본 공통 필수
        keys = set(keys) | required_keys

        return {k: self.OPTION_DEFINITIONS[k] for k in keys if k in self.OPTION_DEFINITIONS}

    def get_option_map(self, sub_command: str) -> dict:
        match sub_command:
            case "open":
                return self.option_map_define("url", "headless", "window_size", "user_agent")
            case "click":
                return self.option_map_define("selector")
            case "put_text":
                return self.option_map_define("selector", "text", "clear_before")
            case "wait":
                return self.option_map_define("selector", "until", "timeout")
            case "get_text":
                return self.option_map_define("selector", "to_var")
            case "close":
                return {}
            case _:
                raise KavanaBrowserError(f"지원하지 않는 browser sub_command: {sub_command}")
