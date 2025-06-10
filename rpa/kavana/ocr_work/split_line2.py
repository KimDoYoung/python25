import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import re
import pandas as pd
from typing import List, Tuple, Dict

class LineTextExtractor:
    def __init__(self):
        # Tesseract 설정
        self.korean_config = '--oem 3 --psm 7 -l kor'  # 한국어, 단일 라인
        self.number_config = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789,.'  # 숫자만
        
    def preprocess_line_image(self, image: np.ndarray) -> np.ndarray:
        """라인 이미지 전처리"""
        # 그레이스케일 변환
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # 노이즈 제거
        denoised = cv2.medianBlur(gray, 3)
        
        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 이진화
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def detect_vertical_split(self, binary_image: np.ndarray) -> int:
        """수직 분할점 찾기"""
        height, width = binary_image.shape
        
        # 수직 투영 (각 열의 검은색 픽셀 개수)
        vertical_projection = np.sum(binary_image == 0, axis=0)
        
        # 중간 지점부터 검색 (보통 한글 제목이 왼쪽, 숫자가 오른쪽)
        middle = width // 2
        
        # 오른쪽 절반에서 텍스트가 시작하는 지점 찾기
        threshold = height * 0.1  # 전체 높이의 10% 이상 텍스트가 있으면
        
        for x in range(middle, width):
            if vertical_projection[x] > threshold:
                # 숫자 영역 시작점 발견
                # 조금 여백을 두고 분할점 설정
                split_point = max(middle, x - 10)
                return split_point
        
        # 분할점을 찾지 못한 경우 중간점 사용
        return middle
    
    def extract_korean_text(self, image: np.ndarray) -> str:
        """한국어 텍스트 추출"""
        # PIL Image로 변환
        pil_image = Image.fromarray(image)
        
        # 한국어 OCR
        try:
            text = pytesseract.image_to_string(pil_image, config=self.korean_config).strip()
            # 숫자와 특수문자 제거, 한글만 추출
            korean_only = re.sub(r'[^가-힣a-zA-Z\s]', '', text).strip()
            return korean_only
        except Exception as e:
            print(f"한국어 OCR 오류: {e}")
            return ""
    
    def extract_number_text(self, image: np.ndarray) -> str:
        """숫자 텍스트 추출"""
        # PIL Image로 변환
        pil_image = Image.fromarray(image)
        
        try:
            # 일반 OCR로 먼저 시도
            text = pytesseract.image_to_string(pil_image, config='--oem 3 --psm 8').strip()
            
            # 숫자, 콤마, 점만 추출
            numbers = re.findall(r'[\d,\.]+', text)
            if numbers:
                # 가장 긴 숫자 문자열 선택
                longest_number = max(numbers, key=len)
                return longest_number
            
            # 숫자 전용 OCR로 재시도
            number_text = pytesseract.image_to_string(pil_image, config=self.number_config).strip()
            return number_text
        except Exception as e:
            print(f"숫자 OCR 오류: {e}")
            return ""
    
    def process_single_line(self, image_path: str) -> Dict[str, str]:
        """단일 라인 이미지 처리"""
        # 이미지 로드
        original = cv2.imread(image_path)
        if original is None:
            return {"korean": "", "number": "", "error": f"이미지 로드 실패: {image_path}"}
        
        # 전처리
        binary = self.preprocess_line_image(original)
        
        # 수직 분할점 찾기
        split_point = self.detect_vertical_split(binary)
        
        # 왼쪽 영역 (한국어)
        korean_region = binary[:, :split_point]
        korean_text = self.extract_korean_text(korean_region)
        
        # 오른쪽 영역 (숫자)
        number_region = binary[:, split_point:]
        number_text = self.extract_number_text(number_region)
        
        return {
            "korean": korean_text,
            "number": number_text,
            "split_point": split_point,
            "image_width": binary.shape[1]
        }
    
    def process_all_lines(self, lines_dir: str = "lines") -> pd.DataFrame:
        """모든 라인 이미지 처리"""
        results = []
        
        # lines 디렉토리의 모든 png 파일 처리
        if not os.path.exists(lines_dir):
            print(f"디렉토리가 존재하지 않습니다: {lines_dir}")
            return pd.DataFrame()
        
        # 파일명으로 정렬 (1.png, 2.png, ...)
        png_files = [f for f in os.listdir(lines_dir) if f.endswith('.png') and f[0].isdigit()]
        png_files.sort(key=lambda x: int(x.split('.')[0]))
        
        print(f"처리할 파일 수: {len(png_files)}")
        
        for filename in png_files:
            if filename.startswith('debug'):  # 디버그 파일 제외
                continue
                
            filepath = os.path.join(lines_dir, filename)
            print(f"\n처리 중: {filename}")
            
            # 라인 처리
            result = self.process_single_line(filepath)
            
            if "error" in result:
                print(f"오류: {result['error']}")
                continue
            
            # 결과 저장
            line_data = {
                "파일명": filename,
                "순번": int(filename.split('.')[0]),
                "계정명": result["korean"],
                "금액": result["number"],
                "분할점": result["split_point"],
                "이미지너비": result["image_width"]
            }
            
            results.append(line_data)
            print(f"  한국어: '{result['korean']}'")
            print(f"  숫자: '{result['number']}'")
            print(f"  분할점: {result['split_point']}/{result['image_width']}")
        
        # DataFrame 생성
        df = pd.DataFrame(results)
        return df
    
    def save_debug_images(self, lines_dir: str = "lines", debug_dir: str = "debug"):
        """디버깅용: 분할된 영역 이미지 저장"""
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        
        png_files = [f for f in os.listdir(lines_dir) if f.endswith('.png') and f[0].isdigit()]
        png_files.sort(key=lambda x: int(x.split('.')[0]))
        
        for filename in png_files:
            if filename.startswith('debug'):
                continue
                
            filepath = os.path.join(lines_dir, filename)
            original = cv2.imread(filepath)
            if original is None:
                continue
                
            binary = self.preprocess_line_image(original)
            split_point = self.detect_vertical_split(binary)
            
            # 왼쪽 영역 (한국어)
            korean_region = binary[:, :split_point]
            korean_path = os.path.join(debug_dir, f"{filename}_korean.png")
            cv2.imwrite(korean_path, korean_region)
            
            # 오른쪽 영역 (숫자)
            number_region = binary[:, split_point:]
            number_path = os.path.join(debug_dir, f"{filename}_number.png")
            cv2.imwrite(number_path, number_region)
            
            # 분할선이 그어진 원본
            debug_img = original.copy()
            cv2.line(debug_img, (split_point, 0), (split_point, debug_img.shape[0]), (0, 255, 0), 2)
            split_path = os.path.join(debug_dir, f"{filename}_split.png")
            cv2.imwrite(split_path, debug_img)
            
        print(f"디버그 이미지가 {debug_dir} 폴더에 저장되었습니다.")

# 사용 예제
if __name__ == "__main__":
    # 텍스트 추출기 초기화
    extractor = LineTextExtractor()
    
    try:
        # 모든 라인 이미지 처리
        print("=== 라인별 텍스트 추출 ===")
        df = extractor.process_all_lines("lines")
        
        if not df.empty:
            # 결과 출력
            print("\n=== 추출 결과 ===")
            for _, row in df.iterrows():
                print(f"{row['순번']:2d}. {row['계정명']:15s} | {row['금액']:>15s}")
            
            # CSV로 저장
            df.to_csv("extracted_financial_data.csv", index=False, encoding='utf-8-sig')
            print(f"\n결과가 'extracted_financial_data.csv'로 저장되었습니다.")
            
            # 간단한 요약 출력
            print(f"\n총 {len(df)}개 항목이 추출되었습니다.")
            
        else:
            print("추출된 데이터가 없습니다.")
        
        # 디버깅 이미지 저장 (필요시)
        # extractor.save_debug_images()
        
    except Exception as e:
        print(f"오류 발생: {e}")

# 필요한 패키지:
# pip install opencv-python pytesseract pillow pandas numpy