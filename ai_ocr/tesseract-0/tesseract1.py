import os

import pytesseract
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def main():
    base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
    print(f"Base directory is set to: {base_dir}")

    # config = '--oem 3 --psm 3 -l kor+eng'
    # config = '--oem 3 --psm 3 -l kor'
    config = '--oem 1 --psm 4 -l kor'
    for no in range(0, 7):
        image_path = os.path.join(base_dir, f"image_{no}.png")
        if not os.path.exists(image_path):
            print(f"File {image_path} does not exist.")
            exit(1)
        with Image.open(image_path) as img:
            width, height = img.size
            resized_img = img.resize((int(width * 1.5), int(height * 1.5)))
            temp_image_path = os.path.join(base_dir, f"temp_image_{no}.png")
            resized_img.save(temp_image_path)
            image_path = temp_image_path
        text = pytesseract.image_to_string(image_path, config=config)
        print("-" * 30)
        print(f"{image_path} OCR result:")
        print(text)
        print("-" * 30)
    print("Tesseract OCR completed.")
    print("==" * 30)

if __name__ == "__main__":
    main()
