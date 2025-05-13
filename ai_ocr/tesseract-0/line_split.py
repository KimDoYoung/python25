import cv2
import numpy as np
import os

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

    # 5. 각 행 이미지 저장
    for idx, (y1, y2) in enumerate(regions):
        line_img = img[y1:y2, :]
        out_path = os.path.join(output_dir, f'line_{idx}.png')
        cv2.imwrite(out_path, line_img)
        print(f'Saved line {idx} to {out_path}')

# 사용 예시
base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
print(f"Base directory is set to: {base_dir}")
image_path = os.path.join(base_dir, f"image_1.png")

split_lines(image_path, output_dir=base_dir)
