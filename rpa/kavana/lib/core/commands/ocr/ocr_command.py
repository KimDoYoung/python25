from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaOcrError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.ocr_manager import OcrManager  # OCR 처리를 담당하는 매니저

class OcrCommand(BaseCommand):
    '''OCR 명령어 해석'''

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaOcrError("OCR 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.upper()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)

        try:
            ocr_manager = OcrManager(**option_values, executor=executor)

            match sub_command:
                case "READ":
                    result = ocr_manager.read()
                case "FIND":
                    result = ocr_manager.find()
                case "GET_ALL":
                    result = ocr_manager.get_all()
                case _:
                    raise KavanaOcrError(f"지원하지 않는 OCR 서브 명령어: {sub_command}")

            if "to_var" in option_values:
                executor.set_variable(option_values["to_var"], result)

        except KavanaOcrError as e:
            raise KavanaOcrError(f"OCR `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

    OPTION_DEFINITIONS = {
        "region": {"required": False, "allowed_types": [TokenType.STRING]},
        "rectangle": {"required": False, "allowed_types": [TokenType.STRING]},
        "image_path": {"required": False, "allowed_types": [TokenType.STRING]},
        "image": {"required": False, "allowed_types": [TokenType.OBJECT]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},  # FIND용
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    def get_option_map(self, sub_command: str) -> dict:
        match sub_command:
            case "READ":
                return self.option_map_define("region", "rectangle", "image_path", "image", "to_var")
            case "FIND":
                return self.option_map_define("text", "region", "rectangle", "image_path", "image", "to_var")
            case "GET_ALL":
                return self.option_map_define("region", "rectangle", "image_path", "image", "to_var")
            case _:
                raise KavanaOcrError(f"지원하지 않는 OCR sub_command: {sub_command}")

    def option_map_define(self, *keys):
        return {k: self.OPTION_DEFINITIONS[k] for k in keys if k in self.OPTION_DEFINITIONS}
