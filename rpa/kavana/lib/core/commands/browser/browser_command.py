import copy
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaBrowserError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.browser_manager import BrowserManager


class BrowserCommand(BaseCommand):
    ''' BROWSER 명령어 해석 및 실행 '''
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

        #--- switch_frame
        "to_default": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
    }

    COMMAND_SPECS = {
        "open": {
            "keys": ["url", "headless", "window_size", "user_agent"],
            "overrides": {
                "url": {"required": True},
                "headless": {"required": False},
                "window_size": {"required": False},
                "user_agent": {"required": False}
            }
        },
        "wait": {
            "keys": ["select", "until", "select_by", "timeout", "seconds"],
            "overrides": {
                "select": {"required": False},
                "until": {"required": False},
                "select_by": {"required": False},
                "timeout": {"required": False},
                "seconds": {"required": False}
            }
        },
        "extract": {
            "keys": ["select", "select_by", "within", "attr", "to_var"],
            "overrides": {
                "select": {"required": True},
                "select_by": {"required": False},
                "within": {"required": False},
                "attr": {"required": False},
                "to_var": {"required": True}
            }
        },
        "click": {
            "keys": ["select", "select_by", "within", "timeout", "click_js", "scroll_first"],
            "overrides": {
                "select": {"required": True},
                "select_by": {"required": False},
                "within": {"required": False},
                "timeout": {"required": False},
                "click_js": {"required": False},
                "scroll_first": {"required": True}
            }
        },
        "put_text": {
            "keys": ["select", "select_by", "within", "timeout", "text", "clear_before", "scroll_first"],
            "overrides": {
                "select": {"required": True},
                "select_by": {"required": False},
                "within": {"required": False},
                "timeout": {"required": False},
                "text": {"required": True},
                "clear_before": {"required": False},
                "scroll_first": {"required": True}
            }
        },
        "get_text": {
            "keys": ["select", "select_by", "within", "attr", "to_var"],
            "overrides": {
                "select": {"required": True},
                "select_by": {"required": False},
                "within": {"required": False},
                "attr": {"required": False},
                "to_var": {"required": True}
            }
        },
        "capture": {
            "keys": ["select", "select_by", "within", "scroll_first", "to_file", "multi"],
            "overrides": {
                "select": {"required": True},
                "select_by": {"required": False},
                "within": {"required": False},
                "scroll_first": {"required": True},
                "to_file": {"required": True},
                "multi": {"required": False}
            }
        },
        "script_js": {
            "keys": ["script", "select", "select_by", "within", "scroll_first", "to_var"],
            "overrides": {
                "script": {"required": True},
                "select": {"required": False},
                "select_by": {"required": False},
                "within": {"required": False},
                "scroll_first": {"required": True},
                "to_var": {"required": False}
            }
        },
        "switch_frame": {
            "keys": ["select", "select_by", "within", "scroll_first", "to_default"],
            "overrides": {
                "select": {"required": True},
                "select_by": {"required": False},
                "within": {"required": False},
                "scroll_first": {"required": True},
                "to_default": {"required": False}
            }
        },
        "close": {
            "keys": [],
            "overrides": {}
        }
    }


    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaBrowserError("Browser 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)
        
        try:
            manager = BrowserManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
        except KavanaBrowserError as e:
            raise KavanaBrowserError(f"Browser `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

