import pytest
from lib.core.custom_token_maker import CustomTokenMaker
from lib.core.token_type import TokenType
from tests.helper_func import get_tokens  # 앞서 만든 get_tokens를 임포트하세요


@pytest.mark.parametrize("source, expected_count", [
    ('Image("1.png")', 1),
    ('Image(abc + "1.png")', 3),
    ('Image(substr("abcdef",1,2) + ".png")', 10),
])
def test_image_expression_token_count(source, expected_count):
    tokens, start_idx = get_tokens(source)

    # ✅ 리팩토링 이후 방식으로 호출
    image_token, next_idx = CustomTokenMaker.custom_object_token(tokens, start_idx, TokenType.IMAGE)
    actual_count = len(image_token.expressions[0])

    assert actual_count == expected_count, (
        f"토큰 수 불일치: 예상={expected_count}, 실제={actual_count}, 표현식={[t.type.name for t in image_token.expressions[0]]}"
    )
