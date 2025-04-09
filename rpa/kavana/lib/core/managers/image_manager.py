import tempfile
from PIL import  ImageFilter, ImageOps
import cv2
import numpy as np
from lib.core.datatypes.image import Image
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.managers.base_manager import BaseManager
from lib.core.token import TokenStatus
from lib.core.token_custom import ImageToken
from lib.core.token_type import TokenType

class ImageManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")  # resize, clip, ...
        self.from_var = kwargs.get("from_var", None)
        self.to_var = kwargs.get("to_var", None)
        self.from_file = kwargs.get("from_file", None)
        self.to_file = kwargs.get("to_file", None)
        # 옵션들
        self.factor = kwargs.get("factor", None)
        self.width = kwargs.get("width", None)
        self.height = kwargs.get("height", None)
        self.region = kwargs.get("region")      # (x, y, w, h)
        self.angle = kwargs.get("angle", 0)
        self.radius = kwargs.get("radius", 2)
        self.level = kwargs.get("level", 128)
        

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
        }

        func = commands.get(self.command)
        if not func:
            self.raise_error(f"지원하지 않는 명령어입니다: {self.command}")
        func()

    def save(self):
        from_img_token = self.executor.get_variable(self.from_var)
        if not from_img_token:
            self.raise_error(f"변수 {self.from_var}에 이미지가 없습니다.")

        img_obj = from_img_token.data  # Image 인스턴스

        if hasattr(img_obj, "load") and from_img_token.status == TokenStatus.PARSED:
            img_obj.load()  # ✅ 이미지 로딩

        img = img_obj.data

        if not isinstance(img, np.ndarray):
            self.raise_error("이미지 데이터가 numpy 배열이 아닙니다.")

        if not self.to_file:
            self.raise_error("to_file 파라미터가 필요합니다.")

        cv2.imwrite(self.to_file, img)
        self.log("INFO", f"저장 완료: {self.to_file}")
    
    def resize(self):
        ''' 이미지 크기 조정 '''
        if self.from_var:
            from_img_token = self.executor.get_variable(self.from_var)
            if not from_img_token:
                self.raise_error(f"변수 {self.from_var}에 이미지가 없습니다.")
            img_obj = from_img_token.data
        elif self.from_file:
            img_obj = Image(self.from_file)
            img_obj.load()  # 이미지 로딩
        else:
            self.raise_error("IMAGE resize: from_var 또는 from_file 중 하나는 필요합니다.")

        if self.factor:
            w = img_obj.width * self.factor
            h = img_obj.height * self.factor
        elif self.width is not None:
                ratio = self.width / img_obj.width
                w = self.width 
                h = int(img_obj.height * ratio)
        elif self.height is not None:
                ratio = self.height / img_obj.height
                h = self.height
                w = int(img_obj.width * ratio)
        else:
            raise KavanaValueError("IMAGE resize: width 또는 height 중 하나는 지정해야 합니다.")

        # resize
        resized_img = cv2.resize(img_obj.data, (w, h))

        if self.to_file is not None:
            cv2.imwrite(self.to_file, resized_img)
        elif self.to_var is not None:
            # 임시로 저장한 후 불러들인다.
            temp_file_path = self._save_temp_image(resized_img)
            new_img = Image(temp_file_path)
            new_img.load()  # 이미지 로딩
            new_img_token = ImageToken(data=new_img)
            new_img_token.type = TokenType.IMAGE            
            new_img_token.status = TokenStatus.EVALUATED
            self.executor.set_variable(self.to_var, new_img_token)
        else:
            self.raise_error("IMAGE resize : to_file 또는 to_var 파라미터가 필요합니다.")


    def _save_temp_image(self, img):
        """임시 이미지 저장 후 경로 반환"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_path = tmp_file.name  # 파일 경로 추출

        cv2.imwrite(tmp_path, img)
        return tmp_path
        
    def open_image(self):
        try:
            return Image.open(self.file)
        except Exception as e:
            self.raise_error(f"이미지 열기 실패: {e}")

    def save_image(self, img, default_format=None):
        if not self.save_as:
            self.raise_error("save_as 파라미터가 필요합니다.")
        fmt = self.format or default_format or None
        img.save(self.save_as, format=fmt)
        self.log("INFO", f"저장 완료: {self.save_as}")



    def clip(self):
        img = self.open_image()
        if not self.region or len(self.region) != 4:
            self.raise_error("clip에는 region=(x, y, w, h)가 필요합니다.")
        x, y, w, h = self.region
        cropped = img.crop((x, y, x + w, y + h))
        self.save_image(cropped)

    def to_gray(self):
        img = self.open_image()
        gray = ImageOps.grayscale(img)
        self.save_image(gray)

    def convert_to(self):
        img = self.open_image()
        if not self.format:
            self.raise_error("convert_to에는 format이 필요합니다.")

        fmt = self.format.upper()
        if (fmt == "JPEG" or fmt=="JPG") and img.mode == "RGBA":
            img = img.convert("RGB")

        self.save_image(img, default_format=fmt)        

    def rotate(self):
        img = self.open_image()
        rotated = img.rotate(-self.angle, expand=True)
        self.save_image(rotated)

    def blur(self):
        img = self.open_image()
        blurred = img.filter(ImageFilter.GaussianBlur(self.radius))
        self.save_image(blurred)

    def threshold(self):
        img = self.open_image().convert("L")
        binary = img.point(lambda p: 255 if p > self.level else 0)
        self.save_image(binary)
