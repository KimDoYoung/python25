from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RPAManager
from lib.core.token_type import TokenType


class KeyInCommand(BaseCommand):
    def execute(self, args, executor):
        """
            KEY_IN [<express:string>, <express:string>..], speed=<express:float, default=0.5>
            KEY_IN "enter", speed=0.5
            example: KEY_IN ["enter", "space", "ctrl+c"], speed=0.5
        """
        option_map = {
            "speed": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        }
        
        # 옵션 값 초기화
        option_values = {key: option_map[key].get("default", None) for key in option_map}        
        rpa_manager = RPAManager(executor=executor)
        executor.set_last_error("")

        # 첫번째 express를 해석해본다.
        express, i = self.get_express(args,0)
        first_token = ExprEvaluator(executor=executor).evaluate(express)
        options, i = self.extract_all_options(args, i) # options 추출
        option_values = self.parse_and_validate_options(options, option_map, executor)
        speed = option_values["speed"]
        if first_token.type == TokenType.LIST_EX:
            rpa_manager.key_press(first_token.data.value, speed=speed)
        elif first_token.type == TokenType.STRING:
            rpa_manager.key_press([first_token.data.value], speed=speed)
        else:
            raise KavanaSyntaxError("KEY_IN 명령어는 인자로 문자열 또는 리스트가 필요합니다.")

        return