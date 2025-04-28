import easyocr
import os
import cv2
import numpy as np
# 1. EasyOCR 리더 객체 생성 (한국어+영어 지원)
reader = easyocr.Reader(['ko', 'en'])

# 2. 이미지 파일 경로 설정
base_img_path = r"C:\Users\PC\Pictures\efreind_uhd_175\source"
image_filename = "인증서선택.png"
img_path = os.path.join(base_img_path, image_filename)
img_array = np.fromfile(img_path, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
results = reader.readtext(img)

# 5. 결과 출력
# 결과 출력
print("=" * 50)
for bbox, text, confidence in results:

    # 좌표 계산
    x_min = int(min(point[0] for point in bbox))
    y_min = int(min(point[1] for point in bbox))
    x_max = int(max(point[0] for point in bbox))
    y_max = int(max(point[1] for point in bbox))

    width = x_max - x_min
    height = y_max - y_min

    print(f"텍스트: {text}, 신뢰도:{confidence:.2f},  Region (x, y, width, height): ({x_min}, {y_min}, {width}, {height})")
print("=" * 50)
