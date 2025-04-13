# RPA 명령어

1. APPLICATION
    - APP_OPEN
    - APP_CLOSE
```kvs
SET esafe = Application(esafe_path)
RPA app_open from_var="esafe"  maximize=False, process_name=process_name
```
2. WAIT
    - WAIT 3
    - WAIT UNTIL image_path=<express>, timeout=<express:integer 60>, confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>

3. WAIT_FOR_IMAGE
```kvs
rpa wait_for_image from_file="" area=Region(0,0,100,200), timeout=10, grayscale=False, confidence=0.8
```
3. CLICK
    1 CLICK <express:integer>, <express:integer>, click_type="double|right"
    2 CLICK image_path=<express>  confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>
    3 CLICK <express:point or region or rectange>
  
    > 구분 expression이 1개 이면 3번, expression이 2개이면 1번, key value에 image_path가 있으면 2번
    1. click x=10, y=10, type="double|right" count=3, 
    2. click area=Region(10,10,100,200), click_type= count
    3. click from_file="a.png", grayscale=, confidence type count

4. MOUSE_MOVE
5. KEY_IN
    KEY_IN [<express:string>, <express:string>..], speed=<express:float, default=0.5>
    example: KEY_IN ["enter", "space", "ctrl+c"]

6. PUT_TEXT
    - PUT_TEXT <express:string>
    - GET_TEXT  VAR_TO=<var:string> clipboard=true

    
7. CAPTURE : 모니터의 screen을 캡쳐한다.
    - CAPTURE
    - CAPTURE <region:express>, SAVE_TO=<path :express>, VAR_TO <string>
    - CAPTURE <rectangle:express>, SAVE_TO <path :express> VAR_TO <string>
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

express_count == 2 : CLICK 100, 200  // 기본 클릭
express_count == 3 and exists_type == true : CLICK 100, 200, type="double"  // 더블 클릭

exists_image_path == true : CLICK image_path="button.png", type="middle"  // 이미지에서 가운데 버튼 클릭
express_count == 1 : CLICK myRegion
express_count == 2 and exists_type == true : CLICK myRegion, type="triple"  // 영역 내 트리플 클릭
exists_x == true CLICK x=200, y=300, type="drag"  // 드래그 시작
CLICK x=250, y=350, type="drop"  // 드래그 끝 (드롭)
CLICK x=150, y=250, type="hold", duration=2  // 2초간 길게 누름
CLICK x=150, y=250, type="release"  // 길게 누름 해제


