import copy
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
        },
        "wait": {
            "mutually_exclusive": [
                 ["select", "seconds"],
            ],
            "required_together": [
                # ["width", "height"]
            ]
        },
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
            raise KavanaBrowserError(f"BROWSER `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
    OPTION_DEFINITIONS = {
        #-----browser open
        "url": {"required": False, "allowed_types": [TokenType.STRING]},
        "headless": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "window_size": {"default": "1920,1080", "allowed_types": [TokenType.STRING]},
        "user_agent": {"required": False, "allowed_types": [TokenType.STRING]},
        #-----wait
        "select": {"required": False, "allowed_types": [TokenType.STRING]},
        "until": {"default": "present", "allowed_types": [TokenType.STRING]},
        "select_by": {"default": "css", "allowed_types": [TokenType.STRING]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "seconds": {"required": False, "allowed_types": [TokenType.INTEGER]},
        #-----browser extract
        "within": {"required": False, "allowed_types": [TokenType.STRING]},
        "attr": {"required": False, "allowed_types": [TokenType.STRING]},
    
        #-----click
        "click_js": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "scroll_first": {"required": True, "allowed_types": [TokenType.BOOLEAN]},
        #-----put_text
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "clear_before": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        #-----get_text
        "attr": {"default": "text", "allowed_types": [TokenType.STRING]},

        #=--- capture
        "to_file": {"required": True, "allowed_types": [TokenType.STRING]},
        "multi": {"default": False, "allowed_types": [TokenType.BOOLEAN]},

        #--- script_js
        "script": {"required": True, "allowed_types": [TokenType.STRING]},

        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},

        "path": {"required": False, "allowed_types": [TokenType.STRING]},
        "script": {"required": False, "allowed_types": [TokenType.STRING]},
        "full_page": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
    }

    def option_map_define(self, option_defs:dict,  *keys):
        return {k: option_defs[k] for k in keys if k in option_defs}

    def get_option_map(self, sub_command: str) -> dict:
        # 원본 옵션 정의 복사
        option_defs = copy.deepcopy(self.OPTION_DEFINITIONS)        
        match sub_command:
            case "open":
                return self.option_map_define(option_defs, "url", "headless", "window_size", "user_agent")
            case "wait":
                return self.option_map_define(option_defs, "select", "until", "select_by","timeout", "seconds")
            case "extract":
                option_defs["to_var"]["required"] = True
                option_defs["select"]["required"] = True
                return self.option_map_define(option_defs, "select", "select_by", "within", "attr", "to_var")        
            case "click":
                option_defs["select"]["required"] = True
                return self.option_map_define(option_defs, "select", "select_by", "within","timeout", "click_js", "scroll_first")
            case "put_text":
                option_defs["select"]["required"] = True
                option_defs["text"]["required"] = True
                return self.option_map_define(option_defs, "select", "select_by", "within", "timeout", "text", "clear_before", "scroll_first") 
            case "get_text":
                return self.option_map_define(option_defs, "selector", "to_var")
            case "capture":
                option_defs["to_file"]["required"] = True
                return self.option_map_define(option_defs, "select", "select_by", "within", "scroll_first", "to_file", "multi")
            case "script_js":
                option_defs["script"]["required"] = True
                return self.option_map_define(option_defs, "script", "select", "select_by", "within", "scroll_first", "to_var")
            case "close":
                return {}
            case _:
                raise KavanaBrowserError(f"지원하지 않는 browser sub_command: {sub_command}")
