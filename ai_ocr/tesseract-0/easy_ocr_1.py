import os
import cv2
import easyocr

def main():
    print("EasyOCR started.")
    base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
    reader = easyocr.Reader(['ko','en'], gpu=False)
    no = "00"
    image_path = os.path.join(base_dir, f"image_{no}.png")

    results = reader.readtext(image_path, paragraph=False)

    for result in results:
        if len(result) == 3:
            bbox, text, confidence = result
            print(f"텍스트: {text}, 신뢰도: {confidence:.2f}, 위치: {bbox}")
        else:
            print(f"⚠️ 잘못된 결과 형식: {result}")

    print("-" * 30)

if __name__ == "__main__":
    main()
