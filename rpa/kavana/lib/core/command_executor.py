
from lib.core.commands.endfunction_command import EndFunctionCommand
from lib.core.commands.function_command import FunctionCommand
from lib.core.commands.print_command import PrintCommand
from lib.core.commands.set_command import SetCommand
from lib.core.expr_evaluator import ExprEvaluator
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
        }

    def execute(self, command: dict):
        """
        주어진 명령을 실행한다.
        :param command: {"cmd": "SET", "args": ["var_name", "=", "expression"]}
        """
        cmd = command["cmd"]
        args = command["args"]

        # ✅ 명령어 실행
        if cmd in self.command_map:
            self.command_map[cmd].execute(args, self)  # 명령어 객체에 실행 위임
        else:
            raise ValueError(f"Unknown command: {cmd}")

    # def _execute_print(self, args):
    #     """
    #     PRINT 명령어 실행 (출력)
    #     예: PRINT("Hello, World!")
    #     """
    #     if not args:
    #         raise SyntaxError("PRINT command requires at least one argument.")

    #     output = args[0]  # 첫 번째 인자를 가져오기
    #     if output.startswith('"') and output.endswith('"'):
    #         output = output[1:-1]  # 따옴표 제거

    #     print(output)

    # def _execute_println(self, args):
    #     """
    #     PRINTLN 명령어 실행 (출력 후 개행)
    #     예: PRINTLN("Hello, World!")
    #     """
    #     if not args:
    #         print()  # ✅ 인자가 없으면 개행만 출력
    #     else:
    #         output = " ".join(args)  # ✅ 여러 인자가 있을 경우 공백으로 결합
    #         if output.startswith('"') and output.endswith('"'):
    #             output = output[1:-1]  # ✅ 따옴표 제거
    #         print(output)  # ✅ 기본 출력 (자동 개행 포함)

    # def _execute_set(self, args):
    #     """
    #     SET 명령어 실행: SET <varname> = <expression> [GLOBAL]
    #     - 함수 내부에서는 기본적으로 Local 변수로 저장
    #     - "GLOBAL" 키워드를 사용하면 함수 내부에서도 전역 변수로 저장 가능
    #     """
    #     if len(args) < 3 or args[1] != "=":
    #         raise SyntaxError("Invalid SET command format. Expected: SET <varname> = <expression> [GLOBAL]")

    #     var_name = args[0]
    #     expression = " ".join(args[2:])  # 수식 부분
    #     local_flag = self.in_function_scope  # ✅ 함수 내부면 자동으로 Local

    #     # GLOBAL 키워드가 붙으면 전역 변수 강제 설정
    #     if args[-1].upper() == "GLOBAL":
    #         local_flag = False
    #         expression = " ".join(args[2:-1])  # GLOBAL 제거

    #     # 수식 평가 (ExprEvaluator 활용)
    #     value = ExprEvaluator.evaluate(expression, self.variable_manager)

    #     # 변수 저장
    #     self.variable_manager.set_variable(var_name, value, local=local_flag)

    # def _execute_function(self, args):
    #     """
    #     FUNCTION 시작: 새로운 지역 변수 스코프 추가
    #     """
    #     self.variable_manager.push_local_scope()  # 지역 변수 스코프 추가
    #     self.in_function_scope = True  # ✅ 함수 내부 상태 활성화

    # def _execute_end_function(self):
    #     """
    #     FUNCTION 종료: 지역 변수 스코프 제거
    #     """
    #     self.variable_manager.pop_local_scope()  # 지역 변수 스코프 제거
    #     self.in_function_scope = False  # ✅ 함수 내부 상태 비활성화