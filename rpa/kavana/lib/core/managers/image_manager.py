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


    def clip(self):
        ''' 이미지 자르기 '''
        # from_file, from_var 처리
        my_img = self._get_my_image_type()
    
        if self.region is not None:
            x, y, w, h = self.region.x, self.region.y, self.region.width, self.region.height
        elif self.rectangle is not None:
            x, y, w, h = self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height
        else:
            self.raise_error("IMAGE clip: region 또는 rectangle 중 하나는 필요합니다.")
        x_end = x + w
        y_end = y + h
        clipped= my_img[x:x_end, y:y_end]    

        # 파일 저장 또는 var에 저장
        self._save_to_file_or_var(clipped)

        return    

    def to_gray(self):
        '''이미지를 흑백(grayscale)으로 변환'''
        my_img = self._get_my_image_type()
        gray_img = cv2.cvtColor(my_img.data, cv2.COLOR_BGR2GRAY)
        
        self._save_to_file_or_var(gray_img)
        return


    def convert_to(self):
        '''이미지를 특정 모드로 변환'''
        if not self.mode:
            self.raise_error("convert_to: mode 파라미터가 필요합니다.")
        if self.mode not in ["1", "L", "RGB", "RGBA", "CMYK", "P"]:
            self.raise_error("convert_to: 지원하지 않는 모드입니다. mode는 '1', 'L', 'RGB', 'RGBA', 'CMYK', 'P' 중 하나여야 합니다.")   

        my_img = self._get_my_image_type()
        if self.mode == "1":
            converted_img = my_img.convert("1")
        elif self.mode == "L":
            converted_img = my_img.convert("L")
        elif self.mode == "RGB":
            converted_img = my_img.convert("RGB")
        elif self.mode == "RGBA":
            converted_img = my_img.convert("RGBA")
        elif self.mode == "CMYK":
            converted_img = my_img.convert("CMYK")
        elif self.mode == "P":
            converted_img = my_img.convert("P")
        else:
            self.raise_error(f"지원하지 않는 모드입니다: {self.mode}")
        self._save_to_file_or_var(converted_img)
        return

    def rotate(self):
        '''이미지를 회전'''
        my_img = self._get_my_image_type()
        
        if self.angle is None:
            self.raise_error("rotate: angle 파라미터가 필요합니다.")
        if self.angle is not None and not isinstance(self.angle, (int)):
            self.raise_error("rotate: angle은 정수여야 합니다.")
        (h, w) = my_img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, self.angle, 1.0)

        # 새 이미지 크기 계산
        cos = abs(M[0, 0])
        sin = abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        # 이동 보정
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        rotated_img =  cv2.warpAffine(my_img, M, (new_w, new_h))
        
        # 파일 저장 또는 var에 저장
        self._save_to_file_or_var(rotated_img)
        return


    def blur(self):
        '''이미지 블러 처리'''
        my_img = self._get_my_image_type()
        radius = self.radius or 2  # radius → sigma

        # 가우시안 블러 사용
        k = int(radius * 2) + 1  # 홀수 커널 사이즈
        blurred = cv2.GaussianBlur(my_img.data, (k, k), sigmaX=radius)

        self._save_to_file_or_var(blurred)
        return

    def threshold(self):
        '''이미지 이진화'''
        level = self.level or 128
        type = self.type.upper()
        if  type not in ["BINARY", "BINARY_INV", "TRUNC", "TOZERO", "TOZERO_INV"]:
            self.raise_error("THRESHOLD: TYPE은 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV' 중 하나여야 합니다.")

        my_img = self._get_my_image_type()

        # 흑백 이미지로 변환
        gray = cv2.cvtColor(my_img.data, cv2.COLOR_BGR2GRAY)

        level = self.level or 128
        if type == "BINARY":
            _, binary = cv2.threshold(gray, level, 255, cv2.THRESH_BINARY)
        elif type == "BINARY_INV":
            _, binary = cv2.threshold(gray, level, 255, cv2.THRESH_BINARY_INV)
        elif type == "TRUNC":
            _, binary = cv2.threshold(gray, level, 255, cv2.THRESH_TRUNC)
        elif type == "TOZERO":
            _, binary = cv2.threshold(gray, level, 255, cv2.THRESH_TOZERO)
        elif type == "TOZERO_INV":
            _, binary = cv2.threshold(gray, level, 255, cv2.THRESH_TOZERO_INV)
        else:
            # 지원하지 않는 타입 처리 (기본적으로 BINARY로 설정)
            self.raise_error(f"지원하지 않는 타입입니다: {type}")
        self._save_to_file_or_var(binary)
        return

    def _save_temp_image(self, img):
        """임시 이미지 저장 후 경로 반환"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_path = tmp_file.name  # 파일 경로 추출

        cv2.imwrite(tmp_path, img)
        return tmp_path
        
    def _get_my_image_type(self):
        if self.from_var:
            from_img_token = self.executor.get_variable(self.from_var)
            if not from_img_token:
                self.raise_error(f"변수 {self.from_var}에 이미지가 없습니다.")
            img_obj = from_img_token.data
        elif self.from_file:
            img_obj = Image(self.from_file)
            img_obj.load()
        else:
            self.raise_error("IMAGE resize: from_var 또는 from_file 중 하나는 필요합니다.")
    
        return img_obj

    def _save_to_file_or_var(self, img):
        if self.to_file is not None:
            cv2.imwrite(self.to_file, img)
        elif self.to_var is not None:
            # 임시로 저장한 후 불러들인다.
            temp_file_path = self._save_temp_image(img)
            new_img = Image(temp_file_path)
            new_img.load()
            new_img_token = ImageToken(data=new_img)
            new_img_token.type = TokenType.IMAGE
            new_img_token.status = TokenStatus.EVALUATED
            self.executor.set_variable(self.to_var, new_img_token)
        else:
            self.raise_error("IMAGE clip : to_file 또는 to_var 파라미터가 필요합니다.")
        return    
