from PIL import Image, ImageFilter, ImageOps
from lib.core.managers.base_manager import BaseManager

class ImageManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")  # resize, clip, ...
        self.from_var = kwargs.get("from_var")
        self.to_var = kwargs.get("to_var")
        self.from_file = kwargs.get("from_file")
        self.to_file = kwargs.get("to_file")
        # 옵션들
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.region = kwargs.get("region")      # (x, y, w, h)
        self.angle = kwargs.get("angle", 0)
        self.radius = kwargs.get("radius", 2)
        self.level = kwargs.get("level", 128)
        self.format = kwargs.get("format")      # jpg, png 등

        if not self.file:
            self.raise_error("file 파라미터는 필수입니다.")
        if not self.command:
            self.raise_error("command 파라미터는 필수입니다.")

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
        pass
    
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

    def resize(self):
        img = self.open_image()
        if not self.width or not self.height:
            self.raise_error("resize에는 width와 height가 필요합니다.")
        resized = img.resize((int(self.width), int(self.height)))
        self.save_image(resized)

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
