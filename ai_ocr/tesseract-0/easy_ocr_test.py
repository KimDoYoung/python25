import os
import cv2
import easyocr

def main():
    print("EasyOCR started.")
    base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
    reader = easyocr.Reader(['ko','en'], gpu=False)

    for no in range(0, 7):
        image_path = os.path.join(base_dir, f"image_{no}.png")
        if not os.path.exists(image_path):
            print(f"File {image_path} does not exist.")
            exit(1)

        print("-" * 30)
        print(f"{image_path} OCR result:")
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        temp_image_path = os.path.join(base_dir, f"temp_image_{no}.png")
        cv2.imwrite(temp_image_path, img)        
        image_path = temp_image_path

        results = reader.readtext(image_path)

        for result in results:
            if len(result) == 3:
                bbox, text, confidence = result
                print(f"텍스트: {text}, 신뢰도: {confidence:.2f}, 위치: {bbox}")
            else:
                print(f"⚠️ 잘못된 결과 형식: {result}")

        print("-" * 30)

if __name__ == "__main__":
    main()
