from lib.core.commands.base_command import BaseCommand
from lib.core.token import Token


class AppOpenCommand(BaseCommand):
    def execute(self, args: list[Token], executor):
        """
        CLICK <x: int>, <y: int>
        CLICK image_path=<express> confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>, type=<express:string "single">
        CLICK <object: Point | Region | Rectangle>
        """
        express_count = self.count_express(args)
        exists_x = self.is_key_exists(args, "x")
        exists_type = self.is_key_exists(args, "type")
        exists_image_path = self.is_key_exists(args, "image_path")
        
        i = 0
        if express_count == 2:
            # 기본 좌표 클릭
            i, express1 = self.get_express(args, i)
            i, express2 = self.get_express(args, i)
            x = self.evaluate_expression(express1, executor)
            y = self.evaluate_expression(express2, executor)
            click_type = "single"
            pyautogui.click(x, y)
            executor.system_variables["$$LastError"] = ""
            return
        
        if express_count == 3 and exists_type:
            # 좌표 클릭 + type 옵션 (예: 더블 클릭)
            i, express1 = self.get_express(args, i)
            i, express2 = self.get_express(args, i)
            i, express3 = self.get_express(args, i)
            x = self.evaluate_expression(express1, executor)
            y = self.evaluate_expression(express2, executor)
            click_type = self.evaluate_expression(express3, executor)
            self.perform_click(click_type, x, y)
            executor.system_variables["$$LastError"] = ""
            return
        
        if exists_image_path:
            # 이미지 클릭
            key_value_map = {}
            i = 0
            while i < len(args):
                key_token, express_tokens, next_index = self.extract_command_option(args, i)
                if key_token is None:
                    break
                key = key_token.data.string.strip().lower()
                key_value_map[key] = self.evaluate_expression(express_tokens, executor)
                i = next_index
            
            image_path = key_value_map["image_path"]
            timeout = key_value_map.get("timeout", 10)
            confidence = key_value_map.get("confidence", 0.8)
            region = key_value_map.get("region", None)
            grayscale = key_value_map.get("grayscale", False)
            click_type = key_value_map.get("type", "single").lower()
            
            try:
                location = wait_for_image(image_path, timeout, confidence, region, grayscale, executor)
                if location:
                    x, y = pyautogui.center(location)
                    self.perform_click(click_type, x, y)
                    executor.system_variables["$$LastError"] = ""
                else:
                    executor.system_variables["$$LastError"] = "not found"
            except Exception as e:
                executor.system_variables["$$LastError"] = f"error: {str(e)}"
            return
        
        if express_count == 1:
            # 객체 클릭 (Point, Region, Rectangle)
            i, express1 = self.get_express(args, i)
            obj = self.evaluate_expression(express1, executor)
            if isinstance(obj, Point):
                x, y = obj.x, obj.y
            elif isinstance(obj, Region) or isinstance(obj, Rectangle):
                x = obj.x + obj.width // 2
                y = obj.y + obj.height // 2
            click_type = "single"
            self.perform_click(click_type, x, y)
            executor.system_variables["$$LastError"] = ""
            return
        
        if express_count == 2 and exists_type:
            # 객체 클릭 + type 옵션
            i, express1 = self.get_express(args, i)
            i, express2 = self.get_express(args, i)
            obj = self.evaluate_expression(express1, executor)
            click_type = self.evaluate_expression(express2, executor)
            if isinstance(obj, Point):
                x, y = obj.x, obj.y
            elif isinstance(obj, Region) or isinstance(obj, Rectangle):
                x = obj.x + obj.width // 2
                y = obj.y + obj.height // 2
            self.perform_click(click_type, x, y)
            executor.system_variables["$$LastError"] = ""
            return
        
        if exists_x:
            # 키워드 인자 기반 클릭 (예: 드래그, 드롭, 홀드, 릴리즈)
            key_value_map = {}
            i = 0
            while i < len(args):
                key_token, express_tokens, next_index = self.extract_command_option(args, i)
                if key_token is None:
                    break
                key = key_token.data.string.strip().lower()
                key_value_map[key] = self.evaluate_expression(express_tokens, executor)
                i = next_index
            
            x = key_value_map["x"]
            y = key_value_map["y"]
            click_type = key_value_map.get("type", "single").lower()
            self.perform_click(click_type, x, y, key_value_map)
            executor.system_variables["$$LastError"] = ""
            return
        
        raise KavanaSyntaxError("CLICK 명령어는 좌표(x, y), 이미지(image_path), 또는 객체(Point, Region, Rectangle) 중 하나를 사용해야 합니다.")
