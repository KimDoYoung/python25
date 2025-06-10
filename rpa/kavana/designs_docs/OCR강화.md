# OCR강화
## 목표
1. 정확한 항목
2. 정확한 숫자
3. cross 체크

| 우선순위 | 기법          | 설명                             |
| ---- | ----------- | ------------------------------ |
| ✅ 1  | 전처리 강화      | adaptive threshold, morphology |
| ✅ 2  | 후처리 정규화     | 숫자 형식 필터링, label 정리            |
| ⬆️ 3 | OCR 멀티모델 비교 | EasyOCR 외 Tesseract/PaddleOCR  |
| ⬆️ 4 | 개별 줄 기반 분석  | readtext로 line별 정리             |

## 다른 것

tesseract image.png stdout --oem 3 --psm 6 -l kor+eng

## 이미지 전처리
```
def _preprocess_image(self, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inverted = cv2.bitwise_not(thresh)

    # Morphology 연산으로 숫자 간격 정리
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel)

    return processed
```

## 후처리
```
import re

def extract_amounts(text: str) -> dict:
    result = {}
    lines = text.splitlines()
    for line in lines:
        match = re.search(r'([\d,]+)', line)
        label = re.sub(r'[^가-힣a-zA-Z]', '', line.split()[0])  # 한글+영문 추출
        amount = match.group(1) if match else "0"
        result[label] = amount
    return result

```
## EasyOCR

- EasyOCR은 PyTorch 기반으로 사전학습된 딥러닝 모델을 사용합니다.
- 따라서 실제 "학습 튜닝"은 모델을 다시 학습(Finetuning) 하거나, 후처리 정제를 추가하는 방식으로 접근해야 합니다.
- EasyOCR은 내부적으로 CRNN + CTC 기반 구조를 사용하므로, 학습 파이프라인은 다음과 같이 구성됩니다:

1. dataset 준비 (이미지 + 텍스트 라벨)
2. label converter 설정 (korean + financial terms)
3. 사전 학습된 모델에서 fine-tune
4. train.py 실행하여 재학습
- 💡 이 부분은 공식 EasyOCR 레포를 clone 후, training 디렉토리에서 조정할 수 있습니다.
- 학습에 GPU 필요.

## 한줄씩 잘라내서 tesseract로 처리하는 것
까먹어 버렸네... 어떻게 했더라...
