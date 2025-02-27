import cv2
import numpy as np
from PIL import Image
import pyautogui
from lib.core.datatypes.region import Region
from lib.actions.image_utils import create_image_with_text

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
    # key = "추정자산"
    # keyImage = create_image_with_text(key, font_size=12, padding=1)
    # keyImage = keyImage.convert("L") 
    # keyImage.save(f"{key}.png")

    # targetImage = Image.open("한국투자증권화면1.png")
    
    # region = find_image_in_image(keyImage, targetImage)
    # print(region if region else "이미지를 찾을 수 없음")
    keyImage = Image.open("2.png")
    targetImage = Image.open("한국투자증권화면1.png")
    region = find_image_in_image(keyImage, targetImage)
    print(region if region else "이미지를 찾을 수 없음")
