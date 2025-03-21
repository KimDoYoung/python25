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
        i,express= self.get_express(args,0)
        first_token = ExprEvaluator(executor=executor).evaluate(express)
        if first_token.type == TokenType.LIST_EX:
            pass
        elif first_token.type == TokenType.STRING:
            pass
        else:
            raise KavanaSyntaxError("KEY_IN 명령어는 인자로 문자열 또는 리스트가 필요합니다.")

        # 속도(speed) 옵션 파싱
        speed = self.extract_option_value(args[i:], executor, option_map, option_values)["speed"]

        # keys_to_press = []

        # if first_token.type == TokenType.STRING:
        #     keys_to_press.append(first_token.value)

        # elif first_token.type == TokenType.LIST_EX:
        #     for item in first_token.value:
        #         if item.type != TokenType.STRING:
        #             raise KavanaSyntaxError("KEY_IN 리스트 내부는 모두 문자열이어야 합니다.")
        #         keys_to_press.append(item.value)

        # # 키 입력 실행
        # for key_str in keys_to_press:
        #     key_str = key_str.strip().lower()
        #     if '+' in key_str:
        #         key_parts = [k.strip() for k in key_str.split('+')]
        #         rpa_manager.key_hotkey(*key_parts)
        #     else:
        #         rpa_manager.key_press(key_str)
        #     if speed > 0:
        #         rpa_manager.sleep(speed)
