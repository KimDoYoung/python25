# tesseract-0

## 설명

1. tesseract 테스트

## 설치
1. tesseract 설치
2. uv add pytesseract pillow
3. 사진/OCR_TEST
   

## 테스트항목

1. 인증서 화면에서 "홍길동" 이름을 찾는가?
2. 팝업영역에서 "확인"을 찾는가?
3. 메뉴에서 "파일로 저장하기"를 찾는가?

## 참조
- `-psm`: Page Segmentation Mode (페이지 세분화 모드)
- `-psm`은 이미지에서 **텍스트의 배치 구조**를 어떻게 해석할지를 지정합니다.
3:  한 페이지에 여러 줄 (기본값) 
4:  단일 열 (단락) 
6:  **단일 균등한 텍스트 블록** (가장 흔히 사용됨) ✅ 
7:  단일 텍스트 줄 

- oem: OCR Engine Mode (OCR 엔진 모드)
 
 0 Legacy 엔진만 사용 (Tesseract 3 방식) 
 1 LSTM (Neural Net 기반) 엔진만 사용 
 2 Legacy + LSTM 결합 
 3 Tesseract가 자동으로 가장 좋은 엔진 선택 (기본값)` 
