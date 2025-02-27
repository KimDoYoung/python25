from dataclasses import dataclass
import os
import cv2
import numpy as np
from PIL import Image
import pyautogui

@dataclass
class Region:
    '''이미지 내에서의 위치 정보를 담는 데이터 클래스''' 
    x: int
    y: int
    w: int
    h: int
def find_image_at_image(keyImage: Image, targetImage: Image, method=cv2.TM_CCOEFF_NORMED) -> Region:
    '''targetImage 안에서 keyImage가 있는 위치를 찾아서 Region 객체로 반환하는 함수'''
    
    # PIL 이미지를 OpenCV 형식으로 변환
    key_np = np.array(keyImage.convert("L"))  # Grayscale 변환
    target_np = np.array(targetImage.convert("L"))

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(target_np, key_np, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # 매칭된 위치
    x, y = max_loc
    h, w = keyImage.size  # PIL 이미지의 크기 사용

    return Region(x, y, w, h)

def find_image_in_image(keyImage: Image, targetImage: Image) -> Region:
    '''targetImage에서 keyImage가 있는 위치를 찾아 Region 객체로 반환'''
    
    box = pyautogui.locate(keyImage, targetImage, confidence=0.8, grayscale=True)  # 이미지 내에서 찾기

    if box:
        return Region(box.left, box.top, box.width, box.height)
    else:
        return None  # 찾지 못한 경우

# 테스트 실행
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../images", "help.png")    
    keyImage = Image.open(image_path)

    target_image_path = os.path.join(script_dir, "../images", "menu1.png")    
    targetImage = Image.open(target_image_path  )
    region = find_image_in_image(keyImage, targetImage)
    print(region if region else "이미지를 찾을 수 없음")
