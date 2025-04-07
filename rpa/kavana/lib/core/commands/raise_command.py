from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.exceptions.kavana_exception import KavanaException
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType


# RAISE "사용자 예외 발생", 5  // ✅ 메시지와 종료 코드 지정
# RAISE 3  // ✅ 종료 코드만 지정 (메시지 없음, 기본 메시지 사용)
# RAISE  // ✅ 기본 메시지와 기본 종료 코드 (1) 사용

class RaiseCommand(BaseCommand):
    def execute(self, args: list[Token], executor):
        from lib.core.command_parser import CommandParser
        from lib.core.command_executor import CommandExecutor
        from lib.core.exception_registry import ExceptionRegistry
        from lib.core.commands.print_command import PrintCommand

        exception_message = "예외가 발생했습니다."  # 기본 메시지
        exit_code = 1  # 기본 종료 코드

        # ✅ 인자의 개수에 따라 메시지와 exit_no를 구분하여 처리
        if len(args) == 1:
            if args[0].type == TokenType.INTEGER:
                exit_code = args[0].data.value  # 메시지 없이 종료 코드만 지정
            else:
                exception_message = ExprEvaluator(executor=executor).evaluate([args[0]]).data.string
        elif len(args) == 2:
            exception_message = ExprEvaluator(executor=executor).evaluate([args[0]]).data.string
            exit_code_token = args[1]
            if exit_code_token.type == TokenType.INTEGER:
                exit_code = exit_code_token.data.value
            else:
                raise KavanaException(f"EXIT CODE는 정수형이어야 합니다. (잘못된 값: {exit_code_token.data.string})")
        elif len(args) == 3 and args[1].type == TokenType.COMMA:
            exception_message = ExprEvaluator(executor=executor).evaluate([args[0]]).data.string
            exit_code_token = args[2]
            if exit_code_token.type == TokenType.INTEGER:
                exit_code = exit_code_token.data.value
            else:
                raise KavanaException(f"EXIT CODE는 정수형이어야 합니다. (잘못된 값: {exit_code_token.data.string})")

        # ✅ 예외 메시지 및 종료 코드 저장
        executor.variable_manager.set_variable("$exception_message", StringToken(data=String(exception_message), type=TokenType.STRING))
        executor.variable_manager.set_variable("$exit_code", Token(data=Integer(exit_code), type=TokenType.INTEGER))

        if ExceptionRegistry._in_try_block:
            raise KavanaException(exception_message)
        # ✅ ON_EXCEPTION 블록이 등록되어 있다면 실행
        exception_commands = ExceptionRegistry.get_exception_commands()
        if exception_commands:
            command_parser = CommandParser()
            command_parser.ignore_main_check = True
            commands = command_parser.parse(exception_commands[1:-1])
            exception_executor = CommandExecutor()
            exception_executor.variable_manager = executor.variable_manager   
            for command in commands:  # 첫번째와 마지막 명령어는 ON_EXCEPTION, END_EXCEPTION이므로 제외
                exception_executor.execute(command)
        else:
            # ✅ 예외 메시지가 있을 경우 출력
            if exception_message:
                print_command = PrintCommand()
                print_command.execute(
                    [StringToken(data=String(exception_message), type=TokenType.STRING)], executor
                )

        # ✅ 사용자 정의 exit 코드로 종료
        exit(exit_code)