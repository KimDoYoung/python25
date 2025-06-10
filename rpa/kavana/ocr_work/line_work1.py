# line_work1.py
"""
모듈 설명: 
    - HTS 박스형태의 데이터를 줄 단위로 OCR 처리하는 스크립트입니다.
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2025-06-10
버전: 1.0
"""
import cv2
import pytesseract
from pytesseract import Output
import os

# 사용자 사진 폴더 경로 지정
user_photo_dir = os.path.expanduser('~/Pictures')

# 이미지 불러오기
imgpath = os.path.join(user_photo_dir, '1.png')
if not os.path.exists(imgpath):
    raise FileNotFoundError(f"Image not found at {imgpath}")
image = cv2.imread(imgpath)

# 그레이스케일 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이진화로 텍스트 강조
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 텍스트 줄 영역 찾기 (수평 projection)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (image.shape[1]//2, 1))
dilated = cv2.dilate(thresh, kernel, iterations=1)

# 줄 단위로 bounding box 추출
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# y좌표로 정렬
contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

# 각 줄 이미지로 자르고 OCR 수행
for i, c in enumerate(contours):
    x, y, w, h = cv2.boundingRect(c)
    line_img = image[y:y+h, x:x+w]
    text = pytesseract.image_to_string(line_img, config='--psm 6 --oem 3 -l kor+eng')  # 한 줄 단위 PSM
    print(f"Line {i+1}: {text.strip()}")
