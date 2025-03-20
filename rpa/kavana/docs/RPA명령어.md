# RPA 명령어

1. APPLICATION
    - APP_OPEN
    - APP_CLOSE
2. WAIT
    - WAIT 3 
    - WAIT UNTIL image_path=<express>, timeout=<express:integer 60>, confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>
3. CLICK
    1 CLICK <express:integer>, <express:integer>
    2 CLICK image_path=<express>  confidence=<express:float 0.8>, region=<express:region default None>, grayscale=<express:boolean>
    3 CLICK <express:point or region or rectange>
  
    > 구분 expression이 1개 이면 3번, expression이 2개이면 1번, key value에 image_path가 있으면 2번 