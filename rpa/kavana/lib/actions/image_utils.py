from PIL import Image, ImageDraw, ImageFont, ImageChops

def get_changed_region(img1: Image, img2: Image, threshold: int = 30) -> Image:
    """
    두 이미지의 차이점을 찾아 변경된 부분을 잘라 반환하는 함수.

    :param img1: 비교할 첫 번째 이미지 (배경 이미지)
    :param img2: 비교할 두 번째 이미지 (변경된 이미지)
    :param threshold: 변경 감지 민감도 (0~255, 낮을수록 더 민감함)
    :return: 변경된 부분만 포함된 잘린 이미지 (변경된 부분이 없으면 None 반환)
    """
    # 두 이미지의 차이 계산 (절대 차이)
    diff = ImageChops.difference(img1, img2)

    # 차이 이미지를 그레이스케일로 변환 후 임계값 적용
    diff = diff.convert("L")  # 흑백 변환 (밝은 부분이 차이가 있는 영역)
    diff = diff.point(lambda p: 255 if p > threshold else 0)  # 임계값 적용

    # 변경된 영역의 경계를 찾기 위한 bounding box 계산
    bbox = diff.getbbox()
    if bbox:
        return img2.crop(bbox)  # 변경된 부분만 잘라서 반환
    else:
        return None  # 변경된 부분이 없으면 None 반환

def create_image_with_text(text: str, font_name: str = "gulim.ttc", font_size: int = 12, padding: int = 5) -> Image:
    """
    입력된 텍스트의 길이에 맞춰 이미지를 생성하는 함수.

    :param text: 생성할 이미지의 텍스트
    :param font_name: 사용할 폰트 파일 이름 (예: 'gulim.ttc', 'arial.ttf')
    :param font_size: 사용할 폰트 크기 (기본값: 12)
    :param padding: 텍스트 주위 여백 (기본값: 5)
    :return: 생성된 PIL 이미지 객체
    """
    try:
        # 폰트 로드
        font = ImageFont.truetype(font_name, font_size)

        # 텍스트 크기 측정
        dummy_img = Image.new("L", (1, 1))  # 임시 이미지
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 이미지 크기 계산 (텍스트 크기 + 패딩)
        width = text_width + 2 * padding
        height = text_height + 2 * padding

        # 실제 이미지 생성
        img = Image.new("L", (width, height), color=255)  # 흰색 배경
        draw = ImageDraw.Draw(img)

        # 텍스트 중앙 정렬
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        draw.text((text_x, text_y), text, fill=0, font=font)  # 검은색 텍스트

        return img

    except Exception as e:
        print(f"이미지 생성 중 오류 발생: {e}")
        return None
