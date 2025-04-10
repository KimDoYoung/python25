from typing import List
import cv2
import numpy as np
import easyocr
from lib.core.datatypes.kavana_datatype import String
from lib.core.datatypes.point import Point
from lib.core.datatypes.region import Region
from lib.core.managers.base_manager import BaseManager
from lib.core.token import NoneToken, StringToken, TokenStatus
from lib.core.token_custom import PointToken, RegionToken
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

class OcrManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")  # READ, FIND, GET_ALL
        self.from_file = kwargs.get("from_file")
        self.from_var = kwargs.get("from_var")  # numpy 이미지 객체
        self.to_var = kwargs.get("to_var")
        self.area = kwargs.get("area")  # (x, y, w, h)
        self.text = kwargs.get("text")  # (x, y, w, h)

        self.preprocess = kwargs.get("preprocess", False)
        self.gray = kwargs.get("gray", False)  # 흑백 변환
        self.blur = kwargs.get("blur", False)  # 블러링
        self.threshold = kwargs.get("threshold", "adaptive")  # adaptive, otsu, none
        self.resize = kwargs.get("resize", 1.0)
        self.invert = kwargs.get("invert", False)

        self.reader = easyocr.Reader(['ko', 'en'])  # 한글 + 영어 지원

        if not self.command:
            self.raise_error("OcR 명령어에 command는 필수입니다.")

    def execute(self):
        command_map = {
            "READ": self.read,
            "FIND": self.find,
            "GET_ALL": self.get_all
        }

        func = command_map.get(self.command.upper())
        if not func:
            self.raise_error(f"OCR 지원하지 않는 명령어: {self.command}")
        return func()


    def read(self):
        # 이미지 로딩
        img = self._get_image_from_file_or_var()
        img = self._preprocess_image(img)

        # 3. area 잘라내기
        if self.area:
            if isinstance(self.area, dict):
                x = self.area["x"]
                y = self.area["y"]
                w = self.area["width"]
                h = self.area["height"]
            elif isinstance(self.area, (tuple, list)):
                x, y, w, h = self.area
            else:
                self.raise_error("area는 dict 또는 (x, y, w, h) 형태여야 합니다.")
            img = img[y:y+h, x:x+w]

        # 4. OCR 실행
        results = self.reader.readtext(img)
        text = " ".join([res[1] for res in results])

        self.log("INFO", f"추출된 텍스트: {text}")

        # 5. 변수 저장
        if self.to_var and self.executor:
            text_token = StringToken(data=String(text), type=TokenType.STRING)
            self.executor.set_variable(self.to_var, text_token)

        return text

    def find(self):
        if not self.text:
            self.raise_error("FIND 명령에는 text 옵션이 필요합니다.")

        # 이미지 불러오기
        img = self._get_image_from_file_or_var()
        img = self._preprocess_image(img)

        # 영역 크롭
        if self.area:
            if isinstance(self.area, dict):
                x = self.area["x"]
                y = self.area["y"]
                w = self.area["width"]
                h = self.area["height"]
            elif isinstance(self.area, (tuple, list)) and len(self.area) == 4:
                x, y, w, h = self.area
            else:
                self.raise_error("area는 dict 또는 (x, y, w, h) 형태여야 합니다.")
            img = img[y:y+h, x:x+w]
            offset_x, offset_y = x, y
        else:
            offset_x, offset_y = 0, 0

        # OCR 실행
        results = self.reader.readtext(img)

        for res in results:
            text_found = res[1]
            box = res[0]  # 박스 좌표: [(x1, y1), (x2, y2), ...]
            if self.text in text_found:
                (x1, y1), (x2, y2), *_ = box
                x = int(min(x1, x2)) + offset_x
                y = int(min(y1, y2)) + offset_y
                w = int(abs(x2 - x1))
                h = int(abs(box[2][1] - y1))  # y2나 y3와 비교해도 무방

                self.log("INFO", f"'{self.text}' 영역: {x}, {y}, {w}, {h}")
                if self.to_var and self.executor:
                    region_token = RegionToken(data=Region(x, y, w, h))
                    region_token.status = TokenStatus.EVALUATED
                    self.executor.set_variable(self.to_var, region_token)
                return x, y, w, h

        # 찾지 못했을 때
        self.log("WARNING", f"'{self.text}'를 찾지 못함.")
        if self.to_var and self.executor:
            none_token = NoneToken()
            self.executor.set_variable(self.to_var, none_token)
        return None


    def get_all(self):
        # 이미지 불러오기
        img = self._get_image_from_file_or_var()
        img = self._preprocess_image(img)
        # 영역 크롭
        if self.area:
            factor = self.resize if self.resize else 1.0

            if isinstance(self.area, dict):
                x = int(self.area["x"] * factor)
                y = int(self.area["y"] * factor)
                w = int(self.area["width"] * factor)
                h = int(self.area["height"] * factor)
            elif isinstance(self.area, (tuple, List)) and len(self.area) == 4:
                x = int(self.area[0] * factor)
                y = int(self.area[1] * factor)
                w = int(self.area[2] * factor)
                h = int(self.area[3] * factor)
            else:
                self.raise_error("area는 dict 또는 (x, y, w, h) 형태여야 합니다.")

            img = img[y:y+h, x:x+w]
            offset_x, offset_y = x, y
        else:
            offset_x, offset_y = 0, 0

        # OCR 실행
        results = self.reader.readtext(img)
        output = []

        for res in results:
            box, text, conf = res
            (x1, y1), (x2, y2), (x3, y3), (x4, y4) = box
            x = int(min(x1, x2, x3, x4)) + offset_x
            y = int(min(y1, y2, y3, y4)) + offset_y
            w = int(max(x1, x2, x3, x4) - min(x1, x2, x3, x4))
            h = int(max(y1, y2, y3, y4) - min(y1, y2, y3, y4))

            entry = {
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "text": text,
                "confidence": round(conf, 3)
            }
            output.append(entry)

        # 결과 변수에 저장
        if self.to_var and self.executor:
            from lib.core.token_type import TokenType
            from lib.core.token import ArrayToken
            from lib.core.datatypes.array import Array
            list = []
            for item in output:
                hash_map = TokenUtil.dict_to_hashmap_token(item)
                list.append(hash_map)
            array = Array(list)
            token = ArrayToken(data=array, element_type=TokenType.HASH_MAP, element_expresses=[])
            token.status = 'Evaled'
            self.executor.set_variable(self.to_var, token)

        self.log("INFO", f"{len(output)}개의 텍스트 요소 추출 완료")
        return output


    def _preprocess_image(self, img):
        ''' 이미지 전처리 '''
        if self.preprocess == False:
            return img
        
        # ✅ threshold 사용 시 자동으로 gray 적용
        if self.threshold and self.threshold.lower() != "none":
            if not self.gray:
                self.gray = True        

        if self.gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if self.invert:
            img = cv2.bitwise_not(img)

        if self.blur:
            k = int(self.blur) * 2 + 1
            img = cv2.GaussianBlur(img, (k, k), 0)

        if self.threshold == "adaptive":
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
        elif self.threshold == "otsu":
            _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if self.resize and self.resize != 1.0:
            w = int(img.shape[1] * self.resize)
            h = int(img.shape[0] * self.resize)
            img = cv2.resize(img, (w, h))

        return img

    def _get_image_from_file_or_var(self):
        """이미지 파일 또는 변수를 로드하여 numpy 배열로 반환"""
        if self.from_file:
            img = cv2.imread(self.from_file)
            if img is None:
                self.raise_error(f"이미지 파일을 열 수 없습니다: {self.from_file}")
        elif self.from_var:
            img = self.executor.get_variable(self.from_var).data
            if not isinstance(img, np.ndarray):
                self.raise_error(f"변수 '{self.from_var}'는 numpy 배열이어야 합니다.")
        else:
            self.raise_error("from_file 또는 from_var가 필요합니다.")
        
        return img
