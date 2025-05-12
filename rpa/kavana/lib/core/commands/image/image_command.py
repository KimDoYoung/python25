from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaImageError
from lib.core.token_type import TokenType
from lib.core.token import Token
from lib.core.managers.image_manager import ImageManager


class ImageCommand(BaseCommand):
    """IMAGE 명령어 해석 및 실행"""

    OPTION_DEFINITIONS = {
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "width": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "height": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "factor": {"required": False, "allowed_types": [TokenType.FLOAT]},
        "area": {"required": False, "allowed_types": [TokenType.REGION]},
        "mode": {"required": False, "allowed_types": [TokenType.STRING]},
        "angle": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "radius": {"required": False, "allowed_types": [TokenType.FLOAT]},
        "level": {"default": 128, "allowed_types": [TokenType.INTEGER]},
        "type": {"default": "BINARY_INV", "allowed_types": [TokenType.STRING]},
        "text": {"required": True, "allowed_types": [TokenType.STRING]},
        "font_name": {"required": False, "allowed_types": [TokenType.STRING]},
        "font_size": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "color": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "bg_color": {"required": False, "allowed_types": [TokenType.ARRAY]},
    }

    COMMAND_SPECS = {
        "save": {
            "keys": ["from_var", "to_file"],
            "overrides": {
                "from_var": {"required": True},
                "to_file": {"required": True}
            }
        },
        "resize": {
            "keys": ["from_var", "from_file", "to_var", "to_file", "width", "height", "factor"],
            "rules": {
                "mutually_exclusive": [
                    ["factor", "width"],
                    ["factor", "height"],
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "clip": {
            "keys": ["to_var", "to_file", "area"],
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "to_gray": {
            "keys": ["from_var", "from_file", "to_var", "to_file"],
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "convert_to": {
            "keys": ["from_var", "from_file", "to_var", "to_file", "mode"],
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "rotate": {
            "keys": ["from_var", "from_file", "to_var", "to_file", "angle"],
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "blur": {
            "keys": ["from_var", "from_file", "to_var", "to_file", "radius"],
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "threshold": {
            "keys": ["from_var", "from_file", "to_var", "to_file", "level", "type"],
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"],
                    ["to_file", "to_var"]
                ]
            }
        },
        "create_text_image": {
            "keys": ["text", "font_name", "font_size", "color", "bg_color", "width", "height", "to_file", "to_var"],
            "rules": {
                "exactly_one": [["to_file", "to_var"]]
            }
        }
    }

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaImageError("Image 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)

        try:
            manager = ImageManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
        except KavanaImageError as e:
            raise KavanaImageError(f"Image `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
