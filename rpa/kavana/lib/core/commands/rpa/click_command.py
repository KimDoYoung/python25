import pyautogui
from lib.actions.actions import wait_for_image
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RPAManager
from lib.core.token import Token
from lib.core.token_type import TokenType

class ClickCommand(BaseCommand):
    def execute(self, args, executor):
        """
        CLICK 10, 20 [count=1] [duration=0.2] [type="single"]
        CLICK <x: int>, <y: int>
        CLICK image_path=<express> confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>, type=<express:string "single">
        CLICK <object: Point | Region | Rectangle>
        """
        # key_value_map, i = self.extract_all_options(args, 0)
        # exists_x = "x" in key_value_map
        # exists_y = "y" in key_value_map
        # exists_type = "type" in key_value_map
        # exists_image_path = "image_path" in key_value_map
        # exists_point_name = "point_name" in key_value_map
        
        # click_type = key_value_map.get("type", {"express": [Token(TokenType.STRING, "single")]})["express"]
        # click_count = key_value_map.get("count", {"express": [Token(TokenType.INTEGER, 1)]})["express"]
        # duration = key_value_map.get("duration", {"express": [Token(TokenType.INTEGER, 0)]})["express"]
        option_map = {
            "count": {"default": 1, "allowed_types": [TokenType.INTEGER]},
            "duration": {"default": 0.2, "allowed_types": [TokenType.FLOAT]},
            "type": {"default": "single", "allowed_types": [TokenType.STRING]},
        }
        
        # 옵션 값 초기화
        option_values = {key: option_map[key].get("default", None) for key in option_map}        
        rpa_manager = RPAManager(executor=executor)
        executor.set_last_error("")
        if (len(args) >= 2  # click 10,20
            and args[0].type == TokenType.INTEGER  
            and args[1].type == TokenType.COMMA  
            and args[2].type == TokenType.INTEGER):
            # 좌표 클릭
            x = ExprEvaluator(executor=executor).evaluate([args[0]]).data.value
            y = ExprEvaluator(executor=executor).evaluate([args[2]]).data.value
            options, i = self.extract_all_options(args, 3) # options 추출
            if options:
                for key, value in options:
                    if key in option_values:    
                        option_values[key] = ExprEvaluator(executor=executor).evaluate([args[2]]).data.value
            rpa_manager.click(x=x, y=y, click_type=option_values["type"], click_count=option_values["count"], duration=option_values["duration"])
            return
        
        # if args[0].type in [TokenType.REGION, TokenType.RECTANGLE]:
        #     # 영역 클릭 (추가 옵션 point_name 지원)
        #     region = args[0].data.value
        #     point_name = key_value_map.get("point_name", {"express": [Token(TokenType.STRING, "center")]})["express"]
        #     x, y = region.get_point(point_name)
        #     self.perform_click(click_type, x, y, click_count, duration)
        #     executor.system_variables["$$LastError"] = ""
        #     return
        
        # if exists_x and exists_y:
        #     # 명시적 x, y 좌표 클릭
        #     x = self.evaluate_expression(key_value_map["x"]["express"], executor)
        #     y = self.evaluate_expression(key_value_map["y"]["express"], executor)
        #     self.perform_click(click_type, x, y, click_count, duration)
        #     executor.system_variables["$$LastError"] = ""
        #     return
        
        # if exists_image_path:
        #     # 이미지 클릭
        #     image_path = key_value_map["image_path"]["express"]
        #     timeout = key_value_map.get("timeout", {"express": [Token(TokenType.INTEGER, 10)]})["express"]
        #     confidence = key_value_map.get("confidence", {"express": [Token(TokenType.FLOAT, 0.8)]})["express"]
        #     region = key_value_map.get("region", {"express": None})["express"]
        #     grayscale = key_value_map.get("grayscale", {"express": [Token(TokenType.BOOLEAN, False)]})["express"]
            
        #     try:
        #         location = wait_for_image(image_path, timeout, confidence, region, grayscale, executor)
        #         if location:
        #             x, y = pyautogui.center(location)
        #             self.perform_click(click_type, x, y, click_count, duration)
        #             executor.system_variables["$$LastError"] = ""
        #         else:
        #             executor.system_variables["$$LastError"] = "not found"
        #     except Exception as e:
        #         executor.system_variables["$$LastError"] = f"error: {str(e)}"
        #     return
        
        raise KavanaSyntaxError("CLICK 명령어는 좌표(x, y), 이미지(image_path), 또는 객체(Point, Region, Rectangle) 중 하나를 사용해야 합니다.")
