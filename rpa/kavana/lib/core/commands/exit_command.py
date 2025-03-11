import sys
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.token import Token
from lib.core.token_type import TokenType

class ExitCommand(BaseCommand):
    def execute(self, args: list[Token], executor):
        """EXIT 명령어 실행 (예: EXIT 0)"""
        exit_no = 0  # 기본 종료 코드

        # ✅ 인자가 없으면 EXIT 0으로 처리
        if len(args) > 1:
            raise KavanaSyntaxError(
                "EXIT 명령어는 정수 하나만 받을 수 있습니다. (예: EXIT 0 또는 EXIT)"
            )

        # ✅ 인자가 있을 경우, 정수인지 확인
        if len(args) == 1:
            exit_no_token = args[0]
            if exit_no_token.type == TokenType.INTEGER:
                exit_no = exit_no_token.data.value
            else:
                raise KavanaSyntaxError(
                    f"EXIT 명령어는 정수를 인자로 받아야 합니다. (예: EXIT 0 또는 EXIT)",
                    exit_no_token.line,
                    exit_no_token.column
                )

        executor.exit(exit_no)
