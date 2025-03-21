from dataclasses import dataclass
import os
import cv2
import pytesseract
import numpy as np
from PIL import Image

@dataclass
class Region:
    '''이미지 내에서의 위치 정보를 담는 데이터 클래스'''
    x: int
    y: int
    w: int
    h: int

# 🔥 Windows 사용자는 Tesseract 경로 설정 필요
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_text_in_image(text: str, targetImage: Image) -> Region:
    '''targetImage 안에서 특정 텍스트의 위치를 찾아 Region 객체로 반환'''
    
    # OpenCV 형식으로 변환 후 Grayscale 적용
    target_np = np.array(targetImage.convert("L"))  # Grayscale 변환
    target_cv = cv2.threshold(target_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # 🔥 OCR을 이용한 텍스트 탐색 (한글 지원)
    custom_config = r'--oem 3 --psm 6 -l kor'
    data = pytesseract.image_to_data(target_cv, config=custom_config, output_type=pytesseract.Output.DICT)

    # data = pytesseract.image_to_data(target_cv, lang='kor', output_type=pytesseract.Output.DICT)

    # 🔍 찾고자 하는 단어가 OCR 결과에서 있는지 확인
    for i, detected_text in enumerate(data["text"]):
        print(detected_text)
        if text in detected_text:  # OCR 결과에서 부분 일치
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            return Region(x, y, w, h)  # 🔥 찾은 위치 반환

    return None  # 텍스트를 찾지 못한 경우

# ✅ 테스트 실행
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../images", "menu3.png")    
    print(image_path)
    key = "종합미니"  # 🔍 찾고 싶은 텍스트
    targetImage = Image.open(image_path)  # OCR 대상 이미지

    region = find_text_in_image(key, targetImage)
    print(region if region else "텍스트를 찾을 수 없음")
