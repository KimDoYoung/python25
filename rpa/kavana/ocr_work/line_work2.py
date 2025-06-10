import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import pandas as pd
from typing import List, Tuple, Dict

class FinancialOCRParser:
    def __init__(self):
        # Tesseract 설정 (한국어 + 영어)
        self.config = '--oem 3 --psm 6 -l kor+eng'
        # 숫자 전용 설정
        self.number_config = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789,.'
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """이미지 전처리"""
        # 이미지 읽기
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")
        
        # 그레이스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 이진화
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def detect_text_lines(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """텍스트 라인 영역 감지"""
        # 수평 커널로 텍스트 라인 감지
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        dilated = cv2.dilate(image, kernel, iterations=1)
        
        # 컨투어 찾기
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 바운딩 박스 추출 및 정렬
        boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # 너무 작은 영역 제외
            if w > 50 and h > 10:
                boxes.append((x, y, w, h))
        
        # y좌표 기준으로 정렬 (위에서 아래로)
        boxes.sort(key=lambda box: box[1])
        
        return boxes
    
    def extract_line_image(self, image: np.ndarray, box: Tuple[int, int, int, int]) -> np.ndarray:
        """특정 라인의 이미지 추출"""
        x, y, w, h = box
        # 여백 추가
        padding = 5
        y_start = max(0, y - padding)
        y_end = min(image.shape[0], y + h + padding)
        x_start = max(0, x - padding)
        x_end = min(image.shape[1], x + w + padding)
        
        line_img = image[y_start:y_end, x_start:x_end]
        
        # 크기 조정 (OCR 정확도 향상)
        scale_factor = 2
        height, width = line_img.shape
        line_img = cv2.resize(line_img, (width * scale_factor, height * scale_factor), 
                             interpolation=cv2.INTER_CUBIC)
        
        return line_img
    
    def ocr_line(self, line_image: np.ndarray) -> Dict[str, str]:
        """한 줄의 텍스트와 숫자 추출"""
        # PIL Image로 변환
        pil_image = Image.fromarray(line_image)
        
        # 전체 텍스트 추출 (한국어 + 영어)
        full_text = pytesseract.image_to_string(pil_image, config=self.config).strip()
        
        # 숫자 부분만 추출
        numbers_text = pytesseract.image_to_string(pil_image, config=self.number_config).strip()
        
        # 텍스트에서 한국어 부분 추출
        korean_text = re.sub(r'[0-9,.\s]+', '', full_text).strip()
        
        # 숫자 정리 (콤마 제거, 빈 문자열 처리)
        clean_numbers = re.sub(r'[^\d,.]', '', numbers_text)
        clean_numbers = clean_numbers.replace(',', '')
        
        return {
            'korean_text': korean_text,
            'numbers': clean_numbers,
            'full_text': full_text
        }
    
    def parse_financial_data(self, image_path: str) -> pd.DataFrame:
        """금융 데이터 파싱 메인 함수"""
        print(f"이미지 처리 중: {image_path}")
        
        # 이미지 전처리
        processed_img = self.preprocess_image(image_path)
        
        # 텍스트 라인 감지
        line_boxes = self.detect_text_lines(processed_img)
        print(f"감지된 텍스트 라인 수: {len(line_boxes)}")
        
        # 각 라인별 OCR 수행
        results = []
        for i, box in enumerate(line_boxes):
            try:
                # 라인 이미지 추출
                line_img = self.extract_line_image(processed_img, box)
                
                # OCR 수행
                ocr_result = self.ocr_line(line_img)
                
                # 결과 저장
                if ocr_result['korean_text'] or ocr_result['numbers']:
                    results.append({
                        'line_number': i + 1,
                        'account_name': ocr_result['korean_text'],
                        'amount': ocr_result['numbers'],
                        'full_text': ocr_result['full_text'],
                        'bbox': box
                    })
                    
                print(f"라인 {i+1}: {ocr_result['korean_text']} | {ocr_result['numbers']}")
                
            except Exception as e:
                print(f"라인 {i+1} 처리 중 오류: {e}")
                continue
        
        # DataFrame으로 변환
        df = pd.DataFrame(results)
        return df
    
    def save_line_images(self, image_path: str, output_dir: str = "line_images"):
        """디버깅용: 각 라인별 이미지 저장"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        processed_img = self.preprocess_image(image_path)
        line_boxes = self.detect_text_lines(processed_img)
        
        for i, box in enumerate(line_boxes):
            line_img = self.extract_line_image(processed_img, box)
            output_path = os.path.join(output_dir, f"line_{i+1:02d}.png")
            cv2.imwrite(output_path, line_img)
            print(f"저장됨: {output_path}")

# 사용 예제
if __name__ == "__main__":
    # OCR 파서 초기화
    parser = FinancialOCRParser()

    user_photo_dir = os.path.expanduser('~/Pictures')

    # 이미지 불러오기
    image_path = os.path.join(user_photo_dir, '1.png')
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    try:
        # 금융 데이터 파싱
        df = parser.parse_financial_data(image_path)
        
        # 결과 출력
        print("\n=== 파싱 결과 ===")
        print(df.to_string(index=False))
        
        # CSV로 저장
        df.to_csv("parsed_financial_data.csv", index=False, encoding='utf-8-sig')
        print("\n결과가 'parsed_financial_data.csv'로 저장되었습니다.")
        
        # 디버깅용: 라인별 이미지 저장
        # parser.save_line_images(image_path)
        
    except Exception as e:
        print(f"오류 발생: {e}")

# 필요한 패키지 설치 명령어:
"""
pip install opencv-python pytesseract pillow pandas numpy

# Windows의 경우 Tesseract 설치 필요:
# https://github.com/UB-Mannheim/tesseract/wiki 에서 다운로드

# 한국어 언어팩 설치:
# tessdata 폴더에 kor.traineddata 파일 추가
"""