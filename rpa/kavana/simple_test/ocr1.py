from lib.core.managers.ocr_manager import OcrManager

def main():
    image_path = "C:/Users/PC/Pictures/efriend1.png"

    # OCRManager 인스턴스 생성
    ocr = OcrManager(
        command="READ",
        image_path=image_path,
        to_var="result_text",  # 없어도 됨. executor 없으면 무시됨
    )

    # 텍스트 추출 실행
    text = ocr.read()

    print("🔍 추출된 텍스트:")
    print(text)

if __name__ == "__main__":
    main()
