from typing import List
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSyntaxError, KavanaTypeError
from lib.core.token_type import TokenType
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import AccessIndexToken, Token

class SetCommand(BaseCommand):
    def execute(self, args:List[Token], executor):
        """
        SET <varname> = <expression> [GLOBAL]
        """
        if len(args) < 3 or args[1].type != TokenType.ASSIGN:
            raise KavanaSyntaxError("잘못된 SET명령어 :  SET <varname> = <expression> [GLOBAL]")

        var_name = args[0].data.value
        expression = args[2:]  # 수식 부분
        local_flag = executor.in_function_scope  # ✅ 함수 내부면 자동으로 Local

        # GLOBAL 키워드가 붙으면 전역 변수 강제 설정
        if args[-1].type == TokenType.GLOBAL:
            local_flag = False
            expression = args[2:-1]  # GLOBAL 제거

        # 수식 평가
        exprEvaluator = ExprEvaluator(executor)
        value_token = exprEvaluator.evaluate(expression)
        # 변수 저장
        if args[0].type == TokenType.ACCESS_INDEX: # SET list[0] = 10
            target_token = args[0]
            access_token: AccessIndexToken = target_token
            var_name = access_token.data.value
            index_expresses = access_token.index_expresses

            container_token = executor.variable_manager.get_variable(var_name)
            current_token = container_token

            evaluator = ExprEvaluator(executor)
            if current_token.type == TokenType.HASH_MAP:
                # 마지막 인덱스 전까지 순회
                for expr in index_expresses[:-1]:
                    index_token = evaluator.evaluate(expr)
                    key = index_token.data.value
                    current_token = current_token.data.get(key)

                # 마지막 인덱스
                last_expr = index_expresses[-1]
                last_index_token = evaluator.evaluate(last_expr)
                last_key = last_index_token.data.value
                current_token.data.set(last_key, value_token.data)
            elif current_token.type == TokenType.ARRAY:
                row_expr = index_expresses[0]
                col_expr = index_expresses[1] if len(index_expresses) > 1 else None
                row = evaluator.evaluate(row_expr).data.value
                col = evaluator.evaluate(col_expr).data.value if col_expr else None
                current_token.data.set(row,col, value_token)
            else:
                raise KavanaTypeError("마지막 인덱싱 대상은 ARRAY 또는 HASH_MAP이어야 합니다.",target_token.line_number, target_token.column_number)
        else:
            executor.variable_manager.set_variable(var_name, value_token, local=local_flag)
