import copy
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaRpaError
from lib.core.managers.rpa_manager import RpaManager
from lib.core.token import Token
from lib.core.token_type import TokenType

# TODO : 모니터갯수 감안
class RpaCommand(BaseCommand):
    """RPA 명령어 해석 및 실행"""

    OPTION_DEFINITIONS = {
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "maximize": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "process_name": {"required": False, "allowed_types": [TokenType.STRING]},
        "seconds": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "grayscale": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "confidence": {"default": 0.8, "allowed_types": [TokenType.FLOAT], "min": 0.0, "max": 1.0},
        "area": {"required": False, "allowed_types": [TokenType.REGION]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "x": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "y": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "click_type": {"default": 'left', "allowed_types": [TokenType.STRING]},
        "click_count": {"default": 1, "allowed_types": [TokenType.INTEGER]},
        "duration": {"default": 0.2, "allowed_types": [TokenType.FLOAT]},
        "relative": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "keys": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "speed": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "strip": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "wait_before": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
    }


    COMMAND_SPECS = {
        "app_open": {
            "keys": ["from_var", "maximize", "process_name"],
            "overrides": {},
            "rules": {}
        },
        "app_close": {
            "keys": ["from_var"],
            "overrides": {
                "from_var": {"required": True}
            },
            "rules": {}
        },
        "wait": {
            "keys": ["seconds"],
            "overrides": {
                "seconds": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [["select", "seconds"]],
                "required_together": []
            }
        },
        # "wait_for_image": {
        "wait_image_and_click": {
            "keys": ["area", "from_var", "from_file", "timeout", "grayscale", "confidence"],
            "overrides": {},
            "rules": {}
        },
        "click_point": {
            "keys": ["x", "y", "click_type", "click_count", "duration"],
            "overrides": {
                "x": {"required": True},
                "y": {"required": True}
            },
            "rules": {}
        },
        "click_image": {
            "keys": ["area", "from_var", "from_file", "timeout", "grayscale", "confidence"],
            "overrides": {},
            "rules": {}
        },
        "mouse_move": {
            "keys": ["x", "y", "duration", "relative"],
            "overrides": {},
            "rules": {}
        },
        "key_in": {
            "keys": ["keys", "speed"],
            "overrides": {
                "keys": {"required": True}
            },
            "rules": {}
        },
        "put_text": {
            "keys": ["text"],
            "overrides": {
                "text": {"required": True}
            },
            "rules": {}
        },
        "get_text": {
            "keys": ["to_var", "strip", "wait_before"],
            "overrides": {},
            "rules": {}
        },
        "capture": {
            "keys": ["area", "to_var", "to_file"],
            "overrides": {},
            "rules": {}
        }
    }


    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaRpaError("RPA 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)
        
        try:
            manager = RpaManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
        except KavanaRpaError as e:
            raise KavanaRpaError(f"RPA `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
