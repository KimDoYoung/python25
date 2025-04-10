import copy
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaImageError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.image_manager import ImageManager

class ImageCommand(BaseCommand):
    '''IMAGE 명령어 해석 및 실행'''

    IMAGE_RULES = {
        "resize": {
            "mutually_exclusive": [  # 서로 동시에 존재하면 안 되는 파라미터들
                ["factor", "width"],
                ["factor", "height"],
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [  # 함께 있어야만 유효한 조합
                # ["width", "height"]
            ]
        },
        "clip": {
            "mutually_exclusive": [
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [
                # ["width", "height"]
            ]
        },
        "to_gray": {
            "mutually_exclusive": [
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [
                # ["width", "height"]
            ]
        },
        "convert_to": {
            "mutually_exclusive": [
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [
                # ["mode"]
            ]
        },
        "rotate": {
            "mutually_exclusive": [
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [
                # ["angle"]
            ]
        },
        "blur": {
            "mutually_exclusive": [
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [
                # ["radius"]
            ]
        },
        "threshold": {
            "mutually_exclusive": [
                ["from_file", "from_var"],
                ["to_file", "to_var"]
            ],
            "required_together": [
                # ["level", "type"]
            ]
        }
    }

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaImageError("IMAGE 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_command_rules(self.IMAGE_RULES, sub_command, option_values)
        try:
            image = ImageManager(command=sub_command, executor=executor, **option_values)
            image.execute()
        except KavanaImageError as e:
            raise KavanaImageError(f"`{sub_command}` 명령어 처리 중 오류: {str(e)}") from e

    OPTION_DEFINITIONS = {
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
        #---
        "width": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "height": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "factor" : {"required": False, "allowed_types": [TokenType.FLOAT]},
        #---
        "area": {"required": False, "allowed_types": [TokenType.REGION]},  
        "mode" : {"required": False, "allowed_types": [TokenType.STRING]},
        #---
        "angle": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "radius": {"required": False, "allowed_types": [TokenType.FLOAT]},
        #---
        "level": {"default": 128, "allowed_types": [TokenType.INTEGER]},
        "type": {"default": "BINARY_INV", "allowed_types": [TokenType.STRING]},
    }

    def get_option_map(self, sub_command: str) -> dict:
        # 원본 옵션 정의 복사
        option_defs = copy.deepcopy(self.OPTION_DEFINITIONS)

        match sub_command:
            case "save":
                option_defs["from_var"]["required"] = True
                option_defs["to_file"]["required"] = True
                return self.option_map_define(option_defs, "from_var", "to_file")
            case "resize":
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file", "width", "height", "factor")
            case "clip":
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file", "area")
            case "to_gray":
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file")
            case "convert_to":
                option_defs["mode"]["required"] = True
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file", "mode")
            case "rotate":
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file", "angle")
            case "blur":
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file", "radius")
            case "threshold":
                return self.option_map_define(option_defs, "from_var", "from_file","to_var", "to_file", "level", "type")
            case _:
                raise KavanaImageError(f"지원하지 않는 IMAGE sub_command: {sub_command}")

    def option_map_define(self, option_defs:dict,  *keys):
        return {k: option_defs[k] for k in keys if k in option_defs}
