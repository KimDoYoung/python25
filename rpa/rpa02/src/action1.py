from dataclasses import dataclass
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import pyautogui
from image_utils import create_image_with_text
@dataclass
class Region:
    '''이미지 내에서의 위치 정보를 담는 데이터 클래스'''
    x: int
    y: int
    w: int
    h: int

def find_image_at_image(keyImage: Image, targetImage: Image) -> Region:
    '''targetImage 안에서 keyImage가 있는 위치를 찾아서 Region 객체로 반환하는 함수'''
    
    # PIL 이미지를 OpenCV 형식으로 변환
    key_np = np.array(keyImage.convert("RGB"))
    target_np = np.array(targetImage.convert("RGB"))

    key_cv = cv2.cvtColor(key_np, cv2.COLOR_RGB2GRAY)
    target_cv = cv2.cvtColor(target_np, cv2.COLOR_RGB2GRAY)

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(target_cv, key_cv, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 매칭된 위치
    x, y = max_loc
    h, w = key_cv.shape

    return Region(x, y, w, h)

def find_image_in_image(keyImage: Image, targetImage: Image) -> Region:
    '''targetImage에서 keyImage가 있는 위치를 찾아 Region 객체로 반환'''
    try:
        box = pyautogui.locate(keyImage, targetImage, confidence=0.8, grayscale=True)  # 이미지 내에서 찾기
    # box = pyautogui.locate(keyImage, targetImage, confidence=0.6, grayscale=True)  # 이미지 내에서 찾기
    except Exception as e:
        print(e)
        return None
    if box:
        return Region(box.left, box.top, box.width, box.height)
    else:
        return None  # 찾지 못한 경우

# 테스트 예제
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_name = "menu1"
    image_path = os.path.join(script_dir, "../images", f"{target_name}.png")       

    key = "투자정보"
    keyImage = create_image_with_text(key, font_size=11, padding=1)
    save_image_path = os.path.join(script_dir, "../images", f"{key}.png")
    keyImage.save(save_image_path)

    targetImage = Image.open(image_path)

    # region = find_image_at_image(keyImage, targetImage)
    region = find_image_in_image(keyImage, targetImage)
    if region is None:
        print("이미지를 찾을 수 없음")
        exit()
    # 🔥 targetImage에 rectangle 그리기
    target_draw = targetImage.convert("RGB")  # PIL 이미지를 RGB로 변환 (그리기 가능하도록)
    draw = ImageDraw.Draw(target_draw)
    
    # 🔥 빨간색 (red) 테두리 (두께=2)
    draw.rectangle([region.x, region.y, region.x + region.w, region.y + region.h], outline="red", width=2)

    # 🔥 새로운 이미지 파일로 저장
    save_target_path = os.path.join(script_dir, "../images", f"{target_name}_{key}.png")
    target_draw.save(save_target_path)

    print(f"✅ 저장 완료: {save_target_path}")
    print(region)


