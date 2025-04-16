from lib.core.command_executor import CommandExecutor
from lib.core.commands.base_command import BaseCommand
from lib.core.token_type import TokenType
from lib.core.token import Token
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.token_type import TokenType


def get_tokens(s: str):
    # s = "SET i = " + s
    s = "MAIN\n" + s + "\nEND_MAIN"
    lines = [s.strip() for s in s.split("\n") if s.strip()]
    command_preprocssed_lines = CommandPreprocessor().preprocess(lines)
    parsed_commands = CommandParser().parse(command_preprocssed_lines)
    return parsed_commands[0]["args"]  # Token 리스트 전체 반환


class DummyCommand(BaseCommand):
    """BaseCommand 상속 + execute() 직접 사용하는 테스트 명령"""

    OPTION_DEFINITIONS = {
        "text": {"required": True, "allowed_types": [TokenType.STRING]},
        "font_size": {"default": 12, "allowed_types": [TokenType.INTEGER]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    COMMAND_SPECS = {
        "create_text_image": {
            "keys": ["text", "font_size", "to_file", "to_var"],
            "rules": {
                "exactly_one": [["to_file", "to_var"]]
            }
        }
    }

    def execute(self, args: list[Token], executor=None):
        if not args:
            raise ValueError("명령어 인자가 필요합니다.")
        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)

        print("✅ 모든 검증 통과:", option_values)


if __name__ == "__main__":
    s = 'Image create_text_image  text="홍길동" to_var="b"'
    tokens = get_tokens(s)

    print(f"\n[토큰 추출 결과]")
    for t in tokens:
        print(f" - {t.type.name} : {t.data}")

    print("\n[실행 결과]")
    cmd = DummyCommand()
    executor = CommandExecutor()
    cmd.execute(tokens, executor=executor)
