# RPA 명령어

## APP_OPEN

```kvs
SET esafe_path = "C:\\Program Files\\esafe\\esafe.exe"
SET esafe = Application(esafe_path)
RPA APP_OPEN from_var="esafe" maximize=True process_name="esafe"
```

## APP_CLOSE

2. WAIT

   - WAIT 3
   - WAIT UNTIL image_path=<express>, timeout=<express:integer 60>, confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>

3. WAIT_FOR_IMAGE

```kvs
rpa wait_for_image from_file="" area=Region(0,0,100,200), timeout=10, grayscale=False, confidence=0.8
```

4. CLICK_POINT
   - x,y위치를 찾아서 클릭한다.
   - click_type: double|right
   - click_count: 클릭 횟수 default 1
   - duration은 클릭 count가 1이상일 때 유효

```kvs
RPA click_point x=10, y=10 click_count = 2
```

5.  CLICK_IMAGE - 이미지를 찾아서 click한다. - 이미지는 from_var에 있는 이미지나, from_file에서 가져온다. - area는 이미지를 찾을 Region이다 생략시 전체 screen에서 찾는다.
    case "click_image":
    return self.option_map_define(option_defs, "area", "from_var", "from_file","timeout", "grayscale", "confidence")

        2 CLICK image_path=<express>  confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>
        3 CLICK <express:point or region or rectange>

        > 구분 expression이 1개 이면 3번, expression이 2개이면 1번, key value에 image_path가 있으면 2번
        1. click x=10, y=10, type="double|right" count=3,
        2. click area=Region(10,10,100,200), click_type= count
        3. click from_file="a.png", grayscale=, confidence type count

6.  MOUSE_MOVE
    1. relative 를 추가하다.
    2. x,y, relative
7.  KEY_IN
    KEY_IN [<express:string>, <express:string>..], speed=<express:float, default=0.5>
    example: KEY_IN ["enter", "space", "ctrl+c"]

8.  PUT_TEXT

    - PUT_TEXT <express:string>
    - GET_TEXT VAR_TO=<var:string> clipboard=true

9.  GET_TEXT

    - GET_TEXT to_var="var1" clipboard=true
    -

10. CAPTURE : 모니터의 screen을 캡쳐한다.
    - CAPTURE to_file or to_var 전체 화면을 to_var의 값을 변수명으로 이미지저장
    - CAPTURE area=<region:express>, to_file or to_var area부분을 clip해서 파일이나 to_var에 저장
    -

```kavana-script
CLICK 100, 200  // 기본 클릭
CLICK 100, 200, type="double"  // 더블 클릭
CLICK 100, 200, type="right"  // 우클릭
CLICK image_path="button.png", type="middle"  // 이미지에서 가운데 버튼 클릭
CLICK myRegion, type="triple"  // 영역 내 트리플 클릭
CLICK x=200, y=300, type="drag"  // 드래그 시작
CLICK x=250, y=350, type="drop"  // 드래그 끝 (드롭)
CLICK x=150, y=250, type="hold", duration=2  // 2초간 길게 누름
CLICK x=150, y=250, type="release"  // 길게 누름 해제
```

express_count = self.count_express(args)
exists_x = self.is_key_exists(args,"x")
exists_type = self.is_key_exists(args,"type")
exists_image_path = self.is_key_exists(args,"image_path")

express_count == 2 : CLICK 100, 200 // 기본 클릭
express_count == 3 and exists_type == true : CLICK 100, 200, type="double" // 더블 클릭

exists_image_path == true : CLICK image_path="button.png", type="middle" // 이미지에서 가운데 버튼 클릭
express_count == 1 : CLICK myRegion
express_count == 2 and exists_type == true : CLICK myRegion, type="triple" // 영역 내 트리플 클릭
exists_x == true CLICK x=200, y=300, type="drag" // 드래그 시작
CLICK x=250, y=350, type="drop" // 드래그 끝 (드롭)
CLICK x=150, y=250, type="hold", duration=2 // 2초간 길게 누름
CLICK x=150, y=250, type="release" // 길게 누름 해제

```python
import copy
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaRpaError
from lib.core.managers.rpa_manager import RpaManager
from lib.core.token import Token
from lib.core.token_type import TokenType

class RpaCommand(BaseCommand):
    """RPA 명령어 해석 및 실행"""

    OPTION_DEFINITIONS = {
        "from_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "maximize": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "process_name": {"required": False, "allowed_types": [TokenType.STRING]},
        "seconds": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "from_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "grayscale": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "confidence": {"default": 0.8, "allowed_types": [TokenType.FLOAT]},
        "area": {"required": False, "allowed_types": [TokenType.REGION]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "x": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "y": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "click_type": {"default": 'left', "allowed_types": [TokenType.STRING]},
        "click_count": {"default": 1, "allowed_types": [TokenType.INTEGER]},
        "duration": {"default": 0.2, "allowed_types": [TokenType.FLOAT]},
        "relative": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
        "keys": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "speed": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "strip": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "wait_before": {"default": 0.5, "allowed_types": [TokenType.FLOAT]},
        "text": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    COMMAND_OPTION_MAP = {
        "app_open": {
            "keys": ["from_var", "maximize", "process_name"]
        },
        "app_close": {
            "keys": ["from_var"],
            "overrides": {
                "from_var": {"required": True}
            }
        },
        "wait": {
            "keys": ["seconds"],
            "overrides": {
                "seconds": {"required": True}
            }
        },
        "wait_for_image": {
            "keys": ["area", "from_var", "from_file", "timeout", "grayscale", "confidence"]
        },
        "click_point": {
            "keys": ["x", "y", "click_type", "click_count", "duration"],
            "overrides": {
                "x": {"required": True},
                "y": {"required": True}
            }
        },
        "click_image": {
            "keys": ["area", "from_var", "from_file", "timeout", "grayscale", "confidence"]
        },
        "mouse_move": {
            "keys": ["x", "y", "duration", "relative"]
        },
        "key_in": {
            "keys": ["keys", "speed"],
            "overrides": {
                "keys": {"required": True}
            }
        },
        "put_text": {
            "keys": ["text"],
            "overrides": {
                "text": {"required": True}
            }
        },
        "get_text": {
            "keys": ["to_var", "strip", "wait_before"]
        },
        "capture": {
            "keys": ["area", "to_var", "to_file"]
        }
    }

    RPA_RULES = {
        "wait": {
            "mutually_exclusive": [["select", "seconds"]],
            "required_together": []
        }
    }

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaRpaError("RPA 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map = self._get_option_definitions(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_command_rules(self.RPA_RULES, sub_command, option_values)

        try:
            manager = RpaManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
        except KavanaRpaError as e:
            raise KavanaRpaError(f"RPA `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

    def _get_option_definitions(self, sub_command: str) -> dict:
        config = self.COMMAND_OPTION_MAP.get(sub_command)
        if not config:
            raise KavanaRpaError(f"지원하지 않는 RPA sub_command: {sub_command}")

        keys = config.get("keys", [])
        overrides = config.get("overrides", {})

        base_defs = copy.deepcopy(self.OPTION_DEFINITIONS)
        result = {}

        for key in keys:
            if key not in base_defs:
                raise KavanaRpaError(f"{sub_command} 명령어에 정의되지 않은 옵션: {key}")
            result[key] = {**base_defs[key], **overrides.get(key, {})}

        return result

```
