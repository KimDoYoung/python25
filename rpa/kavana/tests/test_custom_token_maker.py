import pytest
from lib.core.exceptions.kavana_exception import CustomTokenMakerError
from lib.core.token_type import TokenType
from lib.core.custom_token_maker import CustomTokenMaker
from tests.helper_func import get_raw_tokens
from lib.core.token_custom import PointToken, RectangleToken, RegionToken, ImageToken, WindowToken, ApplicationToken


@pytest.mark.parametrize("expr, expected_class, expected_type, expected_len", [
    ("Point(10, 20)", PointToken, TokenType.POINT, 2),
    ("Rectangle(1,2,3,4)", RectangleToken, TokenType.RECTANGLE, 4),
    ("Region(5,6,7,8)", RegionToken, TokenType.REGION, 4),
    ('Image("img.png")', ImageToken, TokenType.IMAGE, 1),
    ('Window("title", 1001, "class")', WindowToken, TokenType.WINDOW, 3),
    ('Application("path", "proc")', ApplicationToken, TokenType.APPLICATION, 2),
])
def test_custom_object_token_success(expr, expected_class, expected_type, expected_len):
    tokens = get_raw_tokens(expr)
    start_idx = 0
    token, next_idx = CustomTokenMaker.custom_object_token(tokens, start_idx, tokens[start_idx].type)

    assert isinstance(token, expected_class)
    assert token.type == expected_type
    assert len(token.expressions) == expected_len
    assert next_idx > start_idx


def test_custom_token_invalid_type():
    tokens = get_raw_tokens("UnknownObj(1, 2)")
    with pytest.raises(Exception):
        CustomTokenMaker.custom_object_token(tokens, 0, TokenType.UNKNOWN)


def test_custom_token_unmatched_parens():
    tokens = get_raw_tokens("Point(1, 2")
    with pytest.raises(Exception):
        CustomTokenMaker.custom_object_token(tokens, 0, TokenType.POINT)


def test_custom_token_too_few_arguments():
    tokens = get_raw_tokens("Rectangle(1,2,3)")
    with pytest.raises(Exception):
        CustomTokenMaker.custom_object_token(tokens, 0, TokenType.RECTANGLE)


def test_custom_token_too_many_arguments():
    tokens = get_raw_tokens("Point(1,2,3)")
    with pytest.raises(CustomTokenMakerError):
        CustomTokenMaker.custom_object_token(tokens, 0, TokenType.POINT)