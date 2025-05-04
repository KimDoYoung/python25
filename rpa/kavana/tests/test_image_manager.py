# tests/test_image_manager.py

import pytest
import numpy as np
from unittest.mock import MagicMock
from lib.core.managers.image_manager import ImageManager
from lib.core.token_custom import ImageToken
from lib.core.token_type import TokenType
from lib.core.token import TokenStatus


@pytest.fixture
def mock_executor():
    executor = MagicMock()
    return executor


@pytest.fixture
def dummy_image():
    # 100x100 컬러 이미지
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    mock_image_obj = MagicMock()
    mock_image_obj.data = img
    mock_image_obj.width = 100
    mock_image_obj.height = 100
    return mock_image_obj


def make_manager(command, **options):
    options["command"] = command
    return ImageManager(**options)


def test_resize(mock_executor, dummy_image):
    mock_executor.get_variable.return_value = ImageToken(data=dummy_image)
    dummy_image.load = MagicMock()

    manager = make_manager("resize", from_var="img", factor=0.5, to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_clip(mock_executor, dummy_image):
    mock_executor.get_variable.return_value = ImageToken(data=dummy_image)

    manager = make_manager("clip", from_var="img", area=(10, 10, 30, 30), to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_to_gray(mock_executor, dummy_image):
    manager = make_manager("to_gray", from_var="img", to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_convert_to_rgb(mock_executor, dummy_image):
    manager = make_manager("convert_to", from_var="img", mode="RGB", to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_rotate(mock_executor, dummy_image):
    manager = make_manager("rotate", from_var="img", angle=45, to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_blur(mock_executor, dummy_image):
    manager = make_manager("blur", from_var="img", radius=3, to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_threshold(mock_executor, dummy_image):
    manager = make_manager("threshold", from_var="img", level=127, type="BINARY", to_file="out.png", executor=mock_executor)
    manager._get_my_image_type = lambda: dummy_image
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()


def test_create_text_image(mock_executor):
    manager = make_manager("create_text_image", text="Hello", to_file="text.png", executor=mock_executor)
    manager._save_to_file_or_var = MagicMock()
    manager.execute()

    manager._save_to_file_or_var.assert_called_once()
