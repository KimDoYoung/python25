import os
import cv2
import easyocr

def main():
    print("EasyOCR started.")
    base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
    reader = easyocr.Reader(['ko','en'], gpu=False)

    img_path = os.path.join(base_dir, 'image_0.png')
    # 이미지 불러오기 (흑백)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # 크기 확대
    img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

    # 이진화 (흑백 반전 포함)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 저장해서 확인
    cv2.imwrite('preprocessed_zero.png', img)

    # EasyOCR 처리
    reader = easyocr.Reader(['en'])  # 숫자만이라면 영어로도 충분
    results = reader.readtext(img)
    print("-----------------------------------------------------")
    print(results)
    print("-----------------------------------------------------")


if __name__ == "__main__":
    main()
