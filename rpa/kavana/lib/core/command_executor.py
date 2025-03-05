from lib.core.commands.const_command import ConstCommand
from lib.core.commands.endfunction_command import EndFunctionCommand
from lib.core.commands.function_command import FunctionCommand
from lib.core.commands.print_command import PrintCommand
from lib.core.commands.return_command import ReturnCommand
from lib.core.commands.set_command import SetCommand
from lib.core.datatypes.kavana_datatype import Integer
from lib.core.exceptions.kavana_exception import BreakException, CommandExecutionError, ContinueException
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.variable_manager import VariableManager


class CommandExecutor:
    """
    CommandExecutor는 Kavana 스크립트에서 파싱된 명령을 실행한다.
    """
    def __init__(self):
        self.variable_manager = VariableManager()
        self.in_function_scope = False  # ✅ 함수 내부 여부 추적
        self.command_map = {
            "SET": SetCommand(),
            "PRINT": PrintCommand(),
            "FUNCTION": FunctionCommand(),
            "END_FUNCTION": EndFunctionCommand(),
            "RETURN": ReturnCommand() ,
            "CONST" : ConstCommand()
        }
    def execute(self, command):
        cmd = command["cmd"]
        # ✅ IF 문 처리
        if cmd == "IF_BLOCK":
            condition = command["body"][0]["args"]
            if self.eval_express(condition):
                for sub_command in command["body"][1:]:
                    self.execute(sub_command)
            return

        # ✅ WHILE 문 처리
        if cmd == "WHILE_BLOCK":
            condition = command["body"][0]["args"]
            while self.eval_express_primitive(condition):
                try:
                    for sub_command in command["body"][1:]:
                        self.execute(sub_command)
                except ContinueException:
                    continue  # 다음 반복으로 이동
                except BreakException:
                    break  # 반복문 종료
            return

        # ✅ FOR 문 처리
        if cmd == "FOR_BLOCK":
            loop_var, start_value, end_value, step_value = self.parse_for_args(command["body"][0]["args"])
            current_value = start_value

            while current_value <= end_value:
                loop_var_token = Token(Integer(current_value), TokenType.INTEGER)
                self.variable_manager.set_variable(loop_var, loop_var_token)
                try:
                    for sub_command in command["body"][1:]:
                        self.execute(sub_command)
                except ContinueException:
                    current_value += step_value
                    continue  # 다음 반복으로 이동
                except BreakException:
                    break  # 반복문 종료
                current_value += step_value
            return

        # ✅ BREAK 처리
        if cmd == "BREAK":
            raise BreakException()

        # ✅ CONTINUE 처리
        if cmd == "CONTINUE":
            raise ContinueException()

        # ✅ 일반 명령어 실행
        self.execute_standard_command(command)

    def execute_standard_command(self, command):
        """일반 명령어 실행"""
        cmd = command["cmd"]
        args = command["args"]

        if cmd in self.command_map:
            self.command_map[cmd].execute(args, self)  # 명령어 객체에 실행 위임
        else:
            raise CommandExecutionError(f"Unknown command: {cmd}")

    def eval_express(self, express: list[Token])->Token:
        """IF 및 WHILE 조건 평가"""
        exprEvaluator = ExprEvaluator( self.variable_manager)
        result_token =  exprEvaluator.evaluate(express)
        return result_token
    
    def eval_express_primitive(self, express: list[Token]):
        """IF 및 WHILE 조건 평가"""
        exprEvaluator = ExprEvaluator(self.variable_manager)
        result_token =  exprEvaluator.evaluate(express)
        return result_token.data.value

    def parse_for_args(self, args: list[Token]):
        """FOR 루프에서 초기값, 최대값, STEP을 파싱 (조건식과 수식 지원)"""
        
        to_index = self.find_index(args, TokenType.TO)
        if to_index == -1:
            raise CommandExecutionError("FOR 문에는 'TO'가 필요합니다.", args[0].line, args[0].column)
        step_index = self.find_index(args, TokenType.STEP)
        if step_index != -1 and step_index < to_index:
            raise CommandExecutionError("FOR 문에는 'TO'보다 앞에 'STEP'이 올 수 없습니다.", args[0].line, args[0].column)

        if args[1].type != TokenType.OPERATOR or args[1].data.value != "=":
            raise CommandExecutionError("FOR 문의 변수 할당이 잘못되었습니다.", args[0].line, args[0].column)

        loop_var = args[0]  # 반복 변수명
        start_expr = args[2:to_index]  # 초기값 표현식
        end_expr = args[to_index + 1:step_index] if step_index != -1 else args[to_index + 1:]
        step_expr = args[step_index + 1:] if step_index != -1 else [Token(TokenType.INTEGER, "1")]

        # ✅ 표현식 평가
        start_value = self.eval_express(start_expr)
        end_value = self.eval_express(end_expr)
        step_value = self.eval_express(step_expr)

        return loop_var.data.value, start_value.data.value, end_value.data.value, step_value.data.value

    def find_index(self, tokens, token_type):
        for i, token in enumerate(tokens):
            if token.type == token_type:
                return i
        return -1