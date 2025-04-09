import pytest
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.token_custom import (
    PointToken, RectangleToken, RegionToken,
    ImageToken, ApplicationToken, WindowToken
)


class DummyEvaluator:
    def evaluate(self, tokens):
        if isinstance(tokens, list):
            return tokens[0]
        return tokens


@pytest.fixture
def evaluator():
    return DummyEvaluator()


def test_point_token(evaluator):
    point = PointToken(data=None)
    point.expressions = [
        [Token(data=Integer(1), type=TokenType.INTEGER)],
        [Token(data=Integer(2), type=TokenType.INTEGER)]
    ]
    result = point.evaluate(evaluator)
    assert result.data.x == 1
    assert result.data.y == 2


def test_rectangle_token(evaluator):
    rect = RectangleToken(data=None)
    rect.expressions = [
        [Token(data=Integer(10), type=TokenType.INTEGER)],
        [Token(data=Integer(20), type=TokenType.INTEGER)],
        [Token(data=Integer(110), type=TokenType.INTEGER)],
        [Token(data=Integer(120), type=TokenType.INTEGER)],
    ]
    result = rect.evaluate(evaluator)
    assert result.data.p1.x == 10
    assert result.data.p1.y == 20
    assert result.data.p2.x == 110
    assert result.data.p2.y == 120


def test_region_token(evaluator):
    region = RegionToken(data=None)
    region.expressions = [
        [Token(data=Integer(5), type=TokenType.INTEGER)],
        [Token(data=Integer(10), type=TokenType.INTEGER)],
        [Token(data=Integer(150), type=TokenType.INTEGER)],
        [Token(data=Integer(80), type=TokenType.INTEGER)],
    ]
    result = region.evaluate(evaluator)
    assert result.data.x == 5
    assert result.data.y == 10
    assert result.data.width == 150
    assert result.data.height == 80


def test_application_token(evaluator):
    app = ApplicationToken(data=None)
    app.expressions = [
        [Token(data=String("notepad.exe"), type=TokenType.STRING)]
    ]
    result = app.evaluate(evaluator)
    assert result.data.path == "notepad.exe"


def test_window_token(evaluator):
    win = WindowToken(data=None)
    win.expressions = [
        [Token(data=String("MyApp Window"), type=TokenType.STRING)]
    ]
    result = win.evaluate(evaluator)
    assert result.data.title == "MyApp Window"


def test_image_token(tmp_path, evaluator):
    import cv2
    import numpy as np
    from lib.core.datatypes.kavana_datatype import String

    # 테스트용 이미지 생성
    test_image_path = tmp_path / "test_image.png"
    cv2.imwrite(str(test_image_path), np.ones((1, 1, 3), dtype=np.uint8) * 255)

    img = ImageToken(data=None)
    img.expressions = [
        [Token(data=String(str(test_image_path)), type=TokenType.STRING)]
    ]
    result = img.evaluate(evaluator)
    assert result.data.path == str(test_image_path)
    assert result.data.data is not None
