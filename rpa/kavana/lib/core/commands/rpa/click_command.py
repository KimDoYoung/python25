import pyautogui
from lib.actions.actions import wait_for_image
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RpaManager
from lib.core.token import Token
from lib.core.token_type import TokenType

class ClickCommand(BaseCommand):
    def execute(self, args, executor):
        """
        CLICK 10, 20 [count=1] [duration=0.2] [type="single"]
        CLICK <x: int>, <y: int> [count=1] [duration=0.2] [type="single"]
        CLICK image_path=<express> confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>, type=<express:string "single">
        CLICK <object: Point | Region | Rectangle> point_name=<express:string "center"> [count=1] [duration=0.2] [type="single"]
        """
        option_map = {
            "count": {"default": 1, "allowed_types": [TokenType.INTEGER]},
            "duration": {"default": 0.2, "allowed_types": [TokenType.FLOAT]},
            "type": {"default": "single", "allowed_types": [TokenType.STRING]},
        }
        
        # 옵션 값 초기화
        option_values = {key: option_map[key].get("default", None) for key in option_map}        
        rpa_manager = RpaManager(executor=executor)
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
                for key, value_dict in options.items():
                    value_express = value_dict["express"]
                    if key in option_values:    
                        option_values[key] = ExprEvaluator(executor=executor).evaluate(value_express).data.value
            rpa_manager.click(x=x, y=y, click_type=option_values["type"], click_count=option_values["count"], duration=option_values["duration"])
            return
        if self.is_key_exists(args, "x"):
            option_map["x"] = { "required": True,"allowed_types": [TokenType.INTEGER] }
            option_map["y"] = { "required": True,"allowed_types": [TokenType.INTEGER] }
            options, i = self.extract_all_options(args, 0) # options 추출
            option_values = self.parse_and_validate_options(options, option_map, executor)
            rpa_manager.click(x=option_values["x"], y=option_values["y"], 
                            click_type=option_values["type"], click_count=option_values["count"], duration=option_values["duration"])
            return
        if self.is_key_exists(args, "image_path"):
            option_map["image_path"] = { "required": True,"allowed_types": [TokenType.STRING] }
            option_map["confidence"] = { "default": 0.8,"allowed_types": [TokenType.FLOAT] }
            option_map["search_region"] = { "default": None,"allowed_types": [TokenType.REGION, TokenType.NONE] }
            option_map["grayscale"] = { "default": False,"allowed_types": [TokenType.BOOLEAN] }
            option_map["point_name"] = { "default": "center","allowed_types": [TokenType.STRING] }
            options, i = self.extract_all_options(args, 0)
            option_values = self.parse_and_validate_options(options, option_map, executor)
            image_path = option_values["image_path"]
            point_name = option_values["point_name"]
            image_region = rpa_manager.find_image(image_path, search_region=option_values["search_region"])
            if image_region:
                x, y = rpa_manager.get_point_with_name(image_region, point_name)
                rpa_manager.click(x=x,y=y,click_type=option_values["type"], click_count=option_values["count"], duration=option_values["duration"])
            else:
                executor.set_last_error(f"NotFound")
            return
        # 첫번째 express를 해석해본다.
        express, i = self.get_express(args,0)
        first_token = ExprEvaluator(executor=executor).evaluate(express)

        if first_token.type in { TokenType.RECTANGLE, TokenType.REGION, TokenType.POINT }:
            x:int = 0
            y:int = 0
            if first_token.type == TokenType.POINT:
                x = first_token.data.get_x()
                y = first_token.data.get_y()
                options, i = self.extract_all_options(args, i)
                option_values = self.parse_and_validate_options(options, option_map, executor)
            elif first_token.type == TokenType.REGION:
                option_map["point_name"] = { "default": "center","allowed_types": [TokenType.STRING] }
                options, i = self.extract_all_options(args, i)
                option_values = self.parse_and_validate_options(options, option_map, executor)
                point_name = option_values["point_name"]
                x, y = rpa_manager.get_point_with_name(first_token.data, point_name)
            elif first_token.type == TokenType.RECTANGLE:
                option_map["point_name"] = { "default": "center","allowed_types": [TokenType.STRING] }
                options, i = self.extract_all_options(args, i)
                option_values = self.parse_and_validate_options(options, option_map, executor)
                point_name = option_values["point_name"]
                x, y = rpa_manager.get_point_with_name(first_token.data.to_region(), point_name)
            else:
                raise KavanaSyntaxError("CLICK 명령어는 좌표(x, y), 이미지(image_path), 또는 객체(Point, Region, Rectangle) 중 하나를 사용해야 합니다.")

            rpa_manager.click(x=x,y=y,click_type=option_values["type"], click_count=option_values["count"], duration=option_values["duration"])
            return
        
        raise KavanaSyntaxError("CLICK 명령어는 좌표(x, y), 이미지(image_path), 또는 객체(Point, Region, Rectangle) 중 하나를 사용해야 합니다.")
