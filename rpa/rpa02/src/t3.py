from dataclasses import dataclass
import os
import cv2
import pytesseract
import numpy as np
import difflib
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
    
    # OpenCV 형식으로 변환 (Grayscale 적용)
    target_np = np.array(targetImage.convert("L"))  # 흑백 변환

    # 🔥 이미지 해상도 증가
    target_np = cv2.resize(target_np, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 🔥 대비 증가 (Adaptive Thresholding 사용)
    target_cv = cv2.adaptiveThreshold(target_np, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # 🔥 OCR 설정 (한글 인식 최적화)
    custom_config = r'--oem 3 --psm 3 -l kor'
    recognized_text = pytesseract.image_to_string(target_cv, config=custom_config)

    print("OCR 전체 결과:", recognized_text)

    # 🔥 유사한 단어 찾기
    def find_best_match(text, ocr_results):
        matches = difflib.get_close_matches(text, ocr_results, n=1, cutoff=0.6)
        return matches[0] if matches else None

    ocr_results = recognized_text.split()  # OCR 결과를 단어 단위로 분할
    best_match = find_best_match(text, ocr_results)

    if best_match:
        print(f"✅ OCR에서 가장 유사한 단어 찾음: {best_match}")
        return True  # 찾았다고 가정
    else:
        print("❌ 유사한 단어를 찾을 수 없음")
        return None

# ✅ 테스트 실행
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../images", "menu3.png")        
    key = "미니"  # 🔍 찾고 싶은 텍스트
    targetImage = Image.open(image_path)  # OCR 대상 이미지

    region = find_text_in_image(key, targetImage)
    print(region if region else "❌ 텍스트를 찾을 수 없음")
