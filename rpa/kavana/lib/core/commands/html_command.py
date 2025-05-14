from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaHtmlError, KavanaOcrError
from lib.core.managers.html_manager import HtmlManager
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.managers.ocr_manager import OcrManager  # OCR 처리를 담당하는 매니저

class HtmlCommand(BaseCommand):
    '''HTML 명령어 해석 (soup를 이용해서 HTML을 파싱)'''
    OPTION_DEFINITIONS = {
        "css": {"required": False, "allowed_types": [TokenType.STRING]},
        "html": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "otype": {"default": "html", "allowed_types": [TokenType.STRING]},
    }
    COMMAND_SPECS = {
        "select": {
            "keys": ["css", "html", "to_var"],
            "overrides": {},
            "rules": {}
        },
        "select_one": {
            "keys": ["css", "html", "to_var", "otype"],
            "overrides": {},
            "rules": {}
        },
    }


    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaOcrError("HTML 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)
        
        try:
            html_manager = HtmlManager(command=sub_command,**option_values, executor=executor)
            html_manager.execute()
        except KavanaHtmlError as e:
            raise KavanaHtmlError(f"HTML `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

