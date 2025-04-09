import pytest
from lib.core.custom_token_maker import CustomTokenMaker
from lib.core.token_type import TokenType
from tests.test_helper import get_tokens  # 앞서 만든 get_tokens를 임포트하세요


@pytest.mark.parametrize("source, expected_count", [
    ('Image("1.png")', 1),
    ('Image(abc + "1.png")', 3),
    ('Image(substr("abcdef",1,2) + ".png")', 10),
])
def test_image_expression_token_count(source, expected_count):
    tokens, start_idx = get_tokens(source)
    image_token, next_idx = CustomTokenMaker.image_token(tokens, start_idx)
    actual_count = len(image_token.expressions[0])

    assert actual_count == expected_count, (
        f"토큰 수 불일치: 예상={expected_count}, 실제={actual_count}, 표현식={[t.type.name for t in image_token.expressions[0]]}"
    )
