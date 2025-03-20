import time
from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.image import Image
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import KavanaSyntaxError, KavanaTypeError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RPAManager
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

class WaitCommand(BaseCommand):
    def execute(self, args, executor):
        """
        WAIT <seconds>
        WAIT until path=<express:string 필수>, timeout=<express:integer 60>, confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>
        """
        if len(args) >= 1 and (args[0].type != TokenType.IDENTIFIER or args[0].data.string.lower() != "until"):
            # WAIT <seconds> 실행
            expr_evaluator = ExprEvaluator(executor=executor)
            result_token = expr_evaluator.evaluate(args)
            
            if result_token.type == TokenType.INTEGER:
                time.sleep(result_token.data.value)
                return
            else:
                raise KavanaSyntaxError("WAIT 명령어는 정수 시간을 인자로 받거나, WAIT IMAGE 사용해야 합니다.")
        
        if len(args) < 2 or args[0].type != TokenType.IDENTIFIER or args[0].data.string.lower() != "until":
            raise KavanaSyntaxError("WAIT until [image_path, timeout, confidence, region, grayscale] 명령어의 형식이 올바르지 않습니다.")
        
        # 기본 옵션 설정
        option_map = {
            "image_path": {"required": True, "allowed_types": [TokenType.STRING]},
            "timeout": {"default": 60, "allowed_types": [TokenType.INTEGER]},
            "confidence": {"default": 0.8, "allowed_types": [TokenType.FLOAT]},
            "region": {"default": None, "allowed_types": [TokenType.REGION]},
            "grayscale": {"default": False, "allowed_types": [TokenType.BOOLEAN]}
        }
        
        # 옵션 값 초기화
        option_values = {key: option_map[key].get("default", None) for key in option_map}
        
        # 옵션 파싱
        i = 1  # image 다음부터 시작
        while args[i].type == TokenType.COMMA:
            i += 1        
        while i < len(args):
            key_token, express_tokens, next_index = self.extract_command_option(args, i)
            
            if key_token is None:
                break
            
            key = key_token.data.string.strip().lower()
            if key not in option_map:
                raise KavanaSyntaxError(f"알 수 없는 옵션 '{key}'입니다.")
            
            expr_evaluator = ExprEvaluator(executor=executor)
            result_token = expr_evaluator.evaluate(express_tokens)
            
            allowed_types = option_map[key]["allowed_types"]
            if result_token.type not in allowed_types:
                allowed_type_names = [t.name for t in allowed_types]
                raise KavanaTypeError(
                    f"옵션 '{key}'는 {', '.join(allowed_type_names)} 타입만 허용됩니다. (현재: {result_token.type.name})"
                )
            
            option_values[key] = result_token.data.value
            i = next_index
        
        # 필수 옵션 체크
        for key, info in option_map.items():
            if info.get("required") and option_values[key] is None:
                raise KavanaSyntaxError(f"WAIT UNTIL 옵션 '{key}'은(는) 필수입니다.")
        
        # 이미지 탐색 실행
        image_path = option_values["image_path"]
        timeout = option_values["timeout"]
        confidence = option_values["confidence"]
        region = option_values["region"]
        grayscale = option_values["grayscale"]

        try:
            location = RPAManager(executor=executor).wait_for_image(
                image_path=image_path,
                timeout=timeout,
                confidence=confidence,
                grayscale=grayscale,
                region=region
            )
        except Exception as e:
            executor.set_last_error(f"error: {str(e)}")
            return
        
        if location:
            executor.set_last_error("")
        else:
            executor.set_last_error("Not Found")
