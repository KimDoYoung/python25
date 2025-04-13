
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RpaManager
from lib.core.token import Token
from lib.core.token_type import TokenType


class CaptureScreenCommand(BaseCommand):
    '''
    CAPTURE_SCREEN full, var_to=<string>, save_to=<express:string>
    CAPTURE_SCREEN [region|rectangle], var_to=<string>, save_to=<express:string>
    '''
    def execute(self, args, executor):
        option_map = {
            "var_to": {"default": None, "allowed_types": [TokenType.STRING]},
            "save_to_file": {"default": None, "allowed_types": [TokenType.STRING]},
        }        
        # 옵션 값 초기화
        option_values = {key: option_map[key].get("default", None) for key in option_map}        
        rpa_manager = RpaManager(executor=executor)
        executor.set_last_error("")
        express, i  = self.get_express(args, 0)
        area_token = ExprEvaluator(executor=executor).evaluate(express)

        # 옵션 파싱
        options, i = self.extract_all_options(args, i)
        if options:
            for key, value_dict in options.items():
                value_express = value_dict["express"]
                if key in option_values:    
                    option_values[key] = ExprEvaluator(executor=executor).evaluate(value_express).data.value
        save_to_file = option_values["save_to_file"]
        var_to = option_values["var_to"]

        if not save_to_file and not var_to:
            raise KavanaSyntaxError("CAPTURE_SCREEN 명령어는 'save_to_file' 또는 'var_to' 옵션 중 하나는 필수입니다.")

        if (area_token.type == TokenType.IDENTIFIER 
            and area_token.data.string.upper() == "FULL"):
            # 전체 화면 캡쳐
            if save_to_file:
                image1 = rpa_manager.capture_screen(image_path=save_to_file,region=None)
            if var_to:
                img_token = Token(data=image1, type=TokenType.IMAGE)
                executor.set_variable(var_to, img_token)
        elif (area_token.type == TokenType.REGION):
            # 지정 영역 캡쳐
            region = area_token.data
            if save_to_file:
                image1 = rpa_manager.capture_screen(image_path=save_to_file,region=region)
            if var_to:
                img_token = Token(data=image1, type=TokenType.IMAGE)
                executor.set_variable(var_to, img_token)
        elif (area_token.type == TokenType.RECTANGLE):
            region = area_token.data.to_region()
            if save_to_file:
                image1 = rpa_manager.capture_screen(image_path=save_to_file,region=region)
            if var_to:
                img_token = Token(data=image1, type=TokenType.IMAGE)
                executor.set_variable(var_to, img_token)
        else:
            raise KavanaSyntaxError("CAPTURE_SCREEN 명령어의 첫번째 인자는 'full', 'region', 'rectangle' 중 하나여야 합니다.")

