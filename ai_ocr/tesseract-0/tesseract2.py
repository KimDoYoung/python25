import os

import pytesseract
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def main():
    base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
    print(f"Base directory is set to: {base_dir}")
    image_path = os.path.join(base_dir, f"image_a.png")

    # config = '--oem 3 --psm 3 -l kor+eng'
    # config = '--oem 3 --psm 6 -l kor'
    config = '--oem 3 --psm 7 -l kor'
    text = pytesseract.image_to_string(image_path, config=config)
    print("-" * 30)
    print(f"{image_path} OCR result:")
    print(text)
    print("-" * 30)

if __name__ == "__main__":
    main()
