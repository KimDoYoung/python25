import cv2
import numpy as np
import os
from typing import List, Tuple

class ImageLineSplitter:
    def __init__(self):
        pass
    
    def preprocess_image(self, image_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """이미지 전처리 및 원본 반환"""
        # 원본 이미지 읽기
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")
        
        # 그레이스케일 변환 (라인 감지용)
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 이진화 (라인 감지용)
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return original, binary
    
    def detect_text_lines(self, binary_image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """텍스트 라인 영역 감지 (개선된 버전)"""
        height, width = binary_image.shape
        
        # 방법 1: 수평 투영으로 라인 감지
        horizontal_projection = np.sum(binary_image == 0, axis=1)  # 검은색 픽셀 개수
        
        # 텍스트가 있는 라인 찾기
        threshold = width * 0.1  # 전체 너비의 10% 이상 텍스트가 있으면 라인으로 간주
        text_lines = []
        
        in_text = False
        start_y = 0
        
        for y, projection in enumerate(horizontal_projection):
            if projection > threshold and not in_text:
                # 텍스트 라인 시작
                start_y = y
                in_text = True
            elif projection <= threshold and in_text:
                # 텍스트 라인 끝
                if y - start_y > 5:  # 최소 높이 조건
                    text_lines.append((0, start_y, width, y - start_y))
                in_text = False
        
        # 마지막 라인 처리
        if in_text and height - start_y > 5:
            text_lines.append((0, start_y, width, height - start_y))
        
        print(f"수평 투영으로 감지된 라인: {len(text_lines)}")
        
        # 방법 2: 컨투어 방법도 시도
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width//20, 1))
        dilated = cv2.dilate(binary_image, kernel, iterations=1)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > width * 0.3 and h > 5:  # 너비가 전체의 30% 이상, 높이 5 이상
                contour_boxes.append((x, y, w, h))
        
        print(f"컨투어로 감지된 라인: {len(contour_boxes)}")
        
        # 더 많이 감지된 방법 사용
        if len(text_lines) >= len(contour_boxes):
            boxes = text_lines
            print("수평 투영 방법 사용")
        else:
            boxes = contour_boxes
            print("컨투어 방법 사용")
        
        # y좌표 기준으로 정렬
        boxes.sort(key=lambda box: box[1])
        
        return boxes
    
    def extract_and_save_lines(self, image_path: str, output_dir: str = "lines"):
        """이미지를 줄별로 분할하여 저장"""
        # 출력 디렉토리 생성
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"디렉토리 생성: {output_dir}")
        
        # 이미지 전처리
        original, binary = self.preprocess_image(image_path)
        print(f"이미지 로드 완료: {image_path}")
        print(f"이미지 크기: {original.shape}")
        
        # 디버깅: 전처리된 이미지 저장
        cv2.imwrite(os.path.join(output_dir, "debug_binary.png"), binary)
        
        # 텍스트 라인 감지
        line_boxes = self.detect_text_lines(binary)
        print(f"감지된 텍스트 라인 수: {len(line_boxes)}")
        
        # 라인별 상세 정보 출력
        for i, (x, y, w, h) in enumerate(line_boxes):
            print(f"라인 {i+1}: x={x}, y={y}, w={w}, h={h}")
        
        # 각 라인별 이미지 저장
        saved_files = []
        for i, (x, y, w, h) in enumerate(line_boxes):
            try:
                # 여백 추가
                padding = 5
                y_start = max(0, y - padding)
                y_end = min(original.shape[0], y + h + padding)
                x_start = max(0, x - padding)
                x_end = min(original.shape[1], x + w + padding)
                
                # 원본 이미지에서 라인 추출
                line_img = original[y_start:y_end, x_start:x_end]
                
                # 빈 이미지 체크
                if line_img.size == 0:
                    print(f"라인 {i+1}: 빈 이미지, 건너뜀")
                    continue
                
                # 파일명 생성
                filename = f"{i+1}.png"
                filepath = os.path.join(output_dir, filename)
                
                # 이미지 저장
                success = cv2.imwrite(filepath, line_img)
                
                if success:
                    saved_files.append(filepath)
                    print(f"저장 완료: {filepath} (크기: {line_img.shape})")
                else:
                    print(f"저장 실패: {filepath}")
                    
            except Exception as e:
                print(f"라인 {i+1} 처리 중 오류: {e}")
                continue
        
        print(f"\n총 {len(saved_files)}개 파일이 저장되었습니다.")
        return saved_files
    
    def preview_line_detection(self, image_path: str, output_path: str = "preview.png"):
        """라인 감지 결과 미리보기 (디버깅용)"""
        original, binary = self.preprocess_image(image_path)
        line_boxes = self.detect_text_lines(binary)
        
        # 원본 이미지에 감지된 라인 박스 그리기
        preview_img = original.copy()
        for i, (x, y, w, h) in enumerate(line_boxes):
            # 박스 그리기
            cv2.rectangle(preview_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 라인 번호 표시
            cv2.putText(preview_img, str(i+1), (x, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # 미리보기 이미지 저장
        cv2.imwrite(output_path, preview_img)
        print(f"라인 감지 미리보기 저장: {output_path}")
        
        return line_boxes

# 사용 예제
if __name__ == "__main__":
    # 이미지 분할기 초기화
    splitter = ImageLineSplitter()
    
    # 입력 이미지 파일 경로 (업로드한 파일명으로 변경)
    user_photo_dir = os.path.expanduser('~/Pictures')

    # 이미지 불러오기
    input_image = os.path.join(user_photo_dir, '1.png')
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Image not found at {input_image}")    
    
    try:
        # 라인 감지 미리보기 (선택사항)
        print("=== 라인 감지 미리보기 ===")
        detected_lines = splitter.preview_line_detection(input_image)
        
        # 이미지를 줄별로 분할하여 저장
        print("\n=== 줄별 분할 저장 ===")
        saved_files = splitter.extract_and_save_lines(input_image, output_dir="lines")
        
        print(f"\n작업 완료!")
        print(f"저장된 파일들:")
        for file in saved_files:
            print(f"  - {file}")
            
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_image}")
        print("파일명을 확인하고 같은 폴더에 있는지 확인해주세요.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 필요한 패키지 설치:
# pip install opencv-python numpy