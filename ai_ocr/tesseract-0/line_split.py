import cv2
import numpy as np
import os

import pytesseract

def split_lines(image_path, output_dir='lines'):
    os.makedirs(output_dir, exist_ok=True)

    # 1. 이미지 불러오기
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 이진화
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3. 수평 projection (행 기준 픽셀 합)
    hist = np.sum(binary, axis=1)

    # 4. y영역 찾기
    threshold = 10  # 글자 존재 판단 기준
    in_text = False
    y_start = 0
    regions = []

    for i, val in enumerate(hist):
        if not in_text and val > threshold:
            in_text = True
            y_start = i
        elif in_text and val <= threshold:
            in_text = False
            y_end = i
            if y_end - y_start > 5:  # 최소 높이 필터링
                regions.append((y_start, y_end))

    config = '--oem 3 --psm 7 -l kor'
    # 5. 각 행 이미지 저장
    # for idx, (y1, y2) in enumerate(regions):
    #     line_img = img[y1:y2, :]
    #     out_path = os.path.join(output_dir, f'line_{idx}.png')
        # line_img 좀더 ocr에 맞게 확대도 2배로 하고 grayscale로 변환
        # line_img = cv2.resize(line_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # line_img = cv2.cvtColor(line_img, cv2.COLOR_BGR2GRAY)
        # line_img = cv2.GaussianBlur(line_img, (5, 5), 0)

        # cv2.imwrite(out_path, line_img)
        # text = pytesseract.image_to_string(out_path, config=config)
        # print(f"이미지: {out_path}, 뽑은 텍스트:{text.strip()}")

    padding = 5  # 위아래 여백 (픽셀 단위)

    for idx, (y1, y2) in enumerate(regions):
        # 여백을 줄 때 이미지 경계 밖으로 벗어나지 않도록 클리핑
        y1_pad = max(y1 - padding, 0)
        y2_pad = min(y2 + padding, img.shape[0])

        line_img = img[y1_pad:y2_pad, :]
        out_path = os.path.join(output_dir, f'line_{idx}.png')

        # OCR 정확도 개선을 위해 확대, 전처리 적용 가능
        # line_img = cv2.resize(line_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # line_img = cv2.cvtColor(line_img, cv2.COLOR_BGR2GRAY)
        # line_img = cv2.GaussianBlur(line_img, (5, 5), 0)

        cv2.imwrite(out_path, line_img)
        text = pytesseract.image_to_string(out_path, config=config)
        print(f"이미지: {out_path}, 뽑은 텍스트:{text.strip()}")        

# 사용 예시
base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
print(f"Base directory is set to: {base_dir}")
image_path = os.path.join(base_dir, f"image_1.png")
output_dir = os.path.join(base_dir, "lines")
split_lines(image_path, output_dir=output_dir)

    # config = '--oem 3 --psm 7 -l kor'
    # text = pytesseract.image_to_string(image_path, config=config)
    # print("-" * 30)
    # print(f"{image_path} OCR result:")
    # print(text)