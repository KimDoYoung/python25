from dataclasses import dataclass
import cv2
import numpy as np
from lib.core.datatypes.kavana_datatype import KavanaDataType

@dataclass
class Image(KavanaDataType):
    path: str  # 이미지 파일 경로
    data: np.ndarray = None  # OpenCV 이미지 데이터 (lazy loading)

    def __post_init__(self):
        """초기화 시 이미지 로드"""
        if self.path and self.data is None:
            self.load()

    def load(self):
        """이미지 파일 로드"""
        self.data = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        if self.data is None:
            raise ValueError(f"이미지를 불러올 수 없습니다: {self.path}")

    def save(self, save_path: str):
        """이미지 저장"""
        if self.data is None:
            raise ValueError("저장할 이미지 데이터가 없습니다.")
        cv2.imwrite(save_path, self.data)

    def compare(self, other: "Image", threshold: float = 0.9) -> bool:
        """두 이미지가 유사한지 비교"""
        if self.data is None or other.data is None:
            raise ValueError("비교할 이미지 데이터가 없습니다.")

        # 템플릿 매칭을 사용한 비교 (유사도 기반)
        res = cv2.matchTemplate(self.data, other.data, cv2.TM_CCOEFF_NORMED)
        max_val = np.max(res)
        return max_val >= threshold

    def __str__(self):
        return f"Image(path={self.path})"
