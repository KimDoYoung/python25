# PaddleOCR 모델 초기화 - 한국어
import os
from paddleocr import PaddleOCR
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['KMP_DUPLICATE_LIB_OK']='True' #이거 안해주면 오류남

ocr = PaddleOCR(use_angle_cls=True, lang='korean')

# 이미지 파일 경로
base_dir = os.path.expanduser("~/Pictures/OCR_TEST")
img_path = 'image_1.png'

# 이미지에서 텍스트 인식
result = ocr.ocr(img_path, cls=True)

# 결과 출력
for line in result:
    print(line)