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
img_path = os.path.join(base_dir, 'temp_image_1.png')

# 이미지에서 텍스트 인식
result = ocr.ocr(img_path, cls=False)

for r in result[0]:
    pts = r[0]
    text = r[1][0]
    conf = r[1][1]
                            
    print (f"Detected text: {text}, Confidence: {conf:.2f}")