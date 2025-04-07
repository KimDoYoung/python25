from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaImageError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.image_manager import ImageManager

class ImageCommand(BaseCommand):
    '''IMAGE 명령어 해석 및 실행'''

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaImageError("IMAGE 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)

        try:
            image = ImageManager(command=sub_command, executor=executor, **option_values)
            image.execute()
        except KavanaImageError as e:
            raise KavanaImageError(f"`{sub_command}` 명령어 처리 중 오류: {str(e)}") from e

    OPTION_DEFINITIONS = {
        "file": {"required": True, "allowed_types": [TokenType.STRING]},
        "save_as": {"required": True, "allowed_types": [TokenType.STRING]},
        "width": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "height": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "region": {"required": False, "allowed_types": [TokenType.ARRAY]},  # [x, y, w, h]
        "angle": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "radius": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "level": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "format": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    def get_option_map(self, sub_command: str) -> dict:
        match sub_command:
            case "resize":
                return self.option_map_define("file", "save_as", "width", "height")
            case "clip":
                return self.option_map_define("file", "save_as", "region")
            case "to_gray":
                return self.option_map_define("file", "save_as")
            case "convert_to":
                return self.option_map_define("file", "save_as", "format")
            case "rotate":
                return self.option_map_define("file", "save_as", "angle")
            case "blur":
                return self.option_map_define("file", "save_as", "radius")
            case "threshold":
                return self.option_map_define("file", "save_as", "level")
            case _:
                raise KavanaImageError(f"지원하지 않는 IMAGE sub_command: {sub_command}")

    def option_map_define(self, *keys):
        return {k: self.OPTION_DEFINITIONS[k] for k in keys if k in self.OPTION_DEFINITIONS}
