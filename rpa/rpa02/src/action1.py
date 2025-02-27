


# 굴림: gulim.ttc
# 바탕: batang.ttc
# 돋움: dotum.ttc
# 궁서: gungsuh.ttc
# 맑은 고딕: malgun.ttf
# font_names = ["gulim.ttc", "malgun.ttf", "batang.ttc"]
# for font_name in font_names:
#     image = create_image_with_text(
#         text="체결계좌",
#         font_size=12,
#         padding=10
#     )
#     image.save(f"체결계좌1_{font_name}.png")
#     print(f"Saved: 체결계좌1_{font_name}.png")



import cv2
import numpy as np
from PIL import Image
from lib.core.datatypes.region import Region
from lib.actions.image_utils import create_image_with_text

def find_image_at_image(keyImage: Image, targetImage: Image) -> Region:
    '''targetImage 안에서 keyImage가 있는 위치를 찾아서 Region 객체로 반환하는 함수'''
    
    # PIL 이미지를 OpenCV 형식으로 변환
    key_np = np.array(keyImage.convert("RGB"))
    target_np = np.array(targetImage.convert("RGB"))

    key_cv = cv2.cvtColor(key_np, cv2.COLOR_RGB2GRAY)
    target_cv = cv2.cvtColor(target_np, cv2.COLOR_RGB2GRAY)

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(target_cv, key_cv, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 매칭된 위치
    x, y = max_loc
    h, w = key_cv.shape

    return Region(x, y, w, h)

# 테스트 예제
if __name__ == "__main__":
    key = "김도영"
    keyImage = create_image_with_text(key, font_size=12, padding=1)
    keyImage.save(f"{key}.png")
    targetImage = Image.open("한국투자증권화면1.png")

    region = find_image_at_image(keyImage, targetImage)
    print(region)


