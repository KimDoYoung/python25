# tests/test_ocr_manager.py
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from lib.core.managers.ocr_manager import OcrManager


@pytest.fixture
def dummy_image():
    return np.ones((100, 100, 3), dtype=np.uint8)


@pytest.fixture
def mock_executor():
    return MagicMock()


@patch("lib.core.managers.ocr_manager.easyocr.Reader")
@patch("lib.core.managers.ocr_manager.cv2.imread")
def test_read_text(mock_imread, mock_reader_cls, dummy_image, mock_executor):
    mock_imread.return_value = dummy_image
    mock_reader = MagicMock()
    mock_reader.readtext.return_value = [([[(0, 0), (1, 0), (1, 1), (0, 1)]], "hello", 0.9)]
    mock_reader_cls.return_value = mock_reader

    manager = OcrManager(command="READ", from_file="test.png", to_var="result", executor=mock_executor)
    text = manager.execute()

    assert text == "hello"
    mock_executor.set_variable.assert_called_once()
    args = mock_executor.set_variable.call_args[0]
    assert args[0] == "result"
    assert "hello" in str(args[1])


@patch("lib.core.managers.ocr_manager.easyocr.Reader")
@patch("lib.core.managers.ocr_manager.cv2.imread")
def test_find_text(mock_imread, mock_reader_cls, dummy_image):
    from lib.core.token_custom import RegionToken

    mock_executor = MagicMock()
    mock_imread.return_value = dummy_image
    mock_reader = MagicMock()
    mock_reader.readtext.return_value = [
        ([(10, 10), (20, 10), (20, 20), (10, 20)], "target", 0.95)
    ]
    mock_reader_cls.return_value = mock_reader

    manager = OcrManager(
        command="FIND",
        from_file="img.png",
        text="target",
        to_var="loc"
    )
    manager.executor = mock_executor
    result = manager.execute()

    # ✅ 반환값은 튜플
    assert result == (10, 10, 10, 10)

    # ✅ executor에 RegionToken 객체로 전달되었는지 확인
    mock_executor.set_variable.assert_called_once()
    var_name, token = mock_executor.set_variable.call_args[0]
    assert var_name == "loc"
    assert isinstance(token, RegionToken)
    assert token.data.x == 10 and token.data.y == 10 and token.data.width == 10 and token.data.height == 10




@patch("lib.core.managers.ocr_manager.easyocr.Reader")
@patch("lib.core.managers.ocr_manager.cv2.imread")
def test_get_all_text(mock_imread, mock_reader_cls, dummy_image):
    mock_executor = MagicMock()
    mock_imread.return_value = dummy_image
    mock_reader = MagicMock()
    mock_reader.readtext.return_value = [
        ([(0, 0), (10, 0), (10, 10), (0, 10)], "one", 0.8),
        ([(20, 20), (30, 20), (30, 30), (20, 30)], "two", 0.9)
    ]
    mock_reader_cls.return_value = mock_reader

    manager = OcrManager(
        command="GET_ALL",
        from_file="x.png",
        to_var="texts"
    )
    manager.executor = mock_executor  # ✅ 명시적으로 할당
    result = manager.execute()

    assert isinstance(result, list)
    assert result[0]["text"] == "one"
    assert result[1]["text"] == "two"
    mock_executor.set_variable.assert_called_once()
