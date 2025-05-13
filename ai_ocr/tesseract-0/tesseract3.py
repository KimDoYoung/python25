import os

import cv2
import pytesseract
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
# 실행파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Tesseract 명령어 커스텀 (언어 데이터 경로 포함)
config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --oem 3 --psm 6 -l kor'

def main():
    base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
    print(f"Base directory is set to: {base_dir}")
    # image_path = os.path.join(base_dir, f"인증서.png")
    image_path = os.path.join(base_dir, f"image_1.png")

    # image = Image.open(image_path)

    # OCR 결과를 pandas-like 구조로 가져오기
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]
    data = pytesseract.image_to_data(img,  lang='kor', output_type=pytesseract.Output.DICT)

    target = "김도영"
    positions = []

    # 각 단어별로 확인
    for i, word in enumerate(data['text']):
        print(f"Word: {word}, Confidence: {data['conf'][i]}")
        if target in word:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            positions.append((x, y, w, h))

    print("찾은 위치들:", positions)

    # config = '--oem 3 --psm 3 -l kor+eng'
    # config = '--oem 3 --psm 6 -l kor'
    # config = '--oem 3 --psm 3 -l kor'
    # text = pytesseract.image_to_string(image_path, config=config)
    # print("-" * 30)
    # print(f"{image_path} OCR result:")
    # print(text)
    # print("-" * 30)

if __name__ == "__main__":
    main()
