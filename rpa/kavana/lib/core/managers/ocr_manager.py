import cv2
import numpy as np
import easyocr
from base_manager import BaseManager

class OCRManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")  # READ, FIND, GET_ALL
        self.image_path = kwargs.get("image_path")
        self.image = kwargs.get("image")  # numpy 이미지 객체
        self.region = kwargs.get("region")  # (x, y, w, h)
        self.rectangle = kwargs.get("rectangle")  # (x, y, w, h)
        self.text = kwargs.get("text")
        self.to_var = kwargs.get("to_var")

        self.reader = easyocr.Reader(['ko', 'en'])  # 한글 + 영어 지원

        if not self.command:
            self.raise_error("command는 필수입니다.")

    def execute(self):
        command_map = {
            "READ": self.read,
            "FIND": self.find,
            "GET_ALL": self.get_all
        }

        func = command_map.get(self.command.upper())
        if not func:
            self.raise_error(f"지원하지 않는 명령어: {self.command}")
        return func()

    def load_image(self):
        """이미지 경로 or 객체에서 numpy 이미지 추출"""
        if self.image is not None:
            img = self.image
        elif self.image_path:
            img = cv2.imread(self.image_path)
            if img is None:
                self.raise_error(f"이미지 파일을 열 수 없습니다: {self.image_path}")
        else:
            self.raise_error("image_path 또는 image가 필요합니다.")

        # REGION이나 RECTANGLE로 crop
        area = self.region or self.rectangle
        if area:
            x, y, w, h = area
            img = img[y:y+h, x:x+w]
        return img

    def read(self):
        img = self.load_image()
        results = self.reader.readtext(img)
        text = " ".join([res[1] for res in results])
        self.log("INFO", f"추출된 텍스트: {text}")
        if self.to_var and self.executor:
            self.executor.set_var(self.to_var, text)
        return text

    def find(self):
        if not self.text:
            self.raise_error("FIND 명령에는 text 옵션이 필요합니다.")

        img = self.load_image()
        results = self.reader.readtext(img)
        for res in results:
            if self.text in res[1]:
                (x1, y1), (x2, y2), *_ = res[0]
                point = {"x": int(x1), "y": int(y1)}
                if self.to_var and self.executor:
                    self.executor.set_var(self.to_var, point)
                self.log("INFO", f"'{self.text}' 위치: {point}")
                return point

        self.log("WARNING", f"'{self.text}'를 찾지 못함.")
        if self.to_var and self.executor:
            self.executor.set_var(self.to_var, None)
        return None

    def get_all(self):
        img = self.load_image()
        results = self.reader.readtext(img)
        output = []
        for res in results:
            box, text, conf = res
            (x1, y1), *_ = box
            info = {
                "text": text,
                "point": {"x": int(x1), "y": int(y1)},
                "confidence": round(conf, 3)
            }
            output.append(info)

        if self.to_var and self.executor:
            self.executor.set_var(self.to_var, output)
        self.log("INFO", f"{len(output)}개의 텍스트 요소 추출 완료")
        return output
