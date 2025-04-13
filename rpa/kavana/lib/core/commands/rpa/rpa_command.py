import copy
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaRpaError
from lib.core.managers.rpa_manager import RpaManager
from lib.core.token import Token
from lib.core.token_type import TokenType

class RpaCommand(BaseCommand):
    ''' RPA 명령어 해석 및 실행 '''

    RPA_RULES = {
        "url": {
            "mutually_exclusive": [  # 서로 동시에 존재하면 안 되는 파라미터들
                # ["from_file", "from_var"],
            ],
            "required_together": [  # 함께 있어야만 유효한 조합
                # ["width", "height"]
            ]
        },
        "wait": {
            "mutually_exclusive": [
                ["select", "seconds"],
            ],
            "required_together": [
                # ["width", "height"]
            ]
        },
    }

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaRpaError("RPA 명령어는 최소 하나 이상의 인자가 필요합니다.")
        
        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_command_rules(self.RPA_RULES, sub_command, option_values)
        try:
            RPA_manager = RpaManager(command=sub_command,**option_values, executor=executor)
            RPA_manager.execute()
        except KavanaRpaError as e:
            raise KavanaRpaError(f"RPA `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

    OPTION_DEFINITIONS = {
        #-----RPA open
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "maximize": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "process_name": {"required": False, "allowed_types": [TokenType.STRING]},
        #-----RPA wait
        "seconds": {"required": True, "allowed_types": [TokenType.INTEGER]},
        #--------RPA wait for image
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        
        "grayscale": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "confidence": {"default": 0.8, "allowed_types": [TokenType.FLOAT]},
        "area" : {"required": False, "allowed_types": [TokenType.REGION]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        #-----RPA click
        "x": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "y": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "click_type": {"required": False, "allowed_types": [TokenType.STRING]},
        "click_count": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "duration": {"required": False, "allowed_types": [TokenType.FLOAT]},

        #-----RPA key_in
        "keys": {"required": True, "allowed_types": [TokenType.ARRAY]},
        "speed": {"required": False, "allowed_types": [TokenType.FLOAT]},

    }
#rpa wait_for_image from_file="" area=Region(0,0,100,200), timeout=10, grayscale=False, confidence=0.8
    def option_map_define(self, option_defs:dict,  *keys):
        return {k: option_defs[k] for k in keys if k in option_defs}

    def get_option_map(self, sub_command: str) -> dict:
        # 원본 옵션 정의 복사
        option_defs = copy.deepcopy(self.OPTION_DEFINITIONS)        
        match sub_command:
            case "app_open":
                return self.option_map_define(option_defs, "from_var", "maximize", "process_name")
            case "app_close":
                return self.option_map_define(option_defs, "from_var")
            
            case "wait":
                return self.option_map_define(option_defs, "select", "select_by", "within", "attr", "to_var")        

            case "wait_for_image":
                return self.option_map_define(option_defs, "area", "from_var", "from_file","timeout", "grayscale", "confidence")
            
            case "click_point":
                return self.option_map_define(option_defs, "x", "y", "click_type", "click_count", "duration","area", "from_var", "from_file","timeout", "grayscale", "confidence") 

            case "click_image":
                return self.option_map_define(option_defs, "area", "from_var", "from_file","timeout", "grayscale", "confidence")
            
            case "click_region":
                return self.option_map_define(option_defs, "area", "from_var", "from_file","timeout", "grayscale", "confidence")
            
            case "mouse_move":
                return self.option_map_define(option_defs, "x", "y", "duration")
            
            case "key_in":
                return self.option_map_define(option_defs, "keys", "speed")

            case "put_text":
                return self.option_map_define(option_defs, "text")
            
            case "get_text":
                return self.option_map_define(option_defs, "to_var")
            
            case "capture":
                return self.option_map_define(option_defs, "area", "to_var", "to_file")

            case _:
                raise KavanaRpaError(f"지원하지 않는 RPA sub_command: {sub_command}")
