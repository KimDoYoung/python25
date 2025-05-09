from PIL import Image, ImageDraw, ImageFont, ImageChops


def create_image_with_text(text: str, font_name: str = "gulim.ttc", font_size: int = 12, padding: int = 1) -> Image:
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
        width = text_width + 2 #+ 2 * padding
        height = text_height + 4  #+ 2 * padding

        # 실제 이미지 생성
        img = Image.new("L", (width, height), color=255)  # 흰색 배경
        draw = ImageDraw.Draw(img)

        # 텍스트 중앙 정렬
        text_x = 0 # (width - text_width) // 2
        text_y = 2 #(height - text_height) // 2
        draw.text((text_x, text_y), text, fill=0, font=font)  # 검은색 텍스트

        return img

    except Exception as e:
        print(f"이미지 생성 중 오류 발생: {e}")
        return None

# def find_image_at_image(keyImage: Image, targetImage: Image) -> Region:
#     '''targetImage안에서 keyImage가 있는 위치를 찾아서 Region 객체로 반환하는 함수'''
#     # keyImage의 크기
    
