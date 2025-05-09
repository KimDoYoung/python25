from typing import List, Dict, Tuple, Optional, Union, Any
import cv2
import numpy as np
import easyocr
import pyautogui
import os
import tempfile
from lib.core.datatypes.kavana_datatype import String
from lib.core.datatypes.region import Region
from lib.core.managers.base_manager import BaseManager
from lib.core.token import NoneToken, StringToken, TokenStatus, ArrayToken
from lib.core.token_custom import RegionToken
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil
from lib.core.datatypes.array import Array
from rapidfuzz import fuzz

class OcrManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs
        self.reader = easyocr.Reader(['ko', 'en'])

        if not self.command:
            self.raise_error("OCR 명령어에 command는 필수입니다.")

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

    def read(self) -> str:
        ''' OCR READ 명령어 처리: 이미지에서 텍스트를 추출합니다. '''
        area = self.options.get("area")
        to_var = self.options.get("to_var")
        resize = float(self.options.get("resize", 1.0))
        preprocess = self.options.get("preprocess", True)        

        # Get image (from file, variable, or screenshot)
        img = self._get_image()
        if preprocess:
            img = self._preprocess_image(img)

        # Process region of interest if specified
        # offset_x = offset_y = 0
        if area:
            x, y, w, h = self._parse_area(area, factor=resize if preprocess else 1.0)
            img = img[y:y+h, x:x+w]
            # offset_x, offset_y = x, y

        # Extract text from image
        results = self.reader.readtext(img)
        text = " ".join([res[1] for res in results])
        self.log("INFO", f"추출된 텍스트: {text}")

        # Store result in variable if requested
        if to_var and self.executor:
            text_token = StringToken(data=String(text), type=TokenType.STRING)
            text_token.status = TokenStatus.EVALUATED
            self.executor.set_variable(to_var, text_token)

        return text

    def find(self) -> Optional[Tuple[int, int, int, int]]:
        ''' 
            OCR FIND 명령어 처리 : 특정 텍스트를 찾아서 Region반환, 못찾으면 None반환
            fuzzy 비교를 함
        '''
        target_text = self.options.get("text")
        area = self.options.get("area")
        to_var = self.options.get("to_var")
        resize = float(self.options.get("resize", 1.0))
        preprocess = self.options.get("preprocess", True)
        similarity = float(self.options.get("similarity", 70))

        if not target_text:
            self.raise_error("FIND 명령에는 text 옵션이 필요합니다.")

        # Get image (from file, variable, or screenshot)
        img = self._get_image()
        if preprocess:
            img = self._preprocess_image(img)

        # Process region of interest if specified
        offset_x = offset_y = 0
        if area:
            x, y, w, h = self._parse_area(area, factor=resize if preprocess else 1.0)
            img = img[y:y+h, x:x+w]
            offset_x, offset_y = x, y

        # Find text in image
        results = self.reader.readtext(img)
        scale_factor = resize if preprocess else 1.0
        for res in results:
            text_found = res[1]
            box = res[0]
            
            if self._is_similar_substring(ocr_text=text_found, target=target_text, threshold=similarity):
                # Calculate region coordinates
                (x1, y1), (x2, y2), *_ = box
                x = int(min(x1, x2)/scale_factor) + offset_x
                y = int(min(y1, y2)/scale_factor) + offset_y
                w = int(abs(x2 - x1)/scale_factor)
                h = int(abs(box[2][1] - y1)/scale_factor)

                self.log("INFO", f"'{target_text}' 영역: {x}, {y}, {w}, {h}")
                
                # Store result in variable if requested
                if to_var and self.executor:
                    region_token = RegionToken(data=Region(x, y, w, h))
                    region_token.status = TokenStatus.EVALUATED
                    self.executor.set_variable(to_var, region_token)
                    
                return x, y, w, h

        self.log("WARN", f"'{target_text}'를 찾지 못함.")
        
        # Return None token if text not found
        if to_var and self.executor:
            none_token = NoneToken()
            none_token.status = TokenStatus.EVALUATED
            self.executor.set_variable(to_var, none_token)
            
        return None

    def get_all(self) -> List[Dict[str, Any]]:
        ''' OCR GET_ALL 명령어 처리: 이미지에서 모든 텍스트를 추출합니다. '''
        area = self.options.get("area")
        to_var = self.options.get("to_var")
        preprocess = self.options.get("preprocess", False)
        resize = float(self.options.get("resize", 1.0))
        self.log("INFO", f"전처리 옵션: preprocess={preprocess}")
        # Get image (from file, variable, or screenshot)
        img = self._get_image()
        if preprocess:
            img = self._preprocess_image(img)

        # Process region of interest if specified
        offset_x = offset_y = 0
        if area:
            x, y, w, h = self._parse_area(area, factor=resize if preprocess else 1.0)
            img = img[y:y+h, x:x+w]
            offset_x, offset_y = x, y

        # Extract all text elements
        results = self.reader.readtext(img)
        output = []

        for box, text, conf in results:
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            x = int(min(xs)) + offset_x
            y = int(min(ys)) + offset_y
            w = int(max(xs) - min(xs))
            h = int(max(ys) - min(ys))
            output.append({
                "x": x, "y": y, "w": w, "h": h,
                "text": text, "confidence": round(conf, 3)
            })

        # Store results in variable if requested
        if to_var and self.executor:
            array_data = [TokenUtil.dict_to_hashmap_token(item) for item in output]
            token = ArrayToken(data=Array(array_data),
                               element_type=TokenType.HASH_MAP,
                               element_expresses=[])
            token.status = TokenStatus.EVALUATED
            self.executor.set_variable(to_var, token)

        self.log("INFO", f"{len(output)}개의 텍스트 요소 추출 완료")
        return output

    def _get_image(self) -> np.ndarray:
        """
        이미지를 가져오는 함수. 파일, 변수, 스크린샷 중 하나의 소스에서 이미지를 로드합니다.
        """
        from_file = self.options.get("from_file")
        from_var = self.options.get("from_var")

        # 파일이나 변수에서 이미지를 가져올 수 없으면 스크린샷 캡처
        if not from_file and not from_var:
            screenshot = pyautogui.screenshot()
            image_path = self._get_temp_file_path(suffix=".png", prefix="screenshot_")
            screenshot.save(image_path)
            self.options["from_file"] = image_path
            self.log("INFO", f"스크린샷을 저장했습니다: {image_path}")
            from_file = image_path

        if from_file:
            # cv2.imread는 한글 경로에서 오류 발생할 수 있으므로 imdecode 사용
            img = cv2.imdecode(np.fromfile(from_file, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                self.raise_error(f"이미지 파일을 열 수 없습니다: {from_file}")
            return img
        elif from_var:
            if not self.executor:
                self.raise_error("변수를 사용하려면 executor가 필요합니다.")
                
            var_token = self.executor.get_variable(from_var)
            if var_token is None:
                self.raise_error(f"변수 '{from_var}'가 존재하지 않습니다.")
                
            img = var_token.data
            if not isinstance(img, np.ndarray):
                self.raise_error(f"변수 '{from_var}'는 numpy 배열이어야 합니다.")
            return img
        else:
            self.raise_error("이미지 소스(from_file 또는 from_var)가 필요합니다.")

    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """
        OCR 성능 향상을 위한 이미지 전처리
        """
        if not self.options.get("preprocess", False):
            return img

        gray = self.options.get("gray", False)
        blur_value = self.options.get("blur", False)
        threshold = self.options.get("threshold", "adaptive")
        resize = float(self.options.get("resize", 1.0))
        invert = self.options.get("invert", False)
        self.log("INFO", f"전처리 옵션: gray={gray}, blur_value={blur_value}, threshold={threshold}, resize={resize}, invert={invert}")

        # 임계값 처리를 위해 그레이스케일 필요
        if threshold != "none" and not gray:
            gray = True

        # 그레이스케일 변환
        if gray and len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 이미지 반전
        if invert:
            img = cv2.bitwise_not(img)

        # 블러 처리
        if blur_value:
            # 커널 크기는 항상 홀수여야 함
            k = int(blur_value) * 2 + 1
            img = cv2.GaussianBlur(img, (k, k), 0)

        # 임계값 처리
        if threshold == "adaptive" and len(img.shape) == 2:
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
        elif threshold == "otsu" and len(img.shape) == 2:
            _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 크기 조정
        if resize != 1.0:
            h, w = img.shape[:2]
            img = cv2.resize(img, (int(w * resize), int(h * resize)))

        return img

    def _parse_area(self, area: Union[Dict, List, Tuple], factor: float = 1.0) -> Tuple[int, int, int, int]:
        """
        영역 정보를 파싱하여 (x, y, width, height) 형태로 반환
        """
        if isinstance(area, dict):
            # 'width'/'height' 또는 'w'/'h' 키를 모두 지원
            w_key = "width" if "width" in area else "w"
            h_key = "height" if "height" in area else "h"
            
            x = int(area.get("x", 0) * factor)
            y = int(area.get("y", 0) * factor)
            w = int(area.get(w_key, 0) * factor)
            h = int(area.get(h_key, 0) * factor)
        elif isinstance(area, (tuple, list)) and len(area) == 4:
            x, y, w, h = [int(a * factor) for a in area]
        else:
            self.raise_error("area는 dict 또는 (x, y, w, h) 형태여야 합니다.")
        
        return x, y, w, h

    def _is_similar_substring(self, ocr_text: str, target: str, threshold: float = 70.0, margin: int = 1) -> bool:
        """
        OCR 텍스트에서 target 문자열이 포함되어 있다고 판단할 수 있는지 유사도로 확인.
        
        Parameters:
            ocr_text (str): OCR에서 추출된 문자열
            target (str): 찾고 싶은 기준 문자열
            threshold (float): 유사도 기준 값 (0~100)
            margin (int): 슬라이딩 윈도우 여유 길이 (오타 고려)

        Returns:
            bool: 포함된 것으로 판단되면 True, 아니면 False
        """
        # 빈 문자열 처리
        if not ocr_text or not target:
            return False
            
        # 전체 문자열 유사도 먼저 확인 (짧은 문자열의 경우 효율적)
        full_score = fuzz.ratio(ocr_text.strip(), target)
        if full_score >= threshold:
            self.log("INFO", f"'{ocr_text.strip()}'가 '{target}'과 유사도 {full_score}%로 일치함")
            return True
            
        # 긴 문자열의 경우 부분 문자열 검색
        if len(ocr_text) > len(target):
            window_size = len(target) + margin
            
            # 슬라이딩 윈도우 최적화: 전체 길이에서 윈도우 크기를 뺀 만큼만 순회
            for i in range(len(ocr_text) - len(target) + 1):
                window = ocr_text[i:i + window_size]
                score = fuzz.ratio(window.strip(), target)
                if score >= threshold:
                    self.log("INFO", f"'{window.strip()}'가 '{target}'과 유사도 {score}%로 포함됨")
                    return True

        return False

    # def _get_temp_file_path(self, prefix="tmp_", suffix=""):
    #     """임시 파일 경로 생성"""
    #     fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    #     os.close(fd)
    #     return path
    
# from typing import List
# import cv2
# import numpy as np
# import easyocr
# import pyautogui
# from lib.core.datatypes.kavana_datatype import String
# from lib.core.datatypes.region import Region
# from lib.core.managers.base_manager import BaseManager
# from lib.core.token import NoneToken, StringToken, TokenStatus
# from lib.core.token_custom import RegionToken
# from lib.core.token_type import TokenType
# from lib.core.token_util import TokenUtil
# from rapidfuzz import fuzz
# class OcrManager(BaseManager):
#     def __init__(self, **kwargs):
#         super().__init__(kwargs.get("executor", None))
#         self.command = kwargs.get("command")
#         self.options = kwargs
#         self.reader = easyocr.Reader(['ko', 'en'])

#         if not self.command:
#             self.raise_error("OCR 명령어에 command는 필수입니다.")

#     def execute(self):
#         command_map = {
#             "READ": self.read,
#             "FIND": self.find,
#             "GET_ALL": self.get_all
#         }

#         func = command_map.get(self.command.upper())
#         if not func:
#             self.raise_error(f"OCR 지원하지 않는 명령어: {self.command}")
#         return func()

#     def read(self):
#         ''' OCR READ 명령어 처리: 이미지에서 텍스트를 추출합니다. '''

#         area = self.options.get("area")
#         to_var = self.options.get("to_var")

#         # 만약 from_var와 from_file이 모두 비어 있으면 screen capture를 해서 그것을 임시파일로 저장하고 from_file에 임시파일패스를 넣는다.
#         if not self.options.get("from_var") and not self.options.get("from_file"):
#             screenshot = pyautogui.screenshot()
#             image_path = self._get_temp_file_path(suffix=".png", prefix="screenshot_")
#             screenshot.save(image_path)
#             self.options["from_file"] = image_path
#             self.log("INFO", f"스크린샷을 저장했습니다: {image_path}")

#         img = self._get_image_from_file_or_var()
#         img = self._preprocess_image(img)

#         if area:
#             x, y, w, h = self._parse_area(area)
#             img = img[y:y+h, x:x+w]

#         results = self.reader.readtext(img)
#         text = " ".join([res[1] for res in results])
#         self.log("INFO", f"추출된 텍스트: {text}")

#         if to_var and self.executor:
#             text_token = StringToken(data=String(text), type=TokenType.STRING)
#             self.executor.set_variable(to_var, text_token)

#         return text

    
#     def find(self):
#         ''' 
#             OCR FIND 명령어 처리 : 특정 텍스트를 찾아서 Region반환, 못찾으면 None반환
#             fuzzy 비교를 함
#         '''
#         target_text = self.options.get("text")
#         area = self.options.get("area")
#         to_var = self.options.get("to_var")
#         similarity = self.options.get("similarity", 70)

#         if not target_text:
#             self.raise_error("FIND 명령에는 text 옵션이 필요합니다.")

#         # 만약 from_var와 from_file이 모두 비어 있으면 screen capture를 해서 그것을 임시파일로 저장하고 from_file에 임시파일패스를 넣는다.
#         if not self.options.get("from_var") and not self.options.get("from_file"):
#             screenshot = pyautogui.screenshot()
#             image_path = self._get_temp_file_path(suffix=".png", prefix="screenshot_")
#             screenshot.save(image_path)
#             self.options["from_file"] = image_path
#             self.log("INFO", f"스크린샷을 저장했습니다: {image_path}")


#         img = self._get_image_from_file_or_var()
#         img = self._preprocess_image(img)

#         offset_x = offset_y = 0
#         if area:
#             x, y, w, h = self._parse_area(area)
#             img = img[y:y+h, x:x+w]
#             offset_x, offset_y = x, y

#         results = self.reader.readtext(img)

#         for res in results:
#             text_found = res[1]
#             box = res[0]
#             if self._is_similar_substring(ocr_text=text_found, target=target_text, threshold=similarity):
#                 (x1, y1), (x2, y2), *_ = box
#                 x = int(min(x1, x2)) + offset_x
#                 y = int(min(y1, y2)) + offset_y
#                 w = int(abs(x2 - x1))
#                 h = int(abs(box[2][1] - y1))

#                 self.log("INFO", f"'{target_text}' 영역: {x}, {y}, {w}, {h}")
#                 if to_var and self.executor:
#                     region_token = RegionToken(data=Region(x, y, w, h))
#                     region_token.status = TokenStatus.EVALUATED
#                     self.executor.set_variable(to_var, region_token)
#                 return x, y, w, h

#         self.log("WARN", f"'{target_text}'를 찾지 못함.")
#         if to_var and self.executor:
#             self.executor.set_variable(to_var, NoneToken())
#         return None

#     def get_all(self):
#         ''' OCR GET_ALL 명령어 처리: 이미지에서 모든 텍스트를 추출합니다. '''
#         area = self.options.get("area")
#         to_var = self.options.get("to_var")
#         preprocess = self.options.get("preprocess")
#         resize = self.options.get("resize", 1.0)

#         # 만약 from_var와 from_file이 모두 비어 있으면 screen capture를 해서 그것을 임시파일로 저장하고 from_file에 임시파일패스를 넣는다.
#         if not self.options.get("from_var") and not self.options.get("from_file"):
#             screenshot = pyautogui.screenshot()
#             image_path = self._get_temp_file_path(suffix=".png", prefix="screenshot_")
#             screenshot.save(image_path)
#             self.options["from_file"] = image_path
#             self.log("INFO", f"임시 스크린샷을 저장했습니다: {image_path}")

#         img = self._get_image_from_file_or_var()
#         img = self._preprocess_image(img)


#         offset_x = offset_y = 0
#         if area:
#             if preprocess:
#                 x, y, w, h = self._parse_area(area, factor=resize)
#             else:
#                 x, y, w, h = self._parse_area(area)
#             img = img[y:y+h, x:x+w]
#             offset_x, offset_y = x, y

#         results = self.reader.readtext(img)
#         output = []

#         for box, text, conf in results:
#             xs = [p[0] for p in box]
#             ys = [p[1] for p in box]
#             x = int(min(xs)) + offset_x
#             y = int(min(ys)) + offset_y
#             w = int(max(xs) - min(xs))
#             h = int(max(ys) - min(ys))
#             output.append({
#                 "x": x, "y": y, "w": w, "h": h,
#                 "text": text, "confidence": round(conf, 3)
#             })

#         if to_var and self.executor:
#             from lib.core.token_type import TokenType
#             from lib.core.token import ArrayToken
#             from lib.core.datatypes.array import Array
#             array_data = [TokenUtil.dict_to_hashmap_token(item) for item in output]
#             token = ArrayToken(data=Array(array_data),
#                                element_type=TokenType.HASH_MAP,
#                                element_expresses=[])
#             token.status = TokenStatus.EVALUATED
#             self.executor.set_variable(to_var, token)

#         self.log("INFO", f"{len(output)}개의 텍스트 요소 추출 완료")
#         return output

#     def _preprocess_image(self, img):
#         if not self.options.get("preprocess", False):
#             return img

#         gray = self.options.get("gray", False)
#         blur = self.options.get("blur", False)
#         threshold = self.options.get("threshold", "adaptive")
#         resize = self.options.get("resize", 1.0)
#         invert = self.options.get("invert", False)

#         if threshold != "none" and not gray:
#             gray = True

#         if gray:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         if invert:
#             img = cv2.bitwise_not(img)

#         if blur:
#             k = int(blur) * 2 + 1
#             img = cv2.GaussianBlur(img, (k, k), 0)

#         if threshold == "adaptive":
#             img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                         cv2.THRESH_BINARY, 11, 2)
#         elif threshold == "otsu":
#             _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#         if resize and resize != 1.0:
#             h, w = img.shape[:2]
#             img = cv2.resize(img, (int(w * resize), int(h * resize)))

#         return img

#     def _get_image_from_file_or_var(self):
#         from_file = self.options.get("from_file")
#         from_var = self.options.get("from_var")

#         if from_file:
#             # img = cv2.imread(from_file) # cv2.imread는 한글 경로에서 오류 발생
#             img = cv2.imdecode(np.fromfile(from_file, dtype=np.uint8), cv2.IMREAD_COLOR)
#             if img is None:
#                 self.raise_error(f"이미지 파일을 열 수 없습니다: {from_file}")
#             return img
#         elif from_var:
#             img = self.executor.get_variable(from_var).data
#             if not isinstance(img, np.ndarray):
#                 self.raise_error(f"변수 '{from_var}'는 numpy 배열이어야 합니다.")
#             return img
#         else:
#             self.raise_error("from_file 또는 from_var가 필요합니다.")

#     def _parse_area(self, area, factor=1.0):
#         if isinstance(area, dict):
#             x = int(area["x"] * factor)
#             y = int(area["y"] * factor)
#             w = int(area["width"] * factor)
#             h = int(area["height"] * factor)
#         elif isinstance(area, (tuple, list)) and len(area) == 4:
#             x, y, w, h = [int(a * factor) for a in area]
#         else:
#             self.raise_error("area는 dict 또는 (x, y, w, h) 형태여야 합니다.")
#         return x, y, w, h


#     def _is_similar_substring(self,ocr_text: str, target: str, threshold: int = 70, margin: int = 1) -> bool:
#         """
#         OCR 텍스트에서 target 문자열이 포함되어 있다고 판단할 수 있는지 유사도로 확인.
        
#         Parameters:
#             ocr_text (str): OCR에서 추출된 문자열
#             target (str): 찾고 싶은 기준 문자열
#             threshold (int): 유사도 기준 값 (0~100)
#             margin (int): 슬라이딩 윈도우 여유 길이 (오타 고려)

#         Returns:
#             bool: 포함된 것으로 판단되면 True, 아니면 False
#         """
#         max_len = len(ocr_text) - len(target) + 1
#         if max_len < 1:
#             return False

#         for i in range(max_len):
#             window = ocr_text[i:i + len(target) + margin]
#             score = fuzz.ratio(window.strip(), target)
#             if score >= threshold:
#                 self.log("INFO", f"'{window.strip()}'가 '{target}'과 유사도 {score}%로 포함됨")
#                 return True

#         return False
