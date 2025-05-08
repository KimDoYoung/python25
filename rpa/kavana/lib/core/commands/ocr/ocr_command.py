from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaOcrError
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.ocr_manager import OcrManager  # OCR 처리를 담당하는 매니저

class OcrCommand(BaseCommand):
    '''OCR 명령어 해석'''
    OPTION_DEFINITIONS = {
        "preprocess": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        #---------전처리 옵션------------------
        "gray": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "threshold": {"default": "adaptive", "allowed_types": [TokenType.STRING]},
        "blur": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "resize": {"default": 1.0, "allowed_types": [TokenType.FLOAT]},
        "invert": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "similarity": {"default": 70, "allowed_types": [TokenType.INTEGER]},
        #------------------------------------
        "area": {"required": False, "allowed_types": [TokenType.REGION]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }
    COMMAND_SPECS = {
        "read": {
            "keys": ["from_var", "from_file", "area", "to_var",
                     "gray","threshold", "blur", "resize", "invert","preprocess"],
            "overrides": {
            },
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"]
                ],
                "required_together": []
            }
        },
        "find": {
            "keys": [ "area", "to_var", "text", "from_var", "from_file", "similarity",
                     "gray","threshold", "blur", "resize", "invert","preprocess"],
            "overrides": {
            },
            "rules": {
                "mutually_exclusive": ["from_file", "from_var"],
                "required_together": []
            }
        },
        "get_all": {
            "keys": ["from_var", "from_file", "area", "to_var",
                     "gray","threshold", "blur", "resize", "invert","preprocess"],
            "overrides": {
                "from_var": {"required": False},
                "from_file": {"required": False}
            },
            "rules": {
                "mutually_exclusive": [
                    ["from_file", "from_var"]
                ],
                "required_together": []
            }
        }
    }


    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaOcrError("OCR 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)
        
        try:
            ocr_manager = OcrManager(command=sub_command,**option_values, executor=executor)
            ocr_manager.execute()
        except KavanaOcrError as e:
            raise KavanaOcrError(f"OCR `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

