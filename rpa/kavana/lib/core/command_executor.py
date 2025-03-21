import sys
from lib.core.commands.const_command import ConstCommand
from lib.core.commands.endfunction_command import EndFunctionCommand
from lib.core.commands.exit_command import ExitCommand
from lib.core.commands.function_command import FunctionCommand
from lib.core.commands.just_command import JustCommand
from lib.core.commands.log_command import LogConfigCommand, LogDebugCommand, LogErrorCommand, LogInfoCommand, LogWarnCommand
from lib.core.commands.print_command import PrintCommand
from lib.core.commands.raise_command import RaiseCommand
from lib.core.commands.return_command import ReturnCommand
from lib.core.commands.rpa.app_close_command import AppCloseCommand
from lib.core.commands.rpa.app_open_command import AppOpenCommand
from lib.core.commands.rpa.click_command import ClickCommand
from lib.core.commands.rpa.close_child_windows_command import CloseChildWindowsCommand
from lib.core.commands.rpa.mouse_move_command import MouseMoveCommand
from lib.core.commands.rpa.wait_command import WaitCommand
from lib.core.commands.set_command import SetCommand
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.exceptions.kavana_exception import BreakException, CommandExecutionError, ContinueException
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil
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
            "CONST" : ConstCommand(),
            "EXIT" : ExitCommand(),
            "RAISE" : RaiseCommand(),
            "JUST"  : JustCommand(),
            # log 관련 명령어
            "LOG_CONFIG" : LogConfigCommand(),
            "LOG_DEBUG" : LogDebugCommand(),
            "LOG_INFO" : LogInfoCommand(),
            "LOG_WARN" : LogWarnCommand(),
            "LOG_ERROR" : LogErrorCommand(),
        }
        # RPA 명령어 매핑
        self.rpa_command_map = {
            "APP_OPEN": AppOpenCommand(),
            "APP_CLOSE": AppCloseCommand(),
            "CLOSE_CHILD_WINDOWS": CloseChildWindowsCommand(),
            "WAIT": WaitCommand(),
            "CLICK": ClickCommand(),
            "MOUSE_MOVE": MouseMoveCommand(),
            "KEY_IN" :KeyInCommand()

        }
    def execute(self, command):
        cmd = command["cmd"]
      
        # ✅ IF 문 처리
        if cmd == "IF_BLOCK":
            condition = command["body"][0]["args"]
            condition_met = self.eval_express_boolean(condition)  # 현재 블록이 실행될지 여부
            condition_found = condition_met  # 실행된 블록이 있는지 추적
            
            body = command["body"][1:]  # IF_BLOCK 내부 코드

            exec_body = []  # 최종 실행할 코드 저장
            for sub_command in body:
                if sub_command["cmd"] in ["ELIF", "ELSE"]:
                    if condition_found:  
                        break  # IF 또는 ELIF 중 하나라도 실행되었으면 나머지는 실행하지 않음
                    
                    if sub_command["cmd"] == "ELIF":
                        condition = sub_command["args"]
                        condition_met = self.eval_express_boolean(condition)
                    
                    else:  # ELSE
                        condition_met = True  

                    condition_found = condition_met  # 이후 모든 블록 무시하도록 설정
                    continue

                if condition_met:
                    exec_body.append(sub_command)  # 실행할 블록에 추가

            # 최종 실행
            for sub_command in exec_body:
                self.execute(sub_command)

            return
        # ✅ WHILE 문 처리
        if cmd == "WHILE_BLOCK":
            condition = command["body"][0]["args"]
            while self.eval_express_boolean(condition):
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
            args = command["body"][0]["args"]
            if self.find_index(args, TokenType.TO) != -1: # for i = 1 to 10 step 2
                loop_var, start_value, end_value, step_value = self.parse_for_args(args)
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
            elif  self.find_index(args, TokenType.IN) != -1: # for i in range(1,10)
                loop_var_name, iterable = self.parse_for_in_args(args)
                for t in iterable:
                    #TODO iterable이 Integer가 아닌경우
                    # loop_var_token = Token(data=Integer(t.data.value), type=TokenType.INTEGER)
                    loop_var_token = Token(data=t.data, type=t.type)
                    self.variable_manager.set_variable(loop_var_name, loop_var_token)
                    try:
                        for sub_command in command["body"][1:]:
                            self.execute(sub_command)
                    except ContinueException:
                        continue  # 다음 반복으로 이동
                    except BreakException:
                        break  # 반복문 종료               
            return

        # ✅ BREAK 처리
        if cmd == "BREAK":
            raise BreakException("break 명령어 실횅")

        # ✅ CONTINUE 처리
        if cmd == "CONTINUE":
            raise ContinueException("continue 명령어 실행")

        # ✅ RPA 명령어인지 확인 후 실행
        if cmd in self.rpa_command_map:
            self.execute_rpa_command(command)
            return

        # ✅ 일반 명령어 실행
        self.execute_standard_command(command)
    
    def execute_rpa_command(self, command):
        """RPA 명령어 실행"""
        cmd = command["cmd"]
        args = command["args"]

        if cmd in self.rpa_command_map:
            self.rpa_command_map[cmd].execute(args, self)

    def execute_standard_command(self, command):
        """일반 명령어 실행"""
        cmd = command["cmd"]
        args = command["args"]

        if cmd in self.command_map:
            self.command_map[cmd].execute(args, self)  # 명령어 객체에 실행 위임
        else:
            raise CommandExecutionError(f"알려지지 않은 명령어입니다: {cmd}")

    def eval_express(self, express: list[Token])->Token:
        """IF 및 WHILE 조건 평가"""
        exprEvaluator = ExprEvaluator(self)
        result_token =  exprEvaluator.evaluate(express)
        return result_token
    
    def eval_express_boolean(self, express: list[Token]):
        """IF 및 WHILE 조건 평가"""
        exprEvaluator = ExprEvaluator(self)
        result_token =  exprEvaluator.evaluate(express)
        if result_token.type != TokenType.BOOLEAN:
            raise CommandExecutionError("IF 및 WHILE 조건은 BOOL 타입이어야 합니다.", express[0].line, express[0].column)
        return result_token.data.value
    
    def find_index(self, tokens, token_type):
        ''' token list에서 token_type의 index를 찾는다. 못찾으면 -1'''
        for i, token in enumerate(tokens):
            if token.type == token_type:
                return i
        return -1
    def parse_for_in_args(self, args: list[Token]):
        """FOR 루프에서 초기값, 최대값, STEP을 파싱 (조건식과 수식 지원)"""
        in_index = self.find_index(args, TokenType.IN)
        if in_index == -1:
            raise CommandExecutionError("FOR 문에는 'IN'이 필요합니다.", args[0].line, args[0].column)
        loop_var = args[0]
        iterable_express = args[in_index + 1:]
        list_token = self.eval_express(iterable_express)
        if list_token.type != TokenType.LIST_EX:
            raise CommandExecutionError("FOR 문의 IN 다음은 리스트여야 합니다.", args[0].line, args[0].column)
        iterable = list_token.data.primitive
        return loop_var.data.value, iterable


    def parse_for_args(self, args: list[Token]):
        """FOR 루프에서 초기값, 최대값, STEP을 파싱 (조건식과 수식 지원)"""
        
        to_index = self.find_index(args, TokenType.TO)
        if to_index == -1:
            raise CommandExecutionError("FOR 문에는 'TO'가 필요합니다.", args[0].line, args[0].column)
        step_index = self.find_index(args, TokenType.STEP)
        if step_index != -1 and step_index < to_index:
            raise CommandExecutionError("FOR 문에는 'TO'보다 앞에 'STEP'이 올 수 없습니다.", args[0].line, args[0].column)

        if args[1].type != TokenType.ASSIGN:
            raise CommandExecutionError("FOR 문의 변수 할당이 잘못되었습니다.", args[0].line, args[0].column)

        loop_var = args[0]  # 반복 변수명
        start_expr = args[2:to_index]  # 초기값 표현식
        end_expr = args[to_index + 1:step_index] if step_index != -1 else args[to_index + 1:]
        step_expr = args[step_index + 1:] if step_index != -1 else [Token(data=Integer(1),type=TokenType.INTEGER)]

        # ✅ 표현식 평가
        start_value = self.eval_express(start_expr)
        end_value = self.eval_express(end_expr)
        step_value = self.eval_express(step_expr)

        return loop_var.data.value, start_value.data.value, end_value.data.value, step_value.data.value


    def exit(self, code=0):
        """EXIT 실행"""
        sys.exit(code)

    def log_command(self, level, message):
        """로그 기록을 위한 헬퍼 함수"""
        if level.upper() not in ["DEBUG", "INFO", "WARN", "ERROR"]:
            raise ValueError(f"잘못된 로그 레벨: {level}")

        log_command = self.command_map.get(f"LOG_{level.upper()}")
        if log_command:
            message_token = Token(data=String(message), type=TokenType.STRING)
            log_command.execute([message_token], self)
        else:
            raise RuntimeError(f"로그 명령어 실행 실패: LOG_{level.upper()}")

    def raise_command(self, message):
        """예외 발생을 위한 헬퍼 함수"""
        raise_command = self.command_map.get("RAISE")
        if raise_command:
            tokenMsg = Token(data=String(message), type=TokenType.STRING)
            tokenErrorCode = Token(data=Integer(1), type=TokenType.INTEGER)
            raise_command.execute([tokenMsg, tokenErrorCode], self)
        else:
            raise RuntimeError("RAISE 명령어 실행 실패")
        
    def set_last_error(self, value:str):
        """시스템 변수 설정"""
        last_error_token = Token(data=String(value), type=TokenType.STRING)
        self.variable_manager.set_variable("_LastError_", last_error_token)