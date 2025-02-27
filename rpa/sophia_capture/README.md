# sophia_capture

## 프롬프트

근래 RPA 프로그램을 주로 개발하는데,
주로 pyautogui를 사용하고 있음.
그런데 이미지 유틸리티가 필요하지 않나 생각이 듬, GUI프로그램임

주요 기능은 다음과 같음
대상 프로그램의 화면캡쳐를 한 후 저장된 이미지 -> batang.png 이 있다고 가정

gui
1. top menu : file  open
2. toolbar : thumb-buttons
3. main : image영역과 정보영역으로 7:3의 비율을 갖음, 정보영역은 text표시할 수 있으면 됨
4. status bar : 하단에 간단정보표시

기능
1. batang.png을 open (이미지 open)-> 이미지가 화면에 나옴. scrollbar로 이미지 안보이는 부분 이동.
2. zoomin button클릭->화면커짐. 
3. 1:1버튼 클릭 ->원래 이미지 크기로 돌아옴.
4. rectangle버튼 클릭, rectangle_ capture상태가 됨
5. rectangle_capture상태에서 마우스 클릭 후 드래그 후 마우스 up 시 선택된 rectangle(region) 을 정보영역에 표시
6. retangle_capture버튼 클릭 -> rectangle_capture  toggle
7. image_capture 버튼클릭 , image_cpautre 상태가 됨
8. image_capture 상태에서  우스 클릭 후 드래그 후 마우스 up 시 선택된 영역의 이미지를 저장 (이름은 자동으로 숫자증가 예를 들어 image_1.png, image_2.png식으로
9. image_capture 버튼 클릭 -> image_capture상태 toggle


1. 요구조건 1
    status영역을 3부분으로 나누어서
    1. 마우스의 x, y표시
    2. 현재의 상태 즉 rectangle capture on 또는 image capture on을 표시, 물론 아무 상태도 아니면 비어 있게금.
    3. 메세지 표시

2. 요구조건2
    - 정보영역의 넓기가 너무 작음 지금 사이즈의 2배로
    
3. 요구조건3
    -  rectangle_capture on 또는 image_capture on일때 rubber band형식으로 점선으로 표시해 줄 수 없나?
    

요구조건 1
File
    Open
    --------
    Config
    --------
    Quit(alt+f4)

요구조건 2
-Config menu click시 modal로 환경설정 모달창 뜰 것
-config-modal에서
-이미지 저장위치를 설정하게 할 것 
-default 이미지 저장장치는 실행위치아래 images폴더를 만들것


1. 이미지 저장시 -> 정보영역에 'image_0.png' saved 표시
2. 초기상태 maxize
3. rectange_capture on 하면 image_catpure off  반대로 image_capture on 이면 rectange_capture off
4. 정보영역 font 더 크게