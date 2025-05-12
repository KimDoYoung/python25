
import time
import torch
import easyocr
import os
import pandas as pd


def main():
    if torch.cuda.is_available():
        print("GPU 사용 가능:", torch.cuda.device_count(), "개")
        print("Device0 이름:", torch.cuda.get_device_name(0))
        print("CUDA 런타임 버전:", torch.version.cuda)
        print("Compute Capability:", torch.cuda.get_device_capability(0))
    else:
        print("CUDA 지원 GPU를 찾을 수 없습니다.")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("사용할 장치:", device)
    reader = easyocr.Reader(['ko','en'], gpu=(device=='cuda'))

    # 추론 예시
    home_dir = os.path.expanduser("~")
    img_path = os.path.join(home_dir, "Pictures", "1.png")
    if not os.path.exists(img_path):
        print(f"이미지 파일이 존재하지 않습니다: {img_path}")
        return
    print(f"이미지 파일 경로: {img_path}")

    start_time = time.time()

    # result = reader.readtext(img_path)
    results = reader.readtext(img_path, detail=0)

    # 3. 텍스트 정제 및 테이블 구성
    # 리스트에서 항목을 두 개씩 묶어 (항목, 값) 형식으로 변환
    rows = [(results[i], results[i+1]) for i in range(0, len(results), 2)]

    # 4. DataFrame으로 변환
    df = pd.DataFrame(rows, columns=['항목', '값'])

    print(df)

    end_time = time.time()
    print(f"추론 시간: {end_time - start_time:.2f} 초")

if __name__ == "__main__":
    main()
