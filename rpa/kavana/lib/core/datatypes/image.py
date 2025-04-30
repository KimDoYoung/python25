import cv2
import numpy as np
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.exceptions.kavana_exception import KavanaValueError

class Image(KavanaDataType):
    def __init__(self, path: str):
        self.path = path  # 이미지 파일 경로
        self.data = None  # OpenCV 이미지 데이터 (lazy loading)
        self.value = path  # ✅ value를 path로 설정
        self.height = 0  # 이미지 높이
        self.width = 0

    def __eq__(self, other):
        if not isinstance(other, Image):
            return NotImplemented  # Python의 내장 비교 연산자가 처리함
        if self.path == other.path:
            return True  # 경로가 같으면 완전 동일한 이미지로 간주 가능
        try:
            return self.compare(other, threshold=0.95)
        except Exception as e:
            return False

    def load(self):
        """이미지 파일 로드 (lazy loading)"""
        if self.data is None:
            self.data = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
            if self.data is None:
                raise KavanaValueError(f"이미지를 불러올 수 없습니다: {self.path}")
        self.height, self.width = self.data.shape[:2]

    def save(self, save_path: str):
        """이미지 저장"""
        if self.data is None:
            raise KavanaValueError("저장할 이미지 데이터가 없습니다.")
        cv2.imwrite(save_path, self.data)

    def compare(self, other: "Image", threshold: float = 0.9) -> bool:
        """두 이미지가 유사한지 비교"""
        if self.data is None:
            self.load()
        if other.data is None:
            other.load()

        # 템플릿 매칭을 사용한 비교 (유사도 기반)
        res = cv2.matchTemplate(self.data, other.data, cv2.TM_CCOEFF_NORMED)
        max_val = np.max(res)
        return max_val >= threshold

    def __str__(self):
        return f"Image(path={self.path})"

    @property
    def string(self):
        """이미지 경로를 문자열로 변환"""
        return self.path

    @property
    def primitive(self):
        """Python 기본 타입 변환 (이미지는 경로 문자열로 변환)"""
        return self.path

