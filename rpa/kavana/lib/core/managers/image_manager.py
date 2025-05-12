import tempfile
from PIL import ImageFilter, ImageOps, ImageDraw, ImageFont
import cv2
import numpy as np
import pyautogui
from lib.core.datatypes.image import Image
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.managers.base_manager import BaseManager
from lib.core.token import TokenStatus
from lib.core.token_custom import ImageToken
from lib.core.token_type import TokenType
from PIL import Image as PILImage

class ImageManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs

        if not self.command:
            self.raise_error("command는 필수입니다.")

    def execute(self):
        commands = {
            "save": self.save,
            "resize": self.resize,
            "clip": self.clip,
            "to_gray": self.to_gray,
            "convert_to": self.convert_to,
            "rotate": self.rotate,
            "blur": self.blur,
            "threshold": self.threshold,
            "create_text_image" : self.create_text_image,
        }

        func = commands.get(self.command)
        if not func:
            self.raise_error(f"지원하지 않는 명령어입니다: {self.command}")
        func()

    def save(self):
        from_var = self.options.get("from_var")
        to_file = self.options.get("to_file")

        from_img_token = self.executor.get_variable(from_var)
        if not from_img_token:
            self.raise_error(f"변수 {from_var}에 이미지가 없습니다.")

        img_obj = from_img_token.data
        if hasattr(img_obj, "load") and from_img_token.status == TokenStatus.PARSED:
            img_obj.load()

        img = img_obj.data
        if not isinstance(img, np.ndarray):
            self.raise_error("이미지 데이터가 numpy 배열이 아닙니다.")
        if not to_file:
            self.raise_error("to_file 파라미터가 필요합니다.")

        cv2.imwrite(to_file, img)
        self.log("INFO", f"저장 완료: {to_file}")

    def resize(self):
        factor = self.options.get("factor")
        width = self.options.get("width")
        height = self.options.get("height")
        img_obj = self._get_my_image_type()

        if factor:
            w = int(img_obj.width * factor)
            h = int(img_obj.height * factor)
        elif width is not None:
            ratio = width / img_obj.width
            w = width
            h = int(img_obj.height * ratio)
        elif height is not None:
            ratio = height / img_obj.height
            h = height
            w = int(img_obj.width * ratio)
        else:
            raise KavanaValueError("IMAGE resize: width 또는 height 중 하나는 지정해야 합니다.")

        resized_img = cv2.resize(img_obj.data, (w, h))
        self._save_to_file_or_var(resized_img)

    def clip(self):
        area = self.options.get("area")
        from_var = self.options.get("from_var")
        from_file = self.options.get("from_file")
        area = self.options.get("area")
        # from_var과 from_file 모두 없으면 화면캡쳐해서 임시파일로 저장한 후 from_file로 사용
        if not from_var and not from_file:
            if not area:
                self.raise_error("IMAGE clip: area 파라미터가 필요합니다.")
            screenshot = pyautogui.screenshot()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            from_file = temp_file.name
            screenshot.save(from_file)
            temp_file.close()
            self.options["from_file"] = from_file

        my_img = self._get_my_image_type()

        if not area:
            self.raise_error("IMAGE clip: area 파라미터가 필요합니다.")

        if isinstance(area, dict):
            x = area["x"]
            y = area["y"]
            w = area["width"]
            h = area["height"]
        elif isinstance(area, (tuple, list)) and len(area) == 4:
            x, y, w, h = area
        else:
            self.raise_error("IMAGE clip: area는 dict 또는 (x, y, w, h) 형태의 tuple/list여야 합니다.")

        x_end = x + w
        y_end = y + h
        clipped = my_img.data[y:y_end, x:x_end]

        self._save_to_file_or_var(clipped)

    def to_gray(self):
        my_img = self._get_my_image_type()
        gray_img = cv2.cvtColor(my_img.data, cv2.COLOR_BGR2GRAY)
        self._save_to_file_or_var(gray_img)

    def convert_to(self):
        mode = self.options.get("mode")
        if not mode:
            self.raise_error("convert_to: mode 파라미터가 필요합니다.")
        if mode not in ["1", "L", "RGB", "RGBA", "CMYK", "P"]:
            self.raise_error("convert_to: 지원하지 않는 모드입니다.")

        my_img = self._get_my_image_type()
        pil_img = PILImage.fromarray(my_img.data)
        converted_pil = pil_img.convert(mode)
        converted_np = np.array(converted_pil)

        self._save_to_file_or_var(converted_np)

    def rotate(self):
        angle = self.options.get("angle", 0)
        my_img = self._get_my_image_type()

        if not isinstance(angle, int):
            self.raise_error("rotate: angle은 정수여야 합니다.")
        (h, w) = my_img.data.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        cos = abs(M[0, 0])
        sin = abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        rotated_img = cv2.warpAffine(my_img.data, M, (new_w, new_h))
        self._save_to_file_or_var(rotated_img)

    def blur(self):
        radius = self.options.get("radius", 2)
        my_img = self._get_my_image_type()

        k = int(radius * 2) + 1
        blurred = cv2.GaussianBlur(my_img.data, (k, k), sigmaX=radius)
        self._save_to_file_or_var(blurred)

    def threshold(self):
        level = self.options.get("level", 128)
        type_ = self.options.get("type", "BINARY_INV").upper()

        if type_ not in ["BINARY", "BINARY_INV", "TRUNC", "TOZERO", "TOZERO_INV"]:
            self.raise_error(f"지원하지 않는 TYPE입니다: {type_}")

        my_img = self._get_my_image_type()
        gray = cv2.cvtColor(my_img.data, cv2.COLOR_BGR2GRAY)

        threshold_type = getattr(cv2, f"THRESH_{type_}", None)
        if threshold_type is None:
            self.raise_error(f"OpenCV에서 지원하지 않는 THRESH TYPE: {type_}")

        _, binary = cv2.threshold(gray, level, 255, threshold_type)
        self._save_to_file_or_var(binary)


    def create_text_image(self):
        text = self.options.get("text")
        font_name = self.options.get("font_name", "gulim.ttc")
        font_size = self.options.get("font_size", 12)
        color = self.options.get("color", (0, 0, 0))         # 검정 글씨
        bg_color = self.options.get("bg_color", (255, 255, 255))  # 흰색 배경 (RGB 가능)
        width = self.options.get("width", None)
        height = self.options.get("height", None)

        if not text:
            self.raise_error("create_text_image: text 파라미터가 필요합니다.")

        try:
            font = ImageFont.truetype(font_name, font_size)
        except Exception as e:
            self.raise_error(f"폰트 로딩 실패: {font_name} ({str(e)})")

        if width is None or height is None:
            dummy_img = PILImage.new("RGB", (1, 1))
            d = ImageDraw.Draw(dummy_img)
            bbox = d.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            width = width or (text_width + 2)
            height = height or (text_height + 2)

        img = PILImage.new("RGB", (width, height), color=bg_color)
        d = ImageDraw.Draw(img)
        d.text((1, 1), text, fill=color, font=font)

        img_np = np.array(img)
        self._save_to_file_or_var(img_np)

    def _get_my_image_type(self):
        from_var = self.options.get("from_var")
        from_file = self.options.get("from_file")

        if from_var:
            from_img_token = self.executor.get_variable(from_var)
            if not from_img_token:
                self.raise_error(f"변수 {from_var}에 이미지가 없습니다.")
            img_obj = from_img_token.data
        elif from_file:
            img_obj = Image(from_file)
            img_obj.load()
        else:
            self.raise_error("이미지 소스가 필요합니다. (from_var 또는 from_file)")

        return img_obj

    def _save_to_file_or_var(self, img):
        import os
        from pathlib import Path
        from PIL import Image as PILImage  # ← 핵심 포인트!

        to_file = self.options.get("to_file")
        to_var = self.options.get("to_var")

        if isinstance(img, np.ndarray) and img.dtype == np.bool_:
            img = img.astype(np.uint8) * 255

        if to_file:
            from pathlib import Path
            Path(to_file).parent.mkdir(parents=True, exist_ok=True)

            try:
                PILImage.fromarray(img).save(to_file)
                self.log("INFO", f"저장 완료: {to_file}")
            except Exception as e:
                self.raise_error(f"이미지 저장 실패 (PIL): {to_file} -> {e}")            
        elif to_var:
            temp_file_path = self._save_temp_image(img)
            new_img = Image(temp_file_path)
            new_img.load()
            new_img_token = ImageToken(data=new_img)
            new_img_token.type = TokenType.IMAGE
            new_img_token.status = TokenStatus.EVALUATED
            self.executor.set_variable(to_var, new_img_token)
        else:
            self.raise_error("IMAGE 저장 실패: to_file 또는 to_var 파라미터가 필요합니다.")

    def _save_temp_image(self, img):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_path = tmp_file.name

        cv2.imwrite(tmp_path, img)
        return tmp_path

