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
        "focus": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "process_name": {"required": False, "allowed_types": [TokenType.STRING]},
        "seconds": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "minutes": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "grayscale": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "confidence": {"default": 0.8, "allowed_types": [TokenType.FLOAT], "min": 0.0, "max": 1.0},
        "area": {"required": False, "allowed_types": [TokenType.REGION]},
        "name": {"required": True, "allowed_types": [TokenType.REGION]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "x": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "y": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "click_type": {"default": 'left', "allowed_types": [TokenType.STRING]},
        "click_count": {"default": 1, "allowed_types": [TokenType.INTEGER]},
        "duration": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "relative": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "keys": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "speed": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "strip": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "wait_before": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "after": {"required": False, "allowed_types": [TokenType.STRING]},
        "location": {"required": False, "allowed_types": [TokenType.POINT]},
        "locations": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "multi" :{"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "clipboard":{"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "turtle": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
    }


    COMMAND_SPECS = {
        "open_app": {
            "keys": ["from_var", "maximize", "process_name", "focus"],
            "overrides": {},
            "rules": {}
        },
        "close_app": {
            "keys": ["from_var"],
            "overrides": {
                "from_var": {"required": True}
            },
            "rules": {}
        },
        "close_all_children": {
            "keys": ["from_var"],
            "overrides": {
                "from_var": {"required": True}
            },
            "rules": {}
        },
        "focus_app" : {
            "keys": ["from_var"],
            "overrides": {
                "from_var": {"required": True}
            },
            "rules": {}
        },
        "wait": {
            "keys": ["seconds","minutes"],
            "overrides": {
            },
            "rules": {
                "mutually_exclusive": [["seconds", "minutes"]],
                "required_together": [],
                "at_least_one": [["seconds", "minutes"]]
            }
        },
        # "wait_for_image": {
        "wait_image": {
            "keys": ["area", "from_var", "from_file", "to_var", "after", "timeout", "grayscale", "confidence"],
            "overrides": {},
            "rules": {}
        },
        "click_point": {
            "keys": ["x", "y", "location","after", "click_type", "click_count", "duration","speed","turtle"],
            "overrides": {
            },
            "rules": {
                "mutually_exclusive": [
                    ["location", "x"],["location", "y"]
                ],
                "required_together": [["x", "y"]]
            }
        },
        "click_region": {
            "keys": ["name", "after", "click_type", "click_count", "duration","speed","turtle"],
            "overrides": {
            },
            "rules": {}
        },
        "click_image": {
            "keys": ["area", "after", "from_var", "from_file", "to_var", "grayscale", "confidence", "duration","speed","turtle"],
            "overrides": {},
            "rules": {}
        },
        "find_image": {
            "keys": ["area", "after", "from_var", "from_file", "to_var", "grayscale", "confidence", "multi"],
            "overrides": {
                "to_var": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [
                    ["from_var", "from_file"]
                ],
            }
        },
        "move_mouse": {
            "keys": ["x", "y", "location", "locations",  "relative","after","speed"],
            "overrides": {},
            "rules": {
                "mutually_exclusive": [
                    ["location", "x"],["location", "y"], ["locations","location"],
                    ["locations", "x"],["locations", "y"]
                ],
                "required_together": [["x", "y"]]
            }
        },
        "key_in": {
            "keys": ["keys","after", "speed"],
            "overrides": {
                "keys": {"required": True}
            },
            "rules": {}
        },
        "put_text": {
            "keys": ["text","clipboard"],
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

        
        try:
            option_map, rules = self.get_option_spec(sub_command)
            option_values = self.parse_and_validate_options(options, option_map, executor)
            self.check_option_rules(sub_command, option_values, rules)
            manager = RpaManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
        except KavanaRpaError as e:
            raise KavanaRpaError(f"RPA `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
