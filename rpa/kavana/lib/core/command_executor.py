import sys
from lib.core.builtins.datatype_functions import DatatypeFunctions
from lib.core.builtins.dir_functions import DirFunctions
from lib.core.builtins.file_functions import FileFunctions
from lib.core.builtins.numeric_functions import NumericFunctions
from lib.core.builtins.path_functions import PathFunctions
from lib.core.builtins.region_point_functions import RegionPointFunctions
from lib.core.builtins.rpa_functions import RpaFunctions
from lib.core.builtins.string_functions import StringFunctions
from lib.core.builtins.ymd_time_functions import YmdTimeFunctions
from lib.core.commands.browser.browser_command import BrowserCommand
from lib.core.commands.const_command import ConstCommand
from lib.core.commands.database.database_command import DatabaseCommand
from lib.core.commands.database.db_commander import DbCommander
from lib.core.commands.endfunction_command import EndFunctionCommand
from lib.core.commands.exit_command import ExitCommand
from lib.core.commands.function_command import FunctionCommand
from lib.core.commands.html_command import HtmlCommand
from lib.core.commands.image.image_command import ImageCommand
from lib.core.commands.just_command import JustCommand
from lib.core.commands.log_command import LogConfigCommand, LogDebugCommand, LogErrorCommand, LogInfoCommand, LogWarnCommand
from lib.core.commands.network.ftp_command import FtpCommand
from lib.core.commands.network.http_command import HttpCommand
from lib.core.commands.network.sftp_command import SftpCommand
from lib.core.commands.ocr.ocr_command import OcrCommand
from lib.core.commands.print_command import PrintCommand
from lib.core.commands.raise_command import RaiseCommand
from lib.core.commands.return_command import ReturnCommand
from lib.core.commands.rpa.rpa_command import RpaCommand
from lib.core.commands.set_command import SetCommand
from lib.core.datatypes.kavana_datatype import Float, Integer, String
from lib.core.exception_registry import ExceptionRegistry
from lib.core.exceptions.kavana_exception import BreakException, CommandExecutionError, ContinueException, KavanaException
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import ArrayToken, HashMapToken, StringToken, Token, TokenStatus
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
            "CALL"  : JustCommand(),
            # log 관련 명령어
            "LOG_CONFIG" : LogConfigCommand(),
            "LOG_DEBUG" : LogDebugCommand(),
            "LOG_INFO" : LogInfoCommand(),
            "LOG_WARN" : LogWarnCommand(),
            "LOG_ERROR" : LogErrorCommand(),
        }
        # RPA 명령어 매핑
        self.rpa_command_map = {
            "RPA": RpaCommand(),
            "DB": DatabaseCommand(),
            # network
            "FTP": FtpCommand(),
            "SFTP": SftpCommand(),
            "HTTP": HttpCommand(),
            # ocr, browser(selenium), image
            "OCR" : OcrCommand(),
            "BROWSER" : BrowserCommand(),
            "HTML" : HtmlCommand(),
            "IMAGE" : ImageCommand(),
            
        }
        # ✅ Functions에서 log_command를 사용하기 위해서.. injection
        DatatypeFunctions.set_executor(self)
        DirFunctions.set_executor(self)
        FileFunctions.set_executor(self)
        NumericFunctions.set_executor(self)
        PathFunctions.set_executor(self)
        RegionPointFunctions.set_executor(self)
        RpaFunctions.set_executor(self)
        StringFunctions.set_executor(self)
        YmdTimeFunctions.set_executor(self)
        
    def execute(self, command):
        cmd = command["cmd"]

        if cmd == "TRY_BLOCK":
            try:
                ExceptionRegistry.set_in_try_block(True)  # TRY 블록 시작 
                for sub_command in command["try"]:
                    if sub_command["cmd"] == "RAISE":
                        # 명시적으로 RAISE 명령어를 수동 처리
                        conditions = sub_command["args"]
                        message_token = conditions[0]
                        message = message_token.data.value
                        raise RuntimeError(message)  # 또는 custom 예외
                    self.execute(sub_command)  # 일반 명령어는 그대로 실행
            except (BreakException, ContinueException) as flow_control_ex:
                # Flow control 예외는 상위로 전파해야 함
                ExceptionRegistry.set_in_try_block(False)
                # finally 블록 실행 
                for sub_command in command["finally"]:
                    self.execute(sub_command)
                # 원래 예외 다시 던지기
                raise flow_control_ex
            except Exception as e:
                self.set_last_error(str(e))
                for sub_command in command["catch"]:
                    self.execute(sub_command)
                # 일반 예외의 경우 finally 블록 여기서 실행
                for sub_command in command["finally"]:
                    self.execute(sub_command)
            else:
                # 예외가 발생하지 않은 경우만 여기서 finally 블록 실행
                for sub_command in command["finally"]:
                    self.execute(sub_command)
            finally:
                # finally 블록에서는 상태만 초기화
                ExceptionRegistry.set_in_try_block(False)  # TRY 블록 종료 후 상태 초기화    
            return        
        

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
                        # cmd가 SET 인 경우 status를 갖는 토큰을 parsed로 처리, 안그러면 계속 처음값을 유지함.
                        if sub_command["cmd"] == "SET":
                            self.reset_parse_status(sub_command["args"])

                        self.execute(sub_command)
                except ContinueException:
                    continue  # 다음 반복으로 이동
                except BreakException:
                    break  # 반복문 종료
            return

        # ✅ FOR 문 처리
        if cmd == "FOR_BLOCK":
            conditions = command["body"][0]["args"]
            if self.find_index(conditions, TokenType.TO) != -1: # for i = 1 to 10 step 2
                loop_var, start_value, end_value, step_value = self.parse_for_args(conditions)
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
            elif  self.find_index(conditions, TokenType.IN) != -1: # for i in range(1,10)
                loop_var_name, iterable = self.parse_for_in_args(conditions)
                for t in iterable:
                    if isinstance(t, Token):
                        loop_var_token = Token(data=t.data, type=t.type)
                    else:
                        raise CommandExecutionError(f"FOR IN 문에서 지원하지 않는 타입(Not Iterable)입니다: {type(t)}")

                    self.variable_manager.set_variable(loop_var_name, loop_var_token)
                    try:
                        for sub_command in command["body"][1:]:
                            # cmd가 SET 인 경우 status를 갖는 토큰을 parsed로 처리
                            if sub_command["cmd"] == "SET":
                                self.reset_parse_status(sub_command["args"])
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
        try:
            # ✅ RPA 명령어인지 확인 후 실행
            if cmd in self.rpa_command_map:
                self.execute_rpa_command(command)
            else:
                self.execute_standard_command(command)
        except Exception as e:
            self.log_command("ERROR", f"오류 발생: {e}")
            self.raise_command(f"오류 발생: {e}")

    
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
        """FOR IN 루프에서 변수명과 리스트를 파싱"""
        in_index = self.find_index(args, TokenType.IN)
        if in_index == -1:
            raise CommandExecutionError("FOR 문에는 'IN'이 필요합니다.", args[0].line, args[0].column)
        loop_var = args[0]
        iterable_express = args[in_index + 1:]
        list_token = self.eval_express(iterable_express)
        if list_token.type != TokenType.ARRAY:
            raise CommandExecutionError("FOR 문의 IN 다음은 리스트여야 합니다.", args[0].line, args[0].column)
        #iterable = list_token.data.primitive
        iterable = list_token.data
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
            message_token = StringToken(data=String(message), type=TokenType.STRING)
            log_command.execute([message_token], self)
        else:
            raise RuntimeError(f"로그 명령어 실행 실패: LOG_{level.upper()}")

    # def raise_command(self, message):
    #     """예외 발생을 위한 헬퍼 함수"""
    #     raise_command = self.command_map.get("RAISE")
    #     if raise_command:
    #         tokenMsg = StringToken(data=String(message), type=TokenType.STRING)
    #         tokenErrorCode = Token(data=Integer(1), type=TokenType.INTEGER)
    #         raise_command.execute([tokenMsg, tokenErrorCode], self)
    #     else:
    #         raise RuntimeError("RAISE 명령어 실행 실패")
    def raise_command(self, message):
        """예외 발생을 위한 헬퍼 함수"""
        if getattr(self, "_handling_exception", False):
            print("예외 처리 중 예외가 발생하여 중단:", message)
            return

        self._handling_exception = True  # 플래그 설정

        try:
            raise_command = self.command_map.get("RAISE")
            if raise_command:
                tokenMsg = StringToken(data=String(message), type=TokenType.STRING)
                tokenErrorCode = Token(data=Integer(1), type=TokenType.INTEGER)
                raise_command.execute([tokenMsg, tokenErrorCode], self)
            else:
                raise RuntimeError("RAISE 명령어 실행 실패")
        except Exception as e:
            print("RAISE 명령 실행 중 내부 오류:", e)
        finally:
            self._handling_exception = False  # 플래그 해제

    def set_last_error(self, value:str):
        """시스템 변수 설정"""
        last_error_token = StringToken(data=String(value), type=TokenType.STRING)
        self.variable_manager.set_variable("_LastError_", last_error_token)
    
    def set_variable(self, var_name, token):
        """변수 설정"""
        self.variable_manager.set_variable(var_name, token)
    def get_variable(self, var_name):
        """변수 설정"""
        return self.variable_manager.get_variable(var_name)
    
    def get_db_commander(self, db_name):
        """DB Commander 가져오기"""
        return self.variable_manager.get_db_commander(db_name)
    def set_db_commander(self, db_name, db_commander: DbCommander):
        """DB Commander 설정"""
        return self.variable_manager.set_db_commander(db_name, db_commander)
    
    def reset_parse_status(self, args: list[Token]):
        """토큰의 파싱 상태를 초기화"""
        for token in args:
            # if hasattr(token, "status"):
            #     token.status = TokenStatus.PARSED
            if isinstance(token, ArrayToken):
                token.status = TokenStatus.PARSED
            elif isinstance(token, HashMapToken):
                 token.status = TokenStatus.PARSED
        return